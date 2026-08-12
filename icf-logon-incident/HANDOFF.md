# Handover – Logon failure in Web Dynpro applications (CSD / client 400)

**Subject:** Handover – Logon failure in WebDynpro applications (system CSD, client 400)  
**System:** `vhffecsdci.sap.invite.freudenberg:44300` — CSD, client **400**  
**Component (if SAP incident):** **BC-MID-ICF-LGN** (ICF System Login)  
**Related KBAs:** 2900689, 3423597 (Log On button no response / `systemloginjs`)

---

## 1. Problem description

Form **Log On** (User & Password) on the ICF System Logon page does not work: clicking **Log On** produces **no HTTP request** in the browser Network tab (no navigation, no auth error from the server).

Affected examples:

| Application | URL pattern | Notes |
|---|---|---|
| CIM / zetVisions | `/sap/bc/webdynpro/zco/zv_menu`, `cim_hmenu`, … | Branded logon; button dead |
| SAP standard | `/sap/bc/webdynpro/sap/appl_soap_management` (SOAMANAGER) | Reported same Log On failure |

This appears **cross-application**, but SICF shows **different System Logon setups** (see §3) — treat CIM custom class and “pure SAP” services as related but separable tracks.

---

## 2. Analysis already performed

| Check | Result |
|---|---|
| `WDR_TEST_UI_ELEMENTS` | Works → Web Dynpro / UI framework fundamentally healthy |
| `WDLIGHTSPEED=X` | Same behaviour → Lightspeed not the root cause |
| F12 Network on Log On click (CIM) | **No request at all** after clear → click handler never fires (not a failed OAuth/401 round-trip) |
| Lightspeed control JS (`InputField.js`, …) | HTTP **200** |
| SICF `/sap/public/bc/icf/systemloginjs` | **Active** |
| SICF `/sap/public/bc/ur`, `/icons`, `/sap/bc/webdynpro` | **Active** |
| SOAMANAGER IBC warning (“more than one client IBC”, Note 2353589) | **Unrelated** SOA config (separate topic) |

---

## 3. SICF System Logon findings (important)

| Service | System Logon settings | ABAP class |
|---|---|---|
| **`cim_hmenu`** | Service-specific + **Custom Implementation** | **`/ZCO/CL_ICF_CIM_LOGIN`** |
| **`ZV_MENU`** | Service-specific + **Custom Implementation** | **`/ZCO/CL_ICF_CIM_LOGIN`** |
| **`ZV_MENU_RESET`** | **Use Global Settings** + **SAP Implementation** (`SAP_CHROME`) | (none) |
| **SOAMANAGER** (`appl_soap_management` / related) | **Use Global Settings** + **SAP Implementation** | (none) |

**Primary action for CIM / `ZV_MENU`:** A/B test — switch to **SAP Implementation** (temporarily remove `/ZCO/CL_ICF_CIM_LOGIN`), Save, Incognito + hard refresh, retest Log On.

- If Log On works → root cause is **`/ZCO/CL_ICF_CIM_LOGIN`** (hand to Dev / owner of that class; do **not** add this class to `ZV_MENU_RESET` until fixed).  
- If still dead on SAP Implementation → continue §5 (JS / `systemloginjs` / SAP Support).

**Do not** add `/ZCO/CL_ICF_CIM_LOGIN` to `ZV_MENU_RESET` as a “fix” — that propagates the suspect customisation onto the clean global path.

---

## 4. Refined conclusion (vs OAuth-first suspicion)

| Hypothesis | Fit to evidence |
|---|---|
| **Custom System Logon class `/ZCO/CL_ICF_CIM_LOGIN`** (CIM / `ZV_MENU`) | **Strong** for branded CIM URLs — confirmed in SICF; A/B pending |
| Client-side System Logon JS not initializing (`SL_SystemLogin` / `systemloginjs`) | **Strong** where Log On click = **zero** Network (also possible on SAP Implementation services) |
| OAuth/SSO / SOAUTH2 as **primary** cause of dead Log On button | **Weak** for the observed symptom — OAuth failures usually show **302/401** (or similar) in Network; here the button often fires **nothing** |
| DNS/port/cookie/origin mismatch (`test-cim` → `vhffecsdci:44300`) | **Possible secondary** after a request exists; does not explain a click with **no** request |
| WD / Lightspeed framework broken | **Ruled out** (`WDR_TEST_UI_ELEMENTS`, lightspeed 200s) |

OAuth/SSO remains worth checking as a **parallel** topic (especially if separate OAuth test services fail), but it should not replace the System Logon A/B and F12 proof above.

---

## 5. Please check / do next (ordered)

### A. CIM track (immediate)

1. SICF → `ZV_MENU` (and `cim_hmenu`) → Error Pages → System Logon → Configuration.  
2. Switch **Custom Implementation** → **SAP Implementation** → Save.  
3. Test:  
   `https://vhffecsdci.sap.invite.freudenberg:44300/sap/bc/webdynpro/zco/zv_menu?sap-client=400&sap-language=EN`  
   Incognito, Ctrl+F5, F12 Network on Log On.  
4. If fixed → SE24 `/ZCO/CL_ICF_CIM_LOGIN` with development (Forgot-password / custom HTML/JS); fix class, then restore.

### B. “Pure SAP” track (SOAMANAGER / `ZV_MENU_RESET`)

1. Confirm form Log On still fails on SOAMANAGER and/or `zv_menu_reset` **without** custom class.  
2. F12 on that logon page:  
   - Network filter `systemloginjs` on reload (status / body)  
   - Console: `typeof SL_SystemLogin`  
   - Clear Network → Log On → any request? host/port/status?  
3. HAR + screenshots → SAP **BC-MID-ICF-LGN** (KBA 2900689 / 3423597) if still dead.

### C. Optional / parallel (not first for dead button)

- OAuth/SSO: SOAUTH2, SICF OAuth nodes — if OAuth **test** apps fail with visible HTTP errors.  
- `/sap/public/bc/icf/logoff` and central public ICF nodes (already: `systemloginjs` active).  
- SM21 / ST22 / SICF server trace — only meaningful **if** a request reaches the server; less useful when click sends nothing.  
- Host/port/cookie: compare browser URL host with `icm/host_name_full` / redirect chain **after** a request appears.

---

## 6. Short text for ticket / email

```text
CSD client 400 (vhffecsdci…:44300): ICF System Logon “Log On” does nothing
(no HTTP request). WD framework OK (WDR_TEST_UI_ELEMENTS); Lightspeed OK.

SICF: cim_hmenu + ZV_MENU use Custom Implementation class
/ZCO/CL_ICF_CIM_LOGIN. ZV_MENU_RESET + SOAMANAGER use Global SAP
Implementation (no custom class). systemloginjs/ur active.

Please: (1) A/B ZV_MENU to SAP Implementation and retest;
(2) if CIM fixed, repair /ZCO/CL_ICF_CIM_LOGIN with Dev;
(3) if SOAMANAGER/zv_menu_reset still dead, F12 systemloginjs +
typeof SL_SystemLogin + HAR → BC-MID-ICF-LGN (KBA 2900689/3423597).
OAuth/SSO is parallel only — dead button with zero Network is not
explained by OAuth alone.
```

---

## 7. References in this repo

- `STEP-BY-STEP-SICF.md` — click path for A/B  
- `GLOBAL-CHECKS.md` — RZ11 / ICF health checklist  
- `RUNBOOK.md` — current status  
