# Step-by-step: Find and A/B the System Logon customisation

**Who:** Basis (or anyone with SICF change + display rights)  
**System:** CSD client **400** (or the client you use for SICF)  
**Goal:** See if a custom System Logon / Forgot-password class is breaking **Log On**, then prove it with a SAP-standard A/B test.

**Authorizations needed**

| Action | Typical need |
|---|---|
| Display SICF / open Configuration | SICF display |
| Change service + save | SICF change |
| Change **global** System Logon settings | `S_ADMI_FCD` with value **ICFA** |
| Transport | CTS as per your landscape (do A/B first in DEV/QA if possible) |

---

## Step 1 — Open System Logon Configuration (SOAMANAGER)

### 1.1 Start SICF

1. Log on to the ABAP system with SAP GUI (client **400** if that is where ICF is maintained for this SID).
2. Transaction: **`SICF`**.
3. Clear filters if needed → **Execute** (F8) so you see the virtual host tree.

### 1.2 Find the SOAMANAGER service

1. In the tree go to:  
   `default_host` → `sap` → `bc` → `webdynpro` → `sap` → **`appl_soap_management`**  
   **Or** use the filter:
   - Service Name: `appl_soap_management`
   - Apply / Execute.
2. Confirm path is:  
   `/sap/bc/webdynpro/sap/appl_soap_management`

### 1.3 Open the service in change mode

1. **Double-click** `appl_soap_management`.
2. Click **Display/Change** (pencil / Ctrl+F1) so the screen is in **Change** mode.  
   If you only have Display, you can still **read** the class/URL; you will need Change for Step 2.

### 1.4 Open System Logon settings

1. Open the tab **Error Pages**.
2. Under logon-related options, select radio button **System Logon**  
   (not “Explicit Response Page”, not “Redirect to URL”).
3. Click the pushbutton **Configuration** (sometimes labelled **Settings**).  
   A dialog **System Logon Configuration** opens.

### 1.5 Note what is configured (write this down)

In the dialog, record:

| Field / area | What to write down |
|---|---|
| **Global Settings** vs **Service-Specific Settings** (radio buttons at top) | Which one is selected? |
| **Custom Implementation** / **ABAP Class** / class input field | Exact class name, e.g. `ZCL_…`, `/ZCO/…`, vendor class — or empty / SAP standard |
| **Layout** / stylesheet / template | Custom vs SAP default |
| **Links** / header / footer / additional URLs | Any URL for password reset / “Forgot password” / “Forgot your password?” |
| Screenshots | Full dialog + the Error Pages tab showing System Logon selected |

**How to see “Forgot password” specifically**

- Look in the Configuration dialog for link/URL fields (company links, custom links, password-related URLs).
- If the class field is filled: keep that class name for Step 1C (SE24).
- On the browser logon page, right-click **Forgot your password?** → Copy link address → save that URL (shows which app/service the customisation calls).

Click **Enter**/check (✓) or **Cancel** to leave the dialog for now (do not save yet unless you are only displaying).

### 1.6 Repeat for CIM (optional but useful)

Same steps for:

`default_host` → `sap` → `bc` → `webdynpro` → `zco` → **`zv_menu`**  
(and if used) **`zv_menu_reset`**

Compare: same custom class? service-specific vs global?

---

## Step 1B — Check **global** System Logon settings

Custom Forgot-password is often saved as **global**, which is why SOAMANAGER and CIM both break.

1. In **any** service’s System Logon Configuration dialog (from Step 1.4):
2. Select radio button **Global Settings**.  
   - Lower fields may become display-only and show the **effective global** values.
3. Note the **global** ABAP class and any global links/URLs (same table as above).
4. If you have admin rights (`S_ADMI_FCD` = **ICFA**), you will also see **Save as Global Settings** when changing — do **not** use that until you intend to change globals (Step 2B).

**Also check parent nodes** (inheritance):  
If a higher node (e.g. `/sap/bc/webdynpro` or `/sap`) has System Logon + custom class, children inherit it. Open those nodes the same way if service-level shows “Global” or looks empty but the browser still shows branding/Forgot-password.

---

## Step 1C — Inspect the custom class (Development / Basis together)

Only if Step 1 found a **non-empty custom class**:

1. Transaction **`SE24`** (or SE80).
2. Enter the class name → Display.
3. Confirm it is a subclass of **`CL_ICF_SYSTEM_LOGIN`** (or related login base class).
4. Note recent changes / transport (version management) around Forgot-password / password reset.
5. Search class methods/source for: `forgot`, `password`, `reset`, `link`, HTML snippets, JS.
6. Send class name + “who owns this transport” to the password-reset team.

---

## Step 2 — Temporarily switch to SAP standard System Logon (A/B test)

**Prefer DEV or QA first.** If you must use the broken system, do it in a maintenance window and document the old values from Step 1 so you can revert.

### 2.1 Choose one service for the first test

Recommended first target: **`appl_soap_management`** (proves “SAP standard path”)  
Or **`zv_menu`** if that is what users need immediately.

### 2.2 Put service in change mode

1. `SICF` → open the service → **Change**.
2. Tab **Error Pages** → **System Logon** → **Configuration**.

### 2.3 Switch to SAP standard

Do **one** of these, depending on what you found:

**Case A — Service uses Service-Specific Settings + custom class**

1. Select **Service-Specific Settings**.
2. Clear the **Custom Implementation / ABAP Class** field (leave empty)  
   **or** set layout back to an SAP default layout (remove custom layout if listed).
3. Remove/clear custom Forgot-password URL fields if present (optional for the pure A/B; clearing the class is the main test).
4. Confirm with ✓ / Enter.
5. On the service screen: **Save**.

**Case B — Service uses Global Settings (and global has the custom class)**

Then a service-only clear will **not** help until globals change.

Option B1 — quick local override (good A/B):

1. Switch radio button from **Global Settings** → **Service-Specific Settings**.
2. Leave **Custom Implementation / class empty** (SAP standard behaviour).
3. Use SAP default layout.
4. ✓ → **Save** the service.

Option B2 — fix globally (only with ICFA + change control):

1. Select **Global Settings** (or edit globals via the admin path).
2. Clear custom class / restore SAP defaults.
3. **Save as Global Settings**.
4. Expect **all** System Logon pages to change — coordinate first.

### 2.4 Activate / buffer (if needed)

1. Ensure the service is still **Active** (right-click → Activate Service if it was deactivated by mistake).
2. Optional: soft reset ICM if your Basis practice requires it after ICF changes (`SMICM` → Administration → ICM → Exit Soft) — often **not** required for System Logon config alone; try browser test first.

---

## Step 3 — Hard refresh and test Log On

### 3.1 Browser

1. Open an **InPrivate / Incognito** window (avoids stale JS/HTML).
2. Or DevTools → Network → tick **Disable cache**, then reload.
3. Open the **same service you changed**, e.g.  
   `https://vhffecsdci.sap.invite.freudenberg:44300/sap/bc/webdynpro/sap/appl_soap_management?sap-client=400&sap-language=EN`
4. Hard refresh: **Ctrl+F5** (Windows) / **Cmd+Shift+R** (Mac).

### 3.2 What “SAP standard” should look like

- Usually **SAP** logon layout (not zetVisions gold/branded box), unless branding is injected elsewhere.
- Forgot-password link may **disappear** — that is expected if it came from the custom class.

### 3.3 Test

1. F12 → **Network** → clear.
2. Enter a known test user + password.
3. Click **Log On**.

| Result | Meaning | Next |
|---|---|---|
| **Log On works** (navigates / session starts / or real auth error text) | Custom System Logon / Forgot-password implementation was the cause | → Step 4A |
| **Still dead** (no Network request) | Not (only) this service’s custom class — deeper issue | → Step 4B |
| Auth error like “Password logon no longer possible” / wrong password | **Handlers work** — different problem; logon JS is fixed | Treat as success for this A/B |

Also retest CIM URL if you only changed SOAMANAGER (and globals were the source, CIM should follow after global fix).

---

## Step 4A — If SAP standard fixes Log On

1. **Keep a screenshot** of working Log On + the class name you removed.
2. **Revert is optional** for production users: either leave standard temporarily, or re-enable custom only after fix.
3. Hand to the **password-reset / custom logon** team:
   - Class name from Step 1
   - Symptom: Forgot-password link OK; Log On/Change produced no HTTP request
   - Ask them to restore standard script includes / `SL_SystemLogin` init / call `super` in redefined methods
4. After they deliver a fixed class: set it back in SICF (service-specific or global) → retest Log On **and** Forgot password.
5. Transport the SICF change + class fix through the landscape.

---

## Step 4B — If SAP standard does **not** fix Log On

Stay on SAP standard for the test service (so custom class is ruled out), then gather:

1. F12 → Network → Disable cache → filter `systemloginjs` → reload → screenshot (status/rows).
2. Console → run: `typeof SL_SystemLogin` → screenshot result.
3. Clear Network → click Log On → confirm still no request.
4. SICF screenshot: `/sap/public/bc/icf/systemloginjs` active.
5. Open SAP Support incident:

| Field | Value |
|---|---|
| Component | **BC-MID-ICF-LGN** |
| Subject | System Logon Log On button does nothing (no HTTP request); systemwide |
| Notes | KBA **2900689**, **3423597** (and **3272754** if UR JS errors) |
| Attachments | HAR, Console, SICF System Logon config (showing SAP standard), systemloginjs active |

Also check with RISE ops only if `systemloginjs` / public UR URLs return 403/HTML via `:44300`.

---

## Quick checklist (print this)

- [ ] SICF → `appl_soap_management` → Error Pages → System Logon → Configuration  
- [ ] Noted: Global vs Service-Specific  
- [ ] Noted: custom ABAP class name (or empty)  
- [ ] Noted: Forgot-password URL (config and/or browser Copy link)  
- [ ] Repeated for `zv_menu` / checked global settings  
- [ ] A/B: cleared custom class / forced Service-Specific SAP standard → Save  
- [ ] Incognito + Ctrl+F5 → test Log On with Network open  
- [ ] If fixed → password-reset team + class name  
- [ ] If not fixed → BC-MID-ICF-LGN with HAR + KBA 2900689 / 3423597  

---

## Safety notes

- Do not delete the custom class in SE24 during the A/B — only **unlink** it in SICF so you can roll back in one minute.
- Write down the exact old class name before clearing.
- Global **Save as Global Settings** affects the whole system — prefer service-specific override for the first proof.
