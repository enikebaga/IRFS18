# Global checks — Web Dynpro / System Logon health

Use this when apps should accept **User + Password** form logon (CIM, SOAMANAGER, WEBGUI, etc.).

**Important for your incident:** a **dead Log On button (no Network request)** is almost never fixed by RZ11 alone. Check **SICF Global System Logon** first (custom class / Forgot-password). Profile parameters matter once the button actually posts.

---

## 1. SICF — Global System Logon (highest priority)

Transaction **`SICF`** → any WD service (e.g. `appl_soap_management`) → **Error Pages** → **System Logon** → **Configuration**:

| Check | Healthy value |
|---|---|
| Top radio | Know whether **Global Settings** or **Service-Specific** is in effect |
| **Custom Implementation / ABAP class** | Empty = SAP standard. A `Z*` / `/ZCO/*` / vendor class = custom (suspect for your case) |
| Layout | SAP default unless branding is intentional and tested |
| Forgot-password / extra links | Optional; must not break Log On JS |
| **Save as Global Settings** | Only with auth `S_ADMI_FCD` = **ICFA**; changes hit **all** System Logon pages |

Also confirm **System Logon** is selected (not a broken explicit HTML page / bad redirect).

Detail: [`STEP-BY-STEP-SICF.md`](STEP-BY-STEP-SICF.md)

---

## 2. SICF — Services that must be **Active**

| Path | Why |
|---|---|
| `/sap/public/bc/icf/systemloginjs` | Log On / Change button JavaScript |
| `/sap/public/bc/ur` | Unified Rendering / Lightspeed |
| `/sap/public/bc/icons` | Icons on logon UI |
| `/sap/bc/webdynpro` (and your apps under it) | WDA runtime |
| `/sap/bc/webdynpro/sap/appl_soap_management` | SOAMANAGER |
| `/sap/bc/webdynpro/zco/zv_menu` (+ `zv_menu_reset`, …) | CIM |

Grey = inactive → right-click → **Activate Service** (activate parents too).

---

## 3. Profile parameters — transaction **`RZ11`** (display) / **`RZ10`** (change)

Check **Current value**. Do not change in production without Basis change control.

### Host / HTTP (session & cookies)

| Parameter | Typical healthy expectation | If wrong |
|---|---|---|
| `icm/host_name_full` | FQDN, e.g. `vhffecsdci.sap.invite.freudenberg` | Cookie/session issues; logon may reload |
| `SAPLOCALHOSTFULL` | Same FQDN idea on app servers | Same family of problems |
| `login/ticket_only_by_https` | `1` if you only use HTTPS | Ticket/cookie quirks on mixed HTTP |

Your URLs already use FQDN + HTTPS — still verify these match the browser host.

### Form logon / password (after the button works)

| Parameter | Meaning | Note for you |
|---|---|---|
| `login/system_client` | Default client | Should align with `sap-client=400` usage |
| `icf/reject_expired_passwd` | `1` = reject initial/expired password via HTTP without proper change flow | Can break **Change Password / initial password** scenarios (Note 454962 / 1042274 / 2567768). Does **not** explain a completely dead Log On click. |
| `login/password_downwards_compatibility` | Password hash compatibility | Wrong value → auth errors after submit, not silent button |
| `login/fails_to_user_lock` | Lock after N failures | Operational, not dead-button |

### SSO tickets (if you use MYSAPSSO2 / logon tickets alongside form)

| Parameter | Typical | Note |
|---|---|---|
| `login/create_sso2_ticket` | Often `2` (or as per your SSO design) | Needed if apps expect SSO tickets after logon |
| `login/accept_sso2_ticket` | Often `1` | Accept tickets from trusted systems |

SAML (`Z_SAML_CSQ`) / SPNego are configured mainly in **SAML2**, **SPNEGO**, and SICF **Logon Data** tab — not only RZ11.

### ICM (SMICM / profile)

| Parameter / check | Healthy |
|---|---|
| HTTPS service in **SMICM** → Services | Port **44300** (or your WD port) active |
| `icm/server_port_*` | PROT=HTTPS, correct PORT |
| `icm/HTTP/logging_0` (optional) | Useful while debugging |

---

## 4. SICF — Logon Data tab (per service, but check globally used apps)

For SOAMANAGER and `zv_menu` / `zv_menu_reset`:

| Setting | For User/Password form logon |
|---|---|
| Procedure | **Alternative Logon Procedure** (typical) |
| List includes | **Logon Through HTTP Fields** (required for System Logon form) |
| Also present if needed | SSO / SAML / SPNego as ordered alternatives |
| Client | Fixed client 400 or from URL `sap-client=400` |

If only SAML/SPNego are allowed and form fields are removed, browser behaviour differs (redirect/SSO) — still not usually “button does nothing with zero Network”.

---

## 5. Quick smoke tests (same host `:44300`)

Run after any global change; use Incognito + Disable cache.

| URL / action | Pass criteria |
|---|---|
| SOAMANAGER WD URL | Log On **creates a Network request**; success or real auth error |
| CIM `zv_menu` | Same |
| Network filter `systemloginjs` on reload | Row present, **200**, JS body |
| Network filter `lightspeed.js` | **200** |
| Console | `typeof SL_SystemLogin` not `"undefined"` |
| Click Log On | Not silence — some HTTP activity |

---

## 6. What to check vs what to ignore for *your* symptom

| Check | Relevant to “Log On does nothing”? |
|---|---|
| SICF **Global System Logon** custom class / Forgot-password | **Yes — primary** |
| `systemloginjs` / `ur` active | **Yes** |
| `icm/host_name_full` FQDN | Secondary (usually reload/cookie, not zero request) |
| `icf/reject_expired_passwd` | After submit / password-change flows |
| `login/create_sso2_ticket` | After successful auth / SSO |
| SOAMANAGER IBC Note 2353589 | **No** (SOA config only) |

---

## Suggested order for Basis

1. SICF Global System Logon class (A/B to SAP standard) — [`STEP-BY-STEP-SICF.md`](STEP-BY-STEP-SICF.md)  
2. Activate `systemloginjs` + `ur` if not already  
3. RZ11: `icm/host_name_full`, `login/system_client`, `icf/reject_expired_passwd`, SSO ticket params  
4. SICF Logon Data on SOAMANAGER + CIM (HTTP Fields present)  
5. Smoke tests in §5  
