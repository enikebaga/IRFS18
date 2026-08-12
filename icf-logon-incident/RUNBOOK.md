# Runbook — Unresponsive CIM Log On button

## Status

- [x] SICF: `/sap/public/bc/icf/systemloginjs` **active**
- [x] Real CIM logon page reproduced (`zv_menu`, zetVisions branding)
- [x] UR/Lightspeed working — control JS **200** via `lightspeed.js`
- [x] **Confirmed: click Log On after Network clear → no request at all** (no POST/GET). Button handler never runs.
- [x] SOAMANAGER opens on same host/client  
  (`/sap/bc/webdynpro/sap/appl_soap_management?sap-client=400`)  
  — WS config warning **"Logical system has more than one client IBC"** (Note **2353589**)  
  — **Not connected** to dead Log On button (SOA/IBC ≠ System Logon JS)
- [ ] Network on **full reload**: filter `systemloginjs` — any row? status?
- [ ] Console: `typeof SL_SystemLogin`
- [ ] **A/B high priority:** SICF System Logon → SAP standard class (disable zetVisions custom)

### Confirmed symptom

Client-side only: UI paints, UR loads, but **Log On does not call the server**. Not a password/auth/SAML problem at this stage.

### SOAMANAGER “severe inconsistencies” — unrelated

That warning is about **Web Service / IBC** configuration (duplicate client IBC for logical system CSD/400). It does not drive ICF System Logon button handlers. Fix later via Note **2353589** if SOA is needed; ignore for the CIM Log On incident.

If you reached SOAMANAGER via a **form** Log On on the same host, that further isolates the defect to the **zetVisions branded** System Logon on `/zco/zv_menu` (custom class/layout), not a global `systemloginjs` outage.

## 1. Next checks (Log On confirmed dead — no Network)

Do these on the **logon page** tab:

1. **Network** → tick **Disable cache** → filter `systemloginjs` → **F5 reload**  
   - Any row? Status? If **none**, System Logon JS was never requested (custom page / broken script tags).
2. **Console** → Default levels → **Errors** on → F5 → copy messages.  
   In Console also run: `typeof SL_SystemLogin`
3. **Elements** → click the picker → click **Log On** → note element type and whether it sits in a `<form>` with `sap-system-login` fields.
4. **Basis A/B (fastest fix test):** SICF → `/sap/bc/webdynpro/zco/zv_menu` (and `zv_menu_reset`) → Error Pages → System Logon → Settings → switch from zetVisions custom class to **SAP standard** → save → hard refresh → retry Log On.

| Finding | Action |
|---|---|
| No `systemloginjs` row on reload | Custom logon HTML missing script include — fix class / layout |
| `systemloginjs` 403/404/empty | WD / handler — BC-MID-ICF-LGN |
| `typeof SL_SystemLogin` → `"undefined"` | Init never ran — script missing or errored |
| SAP standard Log On works; custom dead | zetVisions branding/class regression — vendor + revert |

## 2. Decision tree (post–SICF-active)

```text
Via :44300, systemloginjs (root) → blank white page  [OBSERVED]
  → Read F12 Status + Content-Type + body (mandatory next step)

  Subpath on real logon page, or lightspeed → 403 / 404 / HTML?
  YES → RISE Web Dispatcher / path rewrite (/sap/public/bc/icf|ur)

  → 500 on *.js?
  YES → SE38 WDG_MAINTAIN_UR_MIMES (force deploy); check /sap/public/bc/ur active

  → 200 + empty body on systemloginjs?
  YES → SICF double-click service: Handler List = CL_ICF_SYSTEM_LOGIN_JS?
        SE24: class exists? Note 3534996 if missing
        Escalate BC-MID-ICF-LGN with HAR

  → 200 + real JS, buttons still dead?
  YES → SICF on zv_menu / zv_menu_reset:
        Error Pages → System Logon → switch custom class to SAP standard
```

## 4. Retest

- [ ] `zv_menu` Log On
- [ ] Initial-password Change
- [ ] Logoff → `zv_menu_reset` Log On
- [ ] Edge + Chrome

## 5. Escalate

- Component: **BC-MID-ICF-LGN**
- Attach F12 HAR + SICF screenshot of `systemloginjs`
- Cite KBA **2900689** / **3423597**
