# IFRS 18 Overview & SAP's Roadmap

A plain-language explainer of IFRS 18 and a summary of SAP's stated
roadmap for supporting it, drawing on three sources:

1. **"IFRS 18 Explained: What SAP S/4HANA Customers Need to Know Before
   2027"** by Praveenirrinki (SAP), published 2025-12-02 on SAP
   Community — *Financial Management Blog Posts by SAP* (an official
   SAP-authored blog, not a generic third-party post as originally
   assumed) — general IFRS 18 background. A comment on this blog from
   KatharinaR (SAP Product and Topic Expert) links to an **SAP webinar
   series (Feb/Mar 2026)** with further technical guidance; the
   registration link was truncated in the source shared for this
   project, so the recordings haven't been located/reviewed yet.
2. The **verified text of SAP Note 3670330** (v7, released 06.01.2026)
   and its three edition-specific companion notes — see
   [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) for full note
   details.
3. An **SAP Community blog co-authored by SAP and PwC**
   ("IFRS 18 and SAP S/4HANA Group Reporting: What It Means and How to
   Get Ahead," by giulio_peretti, published 2025-11-06) — a credible,
   named, SAP-affiliated source with concrete SAP Group Reporting
   feature detail. See the
   [SAP Group Reporting section](#sap-group-reporting-capabilities-for-ifrs-18-sap--pwc-blog)
   below.
4. An **SAP Community blog on SAP Treasury and Risk Management (TRM)**
   ("Unlocking the Value of SAP TRM for Corporate Treasury," by
   mezeshan) — a general TRM tips-and-tricks post; only one of its ~30
   items (#15) is IFRS 18-specific, but it independently corroborates
   Note 3670330 and raises a genuine open question for this landscape
   — see the
   [Treasury (TRM) angle section](#related-consideration-sap-treasury-and-risk-management-trm)
   below. The rest of that blog's content (contract processing, market
   data, RFR/SOFR transition, Fiori roles, etc.) is general TRM
   knowledge unrelated to this project and is intentionally **not**
   reproduced here.

This page complements
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md) (this
landscape's specific GAPs).

> **Note on the "1SG" reference:** an earlier version of this page
> (based only on source #1, the Praveenirrinki blog, before its full
> attribution was known) claimed SAP's IFRS 18 solution would be
> "delivered via the 1SG content package for SAP Group Reporting," and
> attributed that claim to Note 3670330. That attribution was **wrong**
> — the verified text of Note 3670330 does **not** mention "1SG" or
> Group Reporting at all. However, source #3 above (the SAP+PwC blog)
> independently confirms that **"Scope Item 1SG" is real** — it's SAP
> Group Reporting's IFRS-compliant reference content package, and it
> genuinely is being extended/restructured for IFRS 18 (see below). So
> the underlying fact turned out to be substantially correct, just
> **misattributed to the wrong note** by
> the original source. Note 3670330 itself remains scoped to general
> FI-GL/functional-area/valuation-run flexibility, separate from the
> Group-Reporting-specific 1SG update described by SAP+PwC.

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
- Provide a **reconciliation to an official IFRS subtotal** (the most
  directly comparable one).
- For **each reconciling item** in that reconciliation, disclose the
  **income tax effect** and the **effect of non-controlling interest**.
- Disclose all of the above in **a single dedicated note**, and have it
  **audited**.

*(This lines up with the "MPM governance" objective in the
[Demand Charter](../demand-charter/) and the "adjusted performance
numbers" pain point described there in plain language.)*

## Aggregation and disaggregation (third requirement set)

Beyond the new P&L structure and MPM disclosures, IFRS 18 also gives
enhanced guidance on **how to group ("aggregate") and split out
("disaggregate") financial information** based on shared
characteristics — applying to both the primary statements and the notes.
This is the principle behind the "similar costs classified differently
across business units" pain point already captured in the [Demand
Charter](../demand-charter/), and behind the guidance in GAP 6 (Working
Capital reporting) about consistent classification.

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

## SAP Group Reporting capabilities for IFRS 18 (SAP + PwC blog)

Source: *"IFRS 18 and SAP S/4HANA Group Reporting: What It Means and How
to Get Ahead"*, SAP Community blog by giulio_peretti, co-authored with
PwC, published 2025-11-06.

**Applicability disclaimer:** this section describes **SAP Group
Reporting** functionality. This landscape consolidates through **Oracle
HFM** via custom Z-programs, not SAP Group Reporting (see GAP 2/GAP 3 in
the Fit-Gap Analysis), so none of the capabilities below are directly
usable today. They're captured here as reference/context — useful if a
future move to SAP Group Reporting is ever evaluated, and because the
underlying IFRS 18 concepts (parallel versions, restatement, mapping,
hierarchy maintenance) are conceptually similar to what this project
already does with HFM (e.g. the XHFM/XCPL/XUKV backups in GAP 1).

### PwC's implementation approach

PwC frames the work in two phases:

1. **Impact assessment** — training (on-site/virtual, eLearning),
   identifying impacts on reporting, systems (S/4HANA, SAP Group
   Reporting), processes, and cross-business impacts (e.g. covenants,
   remuneration tied to reported metrics).
2. **Implementation** — implementing/testing SAP solutions, updating
   internal controls, and the iXBRL report.

PwC notes most companies had **not yet started implementation** as of
the blog's publication (Nov 2025), and — given the need for restated
comparatives — recommends starting soon given the 2026 comparative
deadline.

### Current SAP Group Reporting capabilities relevant to IFRS 18

| Capability | What it does |
|---|---|
| **Consolidation Extension Versions** | Create derived consolidation versions from a base version for adjustments/restatements without touching the original consolidated results — supports reporting financials under **dual accounting principles from FY2026** (i.e. old + IFRS 18 structure in parallel) |
| **Consolidation Chart of Accounts (CoA) updates** | Maintain/update the Consolidation CoA to align with the new IFRS 18 disclosure requirements |
| **Mapping from Operating CoA** | Automates mapping between Operating and Consolidation CoA; integrates with the Group Reporting preparation ledger to define **custom substitution rules** that derive categorized FS items from underlying posting fields |
| **Time-dependent FS Item Hierarchy Maintenance** | Supports continuous, date-keyed updates to the FS item hierarchy; the **Group Data Analysis** app can restate prior years' data under the updated hierarchy by specifying a key date |
| **Group Reporting Data Collection** | Structures/manages collection of extra information needed for IFRS 18 (e.g. expense items needed to arrive at Adjusted EBITDA — relevant to MPM disclosure) |
| **Consolidation Monitor (new version)** | Open/close multiple fiscal periods across multiple consolidation groups in one click via "process year periods" |
| **Cross Version Balance Validation** | Define cross-version validation rules, including a predefined scenario comparing the Restated Actuals version against Actuals, with configurable validity periods — reconciles the pre- and post-IFRS 18 views |

### Upcoming: Group Reporting Reference Content update (Scope Item 1SG)

SAP's Best-Practice **Group Reporting reference content — Scope Item
1SG** — includes the Consolidation Chart of Accounts and primary
statements (Balance Sheet, Income Statement by Nature, Income Statement
by Function of Expense, Cash Flow Statement (indirect method), Statement
of Changes in Equity, Statement of Comprehensive Income). Per this blog,
SAP will update it for IFRS 18 as follows:

- **Extend & restructure the Income Statement** — extend the
  Consolidation CoA and restructure the Consolidated Income Statement
  for IFRS 18 presentation.
- **Update the Cash Flow Statement** — the indirect-method Consolidated
  Cash Flow Statement's starting point moves to the new **Operating
  Profit** subtotal.

**Important caveat directly from SAP (via this blog):** these updates go
into the **standard reference content**, so **new** cloud customers get
them out-of-the-box — but SAP **will not auto-overwrite** existing
customers' configurations, since customers often customize the
pre-delivered FS items/structures. **Existing customers must assess
their own IFRS 18 impact and implement the changes themselves.** This
directly parallels what this project's GAP 1 already assumes: no
automatic SAP fix, full self-service restructuring required (in this
case, of ZHFM/ZCPL/ZUKV rather than the Group Reporting Consolidation
CoA).

## Related consideration: SAP Treasury and Risk Management (TRM)

Source: *"Unlocking the Value of SAP TRM for Corporate Treasury,"* SAP
Community blog by mezeshan. This is a general TRM tips post; item #15
("IFRS18 – Starting 2027") is its only IFRS 18-specific content, and it:

- Corroborates **Note 3670330** (same note documented in
  [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md)) as the reference for
  implementing IFRS 18 in SAP.
- Links to a dedicated, treasury-focused SAP Community blog titled
  something like *"IFRS 18 compliance for treasury..."*
  (`community.sap.com/t5/financial-management-blog-posts-by-sap/ifrs-18-compliance-for-treasury-...`)
  — the URL was truncated in the source shared for this project, so the
  full content hasn't been reviewed. **Action:** find and read this
  blog in full if SAP TRM is in scope for this landscape.

**Open question this raises for this project:** the current Fit-Gap
Analysis (`IFRS18-Fit-Gap-Analysis.md`) does **not** mention SAP TRM
anywhere, and it isn't known from the material gathered so far whether
this landscape uses TRM for treasury instruments (loans, deposits, FX
deals, derivatives, securities). If it does:

- TRM automatically generates cashflow schedules and posts related
  accounting entries — principal movements, **interest accruals**,
  repayments, fees, bank charges, and **FX valuation** gains/losses —
  via closing transactions like `TPM44`, `TPM1`, `TPM18`.
- Under IFRS 18's IAS 7 changes (see above), **interest paid** must be
  Financing and **interest received**/**FX gains** may need to sit
  under Investing — so the G/L accounts TRM posts to must be correctly
  classified in the restructured FSVs (ZHFM/ZCPL/ZUKV), the same way
  GAP 7 (IFRS 16 lease accounting) already checks its own dedicated
  account range.
- **Recommendation:** confirm with the Finance/Treasury team whether
  SAP TRM (or an equivalent treasury system) is in use. If so, add a
  verification step to Phase 1/Phase 3 of the
  [Project Plan](IFRS18-Project-Plan.md) — similar to Activity 3.4/3.5
  (the `ZFI_IFRS16` mapping table review) — to confirm TRM's G/L
  accounts are correctly categorized under the new IFRS 18 structure.
  This is **not currently a scoped GAP or activity**, since TRM usage
  hasn't been confirmed for this landscape.

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
- Plan for **dual-principle reporting during the 2026 comparative
  period** — this project's Phase 2 already preserves the pre-IFRS 18
  FSVs (XHFM/XCPL/XUKV) as a comparison baseline (GAP 1, Activity 6.7),
  which serves a similar purpose to SAP Group Reporting's "Consolidation
  Extension Versions" concept described above, even though the
  mechanism differs (FSV backup vs. a derived consolidation version).
