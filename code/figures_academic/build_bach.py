"""바흐 자기참조의 형식 — 흑백 학술본 KO/EN (3 패널).

회문(대칭축)·무한상승(루프)·BACH(보표 노트헤드). 회색 오선 + 검정 노트헤드. bare.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, WHITE, svg_doc, arrow_marker, text, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def notehead(cx, cy):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="6.5" ry="4.8" fill="{INK}"/>'


def staff(px, lo=30, hi=310):
    ys = [138, 150, 162, 174, 186]
    return "".join(f'<line x1="{px+lo}" y1="{y}" x2="{px+hi}" y2="{y}" stroke="{RULE}" stroke-width="1"/>' for y in ys)


def build(lang: str):
    from labels import BACH
    L = BACH[lang]
    W, H = 1080, 250
    px_list = [20, 390, 760]
    p = [arrow_marker()]

    for pi, px in enumerate(px_list):
        cxp = px + 170
        p.append(text(cxp, 40, L["panels"][pi], size=14, weight=600))
        p.append(text(cxp, 60, L["subs"][pi], size=11, italic=True, fill=GRAY))
        p.append(f'<line x1="{px+30}" y1="72" x2="{px+310}" y2="72" stroke="{RULE}" stroke-width="0.8"/>')

        if pi == 0:  # 회문 — 대칭축
            p.append(staff(px))
            p.append(f'<line x1="{cxp}" y1="120" x2="{cxp}" y2="204" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
            left = [(px + 70, 186), (px + 100, 174), (px + 130, 162), (px + 158, 150)]
            for i, (nx, ny) in enumerate(left):
                p.append(notehead(nx, ny))
                mx = 2 * cxp - nx
                p.append(notehead(mx, ny))
            p.append(text(px + 95, 112, L["axis_l"], size=10.5, fill=GRAYL))
            p.append(text(px + 245, 112, L["axis_r"], size=10.5, fill=GRAYL))
            p.append(text(cxp, 222, "↔", size=14, fill=GRAY))

        elif pi == 1:  # 무한상승 — 루프
            pts = [(px + 55, 192), (px + 110, 176), (px + 165, 160), (px + 220, 144), (px + 275, 128)]
            p.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[-1][0]}" y2="{pts[-1][1]}" stroke="{INK}" stroke-width="1"/>')
            for nx, ny in pts:
                p.append(notehead(nx, ny))
            # 영원회귀 점선 루프 (위로 돌아 시작점)
            p.append(f'<path d="M {px+275} {120} C {px+320} {86}, {px+30} {86}, {px+50} {184}" fill="none" '
                     f'stroke="{INK}" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#ar)"/>')
            p.append(text(px + 250, 116, L["rise"], size=10.5, fill=GRAYL))
            p.append(text(cxp, 100, L["loop"], size=10.5, fill=GRAYL))
            p.append(text(cxp, 222, "+1 oct ↺", size=11, cls="mono", fill=GRAY))

        else:  # BACH 모티프
            p.append(staff(px))
            notes = [("B♭", px + 80, 174), ("A", px + 140, 180), ("C", px + 200, 150), ("H", px + 258, 162)]
            for nm, nx, ny in notes:
                p.append(notehead(nx, ny))
                p.append(text(nx, 214, nm, size=13, cls="mono", fill=INK))
            p.append(text(cxp, 234, "B–A–C–H", size=11, cls="mono", fill=GRAY))

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Supp_바흐형식도식_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
