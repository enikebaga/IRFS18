# IFRS 18 — SAP OSS Notes Guidance

The central SAP Note for IFRS 18 has now been confirmed (its full text
was shared for this project) and is summarized below, along with the
three edition-specific advisory notes it points to. No note numbers in
this document are fabricated.

## Confirmed: SAP Note 3670330 (central note)

| Field | Value |
|---|---|
| **Note** | [3670330](https://me.sap.com/notes/3670330) |
| **Title** | Financial Reporting according to IFRS 18 in SAP S/4HANA Cloud, SAP S/4HANA |
| **Version / Released** | Version 7, released 06.01.2026 |
| **Component** | FI-GL |

**Summary:** IFRS 18 replaces IAS 1 effective 1 January 2027, requiring a
new statement-of-profit-or-loss format (defined income/expense
categories, mandatory subtotals) and mandatory disclosure of
Management-Defined Performance Measures (MPMs), plus comparative 2026
figures alongside 2027 statements. Key changes called out by the note
match what's already captured in
[`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md):
the 5 new P&L categories, the 3 required subtotals, the IAS 7 cash-flow
reclassification (dividends → Investing, interest paid → Financing,
interest received → Investing), and the MPM reconciliation/audit
requirement.

**SAP's stated solution/status (as of the note's latest version):**

- SAP is still evaluating the legal implications and running an active
  **Customer Engagement Initiative (CEI)** with customers.
- SAP recommends customers **reach out to their SAP account executive**
  and/or **raise a Customer Influence Request** under *S/4HANA Public
  Cloud Finance* or *S/4HANA Private Cloud Finance* to participate.
- SAP had targeted finalizing a **generic solution approach by December
  2025**, evaluating flexibility in existing solutions (functional
  areas, General Ledger, GL valuation run) rather than committing to a
  single prescriptive fix.
- Different solution approaches are expected across editions, with
  **different levels of standardization** (Public Cloud = more
  pre-delivered/standardized; Private Cloud = more governed flexibility;
  On-Premise = potentially most configurable) — consistent with what was
  already captured from the earlier blog summary.
- **The note is explicitly a living document ("updated regularly")** —
  re-check it periodically rather than treating this summary as final.

## Confirmed: edition-specific advisory notes (referenced by 3670330)

| Note | Component | Title | Relevance to this landscape |
|---|---|---|---|
| [**3694359**](https://me.sap.com/notes/3694359) | FI-GL | How to Adopt IFRS 18 for Financial Reporting in S/4HANA Cloud **Public Edition** | Low — this landscape is not on Public Cloud (it relies on classic transactions/custom Z-development such as `OB58`, `SM30`, `/FIT/...` programs, which Public Cloud's extensibility model does not support in this form) |
| [**3696338**](https://me.sap.com/notes/3696338) | FI-GL | Advisory Note on IFRS 18 Transition in S/4HANA **Private Cloud, S/4HANA** | **High — read this one first.** Covers S/4HANA Private Cloud and (per the title) S/4HANA generally, i.e. On-Premise too, which matches this landscape's use of classic FI-GL transactions and custom ABAP developments |
| [**3700153**](https://me.sap.com/notes/3700153) | FI-GL | Advisory Note on IFRS 18 Transition in **SAP ERP** | Low — only relevant if any part of this landscape still runs classic ERP/ECC (not S/4HANA); this project's Fit-Gap Analysis assumes S/4HANA 2023 throughout |

**Recommended reading order for this landscape:** 3670330 (central note,
above) → **3696338** (most relevant edition-specific advisory) → 3694359
and 3700153 only if parts of the landscape turn out to be on those
editions.

## Why IFRS 18 has comparatively light *code-correction* coverage

Unlike standards that change *how transactions are posted* (e.g. IFRS 16
lease accounting, which required new posting logic, new asset classes,
and new BAPIs), **IFRS 18 changes how financial statements are
presented**, not how they are generated. Per Note 3670330 itself, SAP's
own framing is that this is being addressed by evaluating *flexibility
in existing solutions* (FSVs, functional areas, GL valuation run) rather
than by a single corrective note — consistent with GAP 1 in
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md), which relies
on the already-flexible FSV framework (`OB58`) rather than requiring new
SAP code.

## Further search plan (beyond the 4 notes above)

Go to <https://me.sap.com/notes> and search using these combinations to
find any additional notes (e.g. corrections that reference 3670330,
3694359, 3696338, or 3700153, or newer notes published after this
summary was captured):

| Search Term | Application Component | Why |
|---|---|---|
| `IFRS 18` | FI-GL | Core GL changes for IFRS 18 presentation |
| `IFRS 18` | FI-FIO-GL-HIE | Hierarchy/FSV enhancements for new categories |
| `IFRS 18` | FI-FIO-GL-REP | Financial statement reporting updates |
| `IFRS 18` | FI-FIO-GL-KPI | New semantic tags for Operating Profit, Profit before Financing |
| `IFRS 18` | FIN-CS | Group Reporting / consolidation impacts |
| `IFRS 18` | CA-GTF-CSC-EDO | Electronic disclosure / XBRL taxonomy updates |

Also filter by:

- **Software Component:** S4CORE (for S/4HANA core finance)
- **Release:** SAP S/4HANA 2023 (current landscape release) and later
- **Note Category:** "Correction" and "Legal Change"

## Recommended action

1. **Read Note 3696338 in full** (the Private Cloud/On-Premise advisory)
   — this is the most relevant of the four confirmed notes for this
   landscape.
2. **Consider raising a Customer Influence Request** under *S/4HANA
   Private Cloud Finance* (per SAP's own recommendation in 3670330), and
   loop in the account executive — this gives visibility into SAP's
   solution as it's finalized and a channel to flag this landscape's
   HFM-based consolidation as a scenario SAP should consider.
3. **Re-check Note 3670330 periodically** — it's explicitly a living
   document that SAP updates as the solution approach solidifies.
4. **Run the broader search plan above** for anything published after
   this summary, and update this document with findings, including:
   - Note number, title, and release date
   - Whether it's a "Correction" or "Legal Change" note
   - Whether it applies directly to the current release or requires a
     Support Package / backport
