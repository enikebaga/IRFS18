"""
Generates 'IFRS18-Project-Timeline.png' — a professional, rendered Gantt
chart for the IFRS 18 SAP adoption project plan (IFRS18-Project-Plan.md),
replacing the plain-text mermaid diagram with a proper visual.

Usage:
    pip install matplotlib
    python3 generate_gantt_chart.py

Phase date ranges and milestones are kept in sync by hand with
IFRS18-Project-Plan.md — if the plan's dates change, update PHASES and
MILESTONES below to match.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import date

# ---- Brand palette (matches demand-charter/ and fit-gap-analysis/ docs) ---
DARK_BLUE = "#1F3B73"
HEADER_BLUE = "#8EA9DB"
ORANGE = "#F4B183"
LIGHT_GRAY = "#CFD3DA"
GRID_GRAY = "#E4E7EB"

# Phase-level bars: (label, start_date, end_date, effort_pd, color)
PHASES = [
    ("1. Design & Preparation", date(2026, 7, 14), date(2026, 7, 25), 20.0, DARK_BLUE),
    ("2. FSV Restructuring", date(2026, 7, 28), date(2026, 8, 15), 14.0, HEADER_BLUE),
    ("3. Configuration Updates", date(2026, 8, 18), date(2026, 8, 29), 12.5, DARK_BLUE),
    ("4. Development", date(2026, 8, 18), date(2026, 9, 5), 11.0, HEADER_BLUE),
    ("5. Interface Validation", date(2026, 9, 1), date(2026, 9, 19), 12.5, DARK_BLUE),
    ("6. Integration Testing", date(2026, 9, 15), date(2026, 10, 10), 12.5, HEADER_BLUE),
    ("7. QA Transport & UAT", date(2026, 10, 13), date(2026, 11, 7), 14.5, DARK_BLUE),
    ("8. Production Go-Live", date(2026, 11, 10), date(2026, 12, 5), 8.0, HEADER_BLUE),
]

# Milestones: (label, date)
MILESTONES = [
    ("SAP Note 3670330\nreviewed", date(2026, 7, 18)),
    ("Design complete", date(2026, 7, 25)),
    ("FSV restructuring\ncomplete", date(2026, 8, 15)),
    ("Config & dev\ncomplete", date(2026, 9, 5)),
    ("Interface validation\ncomplete", date(2026, 9, 19)),
    ("Integration testing\ncomplete", date(2026, 10, 10)),
    ("Transport to CSQ", date(2026, 10, 13)),
    ("UAT sign-off", date(2026, 11, 7)),
    ("Transport to CSP", date(2026, 11, 10)),
    ("Hypercare ends", date(2026, 12, 5)),
]

EFFECTIVE_DATE = date(2027, 1, 1)

fig, ax = plt.subplots(figsize=(14, 6.5), dpi=160)
fig.patch.set_facecolor("white")

y_positions = list(range(len(PHASES), 0, -1))

for (label, start, end, effort, color), y in zip(PHASES, y_positions):
    duration = (end - start).days + 1
    ax.barh(
        y, duration, left=start, height=0.55,
        color=color, edgecolor="white", linewidth=1.2, zorder=3,
    )
    # Effort label just to the right of the bar
    ax.text(
        mdates.date2num(end) + 1.5, y, f"{effort:g} PD",
        va="center", ha="left", fontsize=9, color="#333333", zorder=4,
    )

ax.set_yticks(y_positions)
ax.set_yticklabels([p[0] for p in PHASES], fontsize=10.5)
ax.set_ylim(0.3, len(PHASES) + 0.7)

# Milestones as diamond markers on a thin horizontal lane above the phases
milestone_y = len(PHASES) + 0.35
for label, d in MILESTONES:
    ax.plot(d, milestone_y, marker="D", markersize=7, color=ORANGE,
            markeredgecolor=DARK_BLUE, markeredgewidth=0.8, zorder=5, clip_on=False)

# IFRS 18 effective date reference line
ax.axvline(EFFECTIVE_DATE, color="#C00000", linestyle="--", linewidth=1.3, zorder=2)
ax.text(
    EFFECTIVE_DATE, len(PHASES) + 0.85, "IFRS 18 effective\n1 Jan 2027",
    color="#C00000", fontsize=9, ha="center", va="bottom", fontweight="bold",
)

# Gridlines and axis formatting
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.grid(axis="x", color=GRID_GRAY, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#999999")
ax.tick_params(axis="x", labelsize=9.5)
ax.set_xlim(date(2026, 7, 8), date(2027, 1, 12))

ax.set_title(
    "IFRS 18 Adoption — SAP Implementation Timeline",
    fontsize=15, fontweight="bold", color=DARK_BLUE, pad=34, loc="left",
)

legend_elements = [
    Line2D([0], [0], marker="D", color="none", markerfacecolor=ORANGE,
           markeredgecolor=DARK_BLUE, markersize=8, label="Milestone"),
    Line2D([0], [0], color="#C00000", linestyle="--", linewidth=1.3,
           label="IFRS 18 effective date"),
]
ax.legend(
    handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 1.10),
    ncol=2, frameon=False, fontsize=9.5,
)

fig.text(
    0.01, 0.01,
    "Total effort: ~105 person-days across ~22 weeks  |  "
    "See IFRS18-Project-Plan.md for the full activity-level breakdown",
    fontsize=8.5, color="#666666",
)

plt.tight_layout(rect=(0, 0.02, 1, 1))
out_path = "IFRS18-Project-Timeline.png"
plt.savefig(out_path, facecolor="white", bbox_inches="tight")
print(f"Saved {out_path}")
