"""Fig1 3단계 모델 — 흑백 학술본 KO/EN (정련).

균일한 흰 박스 3개(hairline 1.1px) + serif 라벨 + 검정 화살표 + 임계 축선(전이 정렬).
색·glow·이모지·chrome 없음. bare diagram.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, svg_doc, arrow_marker, text, box, harrow, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
ROMANS = ["I", "II", "III"]


def build(lang: str):
    from labels import FIG1
    L = FIG1[lang]
    W, H = 1000, 204
    bw, bh, by = 250, 102, 18
    xs = [28, 375, 722]
    cy = by + bh / 2
    p = [arrow_marker()]

    for i, x in enumerate(xs):
        p.append(box(x, by, bw, bh, sw=1.1))
        p.append(text(x + bw / 2, by + 26, f'{L["stage_word"]} {ROMANS[i]}', size=12, fill=GRAYL, ls=3))
        p.append(text(x + bw / 2, by + 61, L["stages"][i], size=24, weight=700))
        p.append(text(x + bw / 2, by + 87, L["subs"][i], size=12.5, italic=True, fill=GRAY))

    # 화살표 (박스 사이 gap 중앙)
    p.append(harrow(xs[0] + bw + 12, cy, xs[1] - 12))
    p.append(harrow(xs[1] + bw + 12, cy, xs[2] - 12))

    # 임계 축선: 자기참조→창발 전이(gap2 중앙)에 틱 정렬
    ay = 168
    gap2 = (xs[1] + bw + xs[2]) / 2  # 박스2 우측과 박스3 좌측의 중앙
    p.append(f'<line x1="28" y1="{ay}" x2="972" y2="{ay}" stroke="{RULE}" stroke-width="1"/>')
    p.append(f'<line x1="{gap2}" y1="{by + bh}" x2="{gap2}" y2="{ay - 6}" stroke="{RULE}" stroke-width="1" stroke-dasharray="2 4"/>')
    p.append(f'<line x1="{gap2}" y1="{ay - 6}" x2="{gap2}" y2="{ay + 6}" stroke="{INK}" stroke-width="1.1"/>')
    p.append(text(gap2, ay + 22, L["threshold"], size=12, fill=INK))
    p.append(text(972, ay - 9, L["axis"], size=12, anchor="end", italic=True, fill=GRAY))

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Fig01_3단계모델_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
