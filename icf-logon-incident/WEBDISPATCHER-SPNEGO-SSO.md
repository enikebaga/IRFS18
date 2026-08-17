# Web Dispatcher & SPNego SSO for `cim.freudenberg.com`

**Context:** SSO fails after redirect/short link to `cim.freudenberg.com` (and `test-cim.freudenberg.com`). ECS Web Dispatcher terminates TLS (see certificate handover). Question: *Where in the Web Dispatcher do you “activate SSO / SPNego”?*

## Short answer

**There is no Web Dispatcher profile switch that “turns on SPNego.”**  
SPNego/Kerberos is authenticated on the **ABAP backend** (transaction **SPNEGO**, parameters `spnego/enable`, keytab). The Web Dispatcher only:

1. Terminates HTTPS for the public hostname  
2. Routes the request to the correct SID  
3. Forwards headers so the backend sees the right host  

If the browser hostname (`cim.freudenberg.com`) is not covered by **AD SPN + ABAP SPNEGO keytab + WD routing/TLS**, SSO breaks after the short-link redirect.

When SPNego itself already works (e.g. on the internal host) but fails after redirect to the short link, ECS **Maintain System Parameters → Static** is used to keep **host routing, Host header, cookies/tickets, and trusted reverse proxy** aligned with `cim.freudenberg.com`.

---

## ECS: Maintain System Parameters → Static (what to maintain for SSO)

Use this when SPNego works on the known internal URL but SSO breaks on **`cim.freudenberg.com`** / **`test-cim.freudenberg.com`**.  
Maintain the **Web Dispatcher** parameters (and, if the console also exposes the **ABAP/ICM** system, the backend trust/ticket parameters). Exact allow-list varies by ECS landscape—if a name is missing in the UI, open an ECS ticket with the same list.

### A. Web Dispatcher (Static) — primary for short-hostname SSO

| Parameter | Purpose | Typical value / action for Freudenberg CIM |
|---|---|---|
| **`wdisp/system_<n>`** | Map incoming host → SID CSD | Include **`SRCVHOST=cim.freudenberg.com:443;test-cim.freudenberg.com:443`** (and existing internal host if needed), plus **`SRCURL`** for `/sap/...` (webdynpro, public, etc.), **`SSL_ENCRYPT=1`** (or as today) |
| **`wdisp/system_conflict_resolution`** | Ambiguous URL/host matches | **`BEST_MATCH`** |
| **`icm/server_port_<n>`** | HTTPS listener | HTTPS on **443** for public short name (avoid relying on `:44300` for Chromium SPNego) |
| **`icm/HTTP/mod_<n>`** | Rewrite / header rules | Point to action file that preserves public Host / sets access-point headers if ECS uses mod rules for CIM |
| **`icm/HTTP/redirect_<n>`** | HTTP→HTTPS or path redirect | Only if short link must redirect; **`HOST=`** must stay **`cim.freudenberg.com`** (not internal only) |
| **`icm/host_name_full`** | Canonical WD FQDN | Set only if ECS requires it; do **not** overwrite public SAN hosts—cert SANs still need `cim.freudenberg.com` |
| **`wdisp/add_clientprotocol_header`** | Tell backend original protocol | **`TRUE`** / `1` (so HTTPS is visible to apps) |
| **`wdisp/handle_webdisp_ap_header`** | Absolute URL / access points | Enable if absolute links/cookies must reflect public host |
| **`wdisp/add_xforwardedfor_header`** | Client IP chain | As per security standard (often on) |
| **`HOST_HEADER`** (subparam of `wdisp/system_*`, newer WD) | Preserve vs replace Host | Prefer **`PRESERVE`** so backend/SPNego see **`cim.freudenberg.com`**. **`REPLACE`** only if ECS/backend explicitly requires internal host (then SPN must match that host instead) |

Example shape (indexes must match your existing `wdisp/system_*` numbering—**extend**, don’t blindly paste):

```text
wdisp/system_conflict_resolution = BEST_MATCH

wdisp/system_<n> = SID=CSD, MSHOST=<ms-host>, MSPORT=<ms-http-port>,
  SRCVHOST=cim.freudenberg.com:443;test-cim.freudenberg.com:443;vhffecsdci.sap.invite.freudenberg:44300,
  SRCURL=/sap/bc/;/sap/public/;/sap/opu/;/sap/saml2/;/sap/bc/webdynpro/,
  SSL_ENCRYPT=1
```

### B. ABAP backend (Static) — trust WD + tickets after SPNego

Maintain on **CSD** if exposed in the same ECS Parameter app (or ask Basis/ECS):

| Parameter | Purpose | Typical for SSO behind WD |
|---|---|---|
| **`icm/trusted_reverse_proxy_0`** (or `_1`, …) | Trust Web Dispatcher as reverse proxy | SUBJECT/ISSUER of WD client cert as per ECS doc (required when WD terminates SSL / forwards identity) |
| **`icm/HTTPS/trust_client_with_subject`** | Legacy trust (if still used) | Only if not fully on `icm/trusted_reverse_proxy_*` |
| **`icm/HTTPS/trust_client_with_issuer`** | Legacy trust issuer | Same |
| **`login/create_sso2_ticket`** | Issue MYSAPSSO2 after auth | Often **`2`** |
| **`login/accept_sso2_ticket`** | Accept logon tickets | **`1`** |
| **`login/ticket_only_by_https`** | Tickets only on HTTPS | **`1`** |
| **`login/ticket_only_to_host`** | Restrict ticket to one host | **`0`** or unset when users switch between `vhffecsdci…` and `cim.freudenberg.com` (KBA **3441950** family) |
| **`spnego/enable`** | SPNego on AS ABAP | Already OK in your landscape—confirm still **on** |
| **`is/HTTP/show_detailed_errors`** | Debug only | Leave default in prod |

**Not a profile parameter but mandatory with short host:** table **`HTTPURLLOC`** (client 400) entries for `cim.freudenberg.com` / `test-cim.freudenberg.com` so generated absolute URLs/cookies match the browser host.

### C. What you do **not** maintain in ECS Static for “SSO on”

| Not applicable | Why |
|---|---|
| A parameter named `spnego/activate` on Web Dispatcher | Does not exist |
| AD `setspn` / keytab | AD + transaction **SPNEGO** (Basis), not ECS Static |
| SICF logon procedure | SICF, not profile Static |

### D. Apply order

1. ECS Static: WD **`wdisp/system_*` + `SRCVHOST`** for public hosts (+ conflict resolution).  
2. Confirm **`SAPSSLS`** cert SAN includes those hosts (separate ECS cert activity).  
3. Backend Static: **`icm/trusted_reverse_proxy_*`**, ticket params, **`login/ticket_only_to_host`**.  
4. **HTTPURLLOC** for public hosts.  
5. Restart/reload as ECS requires for **Static** parameters.  
6. Test from domain PC: `https://cim.freudenberg.com/...` on **443**.

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
Please maintain ECS → Maintain System Parameters → Static (Web Dispatcher)
for SPNego/SSO via public hostnames cim.freudenberg.com and
test-cim.freudenberg.com (backend SID CSD):

1) wdisp/system_<n>: add SRCVHOST=cim.freudenberg.com:443;test-cim.freudenberg.com:443
   (keep existing internal host), SRCURL covering /sap/bc/;/sap/public/;...,
   SSL_ENCRYPT as today; wdisp/system_conflict_resolution=BEST_MATCH
2) Prefer HOST_HEADER=PRESERVE (or equivalent) so backend sees public Host
3) wdisp/add_clientprotocol_header / handle_webdisp_ap_header as required
4) SAPSSLS.pse SAN must include both public hostnames; reload WD after Static apply
5) On CSD Static (if in scope): icm/trusted_reverse_proxy_*; login/create_sso2_ticket;
   login/accept_sso2_ticket; login/ticket_only_by_https; login/ticket_only_to_host=0
6) Confirm HTTPURLLOC client 400 has cim.freudenberg.com / test-cim entries

Please send back the resulting wdisp/system_* lines (redacted).
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
