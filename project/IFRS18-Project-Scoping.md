# IFRS 18 Implementation — Project Scoping Summary

**Demand:** 288 - IFRS 18 · **Demand Manager:** Enikő Baga · **Classification:** Internal

## 1. Why are we doing this?

**IFRS 18 – Presentation and Disclosure in Financial Statements** replaces
IAS 1 and becomes mandatory for financial years starting on or after
**1 January 2027** (with 2026 comparatives needing to be restated). It
requires:

- Three new required income statement groups: **Operating, Investing,
  Financing**.
- Two new required subtotals: **Operating Profit** and **Profit before
  Financing and Income Tax**.
- Formal, disclosed rules for any "adjusted"/management-defined
  performance measures, including reconciliation to official figures.
- Stricter, more consistent grouping of similar income statement items.

We must be compliant before the effective date, or we risk audit
qualification and regulatory exposure.

## 2. Scope

**In scope**

- Restructuring the SAP Financial Statement Versions (ZHFM, ZCPL, ZUKV)
  to the new IFRS 18 categories and subtotals.
- Updating the chart-of-accounts-to-consolidation mapping and the HFM
  (Hyperion Financial Management) data extraction/interface.
- Updating financial statement export (Fiori apps + the AMANA document
  management integration).
- Updating P&L reporting (cost-of-sales method) and working-capital
  balance-sheet reporting.
- Verifying IFRS 16 lease accounting postings are correctly classified
  under the new categories.
- Defining and governing management-defined performance measures (MPMs).
- Testing (unit, integration, QA, UAT) and production go-live/hypercare.

**Out of scope**

- Changes to the chart of accounts' underlying postings, the Universal
  Journal (ACDOCA) structure, or how transactions are recorded — IFRS 18
  only changes *presentation*, not *posting logic*.
- Any SAP core-code changes; the standard FSV framework (OB58) already
  supports the required structure, so this is a configuration-led
  project, not a development-heavy one.

## 3. Objectives

1. Full IFRS 18 compliance ahead of 1 January 2027.
2. A gap assessment of systems/templates completed early, so downstream
   work isn't blocked.
3. Clear governance for management-defined performance measures.
4. Automated (not manual/spreadsheet-based) production of the new
   categories and subtotals.
5. A successful dry-run cycle before go-live, and auditor sign-off on the
   transition approach.

## 4. Timeline & Key Milestones

Target runway: **~22 weeks**, from mid-July 2026 to early December 2026,
leaving buffer before the 1 January 2027 effective date.

| Milestone | Target Date |
|---|---|
| Design complete | 25 Jul 2026 |
| FSV restructuring complete (dev system) | 15 Aug 2026 |
| Configuration & development complete | 5 Sep 2026 |
| Interface validation complete (HFM, AMANA) | 19 Sep 2026 |
| Integration testing complete | 10 Oct 2026 |
| Transport to QA | 13 Oct 2026 |
| UAT sign-off | 7 Nov 2026 |
| Transport to Production | 10 Nov 2026 |
| Hypercare ends | 5 Dec 2026 |
| **IFRS 18 effective** | **1 Jan 2027** |

## 5. Effort & Resourcing

Estimated total effort: **~95 person-days**.

| Role | Effort (PD) | Share |
|---|---|---|
| FI/CO Functional Consultant | 65 | 68% |
| ABAP Developer | 12 | 13% |
| Business Users (UAT) | 5 | 5% |
| Project Manager | 5 | 5% |
| External teams (HFM, Tagetik, AMANA) | 6 | 6% |
| SAP Basis Administrator | 3 | 3% |

Most of the work (~32%) is configuration/customizing rather than
development (~8%), reflecting that IFRS 18 is primarily a presentation
change, not a posting-logic change.

## 6. Key Stakeholders

- Group Finance / Corporate Accounting (project owner)
- Group Controlling / FP&A
- Investor Relations
- IT / Reporting Systems team
- Internal Audit & External Auditors
- Local Finance teams (Business Units)
- External system teams: HFM, Tagetik, AMANA

## 7. Top Risks

| Risk | Mitigation |
|---|---|
| External team delays (HFM, Tagetik, AMANA) — outside our direct control | Kick off coordination early (Phase 1); parallel workstreams |
| Foreign-currency valuation exclusion still required in P&L reporting | Business decision needed early; extra effort already budgeted as optional |
| Hierarchy restructuring more extensive than expected, breaking hardcoded reports | Detailed node mapping done upfront to catch all affected areas |
| Transport window conflicts with other projects | Dedicated transport planning, coordinated with other teams |

## 8. Related Documents

- [`../demand-charter/`](../demand-charter/) — the full Demand Charter
  (288 - IFRS 18) in plain language, as `.md`/`.pptx`/`.docx`.
- [`../fit-gap-analysis/`](../fit-gap-analysis/) — the detailed Fit-Gap
  Analysis (7 GAPs) and full Project Plan (Gantt, activities, RACI),
  including an editable `.xlsx` tracker.
