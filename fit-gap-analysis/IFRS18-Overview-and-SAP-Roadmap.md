# IFRS 18 Overview & SAP's Roadmap

A plain-language explainer of IFRS 18 and a summary of SAP's stated
roadmap for supporting it, captured from an external blog post shared
for this project (Jul 2026). This complements
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md) (this
landscape's specific GAPs) and
[`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) (how to find SAP Notes)
with general background and the one concrete SAP Note reference
available so far.

> **Source note:** this page summarizes third-party/blog content, not an
> official SAP document reviewed directly on the SAP Support Portal.
> Treat the OSS Note number below as a **pointer to verify**, not a
> substitute for pulling it up yourself on <https://me.sap.com/notes>.

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

## SAP's stated roadmap

According to the source blog, SAP is reviewing the impact of IFRS 18
across:

- Functional areas
- General Ledger structure
- Valuation processes
- Reporting frameworks in S/4HANA
- Group Reporting layouts
- Cash-flow classifications
- Universal Journal (ACDOCA) extensibility

**SAP Note referenced:** [**3670330**](https://me.sap.com/notes/3670330)
— per the blog, SAP targeted a formal solution approach by **December
2025**, expected to be delivered as part of IFRS 18 updates for **SAP
Group Reporting**, via the **1SG content package**.

The solution approach may differ by edition:

| Edition | Expected approach |
|---|---|
| SAP S/4HANA Cloud Public Edition | More standardized, pre-delivered content |
| SAP S/4HANA Cloud Private Edition | More flexibility with governance |
| SAP S/4HANA On-Premise | Potentially greater configurability |

**Relevance to this landscape:** this note's scope (1SG content package)
targets **SAP Group Reporting**. This landscape consolidates through
**Oracle Hyperion Financial Management (HFM)** via custom Z-programs
(see GAP 2/GAP 3 in the Fit-Gap Analysis), not SAP Group Reporting — so
the 1SG content package itself won't directly resolve GAP 2/GAP 3. It
may still be worth reviewing for:

- Any general FI-GL/FSV/semantic-tag guidance that also applies outside
  Group Reporting (relevant to GAP 1).
- Cash Flow Statement CDS view updates (relevant if the cash-flow
  reclassification above affects existing reports).

**Action:** since the target date (Dec 2025) has now passed as of this
writing (mid-2026), someone with SAP Support Portal (S-user) access
should pull up **Note 3670330** directly, confirm what was actually
delivered vs. planned, and check for any successor/related notes it
references. Update [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) with
the confirmed details once reviewed.

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
