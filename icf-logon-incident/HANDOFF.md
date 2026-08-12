# Ticket handoff — Systemwide Log On button dead

## Symptom

On S/4HANA 2023 (CSD client 400), ICF System Logon **Log On** and **Change Password** do nothing (no HTTP request in browser Network). Affects:

- Custom: `https://vhffecsdci.sap.invite.freudenberg:44300/sap/bc/webdynpro/zco/zv_menu?…`
- Standard: `https://vhffecsdci.sap.invite.freudenberg:44300/sap/bc/webdynpro/sap/appl_soap_management?sap-client=400&sap-language=EN`

**Forgot your password?** link still works.

## Evidence

- `/sap/public/bc/icf/systemloginjs` **active** in SICF  
- UR/Lightspeed control scripts load (**HTTP 200**)  
- Click Log On after clearing Network → **zero** new requests  
- Scope confirmed **systemwide** by Basis/Dev (not only zetVisions)

## Suspected cause

Custom **System Logon** / **Forgot password** implementation (custom ABAP class subclassing `CL_ICF_SYSTEM_LOGIN` or custom logon HTML/JS) applied globally: link works, submit handlers do not.

## Requested actions

Detailed click-path: see **`STEP-BY-STEP-SICF.md`** in this folder.

1. Identify System Logon **ABAP class** and Forgot-password config (SICF System Logon Configuration — global + affected services).  
2. A/B switch to **SAP standard** System Logon; retest Log On.  
3. Involve team that implemented password reset; fix/revert customisation.  
4. If standard still fails → SAP incident **BC-MID-ICF-LGN**, attach HAR + cite KBA 2900689 / 3423597.

## Out of scope for this ticket

SOAMANAGER warning “Logical system has more than one client IBC” (SAP Note 2353589) — separate SOA issue.
