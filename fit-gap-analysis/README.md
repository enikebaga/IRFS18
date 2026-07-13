# IFRS 18 — Fit-Gap Analysis & Project Plan

Knowledge-base capture of the IFRS 18 SAP adoption fit-gap analysis and
project plan (originally produced in a Fit Gap Analysis chat session on
Jul 9–13, 2026). This complements the [Demand Charter](../demand-charter/)
for demand 288 - IFRS 18.

## Contents

- [`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md) — detailed
  functional design specification and solution description for all 7
  identified GAPs (SAP FI/CO/Consolidation scope), with dependencies and
  effort/type summary tables.
- [`IFRS18-Project-Plan.md`](IFRS18-Project-Plan.md) — the 8-phase, 44-activity
  project plan derived from the GAPs: Gantt chart, detailed activity
  breakdown, effort summary (by phase/role/GAP/work type), milestones,
  risks & assumptions.
- [`IFRS18_Adoption_Project_Plan.xlsx`](IFRS18_Adoption_Project_Plan.xlsx) —
  the same project plan as an editable Excel workbook (4 sheets: Project
  Plan, Effort Summary, Milestones & Risks, RACI Matrix), for tracking and
  resource assignment.
- [`generate_project_plan_xlsx.py`](generate_project_plan_xlsx.py) — the
  `openpyxl` script used to generate the workbook, so it can be
  regenerated/edited programmatically.
- [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) — guidance on how to
  search the SAP Support Portal for IFRS 18-relevant OSS Notes. No note
  numbers are fabricated here — SAP Notes require access to the SAP
  Support Portal (SAP for Me), which was not available when this analysis
  was produced.

## Key takeaway

IFRS 18 (Presentation and Disclosure in Financial Statements, replacing
IAS 1, mandatory for periods beginning on/after 1 Jan 2027) is, in this
SAP landscape, primarily a **configuration exercise** (Financial Statement
Version restructuring + downstream mapping table updates) rather than a
development-heavy change — no changes to the chart of accounts, G/L
postings, or ACDOCA structure are required. The estimated total effort is
**~95 person-days over ~22 weeks**, with 68% of that effort falling on the
FI/CO functional consultant role. The critical path is
**GAP 1 (FSV restructuring) → GAP 2 (account mapping) → GAP 3 (HFM
extraction)**.
