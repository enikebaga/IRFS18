"""
Generates 'IFRS18-Project-Plan-Overview.pptx' — a polished, presentation-
ready executive summary of the IFRS 18 SAP adoption project plan
(IFRS18-Project-Plan.md), for sharing with stakeholders who want a
visual deck rather than a spreadsheet.

Usage:
    pip install python-pptx
    python3 generate_gantt_chart.py            # produces the Gantt PNG first
    python3 generate_project_plan_pptx.py

Uses the same brand palette as demand-charter/generate_charter_pptx.py
for visual consistency across all IFRS 18 deliverables.
"""

import os

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

DARK_BLUE = RGBColor(0x1F, 0x3B, 0x73)
HEADER_BLUE = RGBColor(0x8E, 0xA9, 0xDB)
LIGHT_GRAY = RGBColor(0xCF, 0xD3, 0xDA)
ORANGE = RGBColor(0xF4, 0xB1, 0x83)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
GRAY_TEXT = RGBColor(0x66, 0x66, 0x66)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def add_box(slide, left, top, width, height, fill_color=None, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    if fill_color is not None:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color is not None:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(0.75)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def set_text(shape, text, size=11, bold=False, color=BLACK, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, font_name="Calibri", italic=False):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(6)
    tf.margin_right = Pt(6)
    tf.margin_top = Pt(4)
    tf.margin_bottom = Pt(4)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
        run.font.name = font_name


def add_bullets(shape, items, size=12, color=BLACK, font_name="Calibri", space_after=6):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(6)
    tf.margin_right = Pt(6)
    tf.margin_top = Pt(4)
    tf.margin_bottom = Pt(4)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = f"\u2022 {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = font_name
        p.space_after = Pt(space_after)


def add_kpi_card(slide, left, top, width, height, label, value, sub=None):
    box = add_box(slide, left, top, width, height, fill_color=RGBColor(0xF2, 0xF2, 0xF2))
    label_box = slide.shapes.add_textbox(left, top + Pt(4), width, Pt(18))
    set_text(label_box, label, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    label_bg = add_box(slide, left, top, width, Pt(20), fill_color=HEADER_BLUE)
    label_bg2 = slide.shapes.add_textbox(left, top + Pt(1), width, Pt(18))
    set_text(label_bg2, label, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    value_box = slide.shapes.add_textbox(left, top + Pt(24), width, height - Pt(24) - (Pt(16) if sub else 0))
    set_text(value_box, value, size=22, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    if sub:
        sub_box = slide.shapes.add_textbox(left, top + height - Pt(16), width, Pt(15))
        set_text(sub_box, sub, size=8, italic=True, color=GRAY_TEXT, align=PP_ALIGN.CENTER)


def add_footer(slide, page_label):
    footer = slide.shapes.add_textbox(Inches(10.8), Inches(7.15), Inches(2.3), Inches(0.3))
    set_text(footer, "INNOVATING TOGETHER", size=9, bold=True, color=DARK_BLUE, align=PP_ALIGN.RIGHT)
    pg = slide.shapes.add_textbox(Inches(0.3), Inches(7.15), Inches(3), Inches(0.3))
    set_text(pg, page_label, size=8.5, color=GRAY_TEXT)


def add_title_bar(slide, title):
    bar = add_box(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.85), fill_color=DARK_BLUE)
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.12), Inches(12), Inches(0.6))
    set_text(tb, title, size=24, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)


prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
blank_layout = prs.slide_layouts[6]

# ============================================================
# Slide 1 — Title & KPI summary
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=WHITE)
add_box(slide, Inches(0), Inches(0), SLIDE_W, Inches(2.6), fill_color=DARK_BLUE)

tb = slide.shapes.add_textbox(Inches(0.7), Inches(0.8), Inches(11.9), Inches(0.9))
set_text(tb, "IFRS 18 Adoption", size=40, bold=True, color=WHITE)
tb2 = slide.shapes.add_textbox(Inches(0.7), Inches(1.6), Inches(11.9), Inches(0.6))
set_text(tb2, "SAP Implementation Project Plan — Executive Summary", size=18, color=HEADER_BLUE)
tb3 = slide.shapes.add_textbox(Inches(0.7), Inches(2.15), Inches(11.9), Inches(0.4))
set_text(tb3, "Demand 288 - IFRS 18  |  Updated Jul 14, 2026", size=11, italic=True, color=LIGHT_GRAY)

kpis = [
    ("TOTAL EFFORT", "~105 PD", "was ~95 PD before SAP Note review"),
    ("DURATION", "~22 weeks", "mid-Jul to early Dec 2026"),
    ("ACTIVITIES", "60", "across 8 phases"),
    ("GO-LIVE TARGET", "10 Nov 2026", "ahead of 1 Jan 2027 effective date"),
]
card_w = Inches(2.75)
gap = Inches(0.25)
total_w = card_w * 4 + gap * 3
start_x = (SLIDE_W - total_w) / 2
for i, (label, value, sub) in enumerate(kpis):
    add_kpi_card(slide, start_x + i * (card_w + gap), Inches(3.3), card_w, Inches(1.5), label, value, sub)

body = slide.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.6))
add_bullets(body, [
    "Restructure the Financial Statement Versions (ZHFM, ZCPL, ZUKV) for the new IFRS 18 "
    "categories and subtotals — the foundation all other work depends on.",
    "Update HFM consolidation mapping, financial statement export/AMANA, P&L and working "
    "capital reporting, and IFRS 16 lease data classification.",
    "New this update: review/implement SAP Note 3670330 and verify treasury (TRM) G/L "
    "account classification.",
], size=13, color=RGBColor(0x33, 0x33, 0x33), space_after=8)

add_footer(slide, "1 / 5")

# ============================================================
# Slide 2 — Timeline
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=WHITE)
add_title_bar(slide, "Project Timeline")

gantt_path = "IFRS18-Project-Timeline.png"
if os.path.exists(gantt_path):
    slide.shapes.add_picture(gantt_path, Inches(0.4), Inches(1.05), width=Inches(12.5))
else:
    tb = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(10), Inches(1))
    set_text(tb, "Gantt chart image not found - run generate_gantt_chart.py first.",
             size=14, color=RGBColor(0xC0, 0x00, 0x00))
add_footer(slide, "2 / 5")

# ============================================================
# Slide 3 — Effort Breakdown (3 native charts)
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=WHITE)
add_title_bar(slide, "Effort Breakdown")

phase_labels = [
    "1. Design & Prep", "2. FSV Restructuring", "3. Config Updates", "4. Development",
    "5. Interface Validation", "6. Integration Testing", "7. QA Transport & UAT",
    "8. Production Go-Live",
]
phase_values = [20.0, 14.0, 12.5, 11.0, 12.5, 12.5, 14.5, 8.0]

chart_data = CategoryChartData()
chart_data.categories = phase_labels
chart_data.add_series("Effort (PD)", phase_values)
gframe = slide.shapes.add_chart(
    XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.3), Inches(1.05), Inches(6.3), Inches(3.55), chart_data
)
chart = gframe.chart
chart.has_legend = False
chart.has_title = True
chart.chart_title.text_frame.text = "Effort by Phase (PD)"
chart.chart_title.text_frame.paragraphs[0].font.size = Pt(14)
chart.category_axis.tick_labels.font.size = Pt(9)
chart.value_axis.tick_labels.font.size = Pt(9)
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = "0.#"
plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(9)
plot.series[0].format.fill.solid()
plot.series[0].format.fill.fore_color.rgb = DARK_BLUE

role_labels = [
    "FI/CO Functional Consultant", "ABAP Developer", "Business Users (UAT)",
    "Project Manager", "External Teams (HFM, Tagetik, AMANA)",
    "SAP Basis Administrator", "Treasury Team",
]
role_values = [71.5, 12, 5, 5, 6, 5, 1.5]

chart_data2 = CategoryChartData()
chart_data2.categories = role_labels
chart_data2.add_series("Effort (PD)", role_values)
gframe2 = slide.shapes.add_chart(
    XL_CHART_TYPE.BAR_CLUSTERED, Inches(6.75), Inches(1.05), Inches(6.25), Inches(3.55), chart_data2
)
chart2 = gframe2.chart
chart2.has_legend = False
chart2.has_title = True
chart2.chart_title.text_frame.text = "Effort by Role (PD)"
chart2.chart_title.text_frame.paragraphs[0].font.size = Pt(14)
chart2.category_axis.tick_labels.font.size = Pt(9)
chart2.value_axis.tick_labels.font.size = Pt(9)
plot2 = chart2.plots[0]
plot2.has_data_labels = True
plot2.data_labels.number_format = "0.#"
plot2.data_labels.number_format_is_linked = False
plot2.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot2.data_labels.font.size = Pt(9)
plot2.series[0].format.fill.solid()
plot2.series[0].format.fill.fore_color.rgb = HEADER_BLUE

worktype_labels = [
    "Configuration / Customizing", "Development", "Testing", "External Coordination",
    "Project Management & Go-Live", "Defect Resolution Buffer",
    "SAP Note & Treasury Verification",
]
worktype_values = [30, 8, 27, 8, 14, 8, 10]

chart_data3 = CategoryChartData()
chart_data3.categories = worktype_labels
chart_data3.add_series("Effort (PD)", worktype_values)
gframe3 = slide.shapes.add_chart(
    XL_CHART_TYPE.PIE, Inches(3.6), Inches(4.75), Inches(6.1), Inches(2.55), chart_data3
)
chart3 = gframe3.chart
chart3.has_title = True
chart3.chart_title.text_frame.text = "Effort by Work Type"
chart3.chart_title.text_frame.paragraphs[0].font.size = Pt(14)
chart3.has_legend = True
chart3.legend.position = XL_LEGEND_POSITION.RIGHT
chart3.legend.include_in_layout = False
chart3.legend.font.size = Pt(8.5)
plot3 = chart3.plots[0]
plot3.has_data_labels = True
plot3.data_labels.show_percentage = True
plot3.data_labels.show_category_name = False
plot3.data_labels.show_value = False
plot3.data_labels.number_format = "0%"
plot3.data_labels.number_format_is_linked = False
plot3.data_labels.font.size = Pt(9)

add_footer(slide, "3 / 5")

# ============================================================
# Slide 4 — Key Milestones
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=WHITE)
add_title_bar(slide, "Key Milestones")

milestones = [
    ("Jul 18, 2026", "SAP Note 3670330 reviewed and child notes identified", True),
    ("Jul 25, 2026", "Design complete — FSV node structures and HFM positions defined", False),
    ("Aug 15, 2026", "FSV restructuring complete in CSD (ZHFM, ZCPL, ZUKV)", False),
    ("Sep 5, 2026", "All configuration and development complete in CSD", False),
    ("Sep 19, 2026", "Interface validation complete (HFM, AMANA)", False),
    ("Oct 10, 2026", "Integration testing complete — all defects resolved", False),
    ("Oct 13, 2026", "Transport to CSQ", False),
    ("Nov 7, 2026", "UAT sign-off", False),
    ("Nov 10, 2026", "Transport to CSP (Production)", False),
    ("Dec 5, 2026", "Hypercare ends", False),
    ("Jan 1, 2027", "IFRS 18 effective — system fully operational", False),
]

rows = len(milestones) + 1
table_shape = slide.shapes.add_table(rows, 2, Inches(1.0), Inches(1.1), Inches(11.3), Inches(5.9))
table = table_shape.table
table.columns[0].width = Inches(2.2)
table.columns[1].width = Inches(9.1)
hdr0, hdr1 = table.cell(0, 0), table.cell(0, 1)
hdr0.text, hdr1.text = "Date", "Milestone"
for cell in (hdr0, hdr1):
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK_BLUE
    para = cell.text_frame.paragraphs[0]
    para.font.bold = True
    para.font.color.rgb = WHITE
    para.font.size = Pt(13)

for i, (d, m, is_new) in enumerate(milestones, start=1):
    c0, c1 = table.cell(i, 0), table.cell(i, 1)
    c0.text, c1.text = d, m + (" (NEW)" if is_new else "")
    fill_color = ORANGE if is_new else (RGBColor(0xF2, 0xF2, 0xF2) if i % 2 == 0 else WHITE)
    for cell in (c0, c1):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill_color
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = is_new

add_footer(slide, "4 / 5")

# ============================================================
# Slide 5 — Top Risks & Next Steps
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_box(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=WHITE)
add_title_bar(slide, "Top Risks & Next Steps")

h1 = add_box(slide, Inches(0.4), Inches(1.05), Inches(6.3), Inches(0.4), fill_color=HEADER_BLUE)
set_text(h1, "Top Risks", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
risk_body = add_box(slide, Inches(0.4), Inches(1.45), Inches(6.3), Inches(5.5), fill_color=LIGHT_GRAY)
add_bullets(risk_body, [
    "HFM-side changes delayed (external team dependency) — blocks end-to-end "
    "validation of the consolidation interface.",
    "SAP's own solution approach (Note 3670330) doesn't cover third-party (HFM) "
    "consolidation — HFM alignment remains fully this project's responsibility.",
    "R8: SAP Note 3670330 corrections may not be valid for the current release — "
    "could require an upgrade or manual backport.",
    "R9: Treasury G/L accounts may not be correctly classified under IFRS 18 if "
    "SAP TRM is in use — now addressed by Activities 1.10 and 5.9.",
    "IAS 7 cash-flow reclassification (dividends/interest) may affect existing "
    "cash-flow CDS views — checked in Activity 5.8.",
    "Transport conflicts in CSQ/CSP could delay go-live.",
], size=12, color=RGBColor(0x22, 0x22, 0x22), space_after=10)

h2 = add_box(slide, Inches(7.0), Inches(1.05), Inches(5.9), Inches(0.4), fill_color=HEADER_BLUE)
set_text(h2, "Next Steps", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
next_body = add_box(slide, Inches(7.0), Inches(1.45), Inches(5.9), Inches(5.5), fill_color=LIGHT_GRAY)
add_bullets(next_body, [
    "Kick off Phase 1 (Activities 1.1-1.11): design workshop, FSV/HFM structure "
    "definition, SAP Note review, and treasury G/L account review.",
    "Read SAP Note 3696338 (Private Cloud/On-Premise advisory) — the most "
    "relevant of the confirmed companion notes for this landscape.",
    "Confirm whether SAP TRM is in use for loans/deposits/FX/derivatives with "
    "Finance/Treasury (Activity 1.10).",
    "Consider raising a Customer Influence Request with SAP, per their own "
    "recommendation in Note 3670330.",
    "Get sign-off on the restructured FSVs (Activity 2.5) before starting "
    "downstream configuration/development work (Exec. Order 8+).",
], size=12, color=RGBColor(0x22, 0x22, 0x22), space_after=10)

add_footer(slide, "5 / 5")

out_path = "IFRS18-Project-Plan-Overview.pptx"
prs.save(out_path)
print(f"Saved {out_path}")
