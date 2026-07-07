"""Fig10-12 바흐 자기참조 — 개별 보표 모티프 (흑백 학술본 KO/EN).

Fig10 무한상승 카논 · Fig11 Contrapunctus XIV (BACH) · Fig12 게 카논(회문).
회색 오선 + 검정 노트헤드. 곡명은 식별 정보(소제목). 그 외 bare.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, WHITE, svg_doc, arrow_marker, text, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def notehead(cx, cy):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="7" ry="5.2" fill="{INK}"/>'


def staff(x0, x1, ys=(150, 164, 178, 192, 206)):
    return "".join(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{RULE}" stroke-width="1"/>' for y in ys)


def header(cxp, title, sub):
    return (text(cxp, 42, title, size=15, weight=600)
            + text(cxp, 66, sub, size=11.5, italic=True, fill=GRAY)
            + f'<line x1="{cxp-280}" y1="80" x2="{cxp+280}" y2="80" stroke="{RULE}" stroke-width="0.8"/>')


def fig10(lang):  # 무한상승
    from labels import MUSIC
    L = MUSIC[lang]
    W, H = 640, 300
    cxp = W / 2
    p = [arrow_marker(), header(cxp, L["f10_t"], L["f10_s"])]
    pts = [(120, 240), (200, 214), (280, 188), (360, 162), (440, 136), (520, 110)]
    p.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[-1][0]}" y2="{pts[-1][1]}" stroke="{INK}" stroke-width="1"/>')
    for nx, ny in pts:
        p.append(notehead(nx, ny))
    p.append(f'<path d="M 520 100 C 588 56, 92 56, 120 232" fill="none" stroke="{INK}" stroke-width="1" '
             f'stroke-dasharray="3 3" marker-end="url(#ar)"/>')
    p.append(text(470, 126, L["rise"], size=11, fill=GRAYL))
    p.append(text(150, 150, L["loop"], size=11, anchor="start", fill=GRAYL))
    p.append(text(cxp, 284, "+1 oct", size=12, cls="mono", fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig10_무한상승_{lang}", OUT, W, H)


def fig11(lang):  # BACH 모티프
    from labels import MUSIC
    L = MUSIC[lang]
    W, H = 640, 300
    cxp = W / 2
    p = [header(cxp, L["f11_t"], L["f11_s"]), staff(120, 520)]
    notes = [("B♭", 180, 192), ("A", 280, 199), ("C", 380, 164), ("H", 480, 178)]
    for nm, nx, ny in notes:
        p.append(notehead(nx, ny))
        p.append(text(nx, 240, nm, size=15, cls="mono", fill=INK))
    p.append(text(cxp, 274, "B – A – C – H", size=13, cls="mono", fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig11_BACH_{lang}", OUT, W, H)


def fig12(lang):  # 게 카논 (회문)
    from labels import MUSIC
    L = MUSIC[lang]
    W, H = 640, 300
    cxp = W / 2
    p = [header(cxp, L["f12_t"], L["f12_s"]), staff(120, 520)]
    p.append(f'<line x1="{cxp}" y1="130" x2="{cxp}" y2="222" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
    left = [(160, 206), (210, 192), (260, 178), (300, 164)]
    for nx, ny in left:
        p.append(notehead(nx, ny))
        p.append(notehead(2 * cxp - nx, ny))
    p.append(text(220, 124, L["fwd"], size=11, fill=GRAYL))
    p.append(text(420, 124, L["bwd"], size=11, fill=GRAYL))
    p.append(text(cxp, 244, L["axis"], size=11, fill=GRAY))
    p.append(text(cxp, 274, "P(t) = P(T−t)", size=12, cls="mono", fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig12_회문_{lang}", OUT, W, H)


def main() -> None:
    for lang in ("ko", "en"):
        fig10(lang); fig11(lang); fig12(lang)


if __name__ == "__main__":
    main()
