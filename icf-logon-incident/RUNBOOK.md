# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

**Systemwide** ICF System Logon: **Log On** produces no HTTP request (JS handlers not firing). Affects CIM and SAP standard WD (SOAMANAGER).

**Update from SICF screenshot:** SOAMANAGER uses **Use Global Settings** + **SAP Implementation** (NetWeaver / `SAP_CHROME`) with **no custom ABAP class**. So a custom `CL_ICF_SYSTEM_LOGIN` subclass is **not** configured on that service (global effective UI class looks SAP standard). Next suspects: **Adjust Links and Images** (Forgot-password URLs/logos), **`zv_menu` service-specific** branding, or **`systemloginjs` / `SL_SystemLogin` init failure** → escalate BC-MID-ICF-LGN if pure SAP Implementation still dead.

## Status

- [x] SICF `systemloginjs`, `ur`, `icons`, `webdynpro` **active**  
- [x] Lightspeed OK (200); Log On → no request; systemwide  
- [x] SOAMANAGER System Logon Configuration: **Global Settings** + **SAP Implementation**, class empty  
- [ ] **Adjust Links and Images** on that dialog (Forgot-password / images)  
- [ ] **`zv_menu`** System Logon Configuration (compare — zetVisions branding)  
- [ ] Browser on SOAMANAGER logon: filter `systemloginjs`; `typeof SL_SystemLogin`  
- [ ] If still broken with SAP Implementation → **BC-MID-ICF-LGN** (KBA 2900689 / 3423597)

## Next clicks (you are in the Configuration popup)

1. Click **Adjust Links and Images** → note any Forgot-password / custom URLs → Cancel back.  
2. Close Configuration → Cancel service (don’t save yet).  
3. SICF filter ServiceName `zv_menu` → Error Pages → System Logon → Configuration → note Global vs Service-Specific and class.  
4. Browser SOAMANAGER logon + F12 (see GLOBAL-CHECKS / STEP-BY-STEP).

## Ignore for this incident

- SOAMANAGER “more than one client IBC” (Note 2353589)  
- favicon.ico 404  
