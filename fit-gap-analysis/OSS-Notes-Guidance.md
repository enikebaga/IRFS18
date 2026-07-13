# IFRS 18 — SAP OSS Notes Guidance

**No specific SAP OSS Note numbers are listed in this document.** OSS
Notes are published exclusively on the SAP Support Portal (SAP for Me /
SAP ONE Support Launchpad), which requires an S-user login and was not
accessible when this analysis was produced. Fabricating note numbers
would be actively harmful, so this document instead gives your team a
concrete, actionable search plan.

## Why IFRS 18 may have limited dedicated OSS Note coverage

Unlike standards that change *how transactions are posted* (e.g. IFRS 16
lease accounting, which required new posting logic, new asset classes,
and new BAPIs), **IFRS 18 changes how financial statements are
presented**, not how they are generated. In SAP terms:

- The chart of accounts doesn't change.
- G/L account postings don't change.
- The Universal Journal (ACDOCA) structure doesn't change.
- No new document types, posting keys, or transaction types are needed.

What changes is the **Financial Statement Version hierarchy** — and
SAP's FSV framework (transaction OB58) is already fully flexible and
supports any structure you define (see GAP 1 in
[`IFRS18-Fit-Gap-Analysis.md`](IFRS18-Fit-Gap-Analysis.md)). This means
SAP may not need to deliver code corrections for IFRS 18 the way it did
for standards that changed posting logic.

## How to search the SAP Support Portal

Go to <https://me.sap.com/notes> and search using these combinations:

| Search Term | Application Component | Why |
|---|---|---|
| `IFRS 18` | FI-GL | Core GL changes for IFRS 18 presentation |
| `IFRS 18` | FI-FIO-GL-HIE | Hierarchy/FSV enhancements for new categories |
| `IFRS 18` | FI-FIO-GL-REP | Financial statement reporting updates |
| `IFRS 18` | FI-FIO-GL-KPI | New semantic tags for Operating Profit, Profit before Financing |
| `IFRS 18` | FIN-CS | Group Reporting / consolidation impacts |
| `IFRS 18` | CA-GTF-CSC-EDO | Electronic disclosure / XBRL taxonomy updates |
| `IAS 1 replacement` | FI-GL | IFRS 18 replaces IAS 1 — SAP may reference it this way |
| `operating profit subtotal` | FI-FIO-GL | New mandatory subtotals |

Also filter by:

- **Software Component:** S4CORE (for S/4HANA core finance)
- **Release:** SAP S/4HANA 2023 (current landscape release) and SAP
  S/4HANA 2025
- **Note Category:** "Correction" and "Legal Change"

## Areas most likely to have relevant SAP-delivered updates

1. **New semantic tags** — for "Operating Profit" and "Profit before
   Financing and Income Taxes" subtotals, used by the standard KPI
   framework and Cash Flow Statement apps.
2. **Cash Flow Statement CDS views** — IFRS 18 reclassifies certain items
   between operating/investing/financing in the cash flow statement.
   Check the standard CDS view `2CCFICSHFLINDIFRS` (Cash Flow Statement –
   Indirect Method for IFRS), already available in S/4HANA 2023, for any
   related correction notes.
3. **XBRL/iXBRL taxonomy updates** — if electronic financial reporting
   (e.g. ESEF in the EU) is in scope, the IFRS taxonomy will be updated
   for IFRS 18; SAP Disclosure Management or SAP Document and Reporting
   Compliance may have related notes.
4. **SAP S/4HANA 2025** — released after IFRS 18 was issued, so it is the
   most likely release to contain IFRS 18-specific enhancements. If the
   current landscape is on S/4HANA 2023, any 2025-specific notes would
   need to be checked for backport eligibility via the note's "Validity"
   section.
5. **SAP Group Reporting** — if SAP has added IFRS 18-specific FS items
   or mapping templates. Not directly applicable to an HFM-based
   consolidation setup, but worth checking in case future consolidation
   tooling changes are considered.

## Recommended action

Assign someone with SAP Support Portal access (S-user) to run the
searches above and document any relevant notes found, including:

- Note number, title, and release date
- Application component and validity (software component/release)
- Whether it's a "Correction" or "Legal Change" note
- Whether it applies directly to the current release or requires
  backport/Support Package application

If notes exist for S/4HANA 2025 but not for the current release, check
whether they are backportable via the note's "Validity" section — SAP
often backports legal-change notes to older supported releases.
