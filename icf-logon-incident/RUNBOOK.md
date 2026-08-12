# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

Systemwide **ICF System Logon** JS handlers broken. **Forgot password** (link) works; **Log On / Change** do not (no Network). Likely custom System Logon / password-reset implementation. Not zetVisions app code; not SOAMANAGER IBC warning.

## Status

- [x] SICF `systemloginjs` active  
- [x] Lightspeed OK (200)  
- [x] Log On → no request  
- [x] Systemwide (SOAMANAGER + CIM)  
- [x] Forgot password works (per Basis/Dev)  
- [ ] Identify custom System Logon ABAP class (global + service)  
- [ ] A/B: custom → SAP standard  
- [ ] Coordinate with password-reset implementers  
- [ ] If still broken: `typeof SL_SystemLogin` + `systemloginjs` Network + BC-MID-ICF-LGN  

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
