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
- [`IFRS18-Project-Plan.md`](IFRS18-Project-Plan.md) — the 8-phase,
  60-activity project plan derived from the GAPs: Gantt chart, a
  recommended execution sequence (respecting dependencies), a detailed
  activity breakdown listing the exact SAP transaction(s)/development
  object(s) each activity touches, effort summary (by phase/role/GAP/work
  type), milestones, risks & assumptions. Updated Jul 14, 2026 with 9
  additional activities (~10 PD) covering SAP Note 3670330
  review/implementation and treasury (TRM) G/L account verification —
  total effort now ~105 PD (was ~95).
- [`IFRS18_Adoption_Project_Plan.xlsx`](IFRS18_Adoption_Project_Plan.xlsx) —
  the same project plan as an editable Excel workbook (5 sheets: Project
  Plan — including Execution Order and SAP Transaction(s)/Object(s)
  columns — Effort Summary, Milestones & Risks, RACI Matrix, and a new
  **SAP Notes & References** sheet with the confirmed SAP Notes, a
  child-note search guide, an SAP content deliverables tracker, external
  source references, and a treasury G/L account classification
  checklist), for tracking and resource assignment.
- [`generate_project_plan_xlsx.py`](generate_project_plan_xlsx.py) — the
  `openpyxl` script used to generate the workbook, so it can be
  regenerated/edited programmatically.
- [`OSS-Notes-Guidance.md`](OSS-Notes-Guidance.md) — summary of the
  **confirmed** central SAP Note (3670330) and its three edition-specific
  companion notes (3694359 Public Edition, 3696338 Private
  Cloud/On-Premise, 3700153 SAP ERP), with a recommended reading order
  for this landscape, plus a further search plan for anything newer. No
  note numbers are fabricated by us.
- [`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md)
  — a plain-language explainer of IFRS 18 (new P&L categories, required
  subtotals, MPM rules incl. tax/NCI reconciliation detail, aggregation/
  disaggregation, IAS 7 cash-flow reclassification), SAP's confirmed
  roadmap (per Note 3670330, now properly attributed to an official SAP
  Community blog by Praveenirrinki, 2025-12-02, plus a mention of an SAP
  webinar series), a detailed summary of SAP Group Reporting's IFRS 18
  capabilities and upcoming reference-content update (Scope Item 1SG)
  per an SAP+PwC Community blog, and the SAP TRM open question (now
  addressed with dedicated verification activities in the Project Plan).

## Key takeaway

IFRS 18 (Presentation and Disclosure in Financial Statements, replacing
IAS 1, mandatory for periods beginning on/after 1 Jan 2027) is, in this
SAP landscape, primarily a **configuration exercise** (Financial Statement
Version restructuring + downstream mapping table updates) rather than a
development-heavy change — no changes to the chart of accounts, G/L
postings, or ACDOCA structure are required. The estimated total effort is
**~105 person-days over ~22 weeks** (updated Jul 14, 2026; was ~95 PD),
with the majority of effort falling on the FI/CO functional consultant
role. The critical path is **GAP 1 (FSV restructuring) → GAP 2 (account
mapping) → GAP 3 (HFM extraction)**, with a new gating step — reviewing
SAP Note 3670330 — added at the very start of Phase 1.
