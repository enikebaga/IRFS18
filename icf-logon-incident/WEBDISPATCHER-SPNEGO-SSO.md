# Web Dispatcher & SPNego SSO for `cim.freudenberg.com`

**Context:** SSO fails after redirect/short link to `cim.freudenberg.com` (and `test-cim.freudenberg.com`). ECS Web Dispatcher terminates TLS (see certificate handover). Question: *Where in the Web Dispatcher do you “activate SSO / SPNego”?*

## Short answer

**There is no Web Dispatcher profile switch that “turns on SPNego.”**  
SPNego/Kerberos is authenticated on the **ABAP backend** (transaction **SPNEGO**, parameters `spnego/enable`, keytab). The Web Dispatcher only:

1. Terminates HTTPS for the public hostname  
2. Routes the request to the correct SID  
3. Forwards headers so the backend sees the right host  

If the browser hostname (`cim.freudenberg.com`) is not covered by **AD SPN + ABAP SPNEGO keytab + WD routing/TLS**, SSO breaks after the short-link redirect.

---

## 1. What to request from SAP ECS (Web Dispatcher)

On RISE/ECS you usually **cannot** edit the WD profile yourself. Open an ECS ticket and ask them to confirm/set:

### 1.1 TLS for the short name (prerequisite)

| Item | Expected |
|---|---|
| PSE | **`SAPSSLS.pse`** (server cert) |
| Certificate SAN/CN | includes **`cim.freudenberg.com`** and **`test-cim.freudenberg.com`** |
| Browser check | `https://cim.freudenberg.com/` shows trusted cert, no name mismatch |

(Your 2026-08-14 handover: public cert import was still incomplete — fix this before chasing SPNego.)

### 1.2 Host-based routing to CSD

Ask ECS for the active `wdisp/system_*` (or equivalent) entries. For SPNego via short name you typically need the **virtual host** of the request to select CSD, e.g.:

```text
wdisp/system_<n> = SID=<CSD>, MSHOST=..., MSPORT=...,
  SRCVHOST=cim.freudenberg.com:443;test-cim.freudenberg.com:443,
  SRCURL=/sap/;/ui2/;...,
  SSL_ENCRYPT=1
```

Relevant subparameters:

| Parameter / subparam | Role for SSO |
|---|---|
| `wdisp/system_<xx>` | Maps incoming host/URL → backend SID |
| **`SRCVHOST`** | Match on `Host:` header (`cim.freudenberg.com`) — preferred for short links |
| `SRCSRV` | Match on host:port if used instead of / with SRCVHOST |
| `SRCURL` | URL prefixes forwarded to that SID (`/sap/bc/webdynpro/...`) |
| `SSL_ENCRYPT` | Re-encrypt WD → backend if needed |
| `wdisp/system_conflict_resolution` | `BEST_MATCH` if multiple systems share prefixes |
| `icm/server_port_<xx>` | HTTPS listener (often 443 externally) |
| `icm/HTTP/mod_<xx>` | Optional rewrite/redirect rules (short URL → app path) |
| `icm/HTTP/redirect_<xx>` | Optional host redirects |

There is **no** `spnego/enable` (or similar) in the Web Dispatcher profile.

### 1.3 Headers / cookies (ask ECS to confirm)

| Parameter | Why it matters |
|---|---|
| `wdisp/add_clientprotocol_header` | Backend knows original HTTPS |
| `wdisp/handle_webdisp_ap_header` | Application protocol / absolute URLs |
| Host header preservation | Backend + SPNego must see **`cim.freudenberg.com`**, not only `vhffecsdci...` |

If WD rewrites `Host` to the internal name, the browser may request a Kerberos ticket for the wrong SPN.

---

## 2. Where SPNego is actually activated (ABAP — your Basis)

Transaction / profile on **CSD** (not Web Dispatcher):

| Place | What to check |
|---|---|
| **RZ11** `spnego/enable` | Must be active (`1` / as per your SSO design) |
| **RZ11** `spnego/krbspnego` | Points at keytab / SSO product setting |
| Transaction **`SPNEGO`** | Keytab loaded; SPNs include **`HTTP/cim.freudenberg.com`** (and test host) |
| **SU01** | User Kerberos principal mapping |
| SICF service **Logon Data** | SPNego / SSO in alternative logon procedure for CIM services |

AD (Windows team):

```text
setspn -Q HTTP/cim.freudenberg.com
setspn -Q HTTP/test-cim.freudenberg.com
```

SPN must be on the **same AD account** whose keytab is imported in transaction **SPNEGO** for CSD.

---

## 3. Why short-link redirect breaks SSO (typical)

```text
Browser opens cim.freudenberg.com
  → requests Kerberos ticket for HTTP/cim.freudenberg.com
  → WD terminates TLS, forwards to CSD
  → ABAP SPNEGO decrypts with keytab
```

Fails if any of these is true:

1. Cert on WD is still wrong/missing for `cim.freudenberg.com` (ECS handover status).  
2. No AD SPN `HTTP/cim.freudenberg.com` (only old `HTTP/vhffecsdci.sap.invite.freudenberg`).  
3. Keytab in **SPNEGO** was not regenerated after adding the new SPN.  
4. WD routes the host to the wrong SID / strips Host header.  
5. Browser still ends on **non-default port** (e.g. `:44300`) — Chromium SPNego with ports is problematic (KBA **3346384**). Prefer **443** on the short name.  
6. User not domain-joined / site not in Intranet / local intranet zone for integrated auth.

---

## 4. Checklist to send ECS + Basis

### ECS Web Dispatcher ticket (paste)

```text
Please confirm Web Dispatcher config for SPNego via public hostnames
cim.freudenberg.com and test-cim.freudenberg.com (CSD):

1) SAPSSLS.pse serves public cert with SAN for both hostnames; WD reload done.
2) wdisp/system_* routes SRCVHOST=cim.freudenberg.com / test-cim... to SID CSD
   with required SRCURL (/sap/...).
3) Host header of the browser request is forwarded to the backend (not replaced
   by internal vhffecsdci name only).
4) Provide redacted excerpt of: icm/server_port_*, wdisp/system_*,
   icm/HTTP/mod_* / redirect_* for these hosts.
5) Confirm there is no WD-side "SPNego enable" parameter (we understand SPNego
   is backend); we need routing/TLS/host header correctness only.
```

### Basis ABAP ticket (paste)

```text
Please extend SPNego for CSD to public hosts:
- AD SPN HTTP/cim.freudenberg.com (+ test-cim) on CSD Kerberos service account
- Regenerate/import keytab in transaction SPNEGO
- Confirm spnego/enable and SICF logon procedure includes SPNego for
  /sap/bc/webdynpro/zco/*
- Test: https://cim.freudenberg.com/... (port 443) from domain-joined PC
```

---

## 5. Relation to earlier “dead Log On button” issue

| Topic | Mechanism |
|---|---|
| Dead **Log On** button (no HTTP) | ICF System Logon JS / `/ZCO/CL_ICF_CIM_LOGIN` |
| SSO after short link | Kerberos SPN + WD host routing + TLS for `cim.freudenberg.com` |

They can appear together but are **different** fixes. Completing the public cert + SPN for `cim.freudenberg.com` does not replace the custom System Logon A/B on `ZV_MENU`.

---

## References

- KBA **3239299** — SPNs with one Web Dispatcher / multiple backends  
- KBA **3346384** — SPNego + non-default port in Chromium  
- KBA **3441950** — SPNego after Web Dispatcher in multi-system landscape  
- Component: **BC-SEC-LGN-SPN** (SPNego), **BC-CST-WDP** (Web Dispatcher)  
- Certificate handover: `SAP_ECS_Certificate_Handover_Full_2026-08-14` (SAPSSLS for public hosts)  
