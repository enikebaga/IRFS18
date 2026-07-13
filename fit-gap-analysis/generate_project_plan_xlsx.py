"""
Generates 'IFRS18_Adoption_Project_Plan.xlsx' — an editable/trackable
Excel version of the IFRS 18 SAP adoption project plan described in
IFRS18-Project-Plan.md.

Usage:
    pip install openpyxl
    python3 generate_project_plan_xlsx.py

Sheets produced:
    1. Project Plan       - 44 activities across 8 phases, with dates,
                             dependencies, and a Status column for tracking.
    2. Effort Summary      - effort by phase / by role / by GAP / by work type.
    3. Milestones & Risks  - key milestones, risks, assumptions, critical path.
    4. RACI Matrix         - responsibility assignment across 9 roles.
"""

from datetime import date, timedelta

from openpyxl import Workbook
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
}

activities = [
    ("1.1", "1 - Design & Preparation", "Finalize IFRS 18 P&L category design with group accounting team (Operating/Investing/Financing boundaries, subtotal definitions)", "All", "FC + Accounting", 3, 0, 5, None),
    ("1.2", "1 - Design & Preparation", "Define new FSV hierarchy node structure for ZHFM, ZCPL, ZUKV (node IDs, parent-child relationships, G/L account assignments)", "1", "FC", 5, 0, 8, None),
    ("1.3", "1 - Design & Preparation", "Define new HFM structure positions and attribute flags (consolidation method, functional area, intercompany, movement type, region, sign reversal)", "2, 3", "FC", 3, 5, 5, "1.1"),
    ("1.4", "1 - Design & Preparation", "Kick-off coordination with HFM team (new structure positions, receiving format)", "3", "FC + HFM", 1, 7, 3, None),
    ("1.5", "1 - Design & Preparation", "Kick-off coordination with Tagetik team (account code alignment)", "7", "FC + Tagetik", 1, 7, 3, None),
    ("1.6", "1 - Design & Preparation", "Kick-off coordination with AMANA team (new category handling)", "4", "FC + AMANA", 0.5, 7, 3, None),

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

headers1 = [
    "Activity ID", "Phase", "Description", "GAP Ref", "GAP Name", "Gap Type",
    "Role", "Effort (PD)", "Start Date", "End Date", "Duration (days)",
    "Dependencies", "Status",
]

GAP_TYPE_BY_REF = {
    "1": "CONFIG", "2": "CONFIG", "3": "INTERFACE, CONFIG", "4": "INTERFACE",
    "5": "REPORT", "6": "ENHANCEMENT", "7": "CONFIG", "All": "-",
    "1->2->3": "-", "1->5": "-", "1->6": "-", "1->7": "-", "1->4": "-",
    "2, 3": "-", "-": "-",
}

rows1 = []
for act_id, phase, desc, gap_ref, role, effort, start_off, dur, dep in activities:
    start = d(start_off)
    end = start + timedelta(days=dur - 1)
    rows1.append([
        act_id, phase, desc, gap_ref, GAP_NAMES.get(gap_ref, gap_ref),
        GAP_TYPE_BY_REF.get(gap_ref, "-"), role, effort,
        start, end, dur, dep or "-", "Not Started",
    ])

next_row = write_table(
    ws1, 1, headers1, rows1,
    widths=[10, 26, 60, 9, 34, 16, 16, 11, 12, 12, 14, 12, 14],
)
for r in range(2, next_row):
    ws1.cell(row=r, column=9).number_format = "yyyy-mm-dd"
    ws1.cell(row=r, column=10).number_format = "yyyy-mm-dd"

status_col = "M"
dv = DataValidation(
    type="list",
    formula1='"Not Started,In Progress,Blocked,Complete"',
    allow_blank=False,
)
ws1.add_data_validation(dv)
dv.add(f"{status_col}2:{status_col}{next_row - 1}")

total_effort_row = next_row + 1
ws1.cell(row=total_effort_row, column=7, value="Total").font = Font(bold=True)
ws1.cell(row=total_effort_row, column=8, value=f"=SUM(H2:H{next_row - 1})").font = Font(bold=True)

ws1.freeze_panes = "A2"

# ============================================================
# Sheet 2 — Effort Summary
# ============================================================
ws2 = wb.create_sheet("Effort Summary")

by_phase = [
    ("1. Design & Preparation", "2 weeks", 13.5),
    ("2. FSV Restructuring", "3 weeks", 14.0),
    ("3. Configuration Updates", "2 weeks", 10.5),
    ("4. Development", "3 weeks", 11.0),
    ("5. Interface Validation", "3 weeks", 11.0),
    ("6. Integration Testing", "3.5 weeks", 12.5),
    ("7. QA Transport & UAT", "4 weeks", 14.5),
    ("8. Production Go-Live", "4 weeks", 8.0),
    ("Total", "~22 weeks", 95.0),
]
r = write_table(
    ws2, 1, ["Phase", "Calendar Duration", "Effort (PD)"], by_phase,
    widths=[32, 20, 14], banner="Effort by Phase",
)

by_role = [
    ("FI/CO Functional Consultant", 65, "68%"),
    ("ABAP Developer", 12, "13%"),
    ("Business Users (UAT)", 5, "5%"),
    ("Project Manager", 5, "5%"),
    ("External Teams (HFM, Tagetik, AMANA)", 6, "6%"),
    ("SAP Basis Administrator", 3, "3%"),
    ("Total", 96, "100%"),
]
r = write_table(
    ws2, r + 2, ["Role", "Effort (PD)", "% of Total"], by_role,
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
    ("Cross-cutting (PM, defect resolution, transports, UAT, hypercare)", "-", 30, "Shared across all GAPs"),
    ("Total", "", 95, ""),
]
r = write_table(
    ws2, r + 2, ["GAP", "Type", "Effort (PD)", "Notes"], by_gap,
    widths=[46, 20, 14, 40], banner="Effort by GAP",
)

by_worktype = [
    ("Configuration / Customizing (OB58, SM30, table maintenance)", 30, "32%"),
    ("Development (CDS views, analytical queries)", 8, "8%"),
    ("Testing (unit, integration, QA, UAT)", 27, "28%"),
    ("External Coordination (HFM, Tagetik, AMANA)", 8, "8%"),
    ("Project Management & Go-Live", 14, "15%"),
    ("Defect Resolution Buffer", 8, "9%"),
    ("Total", 95, "100%"),
]
write_table(
    ws2, r + 2, ["Category", "Effort (PD)", "% of Total"], by_worktype,
    widths=[46, 14, 12], banner="Effort by Work Type",
)

# ============================================================
# Sheet 3 — Milestones & Risks
# ============================================================
ws3 = wb.create_sheet("Milestones & Risks")

milestones = [
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

for ws in (ws1, ws2, ws3, ws4):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.save("IFRS18_Adoption_Project_Plan.xlsx")
print("Saved IFRS18_Adoption_Project_Plan.xlsx")
