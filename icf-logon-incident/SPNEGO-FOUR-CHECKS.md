# How to check the 4 SPNEGO questions (ownership: SAP ECS vs Freudenberg)

**Situation:** Kerberos tickets are issued for both `HTTP/vhffecspci.fra3.sap.invite.freudenberg` and `HTTP/cim.freudenberg.com`, but SSO works only on the SAP hostname.

| # | Question | Who primarily checks |
|---|---|---|
| 1 | WD forwards SPNEGO for `cim.freudenberg.com` | **You (browser)** + **SAP ECS** (WD config/mod) |
| 2 | SPNEGO accepts principal `HTTP/cim.freudenberg.com` | **Your Basis** (or SAP if they own SPNEGO/keytab on RISE) |
| 3 | `dev_icm` success/fail for `cim.freudenberg.com` | **SAP ECS / SAP Basis hosting** (OS trace access) — you only reproduce |
| 4 | Keytab contains `HTTP/cim.freudenberg.com` | **Your Basis** + often **SAP ECS** (keytab file on server) |

On RISE/ECS, app-server OS files (`dev_icm`, keytab path) are usually **SAP-accessible**; you raise a ticket and attach reproduction time + URLs. SPNEGO transaction and SU01 are often **customer Basis** if you have GUI access.

---

## Question 1 — Does Web Dispatcher forward SPNEGO for `cim.freudenberg.com`?

### 1A — What **you** check (browser) — Freudenberg

1. On a **domain-joined** PC where SAP-hostname SSO works, open **Edge/Chrome**.
2. F12 → **Network** → tick **Preserve log**.
3. Open the **failing** URL, e.g.  
   `https://cim.freudenberg.com/sap/bc/webdynpro/zco/zv_menu?sap-client=400`
4. Click the first document/XHR to that host.
5. **Request headers** — confirm:
   - `Host: cim.freudenberg.com`
   - `Authorization: Negotiate <long base64…>`  
     (may appear on first or second challenge response)
6. Compare with a **working** call to  
   `https://vhffecspci.fra3.sap.invite.freudenberg:…/…`  
   — same `Authorization: Negotiate` pattern.

| Result | Meaning |
|---|---|
| Negotiate present on `cim.freudenberg.com` | Browser sent SPNEGO; WD must forward it — go to 1B |
| No Negotiate on short host | Browser/zone/SPN issue (you said tickets exist — re-check this URL) |
| 401 without Negotiate retry | Backend/WD challenge path odd — include in ECS ticket |

**Export:** HAR file for both success and fail URLs → attach to ECS ticket.

### 1B — What **SAP ECS** checks (Web Dispatcher)

Ask ECS explicitly:

```text
Please verify for hostname cim.freudenberg.com (SID CSD):

1) wdisp/system_* contains SRCVHOST for cim.freudenberg.com and routes to CSD.
2) Host header toward the app server is PRESERVED as cim.freudenberg.com
   (not replaced by vhffecspci… / internal name).
3) icm/HTTP/mod_* / permission filters do NOT remove header Authorization.
4) Confirm Authorization: Negotiate from the client is present on the
   backend connection (WD or ICM trace) at <date/time UTC>.

Please send redacted wdisp/system_* line and confirm Host + Authorization
forwarding.
```

| Check | Owner |
|---|---|
| Browser HAR / Negotiate header | **You** |
| `wdisp/system_*`, Host preserve, mod rules | **SAP ECS** |
| Proof Negotiate on backend hop | **SAP ECS** |

---

## Question 2 — Does SPNEGO accept `HTTP/cim.freudenberg.com`?

### What **your Basis** checks (SAP GUI on CSD) — Freudenberg

1. Log on to **CSD** (client suitable for admin, often 000 or 400 with rights).
2. Transaction **`SPNEGO`** (or Secure Login / SPNego UI used in your release).
3. Open the Kerberos / SPNego configuration for this system.
4. In the list of **Service Principal Names / SPNs / keys**, look for:  
   **`HTTP/cim.freudenberg.com`**  
   (and the working one `HTTP/vhffecspci.fra3.sap.invite.freudenberg` for comparison).
5. Confirm status **enabled / active**, not only present in AD.
6. Note **keytab last import date** — must be **after** the SPN was added in AD.

If you use SAP Single Sign-On product UIs, same idea: realm + SPN list must include the public host.

| Result | Meaning |
|---|---|
| SPN visible and enabled in SPNEGO | Config accepts that principal name → still verify keytab (Q4) |
| Only internal hostname in SPNEGO | **Root cause candidate** — import new keytab with public SPN |
| No SPNEGO access | Ask **SAP ECS** to check SPNEGO config / keytab for you |

```text
ECS/Basis: Please confirm in transaction SPNEGO on CSD that
HTTP/cim.freudenberg.com is registered and enabled, and that the
active keytab was re-imported after this SPN was added in AD.
```

| Check | Owner |
|---|---|
| Transaction SPNEGO UI | **Your Basis** (if authorized) else **SAP ECS** |
| Align with AD SPN list | **Your AD team** + Basis |

---

## Question 3 — Do `dev_icm` traces show success/fail for `cim.freudenberg.com`?

### What **you** do (reproduce only) — Freudenberg

1. Agree a window with SAP (e.g. 10 minutes).
2. Note **exact UTC time**.
3. In Incognito/domain PC:
   - One **success**: SAP hostname URL (SSO works)
   - One **fail**: `https://cim.freudenberg.com/...` (SSO fails)
4. Send ECS: both URLs, timestamps, user ID, client 400, HAR optional.

### What **SAP ECS / hosting** does — SAP

They must (you normally **cannot** on RISE OS):

1. Raise ICM trace level for SPNEGO/security on the app server that received the request (or system-wide briefly).
2. Reproduce with you, then collect:
   - `dev_icm` (and `dev_wdisp` if on WD)
   - Sometimes `dev_crypto` / Secure Login traces
3. Search around your timestamps for:
   - `Negotiate`, `SPNEGO`, `GSS`, `Kerberos`, `keytab`, `HTTP/cim.freudenberg.com`
   - Success vs `accept` / `verify` / `no key` / `wrong principal` errors
4. Compare the **working** vs **failing** Host in the same trace.

```text
Please enable short ICM/SPNEGO trace on CSD, we will hit:
  OK:  https://vhffecspci.fra3.sap.invite.freudenberg:.../…
  FAIL: https://cim.freudenberg.com/...
at <UTC time>, user <id>, client 400.
Please extract from dev_icm (and WD if needed) whether Kerberos/SPNEGO
succeeded or failed for Host cim.freudenberg.com, and the exact error.
```

| Check | Owner |
|---|---|
| Reproduction + timestamps | **You** |
| `dev_icm` / WD traces | **SAP ECS** (hosting) |

---

## Question 4 — Does the keytab contain `HTTP/cim.freudenberg.com`?

### What **SAP ECS / Basis** checks on the server — mainly SAP

The keytab file lives on the app server (path depends on SSO product / `spnego` setup). On ECS you typically **cannot** SSH freely.

Ask SAP:

```text
Please list principals in the active SPNEGO/Kerberos keytab used by CSD
and confirm it contains:
  HTTP/cim.freudenberg.com@<REALM>
and
  HTTP/vhffecspci.fra3.sap.invite.freudenberg@<REALM>
If cim.freudenberg.com is missing, please regenerate keytab from AD
(account that holds both SPNs) and re-import via SPNEGO, then retest.
```

### What **your AD team** checks — Freudenberg

```text
setspn -Q HTTP/cim.freudenberg.com
setspn -Q HTTP/vhffecspci.fra3.sap.invite.freudenberg
```

Confirm both SPNs are on the **same** service account that was used to generate the keytab SAP imported.

| Check | Owner |
|---|---|
| AD SPN on service account | **Your AD team** |
| Keytab file principals on server | **SAP ECS** |
| Re-import into SPNEGO | **Your Basis** and/or **SAP ECS** |

**Important:** Ticket issued by AD ≠ keytab on ABAP. You can have a valid browser ticket while ABAP keytab still lacks that principal → SSO fails only on that hostname.

---

## Suggested RACI (one page)

| Step | Freudenberg | SAP ECS |
|---|---|---|
| Browser HAR, Negotiate header, Host | **R** | I |
| WD `wdisp/system_*`, Host preserve, no strip Authorization | C | **R** |
| Transaction SPNEGO SPN list | **R** (if access) | **R** if no access |
| `dev_icm` / WD traces | Reproduce | **R** |
| Keytab principal list + re-import | AD SPN ownership | **R** on server/keytab |
| Public TLS `SAPSSLS` for cim.freudenberg.com | C | **R** |

R = responsible, C = consulted, I = informed

---

## Single combined ticket text (copy to SAP ECS)

```text
Subject: SPNEGO works on vhffecspci… but fails on cim.freudenberg.com
(Kerberos tickets issued for both SPNs)

Please verify:
1) Web Dispatcher: SRCVHOST/routing for cim.freudenberg.com; Host header
   PRESERVED to backend; Authorization Negotiate not stripped (mod/filters).
2) SPNEGO on CSD: principal HTTP/cim.freudenberg.com enabled.
3) dev_icm (and WD) at <UTC>: success vs fail for both hostnames.
4) Active keytab lists HTTP/cim.freudenberg.com@REALM; re-import if missing.

We will reproduce OK vs FAIL URLs at agreed time; HARs available.
```
