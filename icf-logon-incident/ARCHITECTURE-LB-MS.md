# Roles: Load balancer vs Message Server (your CIM / CSD setup)

## Big picture (typical ECS / RISE HTTP path)

```text
Browser
  │  https://cim.freudenberg.com  (or vhffecsdci…:44300)
  ▼
[ Optional network / cloud Load Balancer ]   ← VIP, TLS passthrough or terminate, HA
  ▼
SAP Web Dispatcher (ECS-managed)             ← “SAP HTTP load balancer” / reverse proxy
  │  asks Message Server: which app servers are up?
  │  then sends the real HTTP(S) request to one ICM
  ▼
ABAP Application Server ICM  (CSD)           ← runs Web Dynpro, System Logon, SPNego
  ▲
Message Server (MS) ─────────────────────────┘
     (metadata only for HTTP — not the user session)
```

In conversation, “load balancer” often means either the **Web Dispatcher** or an **upstream network LB**. They are different layers.

---

## 1. Message Server — what it does

| Role | Detail |
|---|---|
| **Central directory of the SAP system** | Knows which application servers (instances) belong to SID **CSD**, their status and capacity |
| **GUI / RFC logon balancing** | Classic SAP GUI uses MS + logon groups (**SMLG**) |
| **HTTP info source for Web Dispatcher** | WD connects using **`MSHOST` + `MSPORT`/`MSSPORT`** inside `wdisp/system_*` and downloads the list of HTTP-capable app servers / groups |
| **What it does *not* do in your WD setup** | It does **not** terminate `cim.freudenberg.com`, does **not** hold the user HTTPS session, does **not** run SPNego for the browser |

So: Message Server = **control-plane / directory** for “where can I send this request?”  
Web Dispatcher = **data-plane** for the actual browser HTTP(S) bytes.

If MS is down or `MSHOST`/`MSPORT` wrong, WD cannot refresh the server list → dispatch errors / 503. That is unrelated to “SPNego enable,” but SSO will look broken if nothing reaches an app server.

---

## 2. Load balancer — two meanings

### A. SAP Web Dispatcher (what ECS usually means)

| Role | Detail |
|---|---|
| **Entry point for HTTP(S)** | Browser hits WD hostname/port (or public name pointed at WD) |
| **TLS** | Often terminates HTTPS (`SAPSSLS.pse`) for `cim.freudenberg.com` |
| **Choose backend SID** | Via `wdisp/system_*` (`SRCVHOST` / `SRCURL` / `SRCSRV`) |
| **Choose app server** | Load-balances across ICMs using capacity from the **Message Server** |
| **Sticky sessions** | Keeps stateful Web Dynpro on the same server (cookies / session) |
| **Security / rewrite** | URL filters, redirects, header mods (`icm/HTTP/mod_*`) |

This is the component you tune in **ECS → Maintain System Parameters → Static** for short-host SSO (`SRCVHOST`, headers, etc.).

### B. Network / cloud Load Balancer (if present in front of WD)

| Role | Detail |
|---|---|
| **HA / VIP** | Spreads traffic across multiple Web Dispatcher instances or AZs |
| **May terminate TLS** | If it does, the cert the browser sees is on the LB—not only on `SAPSSLS` in WD (see certificate handover warning) |
| **Does not talk to Message Server** | No SAP awareness; only TCP/HTTP to WD |

Your certificate handover assumed:  
`Browser → public hostname → ECS Web Dispatcher → backend`.  
If a corporate LB sits in front, confirm who owns TLS and whether Host header stays `cim.freudenberg.com`.

---

## 3. Who does what for SSO / SPNego

| Step | Component |
|---|---|
| User opens `https://cim.freudenberg.com/...` | DNS → LB (optional) → **Web Dispatcher** |
| TLS certificate for that name | **WD** (`SAPSSLS`) and/or front LB |
| Kerberos ticket for `HTTP/cim.freudenberg.com` | Browser + AD |
| Route host to SID CSD | **Web Dispatcher** (`SRCVHOST` / `wdisp/system_*`) |
| Pick which app server | **Web Dispatcher**, using list from **Message Server** |
| Validate SPNego / create session | **ABAP ICM** on that app server (`SPNEGO`) |
| Issue MYSAPSSO2 cookie | **ABAP** (`login/create_sso2_ticket`, …) |

Message Server never decrypts Kerberos. Load balancer / WD never runs transaction SPNEGO.

---

## 4. One-line summary

| Component | One-line role |
|---|---|
| **Message Server** | Tells Web Dispatcher which CSD app servers exist and are healthy |
| **Web Dispatcher (SAP LB)** | Public HTTP(S) front door: TLS, host routing, real load balancing to ICM |
| **Network LB (if any)** | VIP/HA in front of WD; may terminate TLS |
| **App Server ICM** | Runs the application and SPNego/System Logon |

---

## 5. Practical implication for your open topics

| Issue | Where to look |
|---|---|
| Short link SSO after redirect to `cim.freudenberg.com` | **WD** Static params + cert SAN + AD SPN + ABAP SPNEGO/HTTPURLLOC — not Message Server |
| WD cannot find servers / 503 | **Message Server** reachability (`MSHOST`/`MSPORT`) + app servers registered |
| Dead Log On button (no HTTP) | **ICF System Logon** / `/ZCO/CL_ICF_CIM_LOGIN` on app server — not MS/LB |
