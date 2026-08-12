# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

**CIM:** Service-specific **Custom Implementation** with ABAP class **`/ZCO/CL_ICF_CIM_LOGIN`** (`cim_hmenu`). That is the primary suspect for CIM Log On / Change / Forgot-password behaviour.

**SOAMANAGER:** Earlier screenshot showed **Global Settings** + **SAP Implementation** (no custom class). If form Log On is also dead there, that is a **second** track (systemloginjs / BC-MID-ICF-LGN) — the `/ZCO/` class does not apply to SOAMANAGER.

## Status

- [x] Public ICF nodes active; Lightspeed OK; Log On → no request on CIM  
- [x] SOAMANAGER: Global + SAP Implementation, class empty  
- [x] **CIM `cim_hmenu`:** Service-Specific + **`/ZCO/CL_ICF_CIM_LOGIN`**  
- [x] **`ZV_MENU`:** Service-Specific + **Custom** + **`/ZCO/CL_ICF_CIM_LOGIN`** (client 400 / EN) — **same class**  
- [x] **`ZV_MENU_RESET`:** Global + SAP Implementation, class empty  
- [ ] **A/B now on this `ZV_MENU` dialog:** SAP Implementation → ✓ → Save → test `zv_menu` URL  
- [x] SE24: **`/ZCO/CL_ICF_CIM_LOGIN`** exists, **Active** (CSD client 400)  
- [ ] SE24 Display: superclass = `CL_ICF_SYSTEM_LOGIN`? redefined methods? Forgot-password / HTML / JS?  
- [ ] **A/B on `ZV_MENU`:** SAP Implementation → Save → test Log On  
- [ ] If A/B fixes → Dev owns this class; leave SAP Implementation until fixed  
- [ ] `zv_menu_reset` / SOAMANAGER still dead → BC-MID-ICF-LGN track  

### SE24 — what to inspect in `/ZCO/CL_ICF_CIM_LOGIN`

1. Click **Display**.  
2. Tab **Properties** / inheritance: superclass should be **`CL_ICF_SYSTEM_LOGIN`** (or SAP login base).  
3. Tab **Methods**: note methods that are **redefined** (not only inherited). Especially anything with HTML, script, link, password, logon, render.  
4. Open redefined methods → look for Forgot-password URL, custom JS, missing `super->…` calls.  
5. **Utilities → Versions** (or Ctrl+F5 version): last change date / transport / author → who owns Forgot-password.  
6. Do **not** change the class yet — first finish SICF A/B on `ZV_MENU`.  

### Service map

| Service | Logon | Class |
|---|---|---|
| `cim_hmenu` | Service-specific custom | `/ZCO/CL_ICF_CIM_LOGIN` |
| `ZV_MENU` | Service-specific custom | `/ZCO/CL_ICF_CIM_LOGIN` |
| `ZV_MENU_RESET` | Global SAP | (none) |
| SOAMANAGER | Global SAP | (none) |

## A/B clicks (**do this now** on the open `ZV_MENU` Configuration)

1. Select **SAP Implementation** (deselect Custom Implementation).  
2. Class `/ZCO/CL_ICF_CIM_LOGIN` should no longer apply (field greys out).  
3. Confirm **✓** / Continue.  
4. **Save** the service.  
5. Incognito →  
   `https://vhffecsdci.sap.invite.freudenberg:44300/sap/bc/webdynpro/zco/zv_menu?sap-client=400&sap-language=EN`  
   → Ctrl+F5 → Network clear → Log On.  

| Result | Next |
|---|---|
| Works / real auth error | Cause = **`/ZCO/CL_ICF_CIM_LOGIN`** → Dev fixes class; leave SAP Implementation until then |
| Still dead | Tell me; check Adjust Links and Images + browser `systemloginjs` |

## Ignore for this incident

- SOAMANAGER “more than one client IBC” (Note 2353589)  
- favicon.ico 404  
