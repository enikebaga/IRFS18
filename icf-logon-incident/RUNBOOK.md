# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

**Systemwide** ICF System Logon JS handlers broken — including **SAP standard** WD (SOAMANAGER), not only CIM. **Forgot password** (link) works; **Log On / Change** do not (no Network). Likely custom System Logon / password-reset implementation applied **globally**. Not zetVisions app code; not the SOAMANAGER IBC warning.

## Status

- [x] SICF `systemloginjs` **active**  
- [x] SICF `/sap/public/bc/ur` **active**  
- [x] SICF `/sap/public/bc/icons` **active**  
- [x] SICF `/sap/bc/webdynpro` **active**  
- [x] Lightspeed OK (200)  
- [x] Log On → no request  
- [x] Systemwide (SOAMANAGER + CIM)  
- [ ] **Next:** SICF → `appl_soap_management` → Error Pages → System Logon → Configuration (note class)  
- [ ] A/B: custom → SAP standard  
- [ ] Coordinate with password-reset implementers  
- [ ] If still broken: `typeof SL_SystemLogin` + HAR → BC-MID-ICF-LGN  

## Basis actions (order)

Full click-path: **[STEP-BY-STEP-SICF.md](STEP-BY-STEP-SICF.md)**

1. **SICF** SOAMANAGER + `zv_menu` → Error Pages → System Logon → Config → note **ABAP Class** / Forgot-password URL.  
2. Find same class on **global** System Logon settings.  
3. **A/B:** set SAP standard class/layout on one service → hard refresh → test Log On.  
4. If fixed: revert custom globally; re-implement Forgot password without breaking `SL_SystemLogin` (keep `super` calls / standard script includes).  
5. If not fixed: F12 `systemloginjs` + Console `typeof SL_SystemLogin` → escalate **BC-MID-ICF-LGN** (KBA 2900689 / 3423597).

## Ignore for this incident

- SOAMANAGER “more than one client IBC” (Note 2353589)  
- favicon.ico 404  
