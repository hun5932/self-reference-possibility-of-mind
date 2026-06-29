"""Table1 4영역 동형성 매트릭스 — 흑백 학술본 KO/EN.

3×4 표(검정 괘선) + 옅은 회색 헤더 밴드. 셀=설명(serif)+노테이션(mono, 회색). bare.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, SOFT, svg_doc, text, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def build(lang: str):
    from labels import TABLE1
    L = TABLE1[lang]
    x0, c0, cw = 20, 160, 232
    xs = [x0, x0 + c0, x0 + c0 + cw, x0 + c0 + 2 * cw, x0 + c0 + 3 * cw, x0 + c0 + 4 * cw]
    W = xs[-1] + 20
    hy, hh, rh = 18, 60, 108
    ys = [hy, hy + hh, hy + hh + rh, hy + hh + 2 * rh, hy + hh + 3 * rh]
    H = ys[-1] + 18
    p = []

    # 헤더 밴드 (옅은 회색 — grayscale-safe)
    p.append(f'<rect x="{x0}" y="{hy}" width="{xs[-1]-x0}" height="{hh}" fill="{SOFT}"/>')

    # 괘선
    for xv in xs:
        p.append(f'<line x1="{xv}" y1="{hy}" x2="{xv}" y2="{ys[-1]}" stroke="{INK}" stroke-width="1"/>')
    for i, yv in enumerate(ys):
        sw = 1.2 if i in (0, 1, len(ys) - 1) else 1
        p.append(f'<line x1="{x0}" y1="{yv}" x2="{xs[-1]}" y2="{yv}" stroke="{INK}" stroke-width="{sw}"/>')

    # 헤더 텍스트
    p.append(text((xs[0] + xs[1]) / 2, hy + 37, L["corner"], size=12.5, fill=GRAY))
    for c in range(4):
        p.append(text((xs[c + 1] + xs[c + 2]) / 2, hy + 37, L["cols"][c], size=13.5, weight=600))

    # 행
    for r in range(3):
        rtop = ys[r + 1]
        p.append(text((xs[0] + xs[1]) / 2, rtop + rh / 2 + 5, L["rows"][r], size=14, weight=700))
        for c in range(4):
            cxm = (xs[c + 1] + xs[c + 2]) / 2
            t, note = L["cells"][r][c]
            p.append(text(cxm, rtop + 44, t, size=12.5, fill=INK))
            p.append(text(cxm, rtop + 70, note, size=10.5, cls="mono", fill=GRAYL))

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Table1_동형성매트릭스_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
