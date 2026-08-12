# Runbook / Basis handoff — Systemwide dead Log On

## Verdict

**CIM:** Service-specific **Custom Implementation** with ABAP class **`/ZCO/CL_ICF_CIM_LOGIN`** (`cim_hmenu`). That is the primary suspect for CIM Log On / Change / Forgot-password behaviour.

**SOAMANAGER:** Earlier screenshot showed **Global Settings** + **SAP Implementation** (no custom class). If form Log On is also dead there, that is a **second** track (systemloginjs / BC-MID-ICF-LGN) — the `/ZCO/` class does not apply to SOAMANAGER.

## Status

- [x] Public ICF nodes active; Lightspeed OK; Log On → no request on CIM  
- [x] SOAMANAGER config: Global + SAP Implementation, class empty  
- [x] **CIM `cim_hmenu`:** Service-Specific + **Custom Implementation** + **`/ZCO/CL_ICF_CIM_LOGIN`**  
- [ ] **A/B now:** switch `cim_hmenu` to **SAP Implementation**, Save, test Log On  
- [ ] Optional: same check on `zv_menu` / `zv_menu_reset`  
- [ ] SE24 `/ZCO/CL_ICF_CIM_LOGIN` → password-reset / zetVisions owners  
- [ ] Re-test SOAMANAGER form Log On separately if still needed  

## A/B clicks (you are on the CIM Configuration popup)

1. Select **SAP Implementation** (not Custom Implementation).  
2. Leave Screen/Theme at SAP defaults (e.g. NetWeaver / Signature — whatever appears).  
3. Confirm with **✓** / Enter / Continue on the dialog.  
4. On the service screen: **Save**.  
5. Browser: Incognito → CIM logon URL → Ctrl+F5 → F12 Network clear → Log On.  

| Result | Next |
|---|---|
| Log On works (or real auth error) | Cause = `/ZCO/CL_ICF_CIM_LOGIN` → fix/revert with Dev; do **not** put custom back until fixed |
| Still dead | Put custom back if needed; check `zv_menu`; escalate JS/`systemloginjs` |

## Ignore for this incident

- SOAMANAGER “more than one client IBC” (Note 2353589)  
- favicon.ico 404  
