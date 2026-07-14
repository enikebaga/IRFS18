# IFRS 18 Overview & SAP's Roadmap

A plain-language explainer of IFRS 18 and a summary of SAP's stated
roadmap for supporting it. The general IFRS 18 explanation was first
captured from an external blog post (Jul 2026); the SAP roadmap section
has since been **updated with the verified text of SAP Note 3670330**
(v7, released 06.01.2026) and its three edition-specific companion
notes, shared directly for this project. See
[`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) for the full note
details. This page complements
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md) (this
landscape's specific GAPs).

> **Correction vs. the original blog summary:** the earlier version of
> this page (based only on the blog) stated that SAP's solution would be
> "delivered via the 1SG content package for SAP Group Reporting." The
> **actual verified text of Note 3670330 does not say this** — it only
> says SAP is evaluating flexibility in "functional areas, general
> ledger, [and the] valuation run in General Ledger," without naming a
> specific content package or committing to Group Reporting as the
> delivery vehicle. That earlier claim should be treated as inaccurate
> or outdated blog speculation, not as confirmed SAP guidance. The
> sections below now reflect the verified note text only.

## What is IFRS 18 and why does it matter?

IFRS 18 (*Presentation and Disclosure in Financial Statements*) is a new
IASB standard that **replaces IAS 1** and becomes mandatory for annual
periods beginning on or after **1 January 2027** (with 2026 comparatives
required in the new structure). It changes *how* companies present their
income statement and explain performance — not how transactions are
recorded. The goals: easier-to-understand statements, more consistency
across companies, more transparency for investors, and fairer
company-to-company comparison.

## What changes in the P&L?

Every income/expense item must now be classified into one of five
categories (three of which are new mandatory groupings for the "main"
part of the P&L):

| Category | What it covers |
|---|---|
| **Operating** | Day-to-day business activities |
| **Investing** | Returns or costs related to long-term investments |
| **Financing** | Borrowings, interest, and funding-related items |
| **Income Tax** | All tax-related items |
| **Discontinued Operations** | Business operations shut down or sold |

Two new required subtotals must be shown (on top of the existing
"Profit or Loss" total), so that "operating profit" means the same thing
across every IFRS preparer:

- **Operating Profit**
- **Profit or Loss Before Financing and Income Tax**

*(This lines up with GAP 1 in the Fit-Gap Analysis — restructuring
ZHFM/ZCPL/ZUKV to introduce these categories and subtotals.)*

## Management-Defined Performance Measures (MPMs)

Custom KPIs many companies already report — "Adjusted EBITDA," "Core
Profit," "Underlying Margin" — become formally regulated as
**Management-Defined Performance Measures**. Under IFRS 18, companies
must, for each MPM:

- Explain how it's calculated.
- Explain why it's useful.
- Provide a **reconciliation to an official IFRS subtotal**.
- Disclose that reconciliation in the notes, and have it **audited**.

*(This lines up with the "MPM governance" objective in the
[Demand Charter](../demand-charter/) and the "adjusted performance
numbers" pain point described there in plain language.)*

## Cash Flow Statement changes (IAS 7)

IFRS 18 also updates IAS 7 and removes the classification choices
companies previously had for certain cash flows:

| Item | Old | New (IFRS 18) |
|---|---|---|
| Dividends paid | Choice of Operating/Financing | **Investing** |
| Interest paid | Choice of Operating/Financing | **Financing** |
| Interest received | Choice of Operating/Investing | **Investing** |

This is a smaller, more mechanical change than the P&L restructuring,
but it does affect any SAP cash-flow statement CDS views/reports that
currently rely on the old flexible classification (see the "Cash Flow
Statement CDS views" item in `OSS-Notes-Guidance.md`).

## Broader reporting impact

- **P&L structure** — charts of accounts and reporting hierarchies need
  reorganizing (GAP 1).
- **Disclosures & notes** — more detail required, especially for MPMs,
  aggregation rules, and reconciliations.
- **Comparative reporting** — 2026 figures must be disclosed in the new
  IFRS 18 structure when reporting for 2027, i.e. the restructuring must
  be live well before the 2027 year-end.

## SAP's stated roadmap (verified via Note 3670330)

**Central note:** [**3670330** — "Financial Reporting according to IFRS
18 in SAP S/4HANA Cloud, SAP S/4HANA"](https://me.sap.com/notes/3670330)
(FI-GL, v7, released 06.01.2026). Confirmed content:

- SAP is still **evaluating the legal implications** of IFRS 18 and
  running an active consultation with customers (the **Customer
  Engagement Initiative**, CEI).
- SAP recommends customers **contact their SAP account executive** and/or
  **raise a Customer Influence Request** under *S/4HANA Public Cloud
  Finance* or *S/4HANA Private Cloud Finance* to participate.
- SAP is evaluating flexibility in **existing** solution areas —
  "functional areas, general ledger, [and the] valuation run in General
  Ledger" — rather than committing to a specific new content package or
  delivery mechanism. (The note text does **not** mention "Group
  Reporting" or a "1SG content package" — see the correction notice at
  the top of this page.)
- SAP had targeted finalizing a **generic solution approach by December
  2025**, once discussions with CEI-enrolled customers concluded.
- **Different solution approaches, with different levels of
  standardization, are expected per edition:**

| Edition | Expected approach | Companion note |
|---|---|---|
| SAP S/4HANA Cloud **Public Edition** | More standardized, pre-delivered content | [3694359](https://me.sap.com/notes/3694359) — How to Adopt IFRS 18 for Financial Reporting in S/4HANA Cloud Public Edition |
| SAP S/4HANA **Private Cloud** / S/4HANA (On-Premise) | More flexibility, more governance/configuration required | [3696338](https://me.sap.com/notes/3696338) — Advisory Note on IFRS 18 Transition in S/4HANA Private Cloud, S/4HANA |
| **SAP ERP** (classic ECC, pre-S/4HANA) | Separate advisory, not S/4HANA-specific | [3700153](https://me.sap.com/notes/3700153) — Advisory Note on IFRS 18 Transition in SAP ERP |

- **Note 3670330 is explicitly a living document** ("updated regularly
  as soon as new information...becomes available") — re-check it
  periodically.

**Relevance to this landscape:** based on the transactions and custom
developments already documented in the Fit-Gap Analysis (`OB58`, `SM30`,
classic ABAP programs like `/FIT/FI_D_HFM_INTF_001`), this landscape is
most likely **S/4HANA Private Cloud or On-Premise**, not Public Edition
and not classic ERP/ECC. That makes **Note 3696338 the most relevant
companion note to read next** — see
[`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) for the reading order
and recommended actions. Separately, this landscape consolidates through
**Oracle Hyperion Financial Management (HFM)** via custom Z-programs
(GAP 2/GAP 3), which none of these four SAP notes are likely to address
directly, since they're scoped to SAP's own G/L, functional areas, and
valuation-run flexibility rather than third-party consolidation
interfaces — HFM-side alignment will still need to be handled through
this project's own plan (GAP 3, Phase 5).

## How to prepare (general guidance, matches this project's plan)

- Review current P&L structures — done in GAP 1 / Phase 1-2 of the
  [Project Plan](IFRS18-Project-Plan.md).
- Identify where income/expense items map under IFRS 18 — done via the
  FSV restructuring design (Activity 1.2).
- Understand new disclosure requirements — MPM governance (Activity
  4.1/objectives in the Demand Charter).
- Review cash-flow classifications — worth adding as an explicit check
  during Phase 2 unit testing (Activity 2.4) given the IAS 7 changes
  described above; not currently a separate line item in the Fit-Gap
  Analysis, since the existing GAPs were scoped before this cash-flow
  detail was available.
- Collect internal MPM definitions — part of Activity 1.1/4.1.
- Engage with SAP through a Customer Engagement Initiative (CEI) or
  Customer Influence Request — recommended in addition to the OSS Note
  search in `OSS-Notes-Guidance.md`.
