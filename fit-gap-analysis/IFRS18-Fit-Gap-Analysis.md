# IFRS 18 Adoption — Functional Design Specification & Solution Description

Consolidated functional design specification and solution description for
the 7 identified GAPs in the IFRS 18 adoption analysis (SAP S/4HANA
landscape). GAPs are ordered by dependency (upstream capabilities first).

---

## GAP 1 — IFRS Financial Statement Structure Definition

| Attribute | Detail |
|---|---|
| Gap Type | CONFIG |
| Business Fit | FIT |
| Technical Fit | GAP |

**Functional Description of the Gap**

The three IFRS financial statement version structures (ZHFM for HFM
consolidation, ZCPL for controlling P&L, ZUKV for cost-of-sales P&L) must
be restructured to introduce the IFRS 18 income statement categories —
Operating, Investing, and Financing — along with two new mandatory
subtotals: "Operating Profit" and "Profit before Financing and Income
Taxes." SAP standard fully supports this through transaction OB58; no
custom development is needed. Pre-IFRS 18 backups (XHFM, XCPL, XUKV) were
already created in December 2025.

**As-Is State**

The three FSVs currently follow the IAS 1 income statement structure
without the IFRS 18 mandatory categories or subtotals. Backup copies
preserve the pre-change state.

**To-Be State**

Each FSV will contain new hierarchy nodes for Operating, Investing, and
Financing categories, with subtotal nodes for "Operating Profit" and
"Profit before Financing and Income Taxes." All P&L G/L accounts on chart
of accounts ZFRE will be reassigned to the appropriate new category
nodes. Balance sheet nodes remain unchanged.

**Solution Description**

1. Restructure **ZHFM** via OB58: add the three IFRS 18 income statement
   category nodes and two subtotal nodes; reassign all P&L G/L accounts to
   the correct categories.
2. Restructure **ZCPL** via OB58: apply the same IFRS 18 structure adapted
   for the controlling P&L perspective.
3. Restructure **ZUKV** via OB58: apply IFRS 18 categories while
   preserving the cost-of-sales method classification (COGS, selling,
   administrative).
4. Retain XHFM, XCPL, XUKV as audit trail.
5. Optionally evaluate migration to Global Hierarchies (Fiori app F4965)
   for future-proofing.

**Dependencies:** Foundational capability — all other GAPs depend on the
FSV restructuring being completed first.

**Effort Estimate:** Configuration only (functional consultant). No
development objects created or modified.

---

## GAP 2 — G/L Account to Consolidation Structure Mapping

| Attribute | Detail |
|---|---|
| Gap Type | CONFIG |
| Business Fit | FIT |
| Technical Fit | GAP |

**Functional Description of the Gap**

The custom mapping program that assigns G/L accounts to HFM consolidation
structure positions must be re-executed after the FSV restructuring.
Before that, the HFM structure configuration table (`/FIT/FI_F_STRUCT`,
387 entries) needs new or updated entries reflecting the IFRS 18 income
statement categories. The mapping program itself is fully data-driven and
requires no code changes.

**As-Is State**

The program `/FIT/FI_D_HFM_BIL_ZUORD_001` (transaction ZHFMB0, 33,984
executions/38 days) reads the FSV hierarchy and generates a flat mapping
in `/FIT/FI_F_HKONT` (2,461 rows). The structure table `/FIT/FI_F_STRUCT`
defines attributes for each HFM position (consolidation method,
functional area, intercompany, movement type, region, sign reversal).

**To-Be State**

The structure table will contain new entries for IFRS 18 P&L categories
(Operating, Investing, Financing) with appropriate attribute flags. The
mapping table will be regenerated to reflect the restructured FSV,
correctly assigning all P&L accounts to the new structure positions.

**Solution Description**

1. Update `/FIT/FI_F_STRUCT` via SM30: add entries for new IFRS 18 P&L
   structure positions (codes in the `21xxxx` range). Set consolidation
   method flags (KNSAA-D), functional area (KZFKB/KZFKCHNG), trading
   partner (KZVBUND), movement type (KZRMVCT), region (KZREGION), and sign
   reversal (KZVZUMK) for each new position.
2. Re-execute `/FIT/FI_D_HFM_BIL_ZUORD_001` (transaction ZHFMB0) with
   parameters: FSV = updated ZHFM, accounting principle = GRUP, chart of
   accounts = ZFRE, delete flag = X (regenerate).
3. Validate the regenerated `/FIT/FI_F_HKONT` entries — confirm all P&L
   accounts map to the correct new IFRS 18 structure positions and that
   balance sheet mappings remain intact.
4. Coordinate with the HFM system team to ensure the receiving
   consolidation system recognizes the new structure positions.

**Dependencies:** Depends on GAP 1 (FSV restructuring) being completed.
Downstream: GAP 3 (HFM extraction) consumes this mapping.

**Effort Estimate:** Configuration only (functional consultant
maintaining table entries + re-running the mapping program).

---

## GAP 3 — Financial Data Extraction for Group Consolidation

| Attribute | Detail |
|---|---|
| Gap Type | INTERFACE, CONFIG |
| Business Fit | GAP |
| Technical Fit | GAP |

**Functional Description of the Gap**

SAP S/4HANA has no standard interface to Oracle Hyperion Financial
Management. The two custom extraction programs, the shared function group
(119,486 executions/38 days), the staging table, and all HFM-specific
configuration tables must be retained. The extraction logic is entirely
data-driven through configuration tables, so IFRS 18 changes are
implemented through configuration updates — no ABAP code modifications
are needed.

**As-Is State**

Two programs operate in sequence:

- `/FIT/FI_D_HFM_INTF_001` (transaction ZHFM01, 176 executions/38 days):
  reads GL balances from FAGLFLEXT/ACDOCA, maps accounts to HFM structure
  positions using `/FIT/FI_F_HKONT`, enriches with intercompany,
  consolidation method, movement type, and region dimensions, and writes
  to staging table `/FIT/FI_F_HYPINT`.
- `/FIT/FI_D_HFM_INTF_010` (transaction ZHFM10, 10 executions/38 days):
  reads the staging table and transforms data through a four-step
  aggregation pipeline (INTF1→INTF2→INTF3→INTF4) to produce the HFM
  interface file.

Seven configuration tables drive the extraction: `/FIT/FI_F_HKONT`
(account mapping), `/FIT/FI_F_STRUCT` (structure attributes),
`/FIT/FI_F_VBUND` (intercompany), `/FIT/FI_F_KONSM` (consolidation
method), `/FIT/FI_F_REGION` (country-to-region), `/FIT/FI_F_RMVCT`
(movement types), `/FIT/FI_F_TRANS` (transaction types).

**To-Be State**

The same programs and architecture are retained. The configuration tables
are updated to reflect the IFRS 18 income statement structure. The output
file will contain the new IFRS 18 categories and subtotals as expected by
HFM.

**Solution Description**

1. Verify that the updated `/FIT/FI_F_HKONT` mapping (from GAP 2)
   correctly references the new IFRS 18 structure positions, with
   correct XBILK (B/G) and ZEITR flags.
2. Verify `/FIT/FI_F_KONSM` consolidation method suffixes are appropriate
   for the new IFRS 18 positions.
3. Verify `/FIT/FI_F_RMVCT` movement type mappings are correct for the
   new categories.
4. No changes expected to `/FIT/FI_F_VBUND` (company/partner mapping) or
   `/FIT/FI_F_REGION` (region mapping) — these are independent of income
   statement structure.
5. Run test extractions in simulation mode (`PX_SIMUL = 'X'`) to verify
   output correctness.
6. Validate the four-step aggregation pipeline correctly handles the new
   structure positions.
7. Coordinate with the HFM system team: the HFM receiving structure must
   be updated to accept the new IFRS 18 categories. New HFM
   accounts/categories may need to be created on the HFM side. Validate
   the output file format against HFM's expected input.
8. Note: `FAGLFLEXT` is a compatibility view in S/4HANA (on top of
   ACDOCA). The existing code works but could optionally be optimized to
   read directly from ACDOCA for performance. This is not required for
   IFRS 18.

**Dependencies:** Depends on GAP 1 (FSV restructuring) and GAP 2 (account
mapping regeneration). Also requires coordination with the external HFM
system team.

**Effort Estimate:** Configuration (updating config table entries) +
integration testing with HFM. No ABAP code changes. The HFM-side changes
are outside SAP scope but critical for end-to-end success.

---

## GAP 4 — Financial Statement Data Export

| Attribute | Detail |
|---|---|
| Gap Type | INTERFACE |
| Business Fit | FIT |
| Technical Fit | GAP |

**Functional Description of the Gap**

The core business need for financial statement data export is met by
standard Fiori apps (F0708 for PDF, W0161 for Excel). The gap is the
custom integration with the AMANA document management system, which
receives parsed financial statement data via SAP PI/PO middleware. This
has no standard equivalent.

**As-Is State**

The custom program `ZFI_R_RFBILA00_DOWN` (transaction
`ZFI_RFBILA00_DOWN`, 945 executions/38 days) wraps the standard RFBILA00
report and offers three export paths: PC download, application server
download, and AMANA transfer. The AMANA path calls function module
`ZFI_AMANA_PROXY`, which parses the ASCII list output and sends structured
data via proxy class `ZFI_CO_SI_OA_AMANA_MESSAGE` (90 executions/38 days)
through SAP PI/PO (logical port LP_AMANA).

**To-Be State**

Interactive users migrate to standard Fiori apps for ad-hoc export. The
AMANA integration is retained as a custom interface. The program is
FSV-agnostic, so IFRS 18 FSV restructuring is automatically reflected in
the output without code changes.

**Solution Description**

1. Activate Fiori apps F0708 (Balance Sheet/Income Statement) and W0161
   (Multidimensional) in the Fiori Launchpad. Configure them to work with
   ZHFM, ZCPL, and ZUKV.
2. Retain the AMANA integration components: function module
   `ZFI_AMANA_PROXY`, proxy class `ZFI_CO_SI_OA_AMANA_MESSAGE`, data type
   structures (`ZFI_MT_AMANA_MESSAGE`, `ZFI_DT_RFBILA00_RECORD`), and the
   PI/PO interface configuration.
3. Coordinate with the AMANA system team to ensure the receiving system
   can handle the new IFRS 18 income statement categories.
4. Test the AMANA proxy parsing logic with the restructured IFRS FSVs —
   the positional parsing (splitting on `|` delimiters, counting `---`
   separators) should continue to work, but this must be verified.
5. Consider refactoring: if AMANA transfer is the only remaining use case
   for `ZFI_R_RFBILA00_DOWN`, either create a dedicated AMANA-only program
   or modernize the integration by replacing the fragile list-output
   parsing with a direct data read (e.g., CDS views or
   FAGL_GET_BALANCE API).
6. Retirement candidates (if interactive users fully migrate to Fiori):
   `ZFI_R_RFBILA00_DOWN`, `ZFI_RFBILA00_DOWN` (transaction),
   `ZFI_R_RFBILA00_DOWN_TYPES`, `ZFI_R_RFBILA00_DOWN_MACROS`.

**Dependencies:** Depends on GAP 1 (FSV restructuring). Requires
coordination with AMANA system team and PI/PO middleware team.

**Effort Estimate:** Fiori app activation (configuration). AMANA
integration testing. Optional refactoring of the AMANA proxy. No
mandatory ABAP code changes for IFRS 18.

---

## GAP 5 — Income Statement Reporting by Cost of Sales Method

| Attribute | Detail |
|---|---|
| Gap Type | REPORT |
| Business Fit | FIT |
| Technical Fit | GAP |
| Standard Extensibility | YES (Custom Analytical Queries app — Key User Extensibility, Clean Core Level A) |

**Functional Description of the Gap**

SAP standard provides released analytical CDS views and Fiori apps that
can deliver income statement reporting by cost of sales method. The gap
is that adopting standard requires creating a custom analytical query on
the standard cube to replicate the specific P&L filtering with functional
area classification. Additionally, the custom cube contains a foreign
currency valuation exclusion (FG/FX document type filtering) that needs
to be evaluated for carry-forward.

**As-Is State**

A three-layer custom CDS view stack:

- `ZC_PROFITANDLOSS_UKV` (analytics query): filters for P&L accounts with
  functional areas, provides drill-down by company code, profit center,
  segment, and other dimensions. The GL account hierarchy is
  user-selectable at runtime.
- `ZI_JournalEntryItemCube` (custom cube): built on standard
  `I_JournalEntryItem`, adds a WHERE clause excluding balance sheet
  accounts with document types FG/FX (foreign currency valuation).
- The report automatically reflects FSV changes because the hierarchy is
  user-selectable — no hardcoded FSV references.

**To-Be State**

A new custom analytical query on the standard released
`I_JournalEntryItemCube` replaces the custom CDS stack. The IFRS 18
categories and subtotals are displayed through the restructured ZUKV
hierarchy. If the FG/FX exclusion is still required, a CDS view extension
is added.

**Solution Description**

1. Validate that standard CDS views `C_PROFITANDLOSSQ2901` and
   `C_FUNCTIONALAREASQ2801` are active in the system.
2. Confirm `I_JournalEntryItemCube` is accessible and includes all
   required dimensions (FunctionalArea, CompanyCode, ProfitCenter,
   Segment, etc.).
3. Assess whether the FG/FX document type exclusion is still a business
   requirement. If yes: create a CDS view extension on
   `I_JournalEntryItemCube` or a custom cube with the filtering logic. If
   no: proceed directly with the Custom Analytical Queries app.
4. Create a custom analytical query via the Custom Analytical Queries app
   (Fiori) on `I_JournalEntryItemCube`:
   - Mandatory filters: `IsProfitLossAccount = 'X'`, `FunctionalArea` is
     not initial
   - Row dimensions: CompanyCode, FunctionalArea, GLAccount (with
     hierarchy display)
   - Column dimensions: LedgerFiscalYear, FiscalPeriod,
     AmountInCompanyCodeCurrency
   - Free characteristics: CostCenter, ProfitCenter, Segment,
     BusinessArea, Customer, Material, Plant, SalesOrganization, etc.
5. After ZUKV is restructured for IFRS 18, validate that the new query
   correctly displays the Operating, Investing, and Financing categories
   and the mandatory subtotals through the GL account hierarchy.
6. Deploy the new query to analytics consumers (Fiori, SAC, Analysis for
   Office).
7. Validate output matches `ZC_PROFITANDLOSS_UKV` for a reference period.
8. Decommission `ZC_PROFITANDLOSS_UKV`. Evaluate whether
   `ZI_JournalEntryItemCube` can also be decommissioned (check for other
   active consumers).

**Dependencies:** Depends on GAP 1 (ZUKV restructuring). Requires business
decision on FG/FX exclusion logic.

**Effort Estimate:** If no FG/FX extension needed: Key User Extensibility
(functional consultant via Custom Analytical Queries app). If FG/FX
extension needed: developer effort for CDS view extension (Clean Core
Level B).

---

## GAP 6 — Working Capital Balance Sheet Reporting

| Attribute | Detail |
|---|---|
| Gap Type | ENHANCEMENT |
| Business Fit | FIT |
| Technical Fit | GAP |
| Standard Extensibility | NO (hardcoded values in custom CDS source code must be directly modified) |

**Functional Description of the Gap**

The custom working capital report classifies balance sheet accounts into
inventories, trade receivables, accounts payable (trade), and advance
payments using hardcoded references to specific ZHFM hierarchy node IDs.
When the ZHFM hierarchy is restructured for IFRS 18, these hardcoded node
references will break if any of the referenced nodes change. A developer
must update the CDS view source code.

**As-Is State**

The CDS view `ZI_GLAcctBalanceCube` contains a CASE WHEN statement that
classifies accounts into working capital categories based on
`ParentNode` values from the ZHFM hierarchy:

- Sales: nodes 0210010, 0210020, 0210035, 021004B, 021004C, 021004D,
  0210040, 021005B, 021005C, 021005D, 0210050
- Inventories: nodes 0004100, 0004200, 0004300, 0004400
- Trade receivables: node 0005000
- Accounts payable (trade): nodes 0107300, 0107350
- Advance payments received on order: nodes 0107200, 0107201

The association to `I_GLAccountHierarchyNode` is hardcoded to
`GLAccountHierarchy = 'ZHFM'`.

A secondary SAC prototype stack (`ZC_WORKINGCAPITAL_CUBE_Q001`,
`ZI_WORKINGCAPITAL_CUBE`, `ZP_WORKINGCAPITAL_ITEM`) has hardcoded dates
for fiscal years 2021/2022 and is not production-ready.

**To-Be State**

The hardcoded hierarchy node references are updated to match the
restructured ZHFM hierarchy. For long-term resilience, the classification
logic is optionally refactored to use semantic tags instead of hardcoded
node IDs.

**Solution Description**

1. **Immediate fix** — After ZHFM is restructured for IFRS 18, identify
   the new `ParentNode` values for each working capital category. Update
   the CASE WHEN statement in `ZI_GLAcctBalanceCube` with the new node
   IDs. Verify the association `GLAccountHierarchy = 'ZHFM'` remains
   valid (the hierarchy name itself is not expected to change).
2. **Verify downstream** — `ZC_WORKINGCAPITAL_Q001` consumes the
   `WorkingCapital` field from the cube and should not need code changes.
   Verify the hierarchy filter binding `{type: #CONSTANT, value: 'ZHFM'}`
   remains correct.
3. **SAC prototype** — Evaluate `ZP_WORKINGCAPITAL_ITEM` and related
   views for retirement (hardcoded 2021/2022 dates make them
   non-functional for current reporting). If SAC-based working capital
   reporting is needed, rebuild with parameterized dates.
4. **Long-term improvement (optional)** — Assign custom semantic tags to
   the relevant ZHFM hierarchy nodes (e.g., `Z_WC_INVENTORY`,
   `Z_WC_TRADE_REC`, `Z_WC_TRADE_PAY`, `Z_WC_ADV_PAY`, `Z_WC_SALES`) via
   OB58. Refactor `ZI_GLAcctBalanceCube` to derive the `WorkingCapital`
   classification from semantic tags instead of hardcoded `ParentNode`
   values. This would make the view resilient to future hierarchy
   restructurings.
5. **Testing** — Compare working capital report output before and after
   using the XHFM backup as a reference. Validate all five categories
   produce correct balances. Verify Working Capital % of Sales
   calculation.

**Dependencies:** Depends on GAP 1 (ZHFM restructuring). Requires
developer to modify CDS view source code.

**Effort Estimate:** Developer effort to update CDS view (small —
updating CASE WHEN values). Optional larger effort if refactoring to
semantic tags.

---

## GAP 7 — IFRS 16 Lease Accounting Data Loading

| Attribute | Detail |
|---|---|
| Gap Type | CONFIG |
| Business Fit | FIT |
| Technical Fit | GAP |

**Functional Description of the Gap**

The custom IFRS 16 lease data loading program (`Z_FI_I_LOAD_IFRS16`,
18,284 executions/38 days) posts journal entries to the IFRS ledger using
a custom mapping table (`ZFI_IFRS16`, 510 entries) that translates
Tagetik account codes to SAP G/L accounts. The program itself is a
posting mechanism agnostic to FSV classification. The gap is that the
mapping table entries must be reviewed to verify that the G/L accounts
used for lease expenses are correctly classified under the new IFRS 18
categories in the FSVs.

**As-Is State**

The mapping table routes lease expenses to specific G/L accounts:

- Depreciation of RoU assets: accounts 670000, 670002, 670005, 670006 →
  should be classified as **Operating** under IFRS 18
- Interest on lease liabilities: accounts 661300, 661302, 661305, 661306
  → should be classified as **Financing** under IFRS 18
- Other lease expenses: accounts 671110–671306 → classification to be
  verified

All 510 mapping entries are generic (company code and asset class fields
are blank), applying uniformly across all company codes.

**To-Be State**

The mapping table entries are verified and, if necessary, updated to
ensure the G/L accounts align with the IFRS 18 income statement
categories. The program continues to operate unchanged. If the chart of
accounts is restructured (new G/L accounts introduced), the HKONT field
in affected mapping entries is updated.

**Solution Description**

1. Review all 510 entries in `ZFI_IFRS16` (via transaction
   `ZFI_IFRS16_MAPPING` / SM30) to verify that the target G/L accounts
   are correctly classified in the restructured IFRS FSVs:
   - Depreciation accounts (670000 series) → confirm classified as
     **Operating** in ZHFM/ZUKV
   - Interest accounts (661300 series) → confirm classified as
     **Financing** in ZHFM/ZUKV
   - Other lease expense accounts (671110 series) → verify correct
     IFRS 18 category
2. If the chart of accounts is restructured for IFRS 18 (new G/L accounts
   introduced), update the HKONT field in affected mapping entries.
3. Coordinate with the Tagetik team to ensure external account codes
   (TAGETIC_ACCOUNT field) remain aligned. If Tagetik introduces new
   account codes for IFRS 18, add corresponding entries to the mapping
   table.
4. No code changes required to `Z_FI_I_LOAD_IFRS16` — the program uses
   `BAPI_ACC_DOCUMENT_POST` (fully supported in S/4HANA 2023) with
   accounting principle 'IFRS', and falls back to `RFBIBL00` for failed
   entries.
5. The actual FSV classification of these G/L accounts is handled by
   GAP 1 (IFRS Financial Statement Structure Definition) — this GAP only
   verifies the mapping table alignment.

**Dependencies:** Depends on GAP 1 (FSV restructuring) to confirm the
correct classification of lease-related G/L accounts. Requires
coordination with the Tagetik team.

**Effort Estimate:** Configuration review only (functional consultant).
No development objects created or modified.

---

## Summary of Dependencies and Sequencing

```
GAP 1: FSV Restructuring (ZHFM, ZCPL, ZUKV)
  ├── GAP 2: G/L Account to HFM Structure Mapping (re-execute after GAP 1)
  │     └── GAP 3: HFM Data Extraction (validate config after GAP 2)
  ├── GAP 4: Financial Statement Data Export / AMANA (test after GAP 1)
  ├── GAP 5: P&L Report - Cost of Sales Method (validate hierarchy after GAP 1)
  ├── GAP 6: Working Capital Report (update CDS view after GAP 1)
  └── GAP 7: IFRS 16 Lease Data Loading (verify mapping after GAP 1)
```

| GAP | Type | Effort Category | Code Change Required? |
|---|---|---|---|
| 1. FSV Structure Definition | CONFIG | Functional consultant | No |
| 2. G/L Account Mapping | CONFIG | Functional consultant | No |
| 3. HFM Data Extraction | INTERFACE + CONFIG | Functional consultant + HFM team | No |
| 4. Financial Statement Export | INTERFACE | Fiori activation + AMANA testing | No (mandatory); Optional refactoring |
| 5. P&L Cost of Sales Report | REPORT | Key User Extensibility or developer | New query (no legacy code change) |
| 6. Working Capital Report | ENHANCEMENT | Developer | Yes (CDS view update) |
| 7. IFRS 16 Lease Data Loading | CONFIG | Functional consultant | No |

The critical path runs through GAP 1 → GAP 2 → GAP 3, as the HFM
consolidation interface depends on both the FSV restructuring and the
account mapping regeneration. All other GAPs can proceed in parallel once
GAP 1 is complete.
