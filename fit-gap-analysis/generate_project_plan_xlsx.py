"""
Generates 'IFRS18_Adoption_Project_Plan.xlsx' — an editable/trackable
Excel version of the IFRS 18 SAP adoption project plan described in
IFRS18-Project-Plan.md.

Usage:
    pip install openpyxl
    python3 generate_gantt_chart.py       # produces the Gantt PNG first
    python3 generate_project_plan_xlsx.py

Sheets produced:
    0. Dashboard           - visual overview: KPI summary cards, the
                             rendered Gantt chart image, and native Excel
                             bar/pie charts for effort by phase, by role,
                             and by work type.
    1. Project Plan        - 60 activities across 8 phases, with dates,
                             dependencies, execution order, SAP
                             transaction(s)/object(s), and a Status
                             column for tracking. Includes 9 activities
                             (1.7-1.11, 3.8-3.9, 5.8-5.9) added after
                             reviewing SAP Note 3670330 and the SAP TRM
                             open question.
    2. Effort Summary      - effort by phase / by role / by GAP / by work type.
    3. Milestones & Risks  - key milestones, risks, assumptions, critical path.
    4. RACI Matrix         - responsibility assignment across roles.
    5. SAP Notes & References - confirmed SAP Notes, child-note search
                             guide, SAP content deliverables tracker,
                             external source references, and a treasury
                             G/L account classification checklist.
"""

import os
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HEADER_FILL = PatternFill("solid", fgColor="1F3B73")
SUBHEADER_FILL = PatternFill("solid", fgColor="8EA9DB")
BANNER_FILL = PatternFill("solid", fgColor="F4B183")
STRIPE_FILL = PatternFill("solid", fgColor="F2F2F2")
HEADER_FONT = Font(bold=True, color="FFFFFF")
BANNER_FONT = Font(bold=True, color="000000")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")


def style_header_row(ws, row, ncols, fill=HEADER_FILL, font=HEADER_FONT):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill
        cell.font = font
        cell.alignment = WRAP_CENTER
        cell.border = BORDER


def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def write_table(ws, start_row, headers, rows, widths, banner=None):
    r = start_row
    if banner:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(headers))
        c = ws.cell(row=r, column=1, value=banner)
        c.fill = BANNER_FILL
        c.font = BANNER_FONT
        c.alignment = WRAP_CENTER
        r += 1
    style_header_row(ws, r, len(headers))
    for col, h in enumerate(headers, start=1):
        ws.cell(row=r, column=col, value=h)
    r += 1
    for i, row_data in enumerate(rows):
        for col, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r, column=col, value=val)
            cell.alignment = WRAP
            cell.border = BORDER
            if i % 2 == 1:
                cell.fill = STRIPE_FILL
        r += 1
    autosize(ws, widths)
    return r


wb = Workbook()

# ============================================================
# Sheet 1 — Project Plan
# ============================================================
ws1 = wb.active
ws1.title = "Project Plan"

PROJECT_START = date(2026, 7, 14)


def d(offset_days):
    return PROJECT_START + timedelta(days=offset_days)


# (activity_id, phase, description, gap_ref, gap_name, gap_type, role,
#  effort_pd, start_offset, duration_days)
GAP_NAMES = {
    "1": "IFRS Financial Statement Structure Definition",
    "2": "G/L Account to Consolidation Structure Mapping",
    "3": "Financial Data Extraction for Group Consolidation",
    "4": "Financial Statement Data Export",
    "5": "Income Statement Reporting (Cost of Sales)",
    "6": "Working Capital Balance Sheet Reporting",
    "7": "IFRS 16 Lease Accounting Data Loading",
    "All": "Cross-cutting",
    "1->2->3": "GAP 1 -> GAP 2 -> GAP 3",
    "1->5": "GAP 1 -> GAP 5",
    "1->6": "GAP 1 -> GAP 6",
    "1->7": "GAP 1 -> GAP 7",
    "1->4": "GAP 1 -> GAP 4",
    "2, 3": "GAP 2, GAP 3",
    "-": "N/A",
    "SAPNOTE": "SAP Notes & Treasury (added after reviewing Note 3670330 and the TRM open question)",
}

activities = [
    ("1.1", "1 - Design & Preparation", "Finalize IFRS 18 P&L category design with group accounting team (Operating/Investing/Financing boundaries, subtotal definitions)", "All", "FC + Accounting", 3, 0, 5, None),
    ("1.2", "1 - Design & Preparation", "Define new FSV hierarchy node structure for ZHFM, ZCPL, ZUKV (node IDs, parent-child relationships, G/L account assignments)", "1", "FC", 5, 0, 8, None),
    ("1.3", "1 - Design & Preparation", "Define new HFM structure positions and attribute flags (consolidation method, functional area, intercompany, movement type, region, sign reversal)", "2, 3", "FC", 3, 5, 5, "1.1"),
    ("1.4", "1 - Design & Preparation", "Kick-off coordination with HFM team (new structure positions, receiving format)", "3", "FC + HFM", 1, 7, 3, None),
    ("1.5", "1 - Design & Preparation", "Kick-off coordination with Tagetik team (account code alignment)", "7", "FC + Tagetik", 1, 7, 3, None),
    ("1.6", "1 - Design & Preparation", "Kick-off coordination with AMANA team (new category handling)", "4", "FC + AMANA", 0.5, 7, 3, None),
    ("1.7", "1 - Design & Preparation", "Review and implement SAP Note 3670330 - check validity for current release, review all child notes (3694359, 3696338, 3700153), implement corrections via SNOTE", "SAPNOTE", "Basis + FC", 2, 0, 4, None),
    ("1.8", "1 - Design & Preparation", "Review SAP IFRS 18 webinar recordings (Feb/Mar 2026) for technical guidance", "SAPNOTE", "FC", 1, 0, 2, None),
    ("1.9", "1 - Design & Preparation", "Review treasury compliance blog and check for TRM-specific notes", "SAPNOTE", "FC", 0.5, 0, 2, None),
    ("1.10", "1 - Design & Preparation", "Review treasury G/L accounts for IFRS 18 classification (interest, FX, dividends, fair value)", "SAPNOTE", "FC + Treasury", 2, 3, 5, "1.1"),
    ("1.11", "1 - Design & Preparation", "Use 1SG content package restructured Income Statement as reference blueprint for FSV design", "SAPNOTE", "FC", 1, 0, 3, None),

    ("2.1", "2 - FSV Restructuring", "Restructure ZHFM via OB58: add Operating/Investing/Financing nodes, two subtotal nodes, reassign P&L G/L accounts", "1", "FC", 5, 14, 7, "1.2"),
    ("2.2", "2 - FSV Restructuring", "Restructure ZCPL via OB58: apply IFRS 18 structure for controlling P&L", "1", "FC", 3, 21, 5, "2.1"),
    ("2.3", "2 - FSV Restructuring", "Restructure ZUKV via OB58: apply IFRS 18 categories preserving cost-of-sales classification", "1", "FC", 3, 21, 5, "2.1"),
    ("2.4", "2 - FSV Restructuring", "Unit test each FSV using standard financial statement reports (F.01 / RFBILA00)", "1", "FC", 2, 26, 3, "2.2"),
    ("2.5", "2 - FSV Restructuring", "Peer review of FSV structures with group accounting", "1", "FC + Accounting", 1, 29, 1, "2.4"),

    ("3.1", "3 - Configuration Updates", "Update /FIT/FI_F_STRUCT table entries via SM30 - add new IFRS 18 P&L structure positions with attribute flags", "2", "FC", 3, 32, 5, "2.5"),
    ("3.2", "3 - Configuration Updates", "Re-execute mapping program /FIT/FI_D_HFM_BIL_ZUORD_001 (ZHFMB0) with delete-and-regenerate", "2", "FC", 0.5, 37, 3, "3.1"),
    ("3.3", "3 - Configuration Updates", "Validate regenerated /FIT/FI_F_HKONT mapping - verify all P&L accounts map to correct new positions, BS mappings intact", "2", "FC", 2, 40, 3, "3.2"),
    ("3.4", "3 - Configuration Updates", "Review all 510 entries in ZFI_IFRS16 mapping table - verify G/L accounts for depreciation (670xxx -> Operating) and interest (661xxx -> Financing) are correctly classified", "7", "FC", 2, 32, 5, "2.5"),
    ("3.5", "3 - Configuration Updates", "Update ZFI_IFRS16 entries if chart of accounts changes or Tagetik introduces new codes", "7", "FC", 1, 37, 3, "3.4"),
    ("3.6", "3 - Configuration Updates", "Activate Fiori apps F0708 and W0161 in Fiori Launchpad", "4", "Basis/FC", 1, 32, 3, "2.5"),
    ("3.7", "3 - Configuration Updates", "Configure Fiori apps for IFRS FSVs (ZHFM, ZCPL, ZUKV)", "4", "FC", 1, 35, 2, "3.6"),
    ("3.8", "3 - Configuration Updates", "Apply SAP Note 3670330 child notes / corrections to CSD via SNOTE", "SAPNOTE", "Basis", 1, 32, 2, "1.7"),
    ("3.9", "3 - Configuration Updates", "Verify new semantic tags for Operating Profit and Profit before Financing and Income Tax", "SAPNOTE", "FC", 1, 32, 2, "1.7"),

    ("4.1", "4 - Development", "Evaluate whether FG/FX document type exclusion is still a business requirement", "5", "FC + Dev", 1, 32, 2, "2.5"),
    ("4.2", "4 - Development", "Create custom analytical query on I_JournalEntryItemCube via Custom Analytical Queries app (P&L filter + functional area classification)", "5", "FC/Dev", 3, 34, 5, "4.1"),
    ("4.3", "4 - Development", "Optional: Create CDS view extension on I_JournalEntryItemCube for FG/FX filtering (if required)", "5", "Dev", 2, 34, 4, "4.1"),
    ("4.4", "4 - Development", "Update ZI_GLAcctBalanceCube CASE WHEN statement - replace hardcoded ZHFM hierarchy node IDs with new node IDs from restructured hierarchy", "6", "Dev", 1, 32, 3, "2.5"),
    ("4.5", "4 - Development", "Verify ZC_WORKINGCAPITAL_Q001 downstream - confirm hierarchy filter binding still valid", "6", "Dev", 0.5, 35, 1, "4.4"),
    ("4.6", "4 - Development", "Evaluate SAC prototype views (ZP_WORKINGCAPITAL_ITEM etc.) for retirement", "6", "Dev", 0.5, 35, 1, "4.4"),
    ("4.7", "4 - Development", "Unit test new P&L analytical query - compare output with ZC_PROFITANDLOSS_UKV for reference period", "5", "FC", 2, 39, 4, "4.2"),
    ("4.8", "4 - Development", "Unit test working capital report - validate all 5 categories produce correct balances", "6", "FC", 1, 36, 2, "4.4"),

    ("5.1", "5 - Interface Validation", "Run HFM extraction in simulation mode (PX_SIMUL = 'X') via ZHFM01", "3", "FC", 1, 43, 4, "3.3"),
    ("5.2", "5 - Interface Validation", "Validate HFM output file format against HFM expected input - verify new structure positions appear correctly in aggregation pipeline (INTF1->4)", "3", "FC + HFM", 2, 47, 4, "5.1"),
    ("5.3", "5 - Interface Validation", "Verify /FIT/FI_F_KONSM and /FIT/FI_F_RMVCT entries are correct for new positions", "3", "FC", 1, 43, 4, "3.3"),
    ("5.4", "5 - Interface Validation", "Test AMANA proxy parsing with restructured FSV output - verify positional parsing still works", "4", "FC", 1, 37, 3, "3.7"),
    ("5.5", "5 - Interface Validation", "Coordinate HFM-side configuration updates (new accounts/categories in HFM)", "3", "HFM team", 3, 35, 20, "1.4"),
    ("5.6", "5 - Interface Validation", "Coordinate Tagetik account code alignment", "7", "Tagetik team", 2, 35, 20, "1.5"),
    ("5.7", "5 - Interface Validation", "Coordinate AMANA receiving system updates", "4", "AMANA team", 1, 35, 20, "1.6"),
    ("5.8", "5 - Interface Validation", "Validate Cash Flow Statement CDS view after note implementation", "SAPNOTE", "FC", 0.5, 47, 2, "3.8"),
    ("5.9", "5 - Interface Validation", "Validate treasury valuation postings in restructured FSVs", "SAPNOTE", "FC + Treasury", 1, 43, 4, "1.10"),

    ("6.1", "6 - Integration Testing", "End-to-end: FSV -> mapping regeneration -> HFM extraction -> file validation", "1->2->3", "FC", 3, 51, 5, "5.2"),
    ("6.2", "6 - Integration Testing", "End-to-end: FSV -> P&L report with IFRS 18 categories and subtotals", "1->5", "FC", 1, 53, 3, "4.7"),
    ("6.3", "6 - Integration Testing", "End-to-end: FSV -> working capital report with updated hierarchy nodes", "1->6", "FC", 1, 53, 3, "4.7"),
    ("6.4", "6 - Integration Testing", "End-to-end: IFRS 16 lease posting -> verify FSV classification (depreciation = Operating, interest = Financing)", "1->7", "FC", 1, 53, 3, "4.7"),
    ("6.5", "6 - Integration Testing", "End-to-end: Financial statement export -> AMANA transfer", "1->4", "FC", 1, 50, 3, "5.4"),
    ("6.6", "6 - Integration Testing", "Regression test: Shareholder reporting (FIT - no changes expected)", "-", "FC", 0.5, 53, 3, None),
    ("6.7", "6 - Integration Testing", "Compare pre-IFRS 18 (XHFM/XCPL/XUKV) vs. post-IFRS 18 output for audit trail", "All", "FC", 2, 53, 3, None),
    ("6.8", "6 - Integration Testing", "Defect resolution buffer", "All", "FC + Dev", 3, 56, 5, "6.1"),

    ("7.1", "7 - QA Transport & UAT", "Prepare transport requests (config + workbench)", "All", "Dev/Basis", 1, 61, 3, "6.8"),
    ("7.2", "7 - QA Transport & UAT", "Execute transport CSD -> CSQ", "All", "Basis", 0.5, 64, 1, "7.1"),
    ("7.3", "7 - QA Transport & UAT", "QA smoke testing - verify all 7 capabilities in CSQ", "All", "FC", 3, 65, 4, "7.2"),
    ("7.4", "7 - QA Transport & UAT", "User acceptance testing with business users (finance, controlling, consolidation)", "All", "Business + FC", 5, 69, 7, "7.3"),
    ("7.5", "7 - QA Transport & UAT", "Defect resolution and re-transport", "All", "FC + Dev", 3, 76, 5, "7.4"),
    ("7.6", "7 - QA Transport & UAT", "Re-test after fixes", "All", "FC", 2, 81, 4, "7.5"),

    ("8.1", "8 - Production Go-Live", "Execute transport CSQ -> CSP", "All", "Basis", 0.5, 85, 2, "7.6"),
    ("8.2", "8 - Production Go-Live", "Production verification - run each capability and validate output", "All", "FC", 2, 87, 3, "8.1"),
    ("8.3", "8 - Production Go-Live", "Go-live communication to business users", "All", "PM", 0.5, 87, 1, "8.1"),
    ("8.4", "8 - Production Go-Live", "Hypercare support (2 weeks - monitor HFM extraction, reports, IFRS 16 postings)", "All", "FC + Dev", 5, 90, 14, "8.2"),
]

# Recommended Execution Order (see IFRS18-Project-Plan.md, "Recommended
# Execution Sequence") - activities sharing the same number have no
# dependency on each other and can be executed in parallel.
EXEC_ORDER = {
    "1.1": 1, "1.2": 2, "1.3": 3, "1.4": 3, "1.5": 3, "1.6": 3,
    "1.7": 1, "1.8": 1, "1.9": 1, "1.10": 3, "1.11": 1,
    "2.1": 4, "2.2": 5, "2.3": 5, "2.4": 6, "2.5": 7,
    "3.1": 8, "3.2": 9, "3.3": 10, "3.4": 8, "3.5": 10, "3.6": 8, "3.7": 10,
    "3.8": 8, "3.9": 8,
    "4.1": 8, "4.2": 9, "4.3": 9, "4.4": 8, "4.5": 10, "4.6": 10, "4.7": 11, "4.8": 11,
    "5.1": 11, "5.2": 12, "5.3": 11, "5.4": 12, "5.5": 13, "5.6": 13, "5.7": 13,
    "5.8": 12, "5.9": 11,
    "6.1": 14, "6.2": 15, "6.3": 15, "6.4": 15, "6.5": 15, "6.6": 15, "6.7": 16, "6.8": 17,
    "7.1": 18, "7.2": 19, "7.3": 20, "7.4": 21, "7.5": 22, "7.6": 23,
    "8.1": 24, "8.2": 25, "8.3": 25, "8.4": 26,
}

# SAP transaction code(s) / development object(s) touched by each activity.
TRANSACTION_OBJECT = {
    "1.1": "Workshop - no transaction; output is a signed-off category definition document",
    "1.2": "Design doc for later use in OB58 (Financial Statement Version: Maintain)",
    "1.3": "Design doc for later use in SM30 on table /FIT/FI_F_STRUCT",
    "1.4": "Meeting - no transaction",
    "1.5": "Meeting - no transaction",
    "1.6": "Meeting - no transaction",
    "1.7": "SNOTE (Note Implementation) for Note 3670330 and its child notes",
    "1.8": "External webinar review - no transaction",
    "1.9": "External blog / Support Portal search - no transaction",
    "1.10": "SM30 / SE16N on TRM accounting-derivation config (Account Assignment Reference) and affected G/L accounts",
    "1.11": "Review of SAP Best Practice content (Scope Item 1SG) - reference only, no transaction in this landscape",
    "2.1": "OB58 (FSV = ZHFM, chart of accounts ZFRE)",
    "2.2": "OB58 (FSV = ZCPL)",
    "2.3": "OB58 (FSV = ZUKV)",
    "2.4": "F.01 / RFBILA00 (or S_ALR_87012284), one run per FSV",
    "2.5": "Review of OB58 output; meeting sign-off",
    "3.1": "SM30 on table /FIT/FI_F_STRUCT (new position codes, 21xxxx range)",
    "3.2": "ZHFMB0 (program /FIT/FI_D_HFM_BIL_ZUORD_001); FSV=ZHFM, principle=GRUP, COA=ZFRE, delete flag=X",
    "3.3": "SE16N (display table /FIT/FI_F_HKONT)",
    "3.4": "ZFI_IFRS16_MAPPING / SM30 on table ZFI_IFRS16",
    "3.5": "ZFI_IFRS16_MAPPING / SM30 on table ZFI_IFRS16 (field HKONT / TAGETIC_ACCOUNT)",
    "3.6": "/UI2/FLPD_CUST (Fiori Launchpad Designer) - activate F0708, W0161",
    "3.7": "F0708 / W0161 app configuration - bind default FSV parameters",
    "3.8": "SNOTE (Note Implementation)",
    "3.9": "OB58 hierarchy node semantic-tag assignment; KPI framework config",
    "4.1": "Business decision workshop - no transaction",
    "4.2": "Custom Analytical Queries app (Fiori) on CDS view I_JournalEntryItemCube",
    "4.3": "ADT/Eclipse - DDLS extend view on I_JournalEntryItemCube; SE09/SE10 transport",
    "4.4": "ADT/Eclipse - CDS view ZI_GLAcctBalanceCube source; SE09/SE10 transport",
    "4.5": "ADT/Eclipse or RSRT - query ZC_WORKINGCAPITAL_Q001 filter binding",
    "4.6": "SAP Analytics Cloud review - no ABAP transaction",
    "4.7": "Run new query + ZC_PROFITANDLOSS_UKV via Fiori / Analysis for Office",
    "4.8": "Run working-capital report (Fiori app on ZC_WORKINGCAPITAL_Q001)",
    "5.1": "ZHFM01 (program /FIT/FI_D_HFM_INTF_001); parameter PX_SIMUL = 'X'",
    "5.2": "ZHFM10 (program /FIT/FI_D_HFM_INTF_010); AL11 / app server output review",
    "5.3": "SM30 on tables /FIT/FI_F_KONSM and /FIT/FI_F_RMVCT",
    "5.4": "ZFI_RFBILA00_DOWN (AMANA path); SE37 test of ZFI_AMANA_PROXY; SLG1 logs",
    "5.5": "External system (Oracle HFM) - no SAP transaction",
    "5.6": "External system (Tagetik) - no SAP transaction",
    "5.7": "External system (AMANA DMS) - no SAP transaction",
    "5.8": "CDS view 2CCFICSHFLINDIFRS (Cash Flow Statement - Indirect Method for IFRS); test via report/app",
    "5.9": "Run TPM44/TPM1/TPM18 closing postings, then F.01/RFBILA00 to verify classification",
    "6.1": "Full chain: ZHFMB0 -> ZHFM01 -> ZHFM10; review final output file",
    "6.2": "Custom analytical query from 4.2 via Fiori / Analysis for Office",
    "6.3": "Working-capital report (ZC_WORKINGCAPITAL_Q001)",
    "6.4": "Z_FI_I_LOAD_IFRS16 test run; F.01 / RFBILA00 classification check",
    "6.5": "Full run of ZFI_RFBILA00_DOWN with AMANA export option",
    "6.6": "Run existing shareholder reports unchanged",
    "6.7": "OB58 (compare XHFM/XCPL/XUKV vs. ZHFM/ZCPL/ZUKV) + F.01 comparison",
    "6.8": "Fixes applied to the specific transaction/object where the defect was found",
    "7.1": "SE09 / SE10 (Transport Organizer) - customizing + workbench requests",
    "7.2": "STMS (Transport Management System) - CSD to CSQ",
    "7.3": "OB58, ZHFMB0, ZHFM01, ZHFM10, F0708/W0161, custom query, Z_FI_I_LOAD_IFRS16, ZFI_RFBILA00_DOWN",
    "7.4": "Business users execute Fiori apps/reports listed in 7.3, in CSQ",
    "7.5": "Fixes in source object + SE09/SE10/STMS re-transport",
    "7.6": "Same transactions as 7.3",
    "8.1": "STMS - CSQ to CSP",
    "8.2": "Same transactions as 7.3, executed in CSP",
    "8.3": "Email/meeting - no transaction",
    "8.4": "SM37 (monitor jobs for ZHFM01/ZHFM10/Z_FI_I_LOAD_IFRS16), SLG1, ST22",
}

headers1 = [
    "Activity ID", "Exec. Order", "Phase", "Description",
    "SAP Transaction(s) / Object(s)", "GAP Ref", "GAP Name", "Gap Type",
    "Role", "Effort (PD)", "Start Date", "End Date", "Duration (days)",
    "Dependencies", "Status",
]

GAP_TYPE_BY_REF = {
    "1": "CONFIG", "2": "CONFIG", "3": "INTERFACE, CONFIG", "4": "INTERFACE",
    "5": "REPORT", "6": "ENHANCEMENT", "7": "CONFIG", "All": "-",
    "1->2->3": "-", "1->5": "-", "1->6": "-", "1->7": "-", "1->4": "-",
    "2, 3": "-", "-": "-", "SAPNOTE": "CONFIG + ADVISORY",
}

rows1 = []
for act_id, phase, desc, gap_ref, role, effort, start_off, dur, dep in activities:
    start = d(start_off)
    end = start + timedelta(days=dur - 1)
    rows1.append([
        act_id, EXEC_ORDER.get(act_id, "-"), phase, desc,
        TRANSACTION_OBJECT.get(act_id, "-"), gap_ref,
        GAP_NAMES.get(gap_ref, gap_ref),
        GAP_TYPE_BY_REF.get(gap_ref, "-"), role, effort,
        start, end, dur, dep or "-", "Not Started",
    ])

next_row = write_table(
    ws1, 1, headers1, rows1,
    widths=[10, 9, 26, 55, 45, 9, 34, 16, 16, 11, 12, 12, 14, 12, 14],
)
for r in range(2, next_row):
    ws1.cell(row=r, column=11).number_format = "yyyy-mm-dd"
    ws1.cell(row=r, column=12).number_format = "yyyy-mm-dd"

status_col = "O"
dv = DataValidation(
    type="list",
    formula1='"Not Started,In Progress,Blocked,Complete"',
    allow_blank=False,
)
ws1.add_data_validation(dv)
dv.add(f"{status_col}2:{status_col}{next_row - 1}")

total_effort_row = next_row + 1
ws1.cell(row=total_effort_row, column=9, value="Total").font = Font(bold=True)
ws1.cell(row=total_effort_row, column=10, value=f"=SUM(J2:J{next_row - 1})").font = Font(bold=True)

ws1.freeze_panes = "C2"

# ============================================================
# Sheet 2 — Effort Summary
# ============================================================
ws2 = wb.create_sheet("Effort Summary")

by_phase = [
    ("1. Design & Preparation", "2 weeks", 20.0),
    ("2. FSV Restructuring", "3 weeks", 14.0),
    ("3. Configuration Updates", "2 weeks", 12.5),
    ("4. Development", "3 weeks", 11.0),
    ("5. Interface Validation", "3 weeks", 12.5),
    ("6. Integration Testing", "3.5 weeks", 12.5),
    ("7. QA Transport & UAT", "4 weeks", 14.5),
    ("8. Production Go-Live", "4 weeks", 8.0),
    ("Total", "~22 weeks", 105.0),
]
by_phase_start = 1
r = write_table(
    ws2, by_phase_start, ["Phase", "Calendar Duration", "Effort (PD)"], by_phase,
    widths=[32, 20, 14], banner="Effort by Phase (updated Jul 14, 2026 - was 95 PD; +10 PD for SAP Note / Treasury activities)",
)

by_role = [
    ("FI/CO Functional Consultant", 71.5, "67%"),
    ("ABAP Developer", 12, "11%"),
    ("Business Users (UAT)", 5, "5%"),
    ("Project Manager", 5, "5%"),
    ("External Teams (HFM, Tagetik, AMANA)", 6, "6%"),
    ("SAP Basis Administrator", 5, "5%"),
    ("Treasury Team", 1.5, "1%"),
    ("Total", 106, "100%"),
]
by_role_start = r + 2
r = write_table(
    ws2, by_role_start, ["Role", "Effort (PD)", "% of Total"], by_role,
    widths=[36, 14, 12], banner="Effort by Role",
)

by_gap = [
    ("1. IFRS Financial Statement Structure Definition", "CONFIG", 19, "Largest single item - 3 FSVs to restructure"),
    ("2. G/L Account to Consolidation Structure Mapping", "CONFIG", 9, "Table updates + mapping regeneration"),
    ("3. Financial Data Extraction for Group Consolidation", "INTERFACE + CONFIG", 10, "Includes HFM-side coordination"),
    ("4. Financial Statement Data Export", "INTERFACE", 7, "Fiori activation + AMANA testing"),
    ("5. Income Statement Reporting (Cost of Sales)", "REPORT", 9, "New analytical query + optional CDS extension"),
    ("6. Working Capital Balance Sheet Reporting", "ENHANCEMENT", 5, "CDS view node ID update"),
    ("7. IFRS 16 Lease Accounting Data Loading", "CONFIG", 6, "Mapping table review + Tagetik coordination"),
    ("SAP Notes & Treasury (Activities 1.7-1.11, 3.8-3.9, 5.8-5.9)", "CONFIG + ADVISORY", 10, "Not one of the original 7 GAPs - added after reviewing SAP Note 3670330 and the TRM open question"),
    ("Cross-cutting (PM, defect resolution, transports, UAT, hypercare)", "-", 30, "Shared across all GAPs"),
    ("Total", "", 105, ""),
]
by_gap_start = r + 2
r = write_table(
    ws2, by_gap_start, ["GAP", "Type", "Effort (PD)", "Notes"], by_gap,
    widths=[46, 20, 14, 40], banner="Effort by GAP",
)

by_worktype = [
    ("Configuration / Customizing (OB58, SM30, table maintenance)", 30, "29%"),
    ("Development (CDS views, analytical queries)", 8, "8%"),
    ("Testing (unit, integration, QA, UAT)", 27, "26%"),
    ("External Coordination (HFM, Tagetik, AMANA)", 8, "8%"),
    ("Project Management & Go-Live", 14, "13%"),
    ("Defect Resolution Buffer", 8, "8%"),
    ("SAP Note Implementation & Treasury Verification", 10, "10%"),
    ("Total", 105, "100%"),
]
by_worktype_start = r + 2
r = write_table(
    ws2, by_worktype_start, ["Category", "Effort (PD)", "% of Total"], by_worktype,
    widths=[46, 14, 12], banner="Effort by Work Type",
)

# ============================================================
# Sheet 3 — Milestones & Risks
# ============================================================
ws3 = wb.create_sheet("Milestones & Risks")

milestones = [
    ("2026-07-18", "SAP Note 3670330 reviewed and child notes identified (new - precedes FSV restructuring)"),
    ("2026-07-25", "Design complete - FSV node structures and HFM positions defined"),
    ("2026-08-15", "FSV restructuring complete in CSD (ZHFM, ZCPL, ZUKV)"),
    ("2026-09-05", "All configuration and development complete in CSD"),
    ("2026-09-19", "Interface validation complete (HFM, AMANA)"),
    ("2026-10-10", "Integration testing complete - all defects resolved"),
    ("2026-10-13", "Transport to CSQ"),
    ("2026-11-07", "UAT sign-off"),
    ("2026-11-10", "Transport to CSP (Production)"),
    ("2026-11-14", "Go-live verification complete"),
    ("2026-12-05", "Hypercare ends"),
    ("2027-01-01", "IFRS 18 effective - system fully operational"),
]
r = write_table(
    ws3, 1, ["Date", "Milestone"], milestones,
    widths=[16, 60], banner="Key Milestones",
)

risks = [
    ("HFM-side changes delayed (external team dependency)", "Blocks end-to-end validation of consolidation interface", "Early kick-off in Phase 1; parallel workstream with HFM team starting Aug 18"),
    ("Tagetik introduces new account codes for IFRS 18", "Additional mapping table entries needed in ZFI_IFRS16", "Coordinate with Tagetik team in Phase 1; buffer in Phase 3"),
    ("FG/FX filtering required for P&L report", "Adds CDS view extension development (2 extra PD)", "Business decision in Phase 4 activity 4.1; effort already included as optional"),
    ("ZHFM hierarchy node IDs change more extensively than expected", "More CDS view updates needed in working capital report", "Detailed node mapping in Phase 1 activity 1.2 identifies all affected nodes upfront"),
    ("Transport conflicts in CSQ/CSP", "Delays go-live", "Dedicated transport request preparation; coordinate with other project teams"),
    ("IFRS 18 updates IAS 7 - dividends paid to Investing, interest paid to Financing, interest received to Investing", "Existing cash-flow reports/CDS views built on the old flexible classification may need updates", "Add cash-flow classification check to Phase 2 unit testing (Activity 2.4); validate CDS view in Activity 5.8"),
    ("SAP's own solution approach (Note 3670330) is still evolving and doesn't cover third-party (HFM) consolidation", "Limited pre-built SAP support beyond the existing FSV/OB58 approach; HFM alignment remains fully this project's responsibility", "Read Note 3696338 (Private Cloud/On-Premise) early in Phase 1 (Activity 1.7); consider a Customer Influence Request; re-check 3670330 periodically"),
    ("R8: SAP Note 3670330 corrections not valid for the current release", "Delays Activity 1.7/3.8; may require upgrade or manual backport", "Check each note's Validity section during Activity 1.7; escalate to Basis/upgrade planning early if needed (Probability: Low)"),
    ("R9: Treasury G/L accounts not correctly classified under IFRS 18", "Misstated Operating/Investing/Financing subtotals for treasury-driven P&L items, discovered late", "Activities 1.10 and 5.9 explicitly verify this; treat confirmed TRM accounts like the ZFI_IFRS16 review in GAP 7 (Probability: Medium)"),
]
r = write_table(
    ws3, r + 2, ["Risk", "Impact", "Mitigation"], risks,
    widths=[46, 42, 46], banner="Risks",
)

assumptions = [
    ("FSV restructuring design (G/L account -> IFRS 18 category mapping) agreed by group accounting", "Phase 1 may need to be extended if not yet agreed"),
    ("CSD development system available for configuration/development throughout the project", "Delays configuration and development work if unavailable"),
    ("No other major transports to CSQ/CSP conflict with this project's transport window", "Could delay QA/production transports"),
    ("HFM, Tagetik, and AMANA teams have capacity for their respective workstreams within the timeline", "External dependency slippage is the largest schedule risk"),
    ("Pre-IFRS 18 backup FSVs (XHFM, XCPL, XUKV) remain untouched for comparison/audit", "Loss of audit trail / comparison baseline if backups are modified"),
]
write_table(
    ws3, r + 2, ["Assumption", "Impact if Invalid"], assumptions,
    widths=[60, 46], banner="Assumptions",
)

# ============================================================
# Sheet 4 — RACI Matrix
# ============================================================
ws4 = wb.create_sheet("RACI Matrix")

raci_roles = [
    "FI/CO Functional\nConsultant", "ABAP\nDeveloper", "SAP Basis",
    "Project\nManager", "Group\nAccounting", "HFM Team", "Tagetik Team",
    "AMANA Team", "Business Users",
]

# R = Responsible, A = Accountable, C = Consulted, I = Informed
raci_rows = [
    ("1. FSV Restructuring (ZHFM, ZCPL, ZUKV)", "R/A", "-", "-", "C", "I", "-", "-", "-"),
    ("2. G/L Account to HFM Structure Mapping", "R/A", "-", "-", "-", "C", "-", "-", "-"),
    ("3. Financial Data Extraction for Consolidation", "R/A", "-", "-", "-", "R", "-", "-", "-"),
    ("4. Financial Statement Data Export / AMANA", "R/A", "C", "C", "-", "-", "-", "R", "-"),
    ("5. P&L Report by Cost of Sales Method", "A", "R", "-", "-", "C", "-", "-", "C"),
    ("6. Working Capital Balance Sheet Report", "A", "R", "-", "-", "-", "-", "-", "C"),
    ("7. IFRS 16 Lease Accounting Data Loading", "R/A", "-", "-", "-", "-", "-", "R", "-"),
    ("Transport management (CSD/CSQ/CSP)", "C", "C", "R/A", "I", "-", "-", "-", "-"),
    ("QA smoke testing", "R/A", "C", "-", "I", "-", "-", "-", "-"),
    ("User acceptance testing (UAT)", "C", "-", "-", "A", "C", "-", "-", "R"),
    ("Go-live communication & hypercare", "R", "R", "C", "A", "I", "I", "I", "I"),
    ("Overall project coordination", "C", "C", "C", "R/A", "I", "I", "I", "I"),
]

r = 1
ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(raci_roles) + 1)
c = ws4.cell(row=r, column=1, value="RACI Matrix (R = Responsible, A = Accountable, C = Consulted, I = Informed)")
c.fill = BANNER_FILL
c.font = BANNER_FONT
c.alignment = WRAP_CENTER
r += 1

style_header_row(ws4, r, len(raci_roles) + 1)
ws4.cell(row=r, column=1, value="Activity / Capability")
for col, role in enumerate(raci_roles, start=2):
    ws4.cell(row=r, column=col, value=role)
    ws4.row_dimensions[r].height = 30
r += 1

for i, row_data in enumerate(raci_rows):
    for col, val in enumerate(row_data, start=1):
        cell = ws4.cell(row=r, column=col, value=val)
        cell.border = BORDER
        if col == 1:
            cell.alignment = WRAP
        else:
            cell.alignment = WRAP_CENTER
        if i % 2 == 1:
            cell.fill = STRIPE_FILL
    r += 1

autosize(ws4, [40] + [13] * len(raci_roles))

# ============================================================
# Sheet 5 — SAP Notes & References
# ============================================================
ws5 = wb.create_sheet("SAP Notes & References")

confirmed_notes = [
    ("3670330", "Financial Reporting according to IFRS 18 in SAP S/4HANA Cloud, SAP S/4HANA", "FI-GL", "v7, released 06.01.2026",
     "Central/umbrella note. Read first. Check Validity section and all child notes."),
    ("3694359", "How to Adopt IFRS 18 for Financial Reporting in S/4HANA Cloud Public Edition", "FI-GL", "Referenced by 3670330",
     "Low relevance - this landscape is not on Public Edition."),
    ("3696338", "Advisory Note on IFRS 18 Transition in S/4HANA Private Cloud, S/4HANA", "FI-GL", "Referenced by 3670330",
     "HIGH relevance - read this one next; matches this landscape's classic transactions/custom ABAP profile."),
    ("3700153", "Advisory Note on IFRS 18 Transition in SAP ERP", "FI-GL", "Referenced by 3670330",
     "Low relevance - only applicable if part of the landscape is still on classic ERP/ECC."),
]
r = write_table(
    ws5, 1, ["Note", "Title", "Component", "Validity / Status", "Relevance / Action"], confirmed_notes,
    widths=[10, 46, 12, 24, 46], banner="Confirmed SAP Notes",
)

child_note_search = [
    ("IFRS 18", "FI-GL", "Core GL changes for IFRS 18 presentation"),
    ("IFRS 18", "FI-FIO-GL-HIE", "Hierarchy/FSV enhancements for new categories"),
    ("IFRS 18", "FI-FIO-GL-REP", "Financial statement reporting updates"),
    ("IFRS 18", "FI-FIO-GL-KPI", "New semantic tags for Operating Profit, Profit before Financing"),
    ("IFRS 18", "FIN-CS", "Group Reporting / consolidation impacts"),
    ("IFRS 18", "CA-GTF-CSC-EDO", "Electronic disclosure / XBRL taxonomy updates"),
]
r = write_table(
    ws5, r + 2, ["Search Term", "Application Component", "Why"], child_note_search,
    widths=[20, 22, 46], banner="Child / Further Note Search Guide (me.sap.com/notes)",
)

sap_deliverables = [
    ("SAP Note 3670330", "Central IFRS 18 note", "Confirmed - see table above", "Review + implement via SNOTE (Activities 1.7, 3.8)"),
    ("Scope Item 1SG (Group Reporting reference content)", "Extends/restructures Consolidation CoA and Income Statement; updates Cash Flow Statement starting point to Operating Profit", "Confirmed via SAP+PwC blog (giulio_peretti, 2025-11-06)", "Reference only - this landscape uses HFM, not SAP Group Reporting (Activity 1.11)"),
    ("SAP IFRS 18 webinar series", "Technical guidance sessions, Feb/Mar 2026", "Recordings likely available", "Review recordings (Activity 1.8)"),
    ("New semantic tags (Operating Profit, Profit before Financing and Income Tax)", "KPI framework / Cash Flow Statement app support", "Not yet confirmed for this release", "Verify during Activity 3.9"),
    ("Cash Flow Statement CDS view 2CCFICSHFLINDIFRS", "Indirect method CFS for IFRS", "Available in current release; update status not yet confirmed", "Validate during Activity 5.8"),
]
r = write_table(
    ws5, r + 2, ["Deliverable", "Description", "Status", "Action / Activity Reference"], sap_deliverables,
    widths=[40, 46, 34, 36], banner="SAP Content Deliverables Tracker",
)

blog_references = [
    ("IFRS 18 Explained: What SAP S/4HANA Customers Need to Know Before 2027", "Praveenirrinki (SAP)", "2025-12-02", "SAP Community - Financial Management Blog Posts by SAP",
     "General IFRS 18 background; confirms Note 3670330; links SAP webinar series (Feb/Mar 2026)"),
    ("IFRS 18 and SAP S/4HANA Group Reporting: What It Means and How to Get Ahead", "giulio_peretti, co-authored with PwC", "2025-11-06", "SAP Community - Financial Management Blog Posts by Members",
     "Detailed SAP Group Reporting IFRS 18 capabilities; Scope Item 1SG update; PwC implementation approach"),
    ("Unlocking the Value of SAP TRM for Corporate Treasury", "mezeshan", "2026 (exact date not captured)", "SAP Community - Financial Management Blog Posts by Members",
     "General TRM tips; item #15 corroborates Note 3670330; links a treasury-specific IFRS 18 blog (URL truncated, not yet reviewed)"),
]
r = write_table(
    ws5, r + 2, ["Blog Title", "Author", "Date", "Platform", "Key Takeaway"], blog_references,
    widths=[42, 26, 16, 34, 50], banner="External Source References",
)

treasury_gl_checklist = [
    ("Interest expense on borrowings", "Financing", "Not confirmed - depends on whether SAP TRM is in use", "Verify in Activity 1.10"),
    ("Interest income on deposits", "Investing", "Not confirmed - depends on whether SAP TRM is in use", "Verify in Activity 1.10"),
    ("Dividend income", "Investing", "Not confirmed - depends on whether SAP TRM is in use", "Verify in Activity 1.10"),
    ("FX gains/losses on financial instruments", "Depends on underlying instrument's category", "Not confirmed - review operating vs. financing FX", "Verify in Activity 1.10"),
    ("Fair value gains/losses on derivatives", "Depends on hedge designation", "Not confirmed - review hedge accounting treatment", "Verify in Activity 1.10"),
    ("Depreciation of RoU assets (IFRS 16)", "Operating", "Confirmed in GAP 7 (accounts 670000/670002/670005/670006)", "Already covered by Activity 3.4"),
    ("Interest on lease liabilities (IFRS 16)", "Financing", "Confirmed in GAP 7 (accounts 661300/661302/661305/661306)", "Already covered by Activity 3.4"),
    ("Other lease expenses (IFRS 16)", "To be verified", "Confirmed in GAP 7 (accounts 671110-671306)", "Already covered by Activity 3.4"),
    ("Amortization (bond/security premium or discount)", "Depends on instrument", "Not confirmed - depends on whether SAP TRM is in use", "Verify in Activity 1.10"),
    ("Current portion reclassification (loans)", "Balance sheet only - not a P&L category", "N/A - reclassification is BS, not P&L", "No P&L category action needed"),
    ("Impairment losses/reversals (financial instruments)", "Operating or Financing, depending on policy", "Not confirmed - depends on whether SAP TRM is in use", "Verify in Activity 1.10"),
]
write_table(
    ws5, r + 2,
    ["Treasury Posting Type", "IFRS 18 Category", "Confirmation Status", "Next Step"],
    treasury_gl_checklist,
    widths=[42, 40, 46, 30], banner="Treasury G/L Account Classification Checklist",
)

# ============================================================
# Sheet 0 — Dashboard (visual overview, placed as the first tab)
# ============================================================
ws0 = wb.create_sheet("Dashboard", 0)
ws0.sheet_view.showGridLines = False

title_cell = ws0.cell(row=1, column=1, value="IFRS 18 Adoption — Project Plan Dashboard")
title_cell.font = Font(bold=True, size=18, color="1F3B73")
ws0.cell(row=2, column=1, value="288 - IFRS 18  |  Updated Jul 14, 2026").font = Font(
    size=10.5, italic=True, color="666666"
)

# ---- KPI summary cards --------------------------------------------------
kpis = [
    ("TOTAL EFFORT", "~105 PD", "was ~95 PD before SAP Note + Treasury review"),
    ("DURATION", "~22 weeks", "mid-July to early December 2026"),
    ("ACTIVITIES", "60", "across 8 phases"),
    ("GO-LIVE TARGET", "10 Nov 2026", "ahead of the 1 Jan 2027 effective date"),
]
kpi_col_width = 4
kpi_start_col = 1
kpi_row = 4
for i, (label, value, sub) in enumerate(kpis):
    col = kpi_start_col + i * kpi_col_width
    ws0.merge_cells(start_row=kpi_row, start_column=col, end_row=kpi_row, end_column=col + kpi_col_width - 2)
    ws0.merge_cells(start_row=kpi_row + 1, start_column=col, end_row=kpi_row + 1, end_column=col + kpi_col_width - 2)
    ws0.merge_cells(start_row=kpi_row + 2, start_column=col, end_row=kpi_row + 2, end_column=col + kpi_col_width - 2)
    label_cell = ws0.cell(row=kpi_row, column=col, value=label)
    label_cell.font = Font(bold=True, size=9.5, color="FFFFFF")
    label_cell.fill = PatternFill("solid", fgColor="8EA9DB")
    label_cell.alignment = WRAP_CENTER
    value_cell = ws0.cell(row=kpi_row + 1, column=col, value=value)
    value_cell.font = Font(bold=True, size=20, color="1F3B73")
    value_cell.fill = PatternFill("solid", fgColor="F2F2F2")
    value_cell.alignment = WRAP_CENTER
    sub_cell = ws0.cell(row=kpi_row + 2, column=col, value=sub)
    sub_cell.font = Font(size=8.5, italic=True, color="666666")
    sub_cell.fill = PatternFill("solid", fgColor="F2F2F2")
    sub_cell.alignment = WRAP_CENTER
    for rr in (kpi_row, kpi_row + 1, kpi_row + 2):
        for cc in range(col, col + kpi_col_width - 1):
            ws0.cell(row=rr, column=cc).border = BORDER
    ws0.row_dimensions[kpi_row + 1].height = 34

# ---- Embedded Gantt chart image -----------------------------------------
gantt_row = kpi_row + 5
ws0.cell(row=gantt_row, column=1, value="Project Timeline").font = Font(
    bold=True, size=12, color="1F3B73"
)
gantt_image_path = "IFRS18-Project-Timeline.png"
if os.path.exists(gantt_image_path):
    img = XLImage(gantt_image_path)
    img.width = 920
    img.height = 460
    ws0.add_image(img, f"A{gantt_row + 1}")
    chart_area_rows = 24
else:
    ws0.cell(
        row=gantt_row + 1, column=1,
        value=(
            "Gantt chart image not found - run 'python3 generate_gantt_chart.py' "
            "before this script to include it here."
        ),
    ).font = Font(italic=True, color="C00000")
    chart_area_rows = 2

# ---- Native Excel charts: Effort by Phase / Role / Work Type ------------
charts_row = gantt_row + 1 + chart_area_rows + 1
ws0.cell(row=charts_row, column=1, value="Effort Breakdown").font = Font(
    bold=True, size=12, color="1F3B73"
)

phase_chart = BarChart()
phase_chart.type = "bar"  # horizontal - avoids rotated/clipped category labels
phase_chart.title = "Effort by Phase (PD)"
phase_chart.style = 10
phase_chart.height = 9
phase_chart.width = 16
phase_chart.gapWidth = 40
phase_n = len(by_phase) - 1  # exclude "Total" row
phase_cats = Reference(ws2, min_col=1, min_row=by_phase_start + 2, max_row=by_phase_start + 1 + phase_n)
phase_vals = Reference(ws2, min_col=3, min_row=by_phase_start + 1, max_row=by_phase_start + 1 + phase_n)
phase_chart.add_data(phase_vals, titles_from_data=True)
phase_chart.set_categories(phase_cats)
phase_chart.legend = None
phase_chart.dataLabels = DataLabelList()
phase_chart.dataLabels.showVal = True
phase_chart.dataLabels.showCatName = False
phase_chart.dataLabels.showSerName = False
phase_chart.dataLabels.showLegendKey = False
phase_chart.dataLabels.numFmt = "0.#"
phase_chart.y_axis.delete = False
phase_chart.x_axis.delete = False
ws0.add_chart(phase_chart, f"A{charts_row + 1}")

role_chart = BarChart()
role_chart.type = "bar"
role_chart.title = "Effort by Role (PD)"
role_chart.style = 11
role_chart.height = 9
role_chart.width = 16
role_chart.gapWidth = 40
role_n = len(by_role) - 1
role_cats = Reference(ws2, min_col=1, min_row=by_role_start + 2, max_row=by_role_start + 1 + role_n)
role_vals = Reference(ws2, min_col=2, min_row=by_role_start + 1, max_row=by_role_start + 1 + role_n)
role_chart.add_data(role_vals, titles_from_data=True)
role_chart.set_categories(role_cats)
role_chart.legend = None
role_chart.dataLabels = DataLabelList()
role_chart.dataLabels.showVal = True
role_chart.dataLabels.showCatName = False
role_chart.dataLabels.showSerName = False
role_chart.dataLabels.showLegendKey = False
role_chart.dataLabels.numFmt = "0.#"
role_chart.y_axis.delete = False
role_chart.x_axis.delete = False
ws0.add_chart(role_chart, f"L{charts_row + 1}")

worktype_chart = PieChart()
worktype_chart.title = "Effort by Work Type"
worktype_chart.style = 10
worktype_chart.height = 9
worktype_chart.width = 18
wt_n = len(by_worktype) - 1
wt_cats = Reference(ws2, min_col=1, min_row=by_worktype_start + 2, max_row=by_worktype_start + 1 + wt_n)
wt_vals = Reference(ws2, min_col=2, min_row=by_worktype_start + 1, max_row=by_worktype_start + 1 + wt_n)
worktype_chart.add_data(wt_vals, titles_from_data=True)
worktype_chart.set_categories(wt_cats)
worktype_chart.dataLabels = DataLabelList()
worktype_chart.dataLabels.showPercent = True
worktype_chart.dataLabels.showCatName = False
worktype_chart.dataLabels.showSerName = False
worktype_chart.dataLabels.showVal = False
worktype_chart.dataLabels.showLegendKey = False
worktype_chart.dataLabels.numFmt = "0%"
worktype_chart.legend.position = "b"
worktype_chart.legend.overlay = False
ws0.add_chart(worktype_chart, f"W{charts_row + 1}")

autosize(ws0, [16] * 40)
ws0.column_dimensions["A"].width = 16

# ============================================================
# Page setup for all sheets
# ============================================================
for ws in (ws0, ws1, ws2, ws3, ws4, ws5):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.save("IFRS18_Adoption_Project_Plan.xlsx")
print("Saved IFRS18_Adoption_Project_Plan.xlsx")
