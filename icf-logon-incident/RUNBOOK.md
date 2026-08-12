# Runbook — Unresponsive CIM Log On button

## 1. Capture evidence (2 min)

On failing URL with F12 → Network + Console:

- [ ] Status of `/sap/public/bc/icf/systemloginjs`
- [ ] Status of `/sap/public/bc/ur/nw7/js/lightspeed.js`
- [ ] Any Console `ReferenceError` / `Unexpected token '<'`
- [ ] Click Log On — confirm **zero** application request vs a failed POST

## 2. Decision tree

```text
systemloginjs or lightspeed → 403/404?
  YES → SICF activate /sap/public/bc/icf/systemloginjs (+ /sap/public/bc/ur)
        Still 403 via :44300? → RISE Web Dispatcher ticket for /sap/public/bc/icf|ur
  NO, → 500 on *.js?
  YES → SE38 WDG_MAINTAIN_UR_MIMES (force deploy)
  NO, all 200 + clean console?
  YES → SICF: switch System Logon to SAP standard (disable zetVisions custom class)
        Works? → vendor fix for custom CL_ICF_SYSTEM_LOGIN subclass
```

## 3. SICF activate (copy-paste path)

```text
/default_host/sap/public/bc/icf/systemloginjs
/default_host/sap/public/bc/ur
/default_host/sap/public/bc/icons
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
