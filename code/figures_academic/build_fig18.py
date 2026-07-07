"""Fig18 TRIH 통합 — 4영역의 재귀적 동형 (흑백 학술본 KO/EN).

4 사분면(흰칸+영역명+단계별 사례) ─ ≅ 연결 ─ 중앙 노드(자기참조의 임계 / 마음의 가능성, 조건부).
색·glow·이모지 없음. bare diagram.
"""
from __future__ import annotations

from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, WHITE, svg_doc, text, box, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def build(lang: str):
    from labels import FIG18, STAGE3
    L = FIG18[lang]
    ST = STAGE3[lang]
    W, H = 1000, 720
    bw, bh = 400, 150
    quads = [(30, 40), (570, 40), (30, 530), (570, 530)]      # TL TR BL BR = 시각 청각 논리 계산
    corners = [(430, 190), (570, 190), (430, 530), (570, 530)]  # 노드 방향 안쪽 모서리
    ncx, ncy, nr = 500, 360, 88
    p = []

    # ── 동형성 연결선 (먼저, 노드 원이 안쪽을 덮음) ──
    for (cxp, cyp) in corners:
        p.append(f'<line x1="{cxp}" y1="{cyp}" x2="{ncx}" y2="{ncy}" stroke="{RULE}" stroke-width="1" stroke-dasharray="3 4"/>')
        # ≅ 기호: 모서리→노드 0.40 지점
        ex = cxp + (ncx - cxp) * 0.40
        ey = cyp + (ncy - cyp) * 0.40
        p.append(f'<rect x="{ex-9}" y="{ey-11}" width="18" height="18" fill="{WHITE}"/>')
        p.append(text(ex, ey + 4, "≅", size=15, fill=GRAY))

    # ── 사분면 ──
    for qi, (x, y) in enumerate(quads):
        p.append(box(x, y, bw, bh, sw=1.1))
        p.append(text(x + bw / 2, y + 30, L["domains"][qi], size=15, weight=700))
        p.append(f'<line x1="{x+26}" y1="{y+42}" x2="{x+bw-26}" y2="{y+42}" stroke="{RULE}" stroke-width="0.8"/>')
        for k in range(3):
            ly = y + 72 + k * 26
            p.append(text(x + 96, ly, ST[k], size=11, anchor="end", fill=GRAYL))
            p.append(text(x + 106, ly, L["cells"][qi][k], size=12.5, anchor="start", fill=INK))

    # ── 중앙 노드 ──
    p.append(f'<circle cx="{ncx}" cy="{ncy}" r="{nr}" fill="{WHITE}" stroke="{INK}" stroke-width="1.4"/>')
    p.append(text(ncx, ncy - 26, L["center"][0], size=12.5, fill=GRAY))
    p.append(f'<line x1="{ncx-54}" y1="{ncy-14}" x2="{ncx+54}" y2="{ncy-14}" stroke="{RULE}" stroke-width="0.8"/>')
    p.append(text(ncx, ncy + 8, L["center"][1], size=17, weight=700))
    p.append(text(ncx, ncy + 32, f'({L["center"][2]})', size=11.5, italic=True, fill=GRAY))

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Fig18_TRIH통합_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
