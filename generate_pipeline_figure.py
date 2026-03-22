"""
generate_pipeline_figure.py
============================================================
Publication-ready pipeline figure — Infrastructure Literacy
three-layer systematic content analysis workflow.

Design philosophy
-----------------
This script uses an absolute-inch coordinate system.
Every element is defined as (x_in, y_in, w_in, h_in) before
any drawing. Overlaps are impossible because positions are
computed, not derived from axes-fraction arithmetic.

Visual style: minimal academic (CONSORT/PRISMA tradition)
  - White boxes with 0.5 pt borders
  - Two colour ramps maximum (blue retrieval; green analysis)
  - No decorative headers, badges, or gradients
  - 6–7 pt text throughout (Nature/JVET standard)
  - Hairline rules and thin arrows

Academic references
-------------------
CONSORT 2024 (Schulz KF et al., BMJ; doi:10.1136/bmj.n702):
  Left-side phase labels; side-branch exclusion box; n= counts.

PRISMA 2020 (Page MJ et al., BMJ 2021; doi:10.1136/bmj.n71):
  Phase separator rules; alternating light band shading.

Nature final submission guidelines:
  Arial/Helvetica; 5–7 pt labels; 300 dpi; TIFF preferred.

Cell Press figure guidelines (2024):
  0.5–1.5 pt line weights; 6–8 pt text at print size;
  panel label 'A' bold capital; TIFF/PDF preferred.

Author:  Devan Cantrell Addison-Turner
         PhD Candidate, Civil and Environmental Engineering
         Stanford Doerr School of Sustainability
         daddisonturner@stanford.edu
         ORCID: 0000-0002-2511-3680

Usage
-----
    python3 generate_pipeline_figure.py
    python3 generate_pipeline_figure.py --format tiff
    python3 generate_pipeline_figure.py --format eps
    python3 generate_pipeline_figure.py --width jvet
    python3 generate_pipeline_figure.py --dpi 600
    python3 generate_pipeline_figure.py --grayscale

Output
------
    figures/Figure_Pipeline_<width>[_grayscale].<ext>

Requirements
------------
    matplotlib >= 3.5  |  Pillow >= 9.0
"""

import argparse, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

# ── Typography ────────────────────────────────────────────────────────────────
FONT       = "Liberation Sans"   # metrically identical to Arial / Helvetica
PT_LABEL   = 6.0    # step label (bold)
PT_TITLE   = 6.5    # box title (bold)
PT_BODY    = 5.8    # body / detail lines
PT_COUNT   = 6.5    # n= count line (bold)
PT_PHASE   = 5.5    # phase strip text
PT_CAP     = 5.0    # caption
PT_PANEL   = 9.0    # panel label A

# ── Minimal colour palette ────────────────────────────────────────────────────
# Retrieval steps: muted steel blue
C_RET_F = "#EBF4FB"   # fill
C_RET_E = "#2565A0"   # edge
C_RET_T = "#0D3A66"   # text

# Coding layers: muted sage green
C_COD_F = "#EBF7EE"
C_COD_E = "#1E7A3D"
C_COD_T = "#0C3D1E"

# Exclusion: warm amber (CONSORT side-branch)
C_EXC_F = "#FEF7EC"
C_EXC_E = "#A06800"
C_EXC_T = "#5A3800"

# Output terminal: neutral light grey
C_OUT_F = "#F5F5F5"
C_OUT_E = "#555555"
C_OUT_T = "#111111"

# Phase band: very subtle fill behind each phase group
C_BAND_RET = "#F5FAFD"   # retrieval phase band
C_BAND_COD = "#F5FBF7"   # coding phase band

# Structural
C_RULE  = "#BBBBBB"
C_ARR   = "#3A3A3A"
C_PHASE = "#888888"      # phase label text

# Line weights
LW_BOX  = 0.5   # box border (Cell Press: 0.5–1.5 pt)
LW_ARR  = 0.6   # arrow shaft
LW_RULE = 0.3   # phase separator hairline

# ── Column widths (cm → inches) ───────────────────────────────────────────────
COL_W = {
    "two-col": 18.4 / 2.54,
    "full":    17.4 / 2.54,
    "jvet":    16.0 / 2.54,
    "one-col":  8.5 / 2.54,
}


# ── Grayscale override ────────────────────────────────────────────────────────

def apply_grayscale():
    g = globals()
    g.update({
        "C_RET_F": "#E8E8E8", "C_RET_E": "#333333", "C_RET_T": "#111111",
        "C_COD_F": "#D8D8D8", "C_COD_E": "#222222", "C_COD_T": "#111111",
        "C_EXC_F": "#C8C8C8", "C_EXC_E": "#111111", "C_EXC_T": "#111111",
        "C_OUT_F": "#F0F0F0", "C_OUT_E": "#444444", "C_OUT_T": "#111111",
        "C_BAND_RET": "#F0F0F0", "C_BAND_COD": "#E8E8E8",
        "C_RULE": "#AAAAAA",  "C_ARR": "#333333",
        "C_PHASE": "#666666",
    })


# ════════════════════════════════════════════════════════════════════════════
# ABSOLUTE-INCH DRAWING ENGINE
# ════════════════════════════════════════════════════════════════════════════

class InchCanvas:
    """
    Draws into a matplotlib Axes using data coordinates equal to inches.
    ax.set_xlim(0, fig_w)  ax.set_ylim(0, fig_h)
    All coordinates passed to drawing methods are in inches from bottom-left.
    This eliminates all fraction-arithmetic drift.
    """
    def __init__(self, ax, fig_w, fig_h):
        self.ax = ax
        self.W  = fig_w
        self.H  = fig_h
        ax.set_xlim(0, fig_w)
        ax.set_ylim(0, fig_h)
        ax.set_aspect("equal")
        ax.axis("off")

    # ── primitives ──────────────────────────────────────────────────────────

    def rect(self, x, y, w, h, fc, ec="none", lw=0, z=1, alpha=1.0):
        self.ax.add_patch(Rectangle(
            (x, y), w, h, facecolor=fc, edgecolor=ec,
            linewidth=lw, zorder=z, alpha=alpha, clip_on=False))

    def box(self, x, y, w, h, fc, ec, lw=LW_BOX, r=0.04, z=3):
        """Rounded box. r in data-inches."""
        self.ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={r}",
            facecolor=fc, edgecolor=ec, linewidth=lw,
            zorder=z, clip_on=False))

    def text(self, x, y, s, size, color="#111111",
             bold=False, italic=False,
             ha="center", va="center", z=6):
        self.ax.text(x, y, s, ha=ha, va=va, fontsize=size,
                     fontweight="bold" if bold else "normal",
                     fontstyle="italic" if italic else "normal",
                     color=color, zorder=z, clip_on=False)

    def arrow(self, x1, y1, x2, y2, color=C_ARR):
        self.ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->,head_width=0.07,head_length=0.08",
                color=color, lw=LW_ARR),
            zorder=4)

    def hline(self, y, x0=None, x1=None, color=C_RULE, lw=LW_RULE):
        x0 = x0 if x0 is not None else 0
        x1 = x1 if x1 is not None else self.W
        self.ax.add_line(Line2D(
            [x0, x1], [y, y], color=color,
            linewidth=lw, zorder=2))

    # ── compound node ────────────────────────────────────────────────────────

    def node(self, x, y, w, h,
             fc, ec, tc,
             step_n, title, body1="", body2="", count=""):
        """
        Standard pipeline node.
        Step-number circle on left; title (bold); body lines; count (bold).
        All text computed relative to node bounds — no hardcoded magic.
        """
        # Box
        self.box(x, y, w, h, fc, ec)

        # Step number badge: small circle left of title
        circ_r = min(0.13, h * 0.28)
        cx_c   = x + 0.14
        cy_c   = y + h * 0.70
        self.ax.add_patch(plt.Circle(
            (cx_c, cy_c), circ_r,
            facecolor=ec, edgecolor="none", zorder=5))
        self.text(cx_c, cy_c, str(step_n),
                  PT_LABEL - 0.5, "#FFFFFF", bold=True, z=6)

        # Title
        tx = x + 0.35     # text column left
        tw = w - 0.40     # text column width
        tcx = tx + tw / 2

        if body1 or count:
            ty_title = y + h * 0.74
        else:
            ty_title = y + h / 2

        self.text(tcx, ty_title, title,
                  PT_TITLE, tc, bold=True)

        lines = [l for l in [body1, body2] if l]
        if count:
            lines.append(None)   # placeholder for count

        total_lines = len([l for l in lines if l is not None])
        if count:
            total_lines += 1

        line_h = h * 0.17
        # Body lines
        i_body = 0
        for line in [body1, body2]:
            if not line:
                continue
            ly = ty_title - line_h * (i_body + 1.0)
            self.text(tcx, ly, line,
                      PT_BODY, tc, italic=False)
            i_body += 1

        # Count (bold, slightly larger)
        if count:
            ly = y + h * 0.16
            self.text(tcx, ly, count,
                      PT_COUNT, tc, bold=True)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE CONSTRUCTION
# ════════════════════════════════════════════════════════════════════════════

def make_figure(width_in: float, dpi: int = 300,
                grayscale: bool = False) -> plt.Figure:

    if grayscale:
        apply_grayscale()

    # ── Canvas dimensions (all in inches) ────────────────────────────────
    FW = width_in          # figure width
    FH = width_in * 1.58   # portrait ~A4 aspect

    # Horizontal layout
    PL  = 0.80   # left margin (phase label column ends here)
    PR  = FW - 0.18   # main column right edge
    MCW = PR - PL     # main column width
    MCX = PL + MCW / 2

    SL  = PR + 0.22   # side branch left
    SR  = FW - 0.08   # side branch right
    SBW = SR - SL
    SBX = SL + SBW / 2

    # Vertical layout — defined bottom-up in inches
    # Each slot: (y_bottom, height)
    # Gap between adjacent slots is explicit

    CAP_H   = 0.42
    CAP_Y   = 0.08

    OUT_H   = 0.82
    OUT_Y   = CAP_Y + CAP_H + 0.18

    ARR_GAP = 0.20   # arrow + gap height between nodes

    L2_H    = 0.82
    L2_Y    = OUT_Y + OUT_H + ARR_GAP

    L1_H    = 0.82
    L1_Y    = L2_Y + L2_H + ARR_GAP

    L0_H    = 0.82
    L0_Y    = L1_Y + L1_H + ARR_GAP

    RULE1_Y = L0_Y + L0_H + 0.15   # phase separator rule

    CPC_H   = 0.70
    CPC_Y   = RULE1_Y + 0.18

    PDF_H   = 0.82
    PDF_Y   = CPC_Y + CPC_H + ARR_GAP

    RULE2_Y = PDF_Y + PDF_H + 0.15   # phase separator rule

    XLS_H   = 0.82
    XLS_Y   = RULE2_Y + 0.18

    HEAD_H  = 0.45
    HEAD_Y  = XLS_Y + XLS_H + 0.18

    FH_actual = HEAD_Y + HEAD_H + 0.18   # actual figure height needed

    # ── Create figure ─────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(FW, FH_actual), dpi=dpi)
    c = InchCanvas(ax, FW, FH_actual)
    fig.patch.set_facecolor("white")

    # ── Phase bands (very light, behind everything) ───────────────────────
    # Retrieval band
    c.rect(PL, XLS_Y - 0.04,
           MCW, (PDF_Y + PDF_H) - XLS_Y + 0.08,
           fc=C_BAND_RET, z=0, alpha=0.7)
    # Coding band
    c.rect(PL, L2_Y - 0.04,
           MCW, (L0_Y + L0_H) - L2_Y + 0.08,
           fc=C_BAND_COD, z=0, alpha=0.7)

    # ── Phase separator rules ─────────────────────────────────────────────
    c.hline(RULE1_Y + 0.04, x0=PL, x1=PR, color=C_RULE, lw=LW_RULE)
    c.hline(RULE2_Y + 0.04, x0=PL, x1=PR, color=C_RULE, lw=LW_RULE)

    # Phase rule labels (centred in rule gap)
    for y, label in [
        (RULE1_Y + 0.04 + 0.06,  "ANALYSIS  ▲           RETRIEVAL  ▼"),
        (RULE2_Y + 0.04 + 0.06,  "RETRIEVAL  ▲           PREPARATION  ▼"),
    ]:
        c.text(MCX, y, label,
               PT_PHASE, C_PHASE, bold=False, italic=False)

    # ── Left-side phase labels (CONSORT style) ────────────────────────────
    phase_labels = [
        (XLS_Y  + XLS_H/2,              "Preparation"),
        ((PDF_Y + PDF_H/2 + CPC_Y + CPC_H/2) / 2, "Source\nretrieval"),
        ((L0_Y + L0_H/2 + L2_Y + L2_H/2) / 2,     "Coding\nlayers"),
        (OUT_Y  + OUT_H/2,              "Output"),
    ]
    for py, lbl in phase_labels:
        c.text(PL / 2, py, lbl,
               PT_PHASE, C_PHASE, bold=True, italic=False,
               ha="center", va="center")

    # ── Header ────────────────────────────────────────────────────────────
    # Simple thin-bordered rectangle — no dark fill
    c.box(PL, HEAD_Y, MCW, HEAD_H, fc="#F8FAFB", ec=C_RET_E,
          lw=LW_BOX, r=0.04, z=3)
    c.text(MCX, HEAD_Y + HEAD_H * 0.64,
           "Three-Layer Systematic Content Analysis Pipeline",
           PT_TITLE + 0.5, C_RET_T, bold=True)
    c.text(MCX, HEAD_Y + HEAD_H * 0.34,
           "Infrastructure Literacy Credential Audit  ·  "
           "4 credentials  ·  3 national systems  ·  431 outcomes",
           PT_BODY, C_RET_T, italic=True)

    # Panel label A (Cell Press convention)
    c.text(PL - 0.55, HEAD_Y + HEAD_H - 0.05,
           "A", PT_PANEL, "#111111", bold=True,
           ha="left", va="top")

    # ── STEP 1 — Load spreadsheet ─────────────────────────────────────────
    c.node(PL, XLS_Y, MCW, XLS_H,
           C_RET_F, C_RET_E, C_RET_T,
           step_n=1,
           title="Load outcome spreadsheet",
           body1="EJT_Binary_Coding_Results_v6.xlsx",
           body2="4 credentials  ·  3 national systems",
           count="n = 431 learning outcomes")

    c.arrow(MCX, XLS_Y - 0.02, MCX, PDF_Y + PDF_H + 0.02)

    # ── STEP 2 — Download main credential PDFs ────────────────────────────
    c.node(PL, PDF_Y, MCW, PDF_H,
           C_RET_F, C_RET_E, C_RET_T,
           step_n=2,
           title="Download main credential documents",
           body1="CA CTE (USA)  ·  CPC30220 R1 (Australia)  ·  City & Guilds 6706-23 (UK)",
           body2="Retrieved from official national registries",
           count="n = 3 credential PDFs")

    # NCCER exclusion side-branch (CONSORT convention)
    exc_y  = PDF_Y + PDF_H * 0.25
    exc_h  = PDF_H * 0.55
    exc_cy = exc_y + exc_h / 2
    c.arrow(PR + 0.02, PDF_Y + PDF_H * 0.55,
            SL - 0.02, exc_cy, color=C_EXC_E)
    c.box(SL, exc_y, SBW, exc_h,
          fc=C_EXC_F, ec=C_EXC_E, lw=LW_BOX, r=0.03, z=3)
    c.text(SBX, exc_y + exc_h * 0.74,
           "Credential A — excluded",
           PT_BODY, C_EXC_T, bold=True)
    c.text(SBX, exc_y + exc_h * 0.50,
           "NCCER Core Curriculum",
           PT_BODY, C_EXC_T)
    c.text(SBX, exc_y + exc_h * 0.26,
           "Institutional purchase",
           PT_BODY - 0.3, C_EXC_T, italic=True)

    c.arrow(MCX, PDF_Y - 0.02, MCX, CPC_Y + CPC_H + 0.02)

    # ── STEP 3 — Download CPC unit PDFs ───────────────────────────────────
    c.node(PL, CPC_Y, MCW, CPC_H,
           C_RET_F, C_RET_E, C_RET_T,
           step_n=3,
           title="Download CPC30220 unit competency PDFs",
           body1="CPCCCA2002 – CPCCWHS2001  ·  training.gov.au  ·  March 2026",
           count="n = 27 unit PDFs  (114 elements)")

    c.arrow(MCX, CPC_Y - 0.02, MCX, L0_Y + L0_H + 0.02)

    # ── STEP 4 — Layer 0 ──────────────────────────────────────────────────
    c.node(PL, L0_Y, MCW, L0_H,
           C_COD_F, C_COD_E, C_COD_T,
           step_n=4,
           title="Layer 0  —  Primary keyword search",
           body1="15 primary EJ terms  ×  4 credentials  =  60 term-credential pairs",
           body2="Binary presence / absence across all credential documents",
           count="Result: 0 / 60  (0 % of pairs contain any Layer 0 term)")

    c.arrow(MCX, L0_Y - 0.02, MCX, L1_Y + L1_H + 0.02)

    # ── STEP 5 — Layer 1 ──────────────────────────────────────────────────
    c.node(PL, L1_Y, MCW, L1_H,
           C_COD_F, C_COD_E, C_COD_T,
           step_n=5,
           title="Layer 1  —  Near-synonym expansion",
           body1="30 additional terms  ×  4 credentials  =  120 term-credential pairs",
           body2="Distributional, equity-adjacent, and community health vocabulary",
           count="Result: 0 / 120  (0 % of pairs contain any Layer 1 term)")

    c.arrow(MCX, L1_Y - 0.02, MCX, L2_Y + L2_H + 0.02)

    # ── STEP 6 — Layer 2 ──────────────────────────────────────────────────
    c.node(PL, L2_Y, MCW, L2_H,
           C_COD_F, C_COD_E, C_COD_T,
           step_n=6,
           title="Layer 2  —  Thematic audit",
           body1="431 learning outcomes × 3 binary equity criteria",
           body2="Criterion A: distributional burdens  ·  B: health equity  ·  C: EJ concepts",
           count="Result: 0 / 431  (0 % of outcomes meet any criterion)")

    c.arrow(MCX, L2_Y - 0.02, MCX, OUT_Y + OUT_H + 0.02)

    # ── OUTPUT terminal ────────────────────────────────────────────────────
    c.box(PL, OUT_Y, MCW, OUT_H,
          fc=C_OUT_F, ec=C_OUT_E, lw=LW_BOX, r=0.04, z=3)
    out_cx = PL + MCW / 2
    c.text(out_cx, OUT_Y + OUT_H * 0.78,
           "irr_source_documents.zip  +  keyword replication report",
           PT_TITLE, C_OUT_T, bold=True)
    c.text(out_cx, OUT_Y + OUT_H * 0.55,
           "Zero per cent of 431 learning outcomes across four credentials "
           "in three national systems",
           PT_BODY, C_OUT_T)
    c.text(out_cx, OUT_Y + OUT_H * 0.36,
           "address environmental justice, community health equity, "
           "or the distributional consequences of infrastructure decisions",
           PT_BODY, C_OUT_T)
    c.text(out_cx, OUT_Y + OUT_H * 0.14,
           "Finding invariant across all three layers  "
           "(L0: 0/60 · L1: 0/120 · L2: 0/431)",
           PT_BODY - 0.2, C_OUT_T, italic=True)

    # ── Legend ─────────────────────────────────────────────────────────────
    leg_y = CAP_Y + CAP_H - 0.14
    items = [
        (C_RET_F, C_RET_E, "Source retrieval step"),
        (C_COD_F, C_COD_E, "Coding / analysis layer"),
        (C_EXC_F, C_EXC_E, "Excluded credential"),
        (C_OUT_F, C_OUT_E, "Output node"),
    ]
    seg = MCW / len(items)
    for k, (ff, ef, lbl) in enumerate(items):
        lx = PL + k * seg + 0.05
        c.box(lx, leg_y - 0.06, 0.16, 0.12, fc=ff, ec=ef,
              lw=LW_BOX, r=0.02, z=5)
        c.text(lx + 0.22, leg_y, lbl,
               PT_BODY, "#555555", ha="left", va="center")

    # ── Caption ────────────────────────────────────────────────────────────
    c.text(MCX, CAP_Y + 0.28,
           "Figure  |  Three-layer systematic content analysis pipeline.",
           PT_CAP + 0.3, "#444444", bold=True)
    c.text(MCX, CAP_Y + 0.18,
           "Companion to: Addison-Turner (2026). Infrastructure Literacy. "
           "J. Vocational Education and Training. "
           "Data: doi:10.5281/zenodo.18893500 (v1.0.2). "
           "IRB: Stanford #84369. Trial: NCT07315919.",
           PT_CAP, "#666666", italic=True)
    c.text(MCX, CAP_Y + 0.08,
           "Style: CONSORT 2024 (doi:10.1136/bmj.n702) · "
           "PRISMA 2020 (doi:10.1136/bmj.n71) · "
           "Cell Press fig. guidelines (2024) · "
           "Nature final submission (Arial, 300 dpi).",
           PT_CAP - 0.3, "#888888", italic=True)

    fig.tight_layout(pad=0)
    return fig


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="Generate journal-style pipeline figure (300 dpi).",
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--format",
                   choices=["png","tiff","eps","both"], default="png")
    p.add_argument("--width",
                   choices=["two-col","full","jvet","one-col"],
                   default="two-col")
    p.add_argument("--dpi",  type=int, default=300)
    p.add_argument("--grayscale", action="store_true")
    p.add_argument("--output-dir", default="figures")
    args = p.parse_args()

    plt.rcParams.update({
        "font.family":        "sans-serif",
        "font.sans-serif":    [FONT,"Arial","Helvetica","DejaVu Sans"],
        "pdf.fonttype":       42,
        "ps.fonttype":        42,
        "savefig.dpi":        args.dpi,
        "savefig.bbox":       "tight",
        "savefig.pad_inches": 0.03,
    })

    os.makedirs(args.output_dir, exist_ok=True)
    gs_tag = "_grayscale" if args.grayscale else ""
    stem   = f"Figure_Pipeline_{args.width}{gs_tag}"

    fig = make_figure(COL_W[args.width], dpi=args.dpi,
                      grayscale=args.grayscale)
    saved = []

    def save(ext, **kw):
        path = os.path.join(args.output_dir, f"{stem}.{ext}")
        fig.savefig(path, dpi=args.dpi, facecolor="white",
                    bbox_inches="tight", **kw)
        saved.append(path)

    save("png", format="png")
    if args.format in ("tiff","both"):
        save("tiff", format="tiff",
             pil_kwargs={"compression":"tiff_lzw"})
    if args.format == "eps":
        save("eps", format="eps")

    plt.close(fig)
    print(f"\nFigure ({args.dpi} dpi · {args.width} · "
          f"{'grayscale' if args.grayscale else 'colour'}):")
    for path in saved:
        from PIL import Image
        img = Image.open(path)
        cm_w = img.size[0] / args.dpi * 2.54
        cm_h = img.size[1] / args.dpi * 2.54
        print(f"  {path}  {img.size[0]}×{img.size[1]}px  "
              f"{cm_w:.1f}×{cm_h:.1f}cm  DPI={img.info.get('dpi','—')}")
    print("\nStyle:  CONSORT 2024 · PRISMA 2020 · Cell Press (2024) · Nature")
    print("Font:   Liberation Sans ≡ Arial/Helvetica")
    print("Embed:  TrueType (pdf.fonttype=42)")

if __name__ == "__main__":
    main()
