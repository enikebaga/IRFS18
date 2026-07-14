# IFRS 18 Transformation Methodology & Technical Deep-Dive

Source: **"Transformation Journey with IFRS 18"**, SAP Community blog by
sanilbhandari (SAP Product and Topic Expert), published 2026-05-25,
co-authored with Pradeep_M. This is an official SAP-authored blog with
concrete technical guidance that goes beyond the general background
already captured in
[`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md) —
particularly on **foreign exchange gain/loss categorization**, which
directly refines GAP 5 in
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md) (see below).

## Key framing: this is a transformation project, not an IT project

The blog's central message: **"IFRS 18 should be approached as a
business transformation initiative, not an IT project."** It drives
changes to financial reporting processes, data models, and governance
frameworks — IT enables these changes, it doesn't lead them. This
reinforces why 68%+ of this project's effort sits with the FI/CO
functional consultant role rather than developers (see
[`IFRS18-Project-Plan.md`](IFRS18-Project-Plan.md), Effort by Role).

One new fact not previously captured: **early adoption is permitted, and
retrospective application is required** (not just "comparative
information" — full retrospective restatement, which is a stronger
requirement than a simple comparative column).

## SAP's recommended 5-phase transformation methodology

The blog lays out a SAP Activate–style methodology: **Discover → Prepare
→ Explore → Realize → Deploy & Run**. This maps onto our existing
8-phase project plan as follows:

| SAP's Methodology Phase | Maps to this Project Plan | Notes |
|---|---|---|
| **Discover** | Phase 1 (Design & Preparation) — Activities 1.1, 1.7-1.9, 1.11 | Auditor alignment, understanding P&L classification options, FSV/CFS approach, FX treatment, TRM/Group Reporting impact — largely research/design activities already in Phase 1 |
| **Prepare** | Phase 1 (Design & Preparation) — Activities 1.2-1.6, 1.10 | Plan creation, team identification, sandbox provisioning — matches our kickoff/design activities |
| **Explore** | Phase 1-2 boundary — Activity 1.2 design work, feeding into Phase 2 | COA-to-IFRS-category mapping, FSV/CFS design, FX bifurcation list, design documentation, gap listing |
| **Realize** | Phases 2-6 (FSV Restructuring, Configuration, Development, Interface Validation, Integration Testing) | Configuration (OB58, functional area derivation, FX valuation config), development, SIT/UAT |
| **Deploy & Run** | Phases 7-8 (QA Transport & UAT, Production Go-Live) | Cutover activities, transport, role/access updates, hypercare |

**Takeaway:** our existing 8-phase structure already substantially
matches SAP's recommended methodology — no restructuring needed, but the
detailed activity list below should be cross-checked against our current
Phase 1-2 activities to make sure nothing is missing (see "Gaps to
consider adding" at the end of this document).

## Detailed technical guidance by topic

### 1. Cost of Sales Accounting & functional area derivation

IFRS 18 requires consistent presentation of expenses by function. SAP's
guidance:

- Activate **Cost of Sales Accounting** (help docs referenced for SAP
  Cloud ERP Private, and classic SAP ERP).
- Ensure the **functional area** is automatically derived in the
  accounting document via configuration and master data assignment (help
  docs referenced for SAP Cloud ERP Private, SAP Cloud ERP, and SAP ERP).
- If Cost of Sales Accounting is already active, any revision to
  functional areas must align with IFRS sub-categorization while not
  disrupting existing statutory/management/operational reporting.

*(Not currently a named activity in our Project Plan — this landscape's
Fit-Gap Analysis doesn't mention Cost of Sales Accounting activation
status. Worth confirming during Phase 1 whether it's already active.)*

### 2. Financial Statement Versions & Cash Flow Statement (Indirect Method)

- IFRS 18's new mandatory subtotals (e.g. Operating Profit) require FSVs
  to be updated or replaced — consistent with GAP 1 in the Fit-Gap
  Analysis.
- The **Manage Global Hierarchies** app can maintain FSV hierarchies by
  G/L account, functional area, or both.
- **SAP will deliver a sample Financial Statement Version**, confirmed
  via the same two notes already documented in
  [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md):
  - **3696338** (S/4HANA Private Cloud, S/4HANA)
  - **3694359** (S/4HANA Cloud Public Edition)

  This is useful **independent cross-confirmation** from a second
  SAP-authored source that these two notes are the right ones to watch
  for FSV template content, not just general advisory text.
- A **new Fiori app for Cash Flow Statement (Indirect Method)** is
  planned for SAP Cloud ERP/Private — check the SAP Roadmap Explorer for
  status/timing.
- **Scope Item 1GA** will be updated with IFRS 18 reference content for
  SAP Cloud ERP and SAP Cloud ERP, Private.

  > **Important — do not confuse with Scope Item 1SG.** An earlier
  > document in this knowledge base
  > ([`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md))
  > described **Scope Item 1SG** — the *Group Reporting* reference
  > content package (per the giulio_peretti/PwC blog). This blog
  > describes a **different** scope item, **1GA**, apparently for the
  > core SAP Cloud ERP / Private Edition financial statement reference
  > content (not Group Reporting specifically). These appear to be two
  > distinct SAP deliverables, not a typo of one another — **both
  > references should be verified directly** (e.g. via SAP's Best
  > Practices Explorer) before relying on either.

### 3. Foreign exchange gain/loss treatment — concrete categorization rule

This is the most actionable new technical detail. Per IFRS 18, FX
gains/losses must be presented in separate categories, **determined by
the nature of the underlying item that generated the gain/loss**, not
by a blanket "FX" classification:

| Source of FX Gain/Loss | IFRS 18 Category |
|---|---|
| Trade Receivables / Payables | **Operating** |
| Cash and Cash Equivalents | **Investing** |
| Issued Bonds, Borrowings | **Financing** |

**Implications for this project:**

- Every G/L account's posting nature must be analyzed to determine
  whether it needs to be **split ("bifurcated")** into multiple accounts
  to avoid mixing transaction types that belong in different IFRS 18
  categories.
- New G/L accounts introduced during this bifurcation need their foreign
  currency valuation treatment reassessed for accurate remeasurement.
- Foreign currency valuation configuration must be adjusted depending on
  whether **Classic** or **Advanced** Foreign Currency Valuation is used:
  - **Advanced FCV**: valuation rules can use multiple steps with
    **semantic tags** to classify monetary items and assign the
    corresponding unrealized gain/loss accounts.
  - **Classic FCV**: if not migrating to Advanced FCV before IFRS 18
    adoption, update the unrealized gain/loss G/L account for
    **transaction key `KDF`** via transaction **`OB09`**.

**This directly refines GAP 5 in the Fit-Gap Analysis.** GAP 5's current
functional description mentions a custom "foreign currency valuation
exclusion (FG/FX document type filtering)" in `ZI_JournalEntryItemCube`,
framed as something to decide whether to "carry forward" or drop. This
new guidance suggests the more IFRS-18-correct approach is **not** to
exclude FX broadly, but to **bifurcate the underlying G/L accounts by
the nature of the item causing the FX**, so each already lands in the
right category without needing a separate FX exclusion/filter at all.
This should be raised as a discussion point before finalizing the GAP 5
solution approach (Activity 4.1 in the Project Plan).

### 4. Treasury & Risk Management (TRM) postings

Confirms the open question already raised in
[`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md#related-consideration-sap-treasury-and-risk-management-trm):
TRM generates diverse P&L items that must be classified as
Operating/Investing/Financing for IFRS 18 compliance. This blog links to
a **dedicated SAP Community blog**:

> *"IFRS 18 Compliance for Treasury and Risk Management in SAP Cloud
> ERP: Key Impacts and Approaches"*

This is very likely the same blog whose URL was truncated in the
earlier TRM tips blog (mezeshan) — **this exact title should make it
findable/searchable on SAP Community** even though the direct link
wasn't captured verbatim here either. Recommended as the next thing to
locate and review for the TRM open question (Activities 1.10/5.9 in the
Project Plan).

### 5. Group Reporting

References the same giulio_peretti/PwC blog already fully captured in
`IFRS18-Overview-and-SAP-Roadmap.md`. No new information beyond what's
already documented there.

### 6. Comparative Financial Statement Version (2026 restatement)

Links to another **new, not-yet-reviewed** SAP Community blog:

> *"IFRS 18 Compliance: Generating Comparative P&L Rep[orts]..."*

This directly addresses the comparative-reporting requirement already
flagged as critical in this project (2026 figures must be reportable in
the new IFRS 18 structure). **Recommended to locate and review this blog
next** — it may contain specific guidance on generating the comparative
P&L (e.g. via an extension ledger or other mechanism), which the
"Realize Phase" section below says depends on "your ERP version and the
approach chosen."

## Phase-by-phase activity detail (for cross-checking against our Project Plan)

### Discover Phase
- Early alignment with auditors (COA/GL structure updates, FX treatment,
  auditor-aligned restatement approach).
- Understand P&L classification options; activate Cost of Sales
  Accounting if needed; derive functional areas.
- Understand FSV & Cash Flow Statement (Indirect Method) options,
  including SAP's sample FSV (Notes 3696338/3694359) and Scope Item 1GA.
- Understand FX gain/loss treatment (see table above).
- Understand TRM posting impacts.
- Understand Group Reporting impacts.
- Understand the comparative FSV/restatement requirement.

### Prepare Phase
- Create an IFRS-18-aligned critical-path plan (COA redesign, Cost of
  Sales activation, FSV updates, FX reconfiguration).
- Identify teams: Project Management, Accounting Policy Owners,
  Controllers, Finance Operations/FP&A, MPM owners, IT/Reporting
  systems, Audit & Controls (internal/external), Change & Training.
- Provision a sandbox environment using a recent copy of production
  data.

### Explore Phase
- Map every P&L account to the 5 IFRS 18 categories, based on
  transaction nature.
- Define functional areas and derivation rules if Cost of Sales
  Accounting is activated.
- List gaps identified during the mapping exercise.
- Agree the new FSV format with the auditor (Operating/Investing/
  Financing/Tax/Discontinued Operations), aligned with functional areas
  and SAP's sample FSV/Cash Flow Statement app.
- List all G/Ls needing foreign currency valuation configuration updates
  due to bifurcation; define posting rules (advanced vs. classic FCV).
- Decide the comparative-FSV approach; possibly add an extension ledger
  or other solution depending on ERP version.
- Document the design: GL requirements, new FSV structure, cash flow
  changes, FX impacts, and a list of gaps where standard isn't enough.

### Realize Phase (Configuration & Testing)
- Create new GL accounts; update chart of accounts and account
  determination settings.
- Configure Cost of Sales Accounting and functional area derivation.
- Create the new FSV via **OB58** or the **Manage Global Hierarchies**
  Fiori app.
- Activate the Fiori Cash Flow Statement (Indirect Method) app, or
  build a custom report if defined in Discover.
- Configure/update allocation rules to reclassify amounts across GLs
  where transaction-level detail isn't available.
- Configure Advanced FCV (valuation rules + semantic tags) or adjust
  Classic FCV (`OB09`, transaction key `KDF`).
- **System validation (SIT & UAT):** verify correct GL posting by
  transaction nature, correct FSV output, correct functional area
  derivation, correct FX gain/loss posting, correct Cash Flow Statement
  output, and simulate month-end/quarter-end close for surprises.

### Deploy & Run Phase (Cutover)
- Transport all standard/custom changes in the correct order.
- Create/update basic financial data: new GL accounts, cost center →
  functional area assignments, new cost element groups.
- Activate and verify the Cash Flow Statement app.
- Verify automatic derivation/substitution rules.
- Update cost allocations.
- Activate Cost of Sales Accounting (if not already active).
- Update user roles/access for new reports and apps.

## Gaps to consider adding to this project

Based on this methodology, a few items aren't yet explicit activities in
[`IFRS18-Project-Plan.md`](IFRS18-Project-Plan.md) and are worth
discussing before Phase 1 kicks off (not yet added as formal activities,
since they need a decision on applicability first):

1. **FX gain/loss bifurcation analysis** — analyze every P&L G/L
   account's FX exposure nature (trade receivables/payables → Operating;
   cash & equivalents → Investing; bonds/borrowings → Financing) and
   list which accounts need splitting. This should probably become part
   of Activity 1.2 (FSV hierarchy design) or a new activity in Phase 1.
2. **Cost of Sales Accounting status check** — confirm whether it's
   already active in this landscape; if not, scope its activation.
3. **Auditor engagement** — the blog stresses *early* auditor alignment
   on COA/GL updates, FX treatment, and the restatement approach as a
   Discover-phase activity; not currently an explicit activity in Phase
   1 (Activity 1.1 covers group accounting, but not external auditors
   specifically — GAP 3's solution description mentions coordinating
   with auditors for HFM, but this is broader).
4. **Retrospective application** (vs. just "comparative figures") —
   confirm with the auditor whether full retrospective restatement is
   required beyond the comparative column already planned for.
