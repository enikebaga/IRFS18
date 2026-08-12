# Runbook — Unresponsive CIM Log On button

## Status

- [x] SICF: `/sap/public/bc/icf/systemloginjs` **active** (inactive-node theory ruled out)
- [ ] Browser proves JS actually loads with **HTTP 200 + `application/javascript`** (not HTML)
- [ ] Console clean on logon page
- [ ] A/B: SAP standard System Logon vs zetVisions custom class

## 1. Capture evidence (2 min) — do this next

On the **same** failing URL (`https://<host>.sap.invite.freudenberg:44300/...`), F12 → Network + Console:

- [ ] Reload logon page; filter `systemloginjs`, `lightspeed`, `domainrelax`
- [ ] For each script: Status = ?  Content-Type = ?  Response starts with `function`/`var` or with `<html`?
- [ ] Console errors (`UCF_LS`, `ur_relax`, `Unexpected token '<'`, `SL_SystemLogin`)
- [ ] Click Log On — any POST at all?

Also open directly in the browser address bar:

```text
https://<host>.sap.invite.freudenberg:44300/sap/public/bc/icf/systemloginjs
https://<host>.sap.invite.freudenberg:44300/sap/public/bc/ur/nw7/js/lightspeed.js
```

- Pass = raw JS text  
- Fail = logon HTML, 403, 404, 500, or blank

## 2. Decision tree (post–SICF-active)

```text
Via :44300, systemloginjs / lightspeed → 403 / 404 / HTML logon page?
  YES → RISE Web Dispatcher / path rewrite ticket (/sap/public/bc/icf|ur)
        Compare same URLs on direct app-server host if accessible

  → 500 on *.js?
  YES → SE38 WDG_MAINTAIN_UR_MIMES (force deploy); check /sap/public/bc/ur active

  → 200 + real JS, but Console still errors / buttons dead?
  YES → SICF on zv_menu / zv_menu_reset:
        Error Pages → System Logon → switch custom class to SAP standard
        Works? → zetVisions CL_ICF_SYSTEM_LOGIN subclass / branding JS
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
