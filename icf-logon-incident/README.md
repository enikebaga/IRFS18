# ICF / Web Dynpro ABAP — Unresponsive Log On / Change Password

**Incident:** Systemwide web System Logon — Log On / Change Password do nothing; “Forgot your password?” still works  
**System:** SAP S/4HANA 2023 · SAP_BASIS 7.58 · SAP_UI 7.58 SP2 (SAPK-75802INSAPUI) · RISE (SAP-managed Web Dispatcher)  
**Scope clarification:** The Log On failure is **not exclusive to CIM**. Form logon with User & Password also fails on **SAP standard Web Dynpro**, e.g. SOAMANAGER (`/sap/bc/webdynpro/sap/appl_soap_management`). Same host/client as CIM.

## Verdict

**Systemwide ICF System Logon defect (client-side):** the HTML page renders, Unified Rendering / Lightspeed loads, but the JavaScript that must handle **Log On** / **Change Password** never runs — Network shows **no request** after click.

This is **not** a zetVisions WDA application bug, **not** wrong passwords, and **not** the SOAMANAGER “client IBC” warning (Note 2353589).

Colleagues’ observation fits the evidence well:

| Control | Needs | Behaviour |
|---|---|---|
| **Forgot your password?** | Usually a plain hyperlink / navigation to a reset app | **Works** |
| **Log On** / **Change Password** | System Logon JS (`SL_SystemLogin` / `systemloginjs`) submit handlers | **Dead — no Network** |

That pattern strongly suggests a **custom System Logon / password-reset implementation** (custom `CL_ICF_SYSTEM_LOGIN` subclass, custom HTML/JS, or global System Logon settings) that added the Forgot-password link but broke or omitted the standard Log On wiring — applied **globally**, hence SOAMANAGER is affected too.

---

## Evidence gathered

| Check | Result |
|---|---|
| SICF `/sap/public/bc/icf/systemloginjs` | **Active** |
| CIM logon page | Renders (zetVisions branding) |
| `lightspeed.js` + control JS | **OK** (HTTP 200) |
| Click Log On (Network cleared) | **No POST/GET at all** |
| Scope | **Systemwide** — SAP standard SOAMANAGER form logon also broken |
| Forgot password link | **Works** (per Basis/Dev) |
| SOAMANAGER IBC inconsistency | Unrelated SOA config (Note 2353589) |

---

## What Basis / password-reset owners should do

### 1. Find the global System Logon customisation (primary)

1. **SICF** → service `/sap/bc/webdynpro/sap/appl_soap_management` (and `/zco/zv_menu`) → **Error Pages** → **Logon Errors** → **System Logon** → **Configuration**.
2. Note:
   - **ABAP Class** (anything other than SAP standard / empty → custom)
   - Layout / links / “Forgot password” URL
   - Global vs service-specific settings
3. Also check **global** System Logon defaults (SICF → right-click `default_host` / SAP help “System Logon” global configuration; table/view usage varies by release — look for the same custom class name systemwide).
4. **SE24**: open that custom class (subclass of `CL_ICF_SYSTEM_LOGIN` or related). Search for password-reset / forgot-password changes, redefined HTML/JS methods, missing `super→` calls.

### 2. Immediate A/B (proves the theory in minutes)

On **one** affected service (e.g. SOAMANAGER or `zv_menu`):

1. Switch System Logon from **custom class → SAP standard** (remove custom class / use SAP default layout).
2. Hard-refresh browser (Disable cache).
3. Retry **Log On**.

| Result | Conclusion |
|---|---|
| Log On works again | Custom System Logon / Forgot-password implementation is the cause — revert globally, then re-add Forgot-password safely |
| Log On still dead | Keep investigating `systemloginjs` load / Notes below — still Basis **BC-MID-ICF-LGN** |

Repeat for global default if service-level A/B succeeds only on the edited service.

### 3. Browser proof to attach to the ticket

On the broken logon page (F12):

1. Network → **Disable cache** → filter `systemloginjs` → reload → screenshot status/rows.
2. Console: `typeof SL_SystemLogin` → expect `"undefined"` if handlers never init.
3. Confirm again: clear Network → Log On → **zero** new requests.
4. Optional HAR export.

### 4. If A/B does not restore Log On

- Confirm `systemloginjs` subpath on the logon page (not only service root) returns real JS.
- KBA **2900689** / **3423597** / **3272754**; component **BC-MID-ICF-LGN**.
- RISE Web Dispatcher only if public JS returns 403/HTML (less likely now that lightspeed 200s).

### 5. Do not chase

- SOAMANAGER “Logical system has more than one client IBC” — separate; Note **2353589**.
- zetVisions application code under `/ZCO/` — ruled out by SOAMANAGER failure.
- SAML/SPNego alone — would redirect or error, not silent dead buttons with working Forgot-password link.

---

## Handoff summary (paste to ticket)

```text
Systemwide ICF System Logon: Log On / Change Password do nothing (no HTTP
request). Forgot password link works. Affects custom CIM (/zco/zv_menu) and
SAP standard SOAMANAGER. Lightspeed/UR JS loads (200). SICF systemloginjs
active. Suspected cause: custom System Logon class / Forgot-password
implementation breaking SL_SystemLogin handlers. Please identify global
System Logon ABAP class, A/B to SAP standard, coordinate with password-reset
implementers. Component BC-MID-ICF-LGN if standard still fails. Evidence:
F12 Network (no POST on Log On), lightspeed 200s, SICF active screenshot.
```

---

## SAP references

| Note / KBA | Use |
|---|---|
| [2900689](https://userapps.support.sap.com/sap/support/knowledge/en/2900689) | Log On does nothing; `systemloginjs` |
| [3423597](https://userapps.support.sap.com/sap/support/knowledge/en/3423597) | Logon button no response |
| [3272754](https://userapps.support.sap.com/sap/support/knowledge/en/3272754) | System Logon unresponsive (UR MIME) |
| [2353589](https://userapps.support.sap.com/sap/support/knowledge/en/2353589) | SOAMANAGER IBC inconsistency — **unrelated** |
| Component | **BC-MID-ICF-LGN** |
