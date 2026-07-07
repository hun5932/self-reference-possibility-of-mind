"""Fig13 괴델 명제 G의 자기참조 구조 — 흑백 학술본 KO/EN.

수직 flow: 형식체계 P → (산술화) → G(자기참조 루프) → 메타-진리(불완전성).
흰 박스·검정선. mono = 실제 노테이션(¬Prov(⌜G⌝)·sub(13,17,13)) 전용. bare.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, WHITE, svg_doc, arrow_marker, text, box, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def build(lang: str):
    from labels import FIG13, FIG13_N
    L = FIG13[lang]
    N = FIG13_N
    W, H = 1000, 660
    bx, bw, cx = 300, 440, 520
    p = [arrow_marker()]

    # 좌측 단계 레일 (회색 라벨만)
    rail_y = [88, 311, 550]
    for k, ry in enumerate(rail_y):
        p.append(text(272, ry, L["rail"][k], size=12, anchor="end", fill=GRAYL))

    # ── Box1 환원: 형식 체계 P ──
    y1 = 36
    p.append(box(bx, y1, bw, 104))
    p.append(text(cx, y1 + 32, L["sys_title"], size=15.5, weight=600))
    p.append(text(cx, y1 + 58, L["sys_sub"], size=12.5, fill=GRAY))
    p.append(text(cx, y1 + 86, N["sys_note"], size=13, cls="mono", fill=INK))

    # 화살표1 + 산술화 라벨
    p.append(f'<line x1="{cx}" y1="140" x2="{cx}" y2="232" stroke="{INK}" stroke-width="1.1" marker-end="url(#ar)"/>')
    p.append(text(cx + 18, 172, L["arith"], size=12.5, anchor="start", fill=INK))
    p.append(text(cx + 18, 192, N["arith_note"][lang], size=12, anchor="start", cls="mono", fill=GRAY))

    # ── Box2 자기참조: G ──
    y2 = 236
    p.append(box(bx, y2, bw, 150))
    p.append(text(cx, y2 + 38, N["g_title"], size=22, cls="mono", weight=600))
    p.append(text(cx, y2 + 76, L["g_def"], size=14))
    p.append(text(cx, y2 + 112, N["g_formula"], size=15, cls="mono", fill=INK))
    # 자기참조 루프 (오른쪽): G의 괴델수가 G를 지시
    p.append(f'<path d="M {bx+bw} {y2+44} H 800 V {y2+106} H {bx+bw}" fill="none" stroke="{INK}" '
             f'stroke-width="1.1" marker-end="url(#ar)"/>')
    p.append(text(812, y2 + 70, N["loop_note"], size=12.5, anchor="start", cls="mono", fill=INK))
    p.append(text(812, y2 + 90, L["loop_sub"], size=11.5, anchor="start", fill=GRAY))

    # 화살표2
    p.append(f'<line x1="{cx}" y1="386" x2="{cx}" y2="478" stroke="{INK}" stroke-width="1.1" marker-end="url(#ar)"/>')

    # ── Box3 창발: 메타-진리 ──
    y3 = 482
    p.append(box(bx, y3, bw, 128, sw=1.3))
    p.append(text(cx, y3 + 30, L["meta_title"], size=15.5, weight=700))
    p.append(text(cx, y3 + 58, L["meta_line"], size=14))
    p.append(text(cx, y3 + 88, N["meta_formula"][lang], size=14.5, cls="mono", fill=INK))
    p.append(text(cx, y3 + 112, L["meta_sub"], size=12, italic=True, fill=GRAY))

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Fig13_괴델G_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
