# IFRS 18 — SAP OSS Notes Guidance

**This document does not fabricate SAP OSS Note numbers.** OSS Notes are
published exclusively on the SAP Support Portal (SAP for Me / SAP ONE
Support Launchpad), which requires an S-user login and was not directly
accessible when this analysis was produced. The one note number below
(3670330) was reported by a third-party blog shared for this project,
**not independently confirmed on the Support Portal** — treat it as a
lead to verify, not a confirmed fact, and use the search plan below to
find anything further.

## Note reported by external source (needs verification)

| Note | Title (as reported) | Reported scope | Status |
|---|---|---|---|
| [**3670330**](https://me.sap.com/notes/3670330) | SAP's IFRS 18 solution approach | Targeted a formal solution approach by Dec 2025, delivered via the **1SG content package** for **SAP Group Reporting** | **Not yet verified by us** — pull up directly on the Support Portal to confirm content, validity, and whether it's actually applicable to this landscape |

See [`IFRS18-Overview-and-SAP-Roadmap.md`](IFRS18-Overview-and-SAP-Roadmap.md)
for full context on where this note came from. Important caveat: this
landscape consolidates via **Oracle HFM**, not **SAP Group Reporting**,
so the 1SG content package referenced by this note may only partially
apply here (e.g. general FI-GL/FSV guidance might be relevant to GAP 1,
but Group-Reporting-specific content would not resolve GAP 2/GAP 3).
Since the targeted delivery date (Dec 2025) has already passed as of
this writing, whoever reviews the note should also check for any
successor/related notes it references.

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

1. **First**, have someone with SAP Support Portal access (S-user) pull
   up **Note 3670330** directly at <https://me.sap.com/notes/3670330> to
   confirm it exists, read its actual content/validity, and check for any
   notes it references or that reference it back.
2. **Then**, run the broader searches below and document any additional
   relevant notes found, including:

- Note number, title, and release date
- Application component and validity (software component/release)
- Whether it's a "Correction" or "Legal Change" note
- Whether it applies directly to the current release or requires
  backport/Support Package application

If notes exist for S/4HANA 2025 but not for the current release, check
whether they are backportable via the note's "Validity" section — SAP
often backports legal-change notes to older supported releases.
