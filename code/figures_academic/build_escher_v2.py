"""에셔 영역 자체제작 개선본 (흑백 학술본) — 구조 추상 도식.

Fig6 폭포=펜로즈 삼각형(불가능 tribar) / Fig7 계단=펜로즈 무한계단.
정확한 등축(isometric) 기하 — 3축(R·U·L) 합=0 → 3빔이 2D에서 닫힘=불가능.
각 빔=솔리드 사각기둥(윗면 흰/옆면 회/끝단 옅은회) + 끝단 캡으로 코너 over/under.
회색조 음영(흑백) + 검정 외곽선. textless. (저널·발표 안전, 저작권 무관)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from style_academic import INK, svg_doc, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
TOP, SIDE, CAP = "#FFFFFF", "#C9C9C9", "#E6E6E6"   # 윗면·옆면·끝단(흑백 3톤)

R = np.array([0.8660254, 0.5])    # 우하 (등축)
U = np.array([0.0, -1.0])         # 상
L = np.array([-0.8660254, 0.5])   # 좌하  (R+U+L = 0)


def poly(pts, fill, sw=1.7):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'


def beam(O, eL, e1, e2, Ln, w, s):
    """등축 사각빔의 두 긴 가시면(윗면 eL-e1, 옆면 eL-e2) 폴리곤. 코너 정확히 만남(연장 없음)."""
    O = np.array(O, float)
    def P(t, a, b):
        return O + (t * Ln * eL + a * w * e1 + b * w * e2) * s
    top = [P(0, 0, 0), P(1, 0, 0), P(1, 1, 0), P(0, 1, 0)]          # eL-e1 윗면
    side = [P(0, 0, 0), P(1, 0, 0), P(1, 0, 1), P(0, 0, 1)]         # eL-e2 옆면
    return top, side


def fig6():
    """펜로즈 삼각형(tribar). 세 빔 R·U·L축, 합=0이라 2D에서 닫힘 → 불가능 도형(폭포의 핵심 구조)."""
    s, Ln, w = 88, 3.0, 1.0
    cx, cy = 300, 322
    O = np.array([cx, cy]) - (Ln * R + (Ln * 0.5) * U) * s
    A0 = O
    B0 = O + Ln * R * s
    C0 = O + (Ln * R + Ln * U) * s
    A = beam(A0, R, U, L, Ln, w, s)
    B = beam(B0, U, L, R, Ln, w, s)
    C = beam(C0, L, R, U, Ln, w, s)
    body = []
    for (top, side), gt, gs in ((A, TOP, SIDE), (B, TOP, "#DADADA"), (C, TOP, SIDE)):
        body.append(poly(side, gs))
        body.append(poly(top, gt))
    return svg_doc(600, 620, "".join(body)), 600, 620


def fig7():
    """펜로즈 무한계단 — 닫힌 사각 루프 위 계단 블록(등축), 한 바퀴 돌며 계속 상승=불가능."""
    s = 34
    cx, cy = 300, 350
    def gp(u, v, h):   # u:R축, v:L축, h:U축(높이)
        return np.array([cx, cy]) + (u * R + v * L + h * U) * s
    bw = 1.0           # 블록 평면 한 변
    rise = 0.5         # 칸당 상승
    th = 0.62          # 블록 두께(보임)
    n = 5
    steps = []
    for i in range(n):   steps.append((i,       0,       i))            # 변1
    for i in range(n):   steps.append((n,       i,       n + i))        # 변2
    for i in range(n):   steps.append((n - i,   n,       2 * n + i))    # 변3
    for i in range(n):   steps.append((0,       n - i,   3 * n + i))    # 변4(→시작보다 높음)
    body = []
    for (u, v, k) in steps:
        h = k * rise
        top = [gp(u, v, h), gp(u + bw, v, h), gp(u + bw, v + bw, h), gp(u, v + bw, h)]
        front = [gp(u, v + bw, h), gp(u + bw, v + bw, h), gp(u + bw, v + bw, h - th), gp(u, v + bw, h - th)]
        side = [gp(u + bw, v, h), gp(u + bw, v + bw, h), gp(u + bw, v + bw, h - th), gp(u + bw, v, h - th)]
        body.append(poly(front, SIDE, 1.3))
        body.append(poly(side, "#DADADA", 1.3))
        body.append(poly(top, TOP, 1.3))
    return svg_doc(660, 600, "".join(body)), 660, 600


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "6"
    if which == "6":
        svg, w, h = fig6(); render(svg, "Fig06_폭포_펜로즈", OUT, w, h)
    else:
        svg, w, h = fig7(); render(svg, "Fig07_계단_펜로즈", OUT, w, h)
