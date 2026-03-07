#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for generate_figure1.py
==============================

Run with:
    python3 -m pytest test_generate_figure1.py -v
    python3 test_generate_figure1.py          # standalone

Requires: pytest (optional), Pillow, numpy, matplotlib
"""

import importlib.util
import os
import shutil
import tempfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

# ── Import the module under test ──────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    'generate_figure1',
    os.path.join(_HERE, 'generate_figure1.py'),
)
fig_mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fig_mod)


# ── Fixtures ──────────────────────────────────────────────

class _TmpDir:
    """Context manager that creates and cleans a temp dir."""

    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix='fig1_test_')
        return self.path

    def __exit__(self, *args):
        shutil.rmtree(self.path, ignore_errors=True)


def _generate(**kwargs):
    """Generate into a fresh temp dir; return (paths, tmpdir)."""
    tmp = tempfile.mkdtemp(prefix='fig1_test_')
    paths = fig_mod.generate_figure(tmp, **kwargs)
    return paths, tmp


# ============================================================
# 1. OUTPUT FILE EXISTENCE
# ============================================================

def test_generates_three_files():
    """PNG, SVG, and JPG are created."""
    paths, tmp = _generate()
    try:
        assert os.path.isfile(paths['png'])
        assert os.path.isfile(paths['svg'])
        assert os.path.isfile(paths['jpg'])
        assert len(paths) == 3
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_filenames_use_basename():
    """Output filenames are derived from the BASENAME constant."""
    paths, tmp = _generate()
    try:
        for key, path in paths.items():
            filename = os.path.basename(path)
            assert filename.startswith(fig_mod.BASENAME), (
                f"{key} filename '{filename}' does not start "
                f"with BASENAME '{fig_mod.BASENAME}'"
            )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_grayscale_opt_in():
    """Grayscale file only created when flag is set."""
    paths_off, tmp1 = _generate(grayscale_test=False)
    paths_on, tmp2 = _generate(grayscale_test=True)
    try:
        assert 'grayscale' not in paths_off
        assert 'grayscale' in paths_on
        assert os.path.isfile(paths_on['grayscale'])
    finally:
        shutil.rmtree(tmp1, ignore_errors=True)
        shutil.rmtree(tmp2, ignore_errors=True)


def test_creates_nested_output_dir():
    """Deeply nested output directories are created."""
    with _TmpDir() as base:
        nested = os.path.join(base, 'a', 'b', 'c')
        paths = fig_mod.generate_figure(nested)
        assert os.path.isfile(paths['png'])


def test_nonzero_file_sizes():
    """All outputs have nonzero size."""
    paths, tmp = _generate()
    try:
        for key, path in paths.items():
            size = os.path.getsize(path)
            assert size > 0, f"{key} is empty"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# 2. PNG VALIDATION
# ============================================================

def test_png_dimensions():
    """PNG is approximately 1993x2294 px."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['png'])
        w, h = img.size
        assert 1980 <= w <= 2010, f"Width {w} out of range"
        assert 2280 <= h <= 2310, f"Height {h} out of range"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_png_dpi():
    """PNG DPI is ~300."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['png'])
        dpi = img.info.get('dpi', (0, 0))
        assert 299 <= dpi[0] <= 301, f"DPI {dpi}"
        assert 299 <= dpi[1] <= 301, f"DPI {dpi}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_png_mode():
    """PNG is RGBA (transparency support)."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['png'])
        assert img.mode == 'RGBA'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_png_not_blank():
    """PNG contains meaningful content (>50 unique colors)."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['png']).convert('RGB')
        arr = np.array(img)
        unique = len(np.unique(
            arr.reshape(-1, 3), axis=0))
        assert unique > 50, f"Only {unique} unique colors"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_png_white_background():
    """Corners of the PNG are white (background)."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['png']).convert('RGB')
        arr = np.array(img)
        corners = [
            arr[5, 5],
            arr[5, -5],
            arr[-5, 5],
            arr[-5, -5],
        ]
        for i, c in enumerate(corners):
            assert all(v > 250 for v in c), (
                f"Corner {i} is not white: {c}"
            )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# 3. JPG VALIDATION
# ============================================================

def test_jpg_mode():
    """JPG is RGB (no alpha channel)."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['jpg'])
        assert img.mode == 'RGB'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_jpg_dpi():
    """JPG DPI is exactly 300."""
    paths, tmp = _generate()
    try:
        img = Image.open(paths['jpg'])
        dpi = img.info.get('dpi', (0, 0))
        assert dpi == (300, 300), f"DPI {dpi}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_jpg_dimensions_match_png():
    """JPG and PNG have identical dimensions."""
    paths, tmp = _generate()
    try:
        png = Image.open(paths['png'])
        jpg = Image.open(paths['jpg'])
        assert png.size == jpg.size
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# 4. SVG VALIDATION
# ============================================================

def test_svg_valid_xml():
    """SVG is well-formed XML with an <svg> root."""
    paths, tmp = _generate()
    try:
        tree = ET.parse(paths['svg'])
        root = tree.getroot()
        # Strip namespace prefix if present
        tag = root.tag.split('}')[-1] if '}' in root.tag else root.tag
        assert tag == 'svg', f"Root tag is {root.tag}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_svg_has_content():
    """SVG file is larger than 10 KB (not empty stub)."""
    paths, tmp = _generate()
    try:
        size_kb = os.path.getsize(paths['svg']) / 1024
        assert size_kb > 10, f"SVG only {size_kb:.0f} KB"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# 5. GRAYSCALE DIFFERENTIATION
# ============================================================

def test_grayscale_three_distinct_circles():
    """Three mechanism circles are distinguishable in grayscale.

    Sampling regions are derived from layout constants so the
    test adapts if mechanism positions change.
    """
    paths, tmp = _generate(grayscale_test=True)
    try:
        gray = np.array(Image.open(paths['grayscale']))
        h, w = gray.shape

        # Convert figure coordinates to pixel fractions.
        # Axes: XLIM=(-4.5,4.5), YLIM=(-5.9,4.5).
        # bbox_inches='tight' crops whitespace, so we use
        # approximate fractions with a generous sampling
        # window (±3% of image).
        x_range = fig_mod.XLIM[1] - fig_mod.XLIM[0]
        y_range = fig_mod.YLIM[1] - fig_mod.YLIM[0]
        margin = 0.03  # sampling half-window as fraction

        mech_coords = []
        for a in fig_mod.MECH_ANGLES:
            mx = fig_mod.TRIANGLE_RADIUS * np.cos(
                np.radians(a))
            my = (fig_mod.TRIANGLE_RADIUS * np.sin(
                np.radians(a)) + fig_mod.CENTROID_Y)
            # Fraction within axes bounds
            fx = (mx - fig_mod.XLIM[0]) / x_range
            # Y is inverted: top of image is YLIM[1]
            fy = 1.0 - (my - fig_mod.YLIM[0]) / y_range
            mech_coords.append((fx, fy))

        labels = ['PR', 'DI', 'AA']
        samples = {}
        for label, (fx, fy) in zip(labels, mech_coords):
            y0 = max(0, int((fy - margin) * h))
            y1 = min(h, int((fy + margin) * h))
            x0 = max(0, int((fx - margin) * w))
            x1 = min(w, int((fx + margin) * w))
            samples[label] = gray[y0:y1, x0:x1]

        medians = {
            k: np.median(v) for k, v in samples.items()
        }
        vals = sorted(medians.values())
        gap1 = vals[1] - vals[0]
        gap2 = vals[2] - vals[1]

        assert gap1 > 15, (
            f"Insufficient grayscale gap: {medians}, "
            f"sorted diffs: {gap1:.0f}, {gap2:.0f}"
        )
        assert gap2 > 15, (
            f"Insufficient grayscale gap: {medians}, "
            f"sorted diffs: {gap1:.0f}, {gap2:.0f}"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# 6. MATHEMATICAL CORRECTNESS
# ============================================================

def test_equilateral_triangle():
    """Mechanism positions form an equilateral triangle."""
    positions = [
        (fig_mod.TRIANGLE_RADIUS * np.cos(np.radians(a)),
         fig_mod.TRIANGLE_RADIUS * np.sin(np.radians(a))
         + fig_mod.CENTROID_Y)
        for a in fig_mod.MECH_ANGLES
    ]
    dists = []
    for i in range(3):
        j = (i + 1) % 3
        d = np.sqrt(
            (positions[i][0] - positions[j][0]) ** 2
            + (positions[i][1] - positions[j][1]) ** 2
        )
        dists.append(d)
    assert max(dists) - min(dists) < 1e-10, (
        f"Not equilateral: {dists}"
    )


def test_no_circle_frame_overlap():
    """No mechanism circle extends outside the frame."""
    for a in fig_mod.MECH_ANGLES:
        x = fig_mod.TRIANGLE_RADIUS * np.cos(np.radians(a))
        y = (fig_mod.TRIANGLE_RADIUS * np.sin(np.radians(a))
             + fig_mod.CENTROID_Y)
        dist = np.sqrt(x ** 2 + y ** 2)
        clearance = (
            fig_mod.FRAME_RADIUS
            - (dist + fig_mod.CIRCLE_RADIUS)
        )
        assert clearance > 0, (
            f"Angle {a}: clearance={clearance:.3f}"
        )


def test_no_circle_circle_overlap():
    """No two mechanism circles overlap."""
    positions = [
        (fig_mod.TRIANGLE_RADIUS * np.cos(np.radians(a)),
         fig_mod.TRIANGLE_RADIUS * np.sin(np.radians(a))
         + fig_mod.CENTROID_Y)
        for a in fig_mod.MECH_ANGLES
    ]
    for i in range(3):
        for j in range(i + 1, 3):
            d = np.sqrt(
                (positions[i][0] - positions[j][0]) ** 2
                + (positions[i][1] - positions[j][1]) ** 2
            )
            gap = d - 2 * fig_mod.CIRCLE_RADIUS
            assert gap > 0, (
                f"Circles {i},{j} overlap: gap={gap:.3f}"
            )


def test_superellipse_symmetry():
    """Superellipse is symmetric about both axes."""
    x, y = fig_mod.superellipse(3.3, 5.5, 1000)
    # Mean of symmetric curve should be near zero
    assert abs(x.mean()) < 0.01, f"x mean: {x.mean()}"
    assert abs(y.mean()) < 0.01, f"y mean: {y.mean()}"
    # Extent should match the requested radius
    assert abs(x.max() - 3.3) < 0.01
    assert abs(y.max() - 3.3) < 0.01
    assert abs(x.min() + 3.3) < 0.01
    assert abs(y.min() + 3.3) < 0.01


# ============================================================
# 7. IDEMPOTENCY & DETERMINISM
# ============================================================

def test_idempotent_output():
    """Two runs produce byte-identical PNGs."""
    with _TmpDir() as tmp1, _TmpDir() as tmp2:
        p1 = fig_mod.generate_figure(tmp1)
        p2 = fig_mod.generate_figure(tmp2)
        with open(p1['png'], 'rb') as f1, \
                open(p2['png'], 'rb') as f2:
            assert f1.read() == f2.read()


# ============================================================
# 8. MODULE INTERFACE
# ============================================================

def test_module_metadata():
    """Module has version and author strings."""
    assert hasattr(fig_mod, '__version__')
    assert hasattr(fig_mod, '__author__')
    assert isinstance(fig_mod.__version__, str)
    assert len(fig_mod.__version__) > 0


def test_public_api():
    """Module exposes expected public functions."""
    assert callable(fig_mod.generate_figure)
    assert callable(fig_mod.verify_outputs)
    assert callable(fig_mod.superellipse)
    assert callable(fig_mod.draw_curved_bidir)
    assert callable(fig_mod.main)


def test_constants_are_numeric():
    """All layout constants are numeric types."""
    numeric_consts = [
        'ARROW_BEZIER_PTS', 'ARROW_GAP',
        'ARROW_HEAD_LEN', 'ARROW_HEAD_W',
        'ARROW_WIDTH',
        'CENTROID_Y', 'CIRCLE_RADIUS',
        'DIM_BORDER_W', 'DIM_FONTSIZE',
        'DIM_LINESPACING', 'DIM_PAD',
        'DPI',
        'FIG_HEIGHT', 'FIG_WIDTH',
        'FRAME_INNER_RADIUS', 'FRAME_INNER_W',
        'FRAME_RADIUS', 'FRAME_SQUARENESS',
        'FRAME_STROKE_W',
        'GUIDE_ALPHA', 'GUIDE_RADIUS', 'GUIDE_WIDTH',
        'HRULE_INSET', 'HRULE_WIDTH', 'HRULE_Y',
        'JPEG_QUALITY',
        'LABEL_FONTSIZE', 'LABEL_Y_OFFSET',
        'LAYOUT_PAD',
        'LEGEND_ARROW_TAIL_X', 'LEGEND_ARROW_TEXT_X',
        'LEGEND_ARROW_TIP_X', 'LEGEND_ARROW_W',
        'LEGEND_ARROW_Y',
        'LEGEND_DESC_X', 'LEGEND_FONTSIZE',
        'LEGEND_FONTSIZE_SM', 'LEGEND_NAME_X',
        'LEGEND_ROW_SPACING', 'LEGEND_SWATCH_EDGE_W',
        'LEGEND_SWATCH_R', 'LEGEND_SWATCH_X',
        'LEGEND_Y_START',
        'MECH_EDGE_W', 'MECH_FONTSIZE',
        'MECH_LINESPACING',
        'SHADOW_ALPHA', 'SHADOW_DX', 'SHADOW_DY',
        'TRIANGLE_RADIUS',
    ]
    for name in numeric_consts:
        val = getattr(fig_mod, name)
        assert isinstance(val, (int, float)), (
            f"{name} = {val!r} is not numeric"
        )


# ============================================================
# 9. EDGE CASES
# ============================================================

def test_draw_bidir_coincident_points():
    """draw_curved_bidir handles coincident points gracefully."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    # Should not raise
    fig_mod.draw_curved_bidir(
        ax, (0, 0), (0, 0), 1.0, 'black', 1.0,
        bulge=0.5, center_y=0.0,
    )
    plt.close(fig)


# ============================================================
# RUNNER
# ============================================================

def _run_all():
    """Run all test functions and report results."""
    tests = [
        (name, obj)
        for name, obj in sorted(globals().items())
        if name.startswith('test_') and callable(obj)
    ]

    passed = 0
    failed = 0
    errors = []

    for name, func in tests:
        try:
            func()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {name}: {exc}")
            failed += 1
            errors.append((name, exc))

    print(f"\n{'=' * 50}")
    print(f"  {passed} passed, {failed} failed, "
          f"{passed + failed} total")
    print(f"{'=' * 50}")

    if errors:
        print("\nFailures:")
        for name, exc in errors:
            print(f"  {name}: {exc}")
        return 1
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(_run_all())
