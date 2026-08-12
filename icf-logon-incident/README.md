# ICF / Web Dynpro ABAP — Unresponsive Log On / Change Password

**Incident:** CIM/CDB (zetVisions) web logon — Log On and Change Password buttons do nothing  
**System:** SAP S/4HANA 2023 · SAP_BASIS 7.58 · SAP_UI 7.58 SP2 (SAPK-75802INSAPUI) · RISE (SAP-managed Web Dispatcher)  
**Apps:** `/sap/bc/webdynpro/zco/` — `cim_hmenu`, `zv_menu`, `zv_main`, `zv_menu_reset`

## Verdict

This is almost certainly a **client-side JavaScript failure on the ICF System Logon page**, not a Web Dynpro application bug and not a wrong username/password. The HTML/branding renders, but the script that wires the **Log On** / **Change** buttons never becomes active — so no (or only a hollow) submit happens, with no server-side error.

### Status update (SICF + browser)

| Check | Result |
|---|---|
| SICF `/sap/public/bc/icf/systemloginjs` | **Active** (inactive-node theory ruled out) |
| Browser `https://vhffecsdci.sap.invite.freudenberg:44300/sap/public/bc/icf/systemloginjs?sap-client=400` | **Blank white page** — not the expected JS source listing |

Blank at the **service root** is suspicious and matches the symptom family in KBA **3423597** / **3267156**, but is not final until F12 shows Status / Content-Type / body. The logon page usually calls a **subpath** under `systemloginjs/…`; that request’s status is decisive.

**Remaining suspects (in order):**

1. `systemloginjs` returns empty / wrong Content-Type / 403 via Web Dispatcher (confirm with F12 on the blank tab)  
2. Unified Rendering JS broken (`lightspeed.js`)  
3. Custom zetVisions System Logon class breaks button handlers while SAP standard works

---

## Why this matches your symptoms

| Observation | Interpretation |
|---|---|
| Page and branding render correctly | HTML/CSS and custom System Logon layout load; problem is not “service down” |
| Log On click → no navigation, no error, **no request** | Button click handler never attached (JS missing / failed) |
| Change Password → fields clear / page reloads, no error | Default form navigation without System Logon JS setting `sap-system-login-*` fields |
| Same after logoff on `zv_menu_reset` | Shared ICF System Logon infrastructure, not one WDA component |
| Multiple users, Edge + Chrome | Server/config issue, not a local browser profile |
| SAML (`Z_SAML_CSQ`) + SPNego also present | Unrelated to the dead button; form logon still needs `systemloginjs` |

Custom WDA under `/ZCO/` only chooses **System Logon** as the ICF error/logon page. The dead buttons live in the **ICF System Logon** framework (`CL_ICF_SYSTEM_LOGIN` / branded subclass), not in `zv_menu` coding.

---

## Confirm in 5 minutes (browser)

Open the failing URL, press **F12**, then:

1. **Network** — reload the logon page; filter for `systemloginjs`, `lightspeed`, `domainrelax`, `nw07`.
2. Click **Log On** once with dummy credentials; confirm whether **any** POST/GET is sent.
3. **Console** — look for:
   - `UCF_LS is not defined`
   - `ur_relax is not defined`
   - `SL_SystemLogin` / `ReferenceError`
   - `Unexpected token '<'` on a `.js` URL (HTML/login page returned instead of JS)

**Expected smoking gun:**

```text
GET /sap/public/bc/icf/systemloginjs/…   → 403 Forbidden  or  404 Not Found
```

or

```text
GET /sap/public/bc/ur/nw7/js/lightspeed.js → 403 / 404 / 500
```

If those URLs return **200** with real JavaScript and Console is clean, skip to [Secondary causes](#secondary-causes).

---

## Fix path A — Activate `systemloginjs` (most common)

**Status:** SICF node is already **active** — skip activation; still verify **browser reachability** via `:44300` (Web Dispatcher).

**Refs:** KBA [2900689](https://userapps.support.sap.com/sap/support/knowledge/en/2900689), [3423597](https://userapps.support.sap.com/sap/support/knowledge/en/3423597), [3194434](https://userapps.support.sap.com/sap/support/knowledge/en/3194434)

1. ~~Transaction **SICF** → activate `systemloginjs`~~ — **done / confirmed active**.
2. Also confirm related public nodes are active:
   - `/sap/public/bc/ur`
   - `/sap/public/bc/icons`
   - `/sap/public/bc/icf` (parent)
3. From a workstation that uses the failing URL, open:
   - `https://<host>:44300/sap/public/bc/icf/systemloginjs`
   - `https://<host>:44300/sap/public/bc/ur/nw7/js/lightspeed.js`  
   Expect raw JavaScript. If you get HTML logon, 403, or 500 → not truly reachable from the client path.
4. On RISE, if SICF is active but the Web Dispatcher still returns 403/HTML, open an **SAP RISE / BTP Ops** ticket to allow `/sap/public/bc/icf/` (and `/sap/public/bc/ur/`) through the managed Web Dispatcher.

---

## Fix path B — Unified Rendering MIME / JS 500s

**Refs:** KBA [3272754](https://userapps.support.sap.com/sap/support/knowledge/en/3272754), [3290983](https://userapps.support.sap.com/sap/support/knowledge/en/3290983)

If Network shows **500** on `lightspeed.js` / `domainrelax.js`, or Console has `UCF_LS` / `ur_relax` undefined:

1. SICF: confirm `/sap/public/bc/ur` is active.
2. SE38: run **`WDG_MAINTAIN_UR_MIMES`** → Deploy / Force MIME Deployment (basis change window).
3. Recheck UR version / notes per **2090746** (Unified Rendering).
4. Retest logon page after MIME deploy + browser cache clear.

---

## Fix path C — Web Dispatcher routing (RISE)

**Ref:** [SAP Community — WDA Log On dead behind Web Dispatcher](https://community.sap.com/t5/technology-q-a/web-dynpro-application-log-on-button-is-not-working/qaq-p/586008)

If the same service works when called **bypassing** the Web Dispatcher (direct app-server URL from a jump host) but fails via  
`https://<host>.sap.invite.freudenberg:44300/...`:

- Public UR/ICF scripts are being routed to the wrong backend (or blocked).
- Ask SAP-managed WD to ensure backend SRCURL includes at least:
  - `/sap/bc/webdynpro/`
  - `/sap/public/` (or explicitly `/sap/public/bc/ur/` and `/sap/public/bc/icf/`)
- Prefer `wdisp/system_conflict_resolution = BEST_MATCH` when multiple systems share prefixes.
- Clear browser cache after WD change (stale wrong JS is a frequent “still broken” trap).

FQDN is already used in your URL pattern — good (IP-only logon cookie issues per KBA **2063490** are unlikely here).

---

## Secondary causes

Check these only if Network shows `systemloginjs` and UR JS as **200** and Console is clean:

1. **Custom System Logon class** (zetVisions branding)  
   In SICF on the WDA service → Error Pages → System Logon → Settings: note the custom class (subclass of `CL_ICF_SYSTEM_LOGIN`). Temporarily switch to SAP standard layout/class. If buttons work again, the custom class/JS/HTML is breaking handlers — fix with vendor or revert branding.

2. **Logon procedure mix (SAML / SPNego / Fields)**  
   For `zv_menu_reset` (“without SSO”), Logon Data should allow **Logon Through HTTP Fields** (and not only SAML/SPNego). Wrong procedure usually yields a **visible** error or SSO redirect, not a fully dead button — lower priority given your symptom.

3. **Initial password / `icf/reject_expired_passwd`**  
   KBA **2567768** covers wrong behaviour on password change when that parameter is `1`, but typically with an error message, not a silent clear. Still verify RZ11 if only the Change screen misbehaves after Log On is fixed.

4. **UI / ICF notes for 7.58**  
   Related corrections referenced from newer KBAs (e.g. 3463884, 3538273, 3597092) — apply if SP level / note analyzer shows them missing. Less likely than inactive `systemloginjs` when **no** request is fired.

---

## SICF checklist for `/sap/bc/webdynpro/zco/*`

| Check | Where |
|---|---|
| Service active | `cim_hmenu`, `zv_menu`, `zv_main`, `zv_menu_reset` |
| Error Pages → Logon | **System Logon** (not a broken explicit HTML page) |
| System Logon settings | Global vs service-specific; custom class name documented |
| Logon Data (`zv_menu_reset`) | Alternative logon includes **HTTP Fields** for manual logon after logoff |
| Client | `sap-client=400` consistent with service / `login/system_client` |

---

## Suggested test matrix (after fix)

1. Incognito Edge + Chrome → `zv_menu?sap-client=400&sap-language=EN` → Log On with known user.
2. User with initial password → Change Password completes and continues into app.
3. Log off → land on `zv_menu_reset` → Log On again.
4. Optional: WEBGUI or SOAMANAGER System Logon — if those were also dead, confirms global ICF/UR issue; if only `/zco/` fails after A/B/C, focus on custom logon class for that service.

---

## SAP references

| Note / KBA | Relevance |
|---|---|
| [2900689](https://userapps.support.sap.com/sap/support/knowledge/en/2900689) | Log On does nothing; 403/404 on `systemloginjs` |
| [3423597](https://userapps.support.sap.com/sap/support/knowledge/en/3423597) | Logon visible, button no response; `/sap/public/bc/icf/systemloginjs` |
| [3194434](https://userapps.support.sap.com/sap/support/knowledge/en/3194434) | 403 on `systemloginjs` |
| [3272754](https://userapps.support.sap.com/sap/support/knowledge/en/3272754) | Unresponsive / broken System Logon; UR MIME / `lightspeed.js` |
| [3290983](https://userapps.support.sap.com/sap/support/knowledge/en/3290983) | JS parse errors → `UCF_LS` / `ur_relax` undefined |
| [2063490](https://userapps.support.sap.com/sap/support/knowledge/en/2063490) | IP vs FQDN cookie issues (probably N/A here) |
| Component | **BC-MID-ICF-LGN** (ICF System Login) |

---

## What this is not

- Not a defect in Web Dynpro component logic of `zv_menu` / `zv_main`.
- Not “wrong password” (that would show a System Logon error text).
- Not primarily a SAML IdP outage (form buttons would still post; SSO would redirect).

---

## Recommended next action for the Basis / RISE team

1. Reproduce with F12 → capture Network status for `systemloginjs` and `lightspeed.js`.  
2. If 403/404 → activate `/sap/public/bc/icf/systemloginjs` (and parents) in SICF; if already active → escalate to SAP-managed Web Dispatcher allow-list for `/sap/public/bc/icf/` and `/sap/public/bc/ur/`.  
3. If 500 on UR JS → `WDG_MAINTAIN_UR_MIMES`.  
4. If all 200 → A/B test SAP standard System Logon vs zetVisions custom class.
