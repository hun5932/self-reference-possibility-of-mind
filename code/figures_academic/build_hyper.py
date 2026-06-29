"""Fig8-9 Circle Limit → 쌍곡 평면 타일링 (푸앵카레 원판) — 흑백 학술본 (textless).

단위원(무한 경계) + 측지선(경계에 직교하는 원호)으로 셀이 경계로 갈수록 작아지는 쌍곡 타일링.
중앙 정다각형을 각 변(측지선)에 대해 원 반전(reflection)으로 2세대 타일링. 색 없음.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
OUT.mkdir(parents=True, exist_ok=True)
INK = "#1A1A1A"


def ortho(p1, p2):
    """단위원에 직교하며 p1,p2 지나는 원 (center, radius)."""
    A = 2 * np.array([p1, p2], float)
    b = np.array([p1 @ p1 + 1.0, p2 @ p2 + 1.0])
    c = np.linalg.solve(A, b)
    r = np.sqrt(max(c @ c - 1.0, 1e-9))
    return c, r


def reflect(z, c, r):
    d = np.array(z, float) - c
    return c + r * r * d / (d @ d)


def geodesic(ax, p1, p2):
    p1 = np.array(p1, float); p2 = np.array(p2, float)
    if abs(p1[0] * p2[1] - p1[1] * p2[0]) < 1e-7:  # 원점 지나는 직선(지름)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=INK, lw=0.8, solid_capstyle="round")
        return
    c, r = ortho(p1, p2)
    a1 = np.degrees(np.arctan2(p1[1] - c[1], p1[0] - c[0]))
    a2 = np.degrees(np.arctan2(p2[1] - c[1], p2[0] - c[0]))
    span = (a2 - a1) % 360
    t1, t2 = (a1, a2) if span <= 180 else (a2, a1)
    ax.add_patch(Arc(c, 2 * r, 2 * r, angle=0, theta1=t1, theta2=t2, color=INK, lw=0.8))


def main():
    p, r0, off, gens = 5, 0.50, np.pi / 2, 2   # 5각형 + 2세대 = 깔끔한 쌍곡 타일(과밀 X)
    verts = [np.array([r0 * np.cos(2 * np.pi * i / p + off), r0 * np.sin(2 * np.pi * i / p + off)]) for i in range(p)]
    polys = [verts]
    seen = {tuple(np.round(np.mean(verts, axis=0), 3))}
    frontier = [verts]
    for _ in range(gens):
        newf = []
        for poly in frontier:
            m = len(poly)
            for i in range(m):
                a, b = poly[i], poly[(i + 1) % m]
                if abs(a[0] * b[1] - a[1] * b[0]) < 1e-7:
                    continue
                c, r = ortho(a, b)
                npoly = [reflect(v, c, r) for v in poly]
                cen = np.mean(npoly, axis=0)
                if np.hypot(*cen) > 0.985:        # 경계 너무 가까운 셀 제외(과밀 방지)
                    continue
                key = tuple(np.round(cen, 3))
                if key in seen:
                    continue
                seen.add(key)
                polys.append(npoly)
                newf.append(npoly)
        frontier = newf
        if len(polys) > 600:
            break

    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    ax.add_patch(Circle((0, 0), 1.0, fill=False, color=INK, lw=1.6))
    for poly in polys:
        m = len(poly)
        for i in range(m):
            geodesic(ax, poly[i], poly[(i + 1) % m])
    ax.set_xlim(-1.04, 1.04); ax.set_ylim(-1.04, 1.04)
    ax.set_aspect("equal"); ax.axis("off")
    for ext in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"Fig08_09_쌍곡타일링.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[hyper] Fig08_09_쌍곡타일링 ({len(polys)} cells)")


if __name__ == "__main__":
    main()
