# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

**CIM:** Service-specific **Custom Implementation** with ABAP class **`/ZCO/CL_ICF_CIM_LOGIN`** (`cim_hmenu`). That is the primary suspect for CIM Log On / Change / Forgot-password behaviour.

**SOAMANAGER:** Earlier screenshot showed **Global Settings** + **SAP Implementation** (no custom class). If form Log On is also dead there, that is a **second** track (systemloginjs / BC-MID-ICF-LGN) — the `/ZCO/` class does not apply to SOAMANAGER.

## Status

- [x] Public ICF nodes active; Lightspeed OK; Log On → no request on CIM  
- [x] SOAMANAGER: Global + SAP Implementation, class empty  
- [x] **CIM `cim_hmenu`:** Service-Specific + **Custom** + **`/ZCO/CL_ICF_CIM_LOGIN`**  
- [x] **`ZV_MENU_RESET`:** **Use Global Settings** + **SAP Implementation** (`SAP_CHROME`), class **empty**  
- [ ] **`zv_menu`** (without `_reset`) Configuration — still needed  
- [ ] **A/B on `cim_hmenu`:** switch to SAP Implementation → Save → test that CIM URL  
- [ ] Browser test **`zv_menu_reset` URL**: if Log On dead here too → not explained by `/ZCO/CL_ICF_CIM_LOGIN` alone → `systemloginjs` / BC-MID-ICF-LGN  
- [ ] SE24 `/ZCO/CL_ICF_CIM_LOGIN` with Dev  

### How to read the two CIM-related services

| Service | Logon config | Implication |
|---|---|---|
| `cim_hmenu` | Custom `/ZCO/CL_ICF_CIM_LOGIN` | A/B this class for branded CIM logon |
| `ZV_MENU_RESET` | Global SAP standard | Dead Log On here ≠ that custom class; separate/global JS issue |

## Ignore for this incident

- SOAMANAGER “more than one client IBC” (Note 2353589)  
- favicon.ico 404  
