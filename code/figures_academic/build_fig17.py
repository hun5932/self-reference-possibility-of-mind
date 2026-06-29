"""Fig17 자체생성 — 귀속 그래프(attribution graph) 양식의 자기참조 회로 (흑백 학술본 KO/EN).

Anthropic 2025 attribution graph는 외부 자료(라이선스 불명) → 자체생성본.
노드=특징(supernode), 엣지=인과(실선 정보흐름·점선 간접). induction(자기참조) 회로 재구성.
(억제 엣지는 기본 induction 회로에 없으므로 범례에서 제외 — 2026-06-28 정정.)
accent 인자로 컬러 학술본(계산 영역 teal)도 생성 가능.
"""
from __future__ import annotations

import math
from pathlib import Path

from style_academic import INK, GRAY, GRAYL, RULE, WHITE, DOMAIN, svg_doc, arrow_marker, text, render

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])


def _edge(c1, c2, dash=False, inhibit=False, accent=INK, off=26):
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    x1, y1 = c1[0] + ux * off, c1[1] + uy * off
    x2, y2 = c2[0] - ux * (off + 6), c2[1] - uy * (off + 6)
    da = ' stroke-dasharray="3 4"' if dash else ""
    s = [f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{accent}" stroke-width="1.2"{da}'
         + ("/>" if inhibit else ' marker-end="url(#ar)"/>')]
    if inhibit:  # T-end (억제)
        px, py = -uy, ux
        s.append(f'<line x1="{x2-px*7:.0f}" y1="{y2-py*7:.0f}" x2="{x2+px*7:.0f}" y2="{y2+py*7:.0f}" stroke="{accent}" stroke-width="1.6"/>')
    return "".join(s)


def build(lang: str, accent: str = INK):
    from labels import FIG17
    L = FIG17[lang]
    W, H = 920, 580
    bw, bh = 168, 46
    soft = accent != INK

    def node(cx, cy, label, strong=False):
        sw = 1.6 if strong else 1.1
        col = accent if strong else INK
        return (f'<rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="4" fill="{WHITE}" '
                f'stroke="{col}" stroke-width="{sw}"/>' + text(cx, cy + 4, label, size=12.5,
                weight=(700 if strong else None), fill=(accent if strong else INK)))

    # 좌표 (center)
    a_prev, b_prev, a_cur = (170, 470), (460, 470), (740, 470)
    prev_f, ind_f = (280, 300), (590, 300)
    out_n = (460, 130)

    edges = [
        _edge(a_prev, prev_f, accent=accent),
        _edge(prev_f, ind_f, accent=accent),
        _edge(a_cur, ind_f, accent=accent),
        _edge(b_prev, out_n, accent=accent),
        _edge(ind_f, out_n, accent=accent),
    ]
    p = [arrow_marker("ar", accent), "".join(edges)]
    # 자기참조 엣지 (점선 곡선): ind_f → b_prev
    p.append(f'<path d="M {ind_f[0]} {ind_f[1]+26} C {ind_f[0]} {ind_f[1]+130}, {b_prev[0]+40} {b_prev[1]-130}, '
             f'{b_prev[0]+30} {b_prev[1]-26}" fill="none" stroke="{accent}" stroke-width="1.2" '
             f'stroke-dasharray="3 4" marker-end="url(#ar)"/>')
    p.append(text((ind_f[0] + b_prev[0]) / 2 + 70, (ind_f[1] + b_prev[1]) / 2, L["selfref"], size=11, fill=GRAY))

    # 노드
    p.append(node(*a_prev, L["a_prev"]))
    p.append(node(*b_prev, L["b_prev"]))
    p.append(node(*a_cur, L["a_cur"]))
    p.append(node(*prev_f, L["prev_feat"]))
    p.append(node(*ind_f, L["ind_feat"], strong=True))
    p.append(node(*out_n, L["out"], strong=True))

    # 범례
    ly = 540
    p.append(f'<line x1="60" y1="{ly}" x2="100" y2="{ly}" stroke="{INK}" stroke-width="1.2" marker-end="url(#ar)"/>')
    p.append(text(108, ly + 4, L["leg"][0], size=10.5, anchor="start", fill=GRAY))
    p.append(f'<line x1="250" y1="{ly}" x2="290" y2="{ly}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="3 4" marker-end="url(#ar)"/>')
    p.append(text(298, ly + 4, L["leg"][1], size=10.5, anchor="start", fill=GRAY))
    # (억제 ⊣ 범례 제거 — 다이어그램에 억제 엣지가 없어 고아 항목이었음, 2026-06-28)

    return svg_doc(W, H, "".join(p)), W, H


def main() -> None:
    for lang in ("ko", "en"):
        svg, W, H = build(lang)
        render(svg, f"Fig17_귀속그래프_{lang}", OUT, W, H)


if __name__ == "__main__":
    main()
