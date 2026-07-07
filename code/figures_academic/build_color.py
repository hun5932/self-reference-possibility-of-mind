"""컬러 학술본 — 색이 정보를 더하는 도판만 (절제된 4영역/영역 색, 흰 배경, glow·장식 없음).

대상: Fig18(4영역 동형)·Table1(4영역 매트릭스)·Fig17(계산 accent)·Fig14·Fig16(데이터).
그 외(타일·쌍곡·펜로즈·괴델·보표 등)는 색이 불필요 → 흑백본 사용.
산출: 05_FIG_도판/도판_학술본_컬러/
"""
from __future__ import annotations

from pathlib import Path

from style_academic import (INK, GRAY, GRAYL, RULE, SOFT, WHITE, DOMAIN, DOMAIN_SOFT,
                            svg_doc, text, box, render)

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본_컬러"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
OUT.mkdir(parents=True, exist_ok=True)
DK = ["visual", "auditory", "logical", "compute"]


# ── Fig18 컬러 (4영역 색) ──────────────────────────────────────────────
def fig18(lang):
    from labels import FIG18, STAGE3
    L, ST = FIG18[lang], STAGE3[lang]
    W, H = 1000, 720
    bw, bh = 400, 150
    quads = [(30, 40), (570, 40), (30, 530), (570, 530)]
    corners = [(430, 190), (570, 190), (430, 530), (570, 530)]
    ncx, ncy, nr = 500, 360, 88
    em = DOMAIN["emergence"]
    p = []
    for cxp, cyp in corners:
        p.append(f'<line x1="{cxp}" y1="{cyp}" x2="{ncx}" y2="{ncy}" stroke="{RULE}" stroke-width="1" stroke-dasharray="3 4"/>')
        ex, ey = cxp + (ncx - cxp) * 0.40, cyp + (ncy - cyp) * 0.40
        p.append(f'<rect x="{ex-9}" y="{ey-11}" width="18" height="18" fill="{WHITE}"/>')
        p.append(text(ex, ey + 4, "≅", size=15, fill=em))
    for qi, (x, y) in enumerate(quads):
        col = DOMAIN[DK[qi]]
        p.append(box(x, y, bw, bh, sw=1.4, fill=DOMAIN_SOFT[DK[qi]], stroke=col))
        p.append(text(x + bw / 2, y + 30, L["domains"][qi], size=15, weight=700, fill=col))
        p.append(f'<line x1="{x+26}" y1="{y+42}" x2="{x+bw-26}" y2="{y+42}" stroke="{col}" stroke-width="1"/>')
        for k in range(3):
            ly = y + 72 + k * 26
            p.append(text(x + 96, ly, ST[k], size=11, anchor="end", fill=GRAY))
            p.append(text(x + 106, ly, L["cells"][qi][k], size=12.5, anchor="start", fill=INK))
    p.append(f'<circle cx="{ncx}" cy="{ncy}" r="{nr}" fill="{DOMAIN_SOFT["emergence"]}" stroke="{em}" stroke-width="1.6"/>')
    p.append(text(ncx, ncy - 26, L["center"][0], size=12.5, fill=GRAY))
    p.append(f'<line x1="{ncx-54}" y1="{ncy-14}" x2="{ncx+54}" y2="{ncy-14}" stroke="{em}" stroke-width="0.9"/>')
    p.append(text(ncx, ncy + 8, L["center"][1], size=17, weight=700, fill=em))
    p.append(text(ncx, ncy + 32, f'({L["center"][2]})', size=11.5, italic=True, fill=GRAY))
    render(svg_doc(W, H, "".join(p)), f"Fig18_TRIH통합_{lang}", OUT, W, H)


# ── Table1 컬러 (영역 색 헤더) ─────────────────────────────────────────
def table1(lang):
    from labels import TABLE1
    L = TABLE1[lang]
    x0, c0, cw = 20, 160, 232
    xs = [x0, x0 + c0, x0 + c0 + cw, x0 + c0 + 2 * cw, x0 + c0 + 3 * cw, x0 + c0 + 4 * cw]
    W = xs[-1] + 20
    hy, hh, rh = 18, 60, 108
    ys = [hy, hy + hh, hy + hh + rh, hy + hh + 2 * rh, hy + hh + 3 * rh]
    H = ys[-1] + 18
    p = [f'<rect x="{x0}" y="{hy}" width="{xs[-1]-x0}" height="{hh}" fill="{SOFT}"/>']
    for c in range(4):
        p.append(f'<rect x="{xs[c+1]}" y="{hy}" width="{cw}" height="{hh}" fill="{DOMAIN_SOFT[DK[c]]}"/>')
    for xv in xs:
        p.append(f'<line x1="{xv}" y1="{hy}" x2="{xv}" y2="{ys[-1]}" stroke="{INK}" stroke-width="1"/>')
    for i, yv in enumerate(ys):
        sw = 1.2 if i in (0, 1, len(ys) - 1) else 1
        p.append(f'<line x1="{x0}" y1="{yv}" x2="{xs[-1]}" y2="{yv}" stroke="{INK}" stroke-width="{sw}"/>')
    p.append(text((xs[0] + xs[1]) / 2, hy + 37, L["corner"], size=12.5, fill=GRAY))
    for c in range(4):
        col = DOMAIN[DK[c]]
        p.append(text((xs[c + 1] + xs[c + 2]) / 2, hy + 37, L["cols"][c], size=13.5, weight=600, fill=col))
        p.append(f'<line x1="{xs[c+1]+6}" y1="{hy+hh-1}" x2="{xs[c+2]-6}" y2="{hy+hh-1}" stroke="{col}" stroke-width="2.5"/>')
    for r in range(3):
        rtop = ys[r + 1]
        p.append(text((xs[0] + xs[1]) / 2, rtop + rh / 2 + 5, L["rows"][r], size=14, weight=700))
        for c in range(4):
            cxm = (xs[c + 1] + xs[c + 2]) / 2
            t, note = L["cells"][r][c]
            p.append(text(cxm, rtop + 44, t, size=12.5, fill=INK))
            p.append(text(cxm, rtop + 70, note, size=10.5, cls="mono", fill=GRAYL))
    render(svg_doc(W, H, "".join(p)), f"Table1_동형성매트릭스_{lang}", OUT, W, H)


# ── Fig17 컬러 (계산 영역 teal accent) ─────────────────────────────────
def fig17(lang):
    from build_fig17 import build
    svg, W, H = build(lang, accent=DOMAIN["compute"])
    render(svg, f"Fig17_귀속그래프_{lang}", OUT, W, H)


# ── 데이터 figs 컬러 (matplotlib) ──────────────────────────────────────
def _mpl(lang):
    import matplotlib as mpl
    serif = (["Noto Serif KR", "Batang", "DejaVu Serif"] if lang == "ko" else ["Source Serif 4", "DejaVu Serif"])
    mpl.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
                         "font.family": "serif", "font.serif": serif, "axes.edgecolor": "#1A1A1A",
                         "axes.labelcolor": "#1A1A1A", "text.color": "#1A1A1A", "xtick.color": "#1A1A1A",
                         "ytick.color": "#1A1A1A", "axes.linewidth": 0.8, "axes.unicode_minus": False})


def data_figs(lang):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from labels import DATA
    _mpl(lang)
    D = DATA[lang]
    teal, violet = DOMAIN["compute"], DOMAIN["emergence"]

    # Fig14 어텐션 (teal cmap)
    toks = ["The", "cat", "sat", "on", "the", "cat"]
    n = len(toks)
    rng = np.random.default_rng(7)
    a = rng.uniform(0, 0.08, (n, n))
    for i in range(n):
        a[i, max(0, i - 1)] += 0.5
        if toks[i] in toks[:i]:
            a[i, toks.index(toks[i])] += 0.6
    a = np.tril(a); a = a / a.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(4.6, 4.3))
    im = ax.imshow(a, cmap="BuGn", vmin=0, vmax=a.max())
    ax.set_xticks(range(n), toks, rotation=45, ha="right"); ax.set_yticks(range(n), toks)
    ax.set_xlabel(D["attn_x"]); ax.set_ylabel(D["attn_y"])
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label(D["attn_w"]); cb.outline.set_linewidth(0.6)
    ax.text(0.5, -0.34, D["attn_note"], transform=ax.transAxes, ha="center", fontsize=8, color="#555")
    for ext in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"Fig14_어텐션_{lang}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Fig16 스케일링 (teal 곡선 + violet 임계)
    x = np.logspace(8, 12, 200); thr = 1e10
    y = 1 / (1 + np.exp(-(np.log10(x) - np.log10(thr)) * 3))
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    ax.semilogx(x, y, color=teal, lw=2.2)
    ax.axvline(thr, color=violet, ls="--", lw=1.2)
    ax.text(thr * 1.25, 0.04, D["scal_thr"], color=violet, fontsize=9)
    ax.text(x[35], 0.13, D["scal_plateau"], color="#555", fontsize=9)
    ax.text(x[150], 0.88, D["scal_emerg"], color=teal, fontsize=9)
    ax.set_xlabel(D["scal_x"]); ax.set_ylabel(D["scal_y"]); ax.set_ylim(0, 1.05)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"Fig16_스케일링_{lang}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[color-data] Fig14·Fig16 ({lang})")


def main() -> None:
    for lang in ("ko", "en"):
        fig18(lang); table1(lang); fig17(lang); data_figs(lang)


if __name__ == "__main__":
    main()
