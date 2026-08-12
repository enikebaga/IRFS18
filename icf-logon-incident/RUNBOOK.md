# Runbook — Unresponsive CIM Log On button

## Status

- [x] SICF: `/sap/public/bc/icf/systemloginjs` **active**
- [x] Real CIM logon page reproduced (`zv_menu`, zetVisions branding)
- [x] UR/Lightspeed working — control JS **200** via `lightspeed.js`
- [x] **Confirmed: click Log On after Network clear → no request at all** (no POST/GET). Button handler never runs.
- [ ] Network on **full reload**: filter `systemloginjs` — any row? status?
- [ ] Console (Errors on) after reload — 2 messages
- [ ] Elements: Inspect **Log On** — tag / `onclick` / surrounding `<form>`
- [ ] Console eval: `typeof SL_SystemLogin` (or similar)
- [ ] **A/B high priority:** SICF System Logon → SAP standard class (disable zetVisions custom)

### Confirmed symptom

Client-side only: UI paints, UR loads, but **Log On does not call the server**. Not a password/auth/SAML problem at this stage.

### Note on the earlier Console 404

`favicon.ico` 404 is irrelevant.

## 1. Capture evidence — do this on the blank tab now

On the blank `systemloginjs` tab, press **F12**:

1. **Network** → click the document request for `systemloginjs`
   - Status code (200 / 403 / 404 / 500 / 302?)
   - **Content-Type** (`application/javascript` / `text/javascript` / `text/html` / empty?)
   - **Size** (0 bytes vs several KB)
2. **Response** / **View Page Source** — empty, HTML, or JS (`function`, `SL_SystemLogin`, …)?
3. Also open:
   ```text
   https://vhffecsdci.sap.invite.freudenberg:44300/sap/public/bc/ur/nw7/js/lightspeed.js
   ```
   Healthy = long JS source. Blank/HTML/error = UR path also broken.

4. Open the **real** CIM logon URL, F12 → Network, filter `systemloginjs` — note the **full** path (often `/sap/public/bc/icf/systemloginjs/<…>/<…>`) and its status. Root URL blank ≠ conclusive; the subpath used by the logon page is decisive (see KBA 3267156).

| Finding | Action |
|---|---|
| 403 / HTML body | RISE Web Dispatcher / auth on `/sap/public/bc/icf/` |
| 200 + **0 bytes** / empty | Handler/`CL_ICF_SYSTEM_LOGIN_JS` content issue — Basis + BC-MID-ICF-LGN |
| 200 + `text/html` | Wrong response / rewrite — WD or ICF |
| 200 + real JS but logon still dead | Check `lightspeed.js` + custom logon class A/B |

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
