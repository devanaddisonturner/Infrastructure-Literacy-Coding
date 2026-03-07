#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Figure 1: Conceptual Model of Infrastructure Literacy
===============================================================

JEE Submission: "Infrastructure Literacy: A Conceptual Framework
for Understanding How Construction Career Students Think About
Environmental Justice"

Authors: Devan Cantrell Addison-Turner & Gretchen Cara Daily
Journal: The Journal of Environmental Education
         (Routledge / Taylor & Francis)
Submitted: February 8, 2026

Description:
    Three mutually reinforcing mechanisms (Problem Recognition,
    Design Integration, Advocacy Activation) situated within four
    defining dimensions (Built Environment Specificity, Health
    Equity Orientation, Professional Situatedness, Action
    Orientation). Curved bidirectional arrows indicate
    non-hierarchical relationships among mechanisms.

Output Files:
    - Figure1_Infrastructure_Literacy_Model.png  (300 DPI)
    - Figure1_Infrastructure_Literacy_Model.svg  (vector)
    - Figure1_Infrastructure_Literacy_Model.jpg  (300 DPI JPEG)

Dependencies:
    pip install matplotlib numpy Pillow

Usage:
    python3 generate_figure1.py
    python3 generate_figure1.py --output-dir ./figures
    python3 generate_figure1.py --grayscale-test

License:
    Copyright (c) 2026 Devan Cantrell Addison-Turner.
    All rights reserved.
    Stanford University, Civil and Environmental Engineering.
"""

__version__ = "1.1.0"
__author__ = "Devan Cantrell Addison-Turner"

import argparse
import os

import matplotlib
matplotlib.use('Agg')  # Must precede pyplot import
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

# ============================================================
# OUTPUT SETTINGS
# ============================================================
DPI = 300                   # Render resolution
JPEG_QUALITY = 95           # JPEG compression quality (0-100)
FIG_WIDTH = 6.5             # Figure width in inches
FIG_HEIGHT = 8.0            # Figure height in inches
LAYOUT_PAD = 0.2            # tight_layout padding
BASENAME = 'Figure1_Infrastructure_Literacy_Model'

# ============================================================
# CANVAS BOUNDS
# ============================================================
XLIM = (-4.5, 4.5)         # Axes x-range
YLIM = (-5.9, 4.5)         # Axes y-range

# ============================================================
# COLOR PALETTE
# Chosen for strong grayscale differentiation:
#   Problem Recognition  (deep teal,  L~32 — darkest)
#   Design Integration   (olive green, L~55 — medium)
#   Advocacy Activation  (warm sand,   L~70 — lightest)
# ============================================================
COLOR_PR = '#1B4F5C'        # Problem Recognition
COLOR_DI = '#6D8C48'        # Design Integration
COLOR_AA = '#D4A37A'        # Advocacy Activation

TEXT_DARK = '#1a1a1a'       # Primary text color
TEXT_MID = '#444444'        # Secondary text color

# ============================================================
# FRAME (superellipse border)
# ============================================================
FRAME_RADIUS = 3.3          # Outer superellipse radius
FRAME_INNER_RADIUS = 3.1    # Inner shadow line radius
FRAME_SQUARENESS = 5.5      # Exponent (higher = squarer)
FRAME_FILL = '#FBFBFB'      # Fill color
FRAME_STROKE = '#B3B3B3'    # Outer edge color
FRAME_STROKE_W = 1.8        # Outer edge linewidth
FRAME_INNER_COLOR = '#CCCCCC'  # Inner shadow color
FRAME_INNER_W = 0.8         # Inner shadow linewidth

# ============================================================
# DIMENSION BOXES (outer ring, 4 cardinal positions)
# Each tuple: (x, y, label, box_width, box_height)
# x/y derived from FRAME_RADIUS at runtime.
# Widths and heights vary per label length — these are
# layout data, not duplicated constants.
# ============================================================
DIM_BG = '#F2F2F2'          # Box fill
DIM_BORDER = '#555555'      # Box edge color
DIM_BORDER_W = 1.0          # Box edge linewidth
DIM_PAD = 0.12              # Box corner padding
DIM_FONTSIZE = 9.5          # Label font size
DIM_LINESPACING = 1.3       # Label line spacing

# ============================================================
# GUIDE CIRCLE (dashed ring behind mechanisms)
# ============================================================
GUIDE_RADIUS = 2.15         # Circle radius
GUIDE_COLOR = '#545454'     # Stroke color
GUIDE_WIDTH = 0.6           # Stroke linewidth
GUIDE_DASH = (0, (5, 5))    # Dash pattern (on, off)
GUIDE_ALPHA = 0.3           # Transparency

# ============================================================
# MECHANISM CIRCLES (3 inner circles)
# ============================================================
CIRCLE_RADIUS = 1.05        # Each mechanism circle radius
TRIANGLE_RADIUS = 1.65      # Centroid-to-vertex distance
CENTROID_Y = -0.34          # Vertical offset for balance
MECH_ANGLES = (90, 210, 330)  # Equilateral triangle angles
MECH_EDGE_COLOR = 'white'   # Circle border color
MECH_EDGE_W = 2.2           # Circle border linewidth
MECH_FONTSIZE = 10          # Label font size
MECH_LINESPACING = 1.2      # Label line spacing

# ============================================================
# DROP SHADOWS (behind mechanism circles)
# ============================================================
SHADOW_DX = 0.04            # Horizontal offset
SHADOW_DY = -0.04           # Vertical offset
SHADOW_COLOR = '#CCCCCC'    # Fill color
SHADOW_ALPHA = 0.35         # Transparency

# ============================================================
# ARROWS (curved bidirectional between mechanisms)
# ============================================================
ARROW_COLOR = '#555555'      # Stroke color
ARROW_WIDTH = 1.2            # Stroke linewidth
ARROW_GAP = 0.1              # Gap between circle edge and tip
ARROW_HEAD_LEN = 0.11        # Arrowhead length
ARROW_HEAD_W = 0.06          # Arrowhead half-width
ARROW_BEZIER_PTS = 80        # Sample points on Bezier curve
# Bulge per arrow pair: (from_idx, to_idx, bulge_amount)
ARROW_PAIRS = [
    (0, 1, 0.4),             # PR <-> DI: bulge left
    (1, 2, 0.55),            # DI <-> AA: bulge down
    (2, 0, 0.4),             # AA <-> PR: bulge right
]

# ============================================================
# CENTER LABEL ("INFRASTRUCTURE LITERACY")
# ============================================================
LABEL_Y_OFFSET = 0.12       # Half-gap between the two words
LABEL_FONTSIZE = 6.5         # Font size

# ============================================================
# LEGEND (below figure)
# ============================================================
HRULE_Y = -4.15             # Horizontal rule y-position
HRULE_INSET = 1.0           # Inset from canvas edge
HRULE_COLOR = '#e0e0e0'     # Rule color
HRULE_WIDTH = 0.6           # Rule linewidth

LEGEND_ARROW_Y = -4.5       # Arrow example y-position
LEGEND_ARROW_TIP_X = 0.2   # Arrow tip x-position
LEGEND_ARROW_TAIL_X = -0.5  # Arrow tail x-position
LEGEND_ARROW_TEXT_X = 0.4   # Arrow caption x-position
LEGEND_ARROW_COLOR = '#666666'  # Arrow example color
LEGEND_ARROW_W = 1.0        # Arrow example linewidth
LEGEND_TEXT_COLOR = '#555555'   # Arrow caption color
LEGEND_FONTSIZE_SM = 6.5    # Arrow caption font size

LEGEND_Y_START = -4.9       # First swatch y-position
LEGEND_ROW_SPACING = 0.38   # Vertical gap between rows
LEGEND_SWATCH_R = 0.12      # Color swatch radius
LEGEND_SWATCH_X = -3.5      # Swatch x-position
LEGEND_SWATCH_EDGE = '#888888'  # Swatch border color
LEGEND_SWATCH_EDGE_W = 0.4  # Swatch border linewidth
LEGEND_NAME_X = -3.25       # Mechanism name x-position
LEGEND_DESC_X = -0.4        # Description x-position
LEGEND_FONTSIZE = 7         # Legend text font size

# Epsilon for floating-point zero guards
_EPS = 1e-9


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def superellipse(radius, exponent, num_points=1000):
    """Generate x, y coordinates for a superellipse.

    A superellipse (Lame curve) with exponent > 2 produces a
    shape between a circle and a rounded square.

    Args:
        radius: Distance from center to edge.
        exponent: Squareness (higher = more square).
        num_points: Sampling density.

    Returns:
        (x, y) tuple of numpy arrays.
    """
    theta = np.linspace(0, 2 * np.pi, num_points)
    exp = 2.0 / exponent
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    x = radius * np.sign(cos_t) * np.abs(cos_t) ** exp
    y = radius * np.sign(sin_t) * np.abs(sin_t) ** exp
    return x, y


def draw_curved_bidir(
    ax, p1, p2, radius, color, linewidth, bulge, center_y
):
    """Draw a curved bidirectional arrow between two circles.

    The Bezier control point is pushed radially outward from the
    triangle centroid so the arc clears the center label.

    The parametric quadratic Bezier is:
        B(t) = (1-t)^2 * start + 2(1-t)t * ctrl + t^2 * end
    for t in [0, 1].

    Args:
        ax: Matplotlib Axes.
        p1: (x, y) center of source circle.
        p2: (x, y) center of target circle.
        radius: Circle radius (for edge offset).
        color: Stroke and head fill color.
        linewidth: Shaft stroke width.
        bulge: Outward offset of the Bezier control point.
        center_y: Y-coordinate of the triangle centroid.
    """
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = np.sqrt(dx ** 2 + dy ** 2)
    if dist < _EPS:
        return  # Degenerate: coincident points
    ux, uy = dx / dist, dy / dist
    gap = radius + ARROW_GAP

    # Endpoints offset from circle edges
    sx, sy = x1 + ux * gap, y1 + uy * gap
    ex, ey = x2 - ux * gap, y2 - uy * gap

    # Control point: push outward from centroid
    mid_x = (sx + ex) / 2
    mid_y = (sy + ey) / 2
    cy_off = mid_y - center_y
    to_mid = np.sqrt(mid_x ** 2 + cy_off ** 2)
    if to_mid > _EPS:
        out_x, out_y = mid_x / to_mid, cy_off / to_mid
    else:
        out_x, out_y = 0.0, -1.0

    ctrl_x = mid_x + out_x * bulge
    ctrl_y = mid_y + out_y * bulge

    # Quadratic Bezier curve: B(t) = (1-t)^2*S + 2(1-t)t*C + t^2*E
    t = np.linspace(0, 1, ARROW_BEZIER_PTS)
    bx = (1 - t)**2 * sx + 2*(1 - t)*t * ctrl_x + t**2 * ex
    by = (1 - t)**2 * sy + 2*(1 - t)*t * ctrl_y + t**2 * ey
    ax.plot(
        bx, by, color=color, lw=linewidth,
        solid_capstyle='round', zorder=5,
    )

    # Arrowheads at both ends
    endpoints = [
        (ex, ey, ex - ctrl_x, ey - ctrl_y, True),
        (sx, sy, ctrl_x - sx, ctrl_y - sy, False),
    ]
    for px, py, ddx, ddy, is_end in endpoints:
        td = np.sqrt(ddx ** 2 + ddy ** 2)
        if td < _EPS:
            continue  # Degenerate arrowhead
        tux, tuy = ddx / td, ddy / td
        tpx, tpy = -tuy, tux
        sign = -1 if is_end else 1
        ax.add_patch(plt.Polygon(
            [
                (px, py),
                (px + sign * tux * ARROW_HEAD_LEN
                 + tpx * ARROW_HEAD_W,
                 py + sign * tuy * ARROW_HEAD_LEN
                 + tpy * ARROW_HEAD_W),
                (px + sign * tux * ARROW_HEAD_LEN
                 - tpx * ARROW_HEAD_W,
                 py + sign * tuy * ARROW_HEAD_LEN
                 - tpy * ARROW_HEAD_W),
            ],
            fc=color, ec='none', zorder=6,
        ))


# ============================================================
# MAIN FIGURE GENERATION
# ============================================================

def generate_figure(output_dir, grayscale_test=False):
    """Generate Figure 1 and save PNG, SVG, and JPG variants.

    Args:
        output_dir: Directory for output files (created if needed).
        grayscale_test: Also save a grayscale verification image.

    Returns:
        Dict mapping format keys ('png', 'svg', 'jpg', and
        optionally 'grayscale') to output file paths.

    Raises:
        OSError: If output directory cannot be created or
            files cannot be written.
        Exception: Any matplotlib or PIL error propagates
            after the figure is safely closed.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(
        1, 1, figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=DPI)

    try:
        ax.set_xlim(*XLIM)
        ax.set_ylim(*YLIM)
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor('white')

        # ------------------------------------------------------
        # Outer frame: superellipse with inner shadow
        # ------------------------------------------------------
        xf, yf = superellipse(FRAME_RADIUS, FRAME_SQUARENESS)
        ax.fill(
            xf, yf, facecolor=FRAME_FILL,
            edgecolor=FRAME_STROKE, linewidth=FRAME_STROKE_W,
            zorder=1,
        )

        xf2, yf2 = superellipse(
            FRAME_INNER_RADIUS, FRAME_SQUARENESS)
        ax.plot(
            xf2, yf2, color=FRAME_INNER_COLOR,
            linewidth=FRAME_INNER_W, zorder=1,
        )

        # ------------------------------------------------------
        # Four dimension boxes (outer ring)
        # Widths/heights are per-label layout data, not
        # constants, because they vary with text length.
        # ------------------------------------------------------
        dims = [
            (0, FRAME_RADIUS,
             'Built Environment\nSpecificity', 2.6, 0.72),
            (FRAME_RADIUS, 0,
             'Health Equity\nOrientation', 1.6, 0.95),
            (0, -FRAME_RADIUS,
             'Professional\nSituatedness', 2.3, 0.72),
            (-FRAME_RADIUS, 0,
             'Action\nOrientation', 1.6, 0.80),
        ]
        for x, y, label, bw, bh in dims:
            box = FancyBboxPatch(
                (x - bw / 2, y - bh / 2), bw, bh,
                boxstyle=f'round,pad={DIM_PAD}',
                facecolor=DIM_BG, edgecolor=DIM_BORDER,
                linewidth=DIM_BORDER_W, zorder=8,
            )
            ax.add_patch(box)
            ax.text(
                x, y, label, ha='center', va='center',
                fontsize=DIM_FONTSIZE, fontweight='bold',
                color=TEXT_DARK, family='sans-serif',
                linespacing=DIM_LINESPACING, zorder=9,
            )

        # ------------------------------------------------------
        # Dashed circle guide (behind mechanisms)
        # ------------------------------------------------------
        guide = plt.Circle(
            (0, CENTROID_Y), GUIDE_RADIUS, fill=False,
            edgecolor=GUIDE_COLOR, linewidth=GUIDE_WIDTH,
            linestyle=GUIDE_DASH, alpha=GUIDE_ALPHA,
            zorder=2,
        )
        ax.add_patch(guide)

        # ------------------------------------------------------
        # Three mechanism circles (equilateral triangle)
        # ------------------------------------------------------
        positions = [
            (TRIANGLE_RADIUS * np.cos(np.radians(a)),
             TRIANGLE_RADIUS * np.sin(np.radians(a))
             + CENTROID_Y)
            for a in MECH_ANGLES
        ]
        mech_data = [
            (COLOR_PR, 'Problem\nRecognition'),
            (COLOR_DI, 'Design\nIntegration'),
            (COLOR_AA, 'Advocacy\nActivation'),
        ]

        for (x, y), (color, title) in zip(
            positions, mech_data
        ):
            # Drop shadow
            ax.add_patch(plt.Circle(
                (x + SHADOW_DX, y + SHADOW_DY),
                CIRCLE_RADIUS,
                facecolor=SHADOW_COLOR, edgecolor='none',
                alpha=SHADOW_ALPHA, zorder=3,
            ))
            # Main circle
            ax.add_patch(plt.Circle(
                (x, y), CIRCLE_RADIUS,
                facecolor=color, edgecolor=MECH_EDGE_COLOR,
                linewidth=MECH_EDGE_W, zorder=4,
            ))
            # Label
            ax.text(
                x, y, title, ha='center', va='center',
                fontsize=MECH_FONTSIZE, fontweight='bold',
                color='white', family='sans-serif',
                linespacing=MECH_LINESPACING, zorder=5,
            )

        # ------------------------------------------------------
        # Curved bidirectional arrows
        # ------------------------------------------------------
        for i, j, bulge in ARROW_PAIRS:
            draw_curved_bidir(
                ax, positions[i], positions[j],
                CIRCLE_RADIUS, ARROW_COLOR, ARROW_WIDTH,
                bulge=bulge, center_y=CENTROID_Y,
            )

        # ------------------------------------------------------
        # Center label
        # ------------------------------------------------------
        for text, y_sign in [
            ('INFRASTRUCTURE', 1), ('LITERACY', -1)
        ]:
            ax.text(
                0, CENTROID_Y + y_sign * LABEL_Y_OFFSET,
                text,
                ha='center', va='center',
                fontsize=LABEL_FONTSIZE, fontweight='bold',
                color=TEXT_MID, family='sans-serif',
                zorder=8,
            )

        # ------------------------------------------------------
        # Horizontal rule
        # ------------------------------------------------------
        ax.plot(
            [XLIM[0] + HRULE_INSET, XLIM[1] - HRULE_INSET],
            [HRULE_Y, HRULE_Y],
            color=HRULE_COLOR, linewidth=HRULE_WIDTH,
            zorder=10,
        )

        # ------------------------------------------------------
        # Legend
        # ------------------------------------------------------
        ax.annotate(
            '',
            xy=(LEGEND_ARROW_TIP_X, LEGEND_ARROW_Y),
            xytext=(LEGEND_ARROW_TAIL_X, LEGEND_ARROW_Y),
            arrowprops=dict(
                arrowstyle='->',
                color=LEGEND_ARROW_COLOR,
                lw=LEGEND_ARROW_W),
        )
        ax.text(
            LEGEND_ARROW_TEXT_X, LEGEND_ARROW_Y,
            'Mutually reinforcing cycle',
            ha='left', va='center',
            fontsize=LEGEND_FONTSIZE_SM,
            color=LEGEND_TEXT_COLOR, family='sans-serif',
            style='italic',
        )

        legend_items = [
            (COLOR_PR, 'Problem Recognition',
             'Spatial empathy & causal tracing'),
            (COLOR_DI, 'Design Integration',
             'Equity-weighted design reasoning'),
            (COLOR_AA, 'Advocacy Activation',
             'Community-informed professional voice'),
        ]
        for i, (color, name, desc) in enumerate(
            legend_items
        ):
            row_y = (
                LEGEND_Y_START - i * LEGEND_ROW_SPACING
            )
            ax.add_patch(plt.Circle(
                (LEGEND_SWATCH_X, row_y),
                LEGEND_SWATCH_R,
                facecolor=color,
                edgecolor=LEGEND_SWATCH_EDGE,
                lw=LEGEND_SWATCH_EDGE_W, zorder=10,
            ))
            ax.text(
                LEGEND_NAME_X, row_y, name, ha='left',
                va='center', fontsize=LEGEND_FONTSIZE,
                fontweight='bold', color=TEXT_DARK,
                family='sans-serif', zorder=10,
            )
            ax.text(
                LEGEND_DESC_X, row_y, desc, ha='left',
                va='center', fontsize=LEGEND_FONTSIZE,
                color=TEXT_MID, family='sans-serif',
                style='italic', zorder=10,
            )

        # ------------------------------------------------------
        # Save all variants
        # ------------------------------------------------------
        fig.tight_layout(pad=LAYOUT_PAD)
        paths = {}

        paths['png'] = os.path.join(
            output_dir, f'{BASENAME}.png')
        fig.savefig(
            paths['png'], dpi=DPI, bbox_inches='tight',
            facecolor='white', edgecolor='none',
        )

        # Re-save PNG via PIL to guarantee DPI metadata is
        # embedded in the file header (matplotlib does not
        # always write pHYs chunk reliably across backends).
        _png_tmp = Image.open(paths['png'])
        _png_tmp.save(paths['png'], dpi=(DPI, DPI))
        _png_tmp.close()
             
        paths['svg'] = os.path.join(
            output_dir, f'{BASENAME}.svg')
        fig.savefig(
            paths['svg'], bbox_inches='tight',
            facecolor='white', edgecolor='none',
        )

        paths['jpg'] = os.path.join(
            output_dir, f'{BASENAME}.jpg')
        pil_img = Image.open(paths['png'])
        try:
            pil_img.convert('RGB').save(
                paths['jpg'], 'JPEG',
                quality=JPEG_QUALITY, dpi=(DPI, DPI),
            )
            if grayscale_test:
                paths['grayscale'] = os.path.join(
                    output_dir,
                    f'{BASENAME}_grayscale.png')
                pil_img.convert('L').save(
                    paths['grayscale'])
        finally:
            pil_img.close()

    finally:
        plt.close(fig)

    return paths


# ============================================================
# VERIFICATION
# ============================================================

def verify_outputs(paths):
    """Print verification summary for all generated files.

    Args:
        paths: Dict from generate_figure().
    """
    with Image.open(paths['png']) as img:
        w, h = img.size
        dpi = img.info.get('dpi', (0, 0))

    print(
        f"PNG:  {w}x{h} px | DPI: {dpi[0]:.0f} | "
        f"{os.path.getsize(paths['png']) / 1024:.0f} KB"
    )
    print(
        f"SVG:  "
        f"{os.path.getsize(paths['svg']) / 1024:.0f} KB"
        f" (vector)"
    )
    print(
        f"JPG:  "
        f"{os.path.getsize(paths['jpg']) / 1024:.0f} KB"
        f" | DPI: {DPI} | quality: {JPEG_QUALITY}"
    )
    print(
        f"Print size: "
        f"{w / DPI:.1f} x {h / DPI:.1f} inches"
    )

    if 'grayscale' in paths:
        print(f"\nGrayscale test: {paths['grayscale']}")
        print(
            "Verify: three mechanism circles should be "
            "clearly distinguishable in grayscale."
        )


# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    """Parse arguments and generate the figure."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate Figure 1: Conceptual Model of "
            "Infrastructure Literacy"
        ),
    )
    parser.add_argument(
        '--output-dir', '-o',
        default=os.path.dirname(os.path.abspath(__file__)),
        help=(
            'Directory for output files '
            '(default: script directory)'
        ),
    )
    parser.add_argument(
        '--grayscale-test',
        action='store_true',
        help='Also save a grayscale verification image',
    )
    args = parser.parse_args()

    print(f"Generating Figure 1 -> {args.output_dir}")
    paths = generate_figure(
        args.output_dir,
        grayscale_test=args.grayscale_test,
    )
    verify_outputs(paths)
    print("\nDone.")


if __name__ == '__main__':
    main()
