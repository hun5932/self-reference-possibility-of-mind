"""Escher 영역 자체제작 도판 (D-018) — 흑백 학술본.

Fig2 주기 타일링(Truchet, textless) · Fig3 17 평면결정군 · Fig4 상호 자기참조 ·
Fig5 드로스테(무한 재귀) · Fig6 폭포(불가능 하강 루프) · Fig7 계단(끝없는 상승).
색·glow·이모지 없음. bare.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, SOFT, WHITE, svg_doc, arrow_marker, text, box, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


# ── Fig2 주기 타일링 (Truchet) — 언어 무관 ──────────────────────────────
def fig2():
    s, n = 64, 8
    W = H = s * n
    p = []
    for i in range(n):
        for j in range(n):
            x, y, r = i * s, j * s, s / 2
            if (i + j) % 2 == 0:
                p.append(f'<path d="M {x+s/2} {y} A {r} {r} 0 0 0 {x} {y+s/2}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
                p.append(f'<path d="M {x+s} {y+s/2} A {r} {r} 0 0 0 {x+s/2} {y+s}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
            else:
                p.append(f'<path d="M {x+s/2} {y} A {r} {r} 0 0 1 {x+s} {y+s/2}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
                p.append(f'<path d="M {x} {y+s/2} A {r} {r} 0 0 1 {x+s/2} {y+s}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    render(svg_doc(W, H, "".join(p)), "Fig02_타일링", OUT, W, H)


# ── Fig3 17 평면결정군 ─────────────────────────────────────────────────
def fig3(lang):
    from labels import FIG3
    L = FIG3[lang]
    rows = [("1", ["p1"]), ("2", ["p2", "pm", "pg", "cm", "pmm", "pmg", "pgg", "cmm"]),
            ("3", ["p3", "p3m1", "p31m"]), ("4", ["p4", "p4m", "p4g"]), ("6", ["p6", "p6m"])]
    bw, bh, gap = 78, 38, 12
    x0, y0 = 150, 64
    W = x0 + 8 * (bw + gap) + 10
    H = y0 + len(rows) * (bh + gap) + 20
    p = [text(W / 2, 32, L["header"], size=15, weight=700)]
    p.append(text(70, y0 - 14, L["rot"], size=10.5, anchor="start", fill=GRAYL))
    for ri, (order, groups) in enumerate(rows):
        ry = y0 + ri * (bh + gap)
        p.append(text(110, ry + bh / 2 + 5, order, size=15, anchor="end", weight=700))
        p.append(text(132, ry + bh / 2 + 4, "차" if lang == "ko" else "", size=10, anchor="start", fill=GRAYL))
        for gi, g in enumerate(groups):
            gx = x0 + gi * (bw + gap)
            p.append(box(gx, ry, bw, bh, sw=1))
            p.append(text(gx + bw / 2, ry + bh / 2 + 5, g, size=13.5, cls="mono"))
    render(svg_doc(W, H, "".join(p)), f"Fig03_평면결정군_{lang}", OUT, W, H)


# ── Fig4 상호 자기참조 (Drawing Hands) ─────────────────────────────────
def fig4(lang):
    from labels import FIG4
    L = FIG4[lang]
    W, H = 760, 320
    bw, bh, by = 150, 120, 70
    ax, bx = 120, 490
    p = [arrow_marker()]
    for x, lab in ((ax, L["a"]), (bx, L["b"])):
        p.append(box(x, by, bw, bh, sw=1.3))
        p.append(text(x + bw / 2, by + bh / 2 + 12, lab, size=34, weight=700))
    # A→B (위 호) , B→A (아래 호)
    p.append(f'<path d="M {ax+bw} {by+38} C {ax+bw+90} {by-8}, {bx-90} {by-8}, {bx} {by+38}" '
             f'fill="none" stroke="{INK}" stroke-width="1.3" marker-end="url(#ar)"/>')
    p.append(f'<path d="M {bx} {by+bh-38} C {bx-90} {by+bh+46}, {ax+bw+90} {by+bh+46}, {ax+bw} {by+bh-38}" '
             f'fill="none" stroke="{INK}" stroke-width="1.3" marker-end="url(#ar)"/>')
    p.append(text(W / 2, by - 24, L["rel"], size=13, fill=GRAY))
    p.append(text(W / 2, by + bh + 70, L["note"], size=12.5, italic=True, fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig04_상호자기참조_{lang}", OUT, W, H)


# ── Fig5 드로스테 (무한 재귀) ──────────────────────────────────────────
def fig5(lang):
    from labels import FIG5
    L = FIG5[lang]
    W, H = 620, 380
    cx, cy = 310, 175
    w0, h0 = 440, 250
    p = []
    for k in range(7):
        sc = 0.74 ** k
        w, h = w0 * sc, h0 * sc
        ang = k * 7
        sw = 1.3 if k == 0 else 1
        p.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="none" '
                 f'stroke="{INK}" stroke-width="{sw}" transform="rotate({ang} {cx} {cy})"/>')
    p.append(text(cx, H - 36, L["note"], size=13, fill=INK))
    p.append(text(cx, H - 16, L["sub"], size=11.5, italic=True, fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig05_드로스테_{lang}", OUT, W, H)


# ── Fig6 폭포: 불가능한 하강 루프 ──────────────────────────────────────
def fig6(lang):
    from labels import FIG6
    L = FIG6[lang]
    W, H = 620, 420
    x1, y1, x2, y2 = 130, 90, 490, 330
    p = [arrow_marker()]
    # 닫힌 사각 수로 (각 변에 "하강" — 따라가면 항상 내려가지만 시작으로 복귀)
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    mids = [((x1 + x2) / 2, y1), (x2, (y1 + y2) / 2), ((x1 + x2) / 2, y2), (x1, (y1 + y2) / 2)]
    for a, b in zip(corners, corners[1:] + corners[:1]):
        p.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="1.4"/>')
    # 흐름 화살표 (시계방향) + 하강 라벨
    arrows = [((x1 + 30, y1), (x1 + 70, y1)), ((x2, y1 + 30), (x2, y1 + 70)),
              ((x2 - 30, y2), (x2 - 70, y2)), ((x1, y2 - 30), (x1, y2 - 70))]
    for (sa, sb) in arrows:
        p.append(f'<line x1="{sa[0]}" y1="{sa[1]}" x2="{sb[0]}" y2="{sb[1]}" stroke="{INK}" stroke-width="1.3" marker-end="url(#ar)"/>')
    for mx, my in mids:
        p.append(f'<rect x="{mx-26}" y="{my-11}" width="52" height="22" fill="{WHITE}"/>')
        p.append(text(mx, my + 4, L["down"], size=12, fill=GRAY))
    p.append(text(W / 2, (y1 + y2) / 2, L["imp"], size=12.5, italic=True, fill=GRAYL))
    p.append(text(W / 2, H - 24, L["note"], size=13, fill=INK))
    render(svg_doc(W, H, "".join(p)), f"Fig06_폭포루프_{lang}", OUT, W, H)


# ── Fig7 계단: 끝없는 상승 ─────────────────────────────────────────────
def fig7(lang):
    from labels import FIG7
    L = FIG7[lang]
    W, H = 620, 420
    x1, y1, x2, y2 = 130, 90, 490, 330
    p = [arrow_marker()]
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    # 계단식 변 (각 변에 짧은 step tick)
    for a, b in zip(corners, corners[1:] + corners[:1]):
        p.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" stroke-width="1.4"/>')
        # step ticks
        for t in range(1, 6):
            tx = a[0] + (b[0] - a[0]) * t / 6
            ty = a[1] + (b[1] - a[1]) * t / 6
            ox, oy = (0, 8) if a[1] == b[1] else (8, 0)
            p.append(f'<line x1="{tx}" y1="{ty}" x2="{tx+ox}" y2="{ty+oy}" stroke="{GRAYL}" stroke-width="1"/>')
    arrows = [((x1 + 70, y1), (x1 + 30, y1)), ((x2, y1 + 70), (x2, y1 + 30)),
              ((x2 - 70, y2), (x2 - 30, y2)), ((x1, y2 - 70), (x1, y2 - 30))]
    mids = [((x1 + x2) / 2, y1), (x2, (y1 + y2) / 2), ((x1 + x2) / 2, y2), (x1, (y1 + y2) / 2)]
    for (sa, sb) in arrows:
        p.append(f'<line x1="{sa[0]}" y1="{sa[1]}" x2="{sb[0]}" y2="{sb[1]}" stroke="{INK}" stroke-width="1.3" marker-end="url(#ar)"/>')
    for mx, my in mids:
        p.append(f'<rect x="{mx-24}" y="{my-11}" width="48" height="22" fill="{WHITE}"/>')
        p.append(text(mx, my + 4, L["up"], size=12, fill=GRAY))
    p.append(text(W / 2, (y1 + y2) / 2, L["imp"], size=12.5, italic=True, fill=GRAYL))
    p.append(text(W / 2, H - 24, L["note"], size=13, fill=INK))
    render(svg_doc(W, H, "".join(p)), f"Fig07_계단루프_{lang}", OUT, W, H)


def main() -> None:
    fig2()
    for lang in ("ko", "en"):
        fig3(lang); fig4(lang); fig5(lang); fig6(lang); fig7(lang)


if __name__ == "__main__":
    main()
