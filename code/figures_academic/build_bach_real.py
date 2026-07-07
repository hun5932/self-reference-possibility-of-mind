# -*- coding: utf-8 -*-
"""바흐 실물 도판 시안 (Phase 2) — 검증된 실제 악보 데이터만 사용 (수기 입력 0).

입력(전부 verify_bach_real.py가 검증·생성):
  data_bach/crab_encoded.json      게 카논 voice1 (Knuth MIDI, 역행대칭 PASS)
  data_bach/pertonos_encoded.json  per tonos 1주기 + 조성 사다리 (장2도 assert PASS)
  data_bach/artfugue-019.krn       Cp.XIV (BACH m.193 assert PASS)
  data_bach/ricercar_entries.json  리체르카레 진입 11회 (제시부 6성부 PASS)

산출: 05_FIG_도판/바흐_실물_시안/  (정본 불침범)
  Fig10R_무한상승_실물 · Fig11R_BACH_실물 · Fig12R_게카논_실물 · Fig12bR_리체르카레_진입지도
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from music21 import clef, converter, key, meter, note, stream

import build_bach_music21 as bm
from style_academic import GRAY, GRAYL, INK, RULE, arrow_marker, render, svg_doc, text

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "바흐_실물_시안"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
OUT.mkdir(parents=True, exist_ok=True)
DATA = Path(__file__).resolve().parent / "data_bach"

ANN = {
    "ko": {
        "f10_t": "무한상승 카논 (Canon a 2 per tonos) — 『음악의 헌정』 BWV 1079",
        "f10_s": "왕의 주제 위 2성 카논 — 매 주기 장2도 상승, 6주기 뒤 옥타브 위 원조 회귀 (제1주기)",
        "f10_ladder": "c → d → e → f♯ → g♯ → b♭ → c′  (장2도 사다리)",
        "f10_loop": "반복마다 +M2 (ad infinitum)",
        "f10_insc": "“Ascendenteque Modulatione ascendat Gloria Regis” — 원보 명문",
        "f10_canon": "카논", "f10_theme": "왕의 주제",
        "f11_t": "푸가의 기법 Contrapunctus XIV — B–A–C–H 진입 (mm.191–196)",
        "f11_s": "제3주제 = 작곡가 이름의 음명 서명 · 악보는 m.239에서 끊김(미완)",
        "f12_t": "게 카논 (Canon a 2 cancrizans) — 『음악의 헌정』 BWV 1079",
        "f12_s": "왕의 주제로 여는 18마디 선율과 그 역행의 동시 결합 — 시간 역전 자기참조",
        "f12_fwd": "선율 전체 (시간 순방향)",
        "f12_bwd": "같은 선율의 역행 (시간 역방향)",
        "f12_rel": "P₂(t) = P₁(T − t)",
        "p_fwd": "정행", "p_bwd": "역행",
    },
    "en": {
        "f10_t": "Endlessly Rising Canon (Canon a 2 per tonos) — Musical Offering, BWV 1079",
        "f10_s": "two-voice canon over the royal theme — rises a major second each cycle, returning an octave higher after six (cycle 1)",
        "f10_ladder": "c → d → e → f♯ → g♯ → b♭ → c′  (whole-tone ladder)",
        "f10_loop": "repeat at +M2 (ad infinitum)",
        "f10_insc": "“Ascendenteque Modulatione ascendat Gloria Regis” — original inscription",
        "f10_canon": "canon", "f10_theme": "royal theme",
        "f11_t": "The Art of Fugue, Contrapunctus XIV — the B–A–C–H entry (mm.191–196)",
        "f11_s": "third subject = the composer's name as pitches · the score breaks off at m.239 (unfinished)",
        "f12_t": "Crab Canon (Canon a 2 cancrizans) — Musical Offering, BWV 1079",
        "f12_s": "the full 18-bar line, opening with the royal theme, combined with its own retrograde",
        "f12_fwd": "the whole line (forward in time)",
        "f12_bwd": "the same line reversed (backward in time)",
        "f12_rel": "P₂(t) = P₁(T − t)",
        "p_fwd": "forward", "p_bwd": "retro",
    },
}


def to_svg_opts(s, opts_override: dict) -> tuple[str, float, float]:
    """build_bach_music21.to_svg와 동일하되 verovio 옵션 오버라이드 허용."""
    import verovio
    from music21.musicxml.m21ToXml import GeneralObjectExporter
    bm._ensure_resources()
    xml = GeneralObjectExporter(s).parse().decode("utf-8")
    tk = verovio.toolkit(False)
    tk.setResourcePath(bm.RES)
    opts = dict(bm.VEROVIO_OPTS)
    opts.update(opts_override)
    tk.setOptions(opts)
    tk.loadData(xml)
    svg = tk.renderToSVG(1)
    svg = svg[svg.index("<svg"):]
    m = re.search(r'width="([\d.]+)px"\s+height="([\d.]+)px"', svg)
    return svg, float(m.group(1)), float(m.group(2))


def part_from(notes_json, name=None, ks=-3, common_time=True):
    """[{n, off, ql}] → music21 Part (c단조 조표, C 박자)."""
    p = stream.Part()
    if name:
        p.partName = name
        p.partAbbreviation = name
    p.insert(0, clef.TrebleClef())
    p.insert(0, key.KeySignature(ks))
    ts = meter.TimeSignature("4/4")
    if common_time:
        ts.symbol = "common"
    p.insert(0, ts)
    for t in notes_json:
        n = note.Note(t["n"], quarterLength=t["ql"])
        p.insert(t["off"], n)
    return p


# ── Fig12R: 게 카논 실물 (18마디 전체 + 역행) ───────────────────────────
def fig_crab(lang):
    L = ANN[lang]
    data = json.loads((DATA / "crab_encoded.json").read_text(encoding="utf-8"))
    v1 = data["voice1"]
    total = 72.0
    v2 = [{"n": t["n"], "off": total - (t["off"] + t["ql"]), "ql": t["ql"]}
          for t in reversed(v1)]
    sc = stream.Score()
    sc.insert(0, part_from(v1, L["p_fwd"]))
    sc.insert(0, part_from(v2, L["p_bwd"]))
    svg, iw, ih = to_svg_opts(sc, {"pageWidth": 2300, "breaks": "auto"})
    W = 660
    piece, sh = embed_w(svg, iw, ih, 24, 116, 612)
    y0, y1 = 116, 116 + sh
    cxp = W / 2
    body = (arrow_marker() + header2(cxp, L["f12_t"], L["f12_s"])
            + piece
            + f'<line x1="{cxp - 180}" y1="{y0 - 12}" x2="{cxp + 180}" y2="{y0 - 12}" '
              f'stroke="{INK}" stroke-width="1" marker-end="url(#ar)"/>'
            + text(cxp, y0 - 20, L["f12_fwd"], size=11, fill=GRAYL)
            + f'<line x1="{cxp + 180}" y1="{y1 + 14}" x2="{cxp - 180}" y2="{y1 + 14}" '
              f'stroke="{INK}" stroke-width="1" marker-end="url(#ar)"/>'
            + text(cxp, y1 + 34, L["f12_bwd"], size=11, fill=GRAYL)
            + text(cxp, y1 + 60, L["f12_rel"], size=12.5, cls="mono", fill=GRAY))
    H = y1 + 82
    render(svg_doc(W, H, body), f"Fig12R_게카논_실물_{lang}", OUT, W, H)


# ── Fig10R: per tonos 실물 (제1주기 3성부 + 조성 사다리) ────────────────
def fig_pertonos(lang):
    L = ANN[lang]
    data = json.loads((DATA / "pertonos_encoded.json").read_text(encoding="utf-8"))
    parts_json = data["cycle1_parts"]
    cut = (int(data["cycle_len_ql"]) // 4) * 4   # 마디 경계로 절단
    sc = stream.Score()
    # 주제(베이스) 식별: 첫 3음 피치클래스 C, E-, G + 최저 음역
    def head(pj):
        return [t["n"].rstrip("0123456789") for t in pj[:3]]
    theme_idx = None
    for i, pj in enumerate(parts_json):
        if head(pj) == ["C", "E-", "G"] and pj[0]["n"].endswith("3"):
            theme_idx = i
    order = [i for i in range(len(parts_json)) if i != theme_idx] + [theme_idx]
    for rank, i in enumerate(order):
        pj = [t for t in parts_json[i] if t["off"] < cut - 1e-6]
        nm = (f"{L['f10_canon']} {rank + 1}" if i != theme_idx else L["f10_theme"])
        p = part_from(pj, nm)
        if i == theme_idx:
            p.replace(p.getElementsByClass(clef.TrebleClef).first(), clef.BassClef())
        sc.insert(0, p)
    svg, iw, ih = to_svg_opts(sc, {"pageWidth": 2300, "breaks": "auto",
                                   "pageMarginLeft": 220})
    W = 660
    piece, sh = embed_w(svg, iw, ih, 24, 112, 612)
    y1 = 112 + sh
    cxp = W / 2
    # 루프 화살표(얕게) → 그 아래 조성 사다리·라벨·명문
    loop = (f'<path d="M {cxp + 230} {y1 + 6} C {cxp + 238} {y1 + 28}, '
            f'{cxp - 238} {y1 + 28}, {cxp - 230} {y1 + 10}" fill="none" '
            f'stroke="{INK}" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#ar)"/>')
    body = (arrow_marker() + header2(cxp, L["f10_t"], L["f10_s"]) + piece + loop
            + text(cxp, y1 + 50, L["f10_ladder"], size=12, cls="mono", fill=INK)
            + text(cxp, y1 + 70, L["f10_loop"], size=10.5, italic=True, fill=GRAYL)
            + text(cxp, y1 + 90, L["f10_insc"], size=10.5, italic=True, fill=GRAY))
    H = y1 + 110
    render(svg_doc(W, H, body), f"Fig10R_무한상승_실물_{lang}", OUT, W, H)


# ── Fig11R: Cp.XIV 발췌 (mm.191–196, BACH 가사 마킹) ────────────────────
def fig_cp14(lang):
    L = ANN[lang]
    af = converter.parse(str(DATA / "artfugue-019.krn"), format="humdrum")
    ex = af.measures(191, 196)
    # 테너(part idx2)의 B♭-A-C-B♮ 4음에 가사 B A C H 부착
    target = ["B-", "A", "C", "B"]
    p2 = list(ex.parts)[2]
    ns = [n for n in p2.flatten().notes if n.isNote]
    for i in range(len(ns) - 3):
        if [ns[i + k].name for k in range(4)] == target:
            for k, ly in enumerate("BACH"):
                ns[i + k].addLyric(ly)
            break
    svg, iw, ih = to_svg_opts(ex, {"pageWidth": 2300, "breaks": "auto"})
    W = 660
    piece, sh = embed_w(svg, iw, ih, 24, 112, 612)
    y1 = 112 + sh
    cxp = W / 2
    note_txt = ("제3주제 진입: 테너, m.193 — 이후 m.239에서 자필보 중단"
                if lang == "ko" else
                "third-subject entry: tenor, m.193 — the autograph breaks off at m.239")
    credit = ("악보 인코딩: C. S. Sapp, github.com/craigsapp/art-of-the-fugue (BGA Band 25.1, 1878 기준)"
              if lang == "ko" else
              "score encoding: C. S. Sapp, github.com/craigsapp/art-of-the-fugue (after BGA Band 25.1, 1878)")
    body = (header2(cxp, L["f11_t"], L["f11_s"]) + piece
            + text(cxp, y1 + 26, "B♭ – A – C – B♮  =  B – A – C – H", size=12,
                   cls="mono", fill=GRAY)
            + text(cxp, y1 + 48, note_txt, size=10.5, italic=True, fill=GRAYL)
            + text(cxp, y1 + 66, credit, size=8.5, fill=GRAYL))
    H = y1 + 82
    render(svg_doc(W, H, body), f"Fig11R_BACH_실물_{lang}", OUT, W, H)


# ── Fig12bR: 리체르카레 진입 지도 + 인과 마스크 (matplotlib, 도14 스타일) ──
# color=True: 컬러 학술본 — 주제/응답=청각 Amber 2단(명도차 grayscale-safe),
#             마스크=BuGn(teal, 도14 컬러판과 동일 계열) → 청각↔계산 평행을 색으로도 표현
def fig_entrymap(lang, color=False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np

    serif = (["Noto Serif KR", "Batang", "Malgun Gothic", "DejaVu Serif"] if lang == "ko"
             else ["Source Serif 4", "DejaVu Serif", "Times New Roman"])
    mpl.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "font.family": "serif", "font.serif": serif,
        "axes.edgecolor": "#1A1A1A", "axes.labelcolor": "#1A1A1A", "text.color": "#1A1A1A",
        "xtick.color": "#1A1A1A", "ytick.color": "#1A1A1A", "axes.linewidth": 0.8,
        "axes.unicode_minus": False, "svg.fonttype": "none",
    })
    ent = json.loads((DATA / "ricercar_entries.json").read_text(encoding="utf-8"))
    # A안(제시부 크롭): 좌측을 제시부 6진입(mm.1–27)으로 한정 — 6진입 ↔ 6×6 마스크 1:1.
    # 전곡 11진입을 다 보이면 우측 6×6과의 평행이 흐려짐(리뷰 방어선).
    EXPO_END = 27
    subj = [tuple(e) for e in ent["subject"] if e[0] <= EXPO_END]
    answ = [tuple(e) for e in ent["answer"] if e[0] <= EXPO_END]
    total_m = EXPO_END + 2
    theme_bars = 4     # 주제 표시 길이 ≈ 제시부 진입 간격(4마디)과 정합
    # y축 = 제시부 진입 순서 (계단 구조가 인과 마스크와 시각적으로 평행하도록)
    expo_order = [p for _, p in sorted(ent["exposition"])]   # [p2,p1,p4,p3,p0,p5]
    row = {p: r for r, p in enumerate(expo_order)}

    lab = {
        "ko": {"voice": "성부", "meas": "마디", "subj": "주제", "answ": "응답(5도)",
               "left": "「6성부 리체르카레」 BWV 1079 — 제시부 주제 진입 (mm.1–27)",
               "right": "인과적 자기집중 마스크",
               "xj": "참조되는 진입 j", "yi": "진입 i",
               "note": "왼쪽: 제시부 6진입 실측(마디·성부, kern 파싱) · 오른쪽: causal mask — 형식적 평행"},
        "en": {"voice": "voice", "meas": "measure", "subj": "subject", "answ": "answer (5th)",
               "left": "Ricercar a 6, BWV 1079 — exposition entries (mm.1–27)",
               "right": "causal self-attention mask",
               "xj": "attended entry j", "yi": "entry i",
               "note": "left: the six exposition entries parsed from the score (kern) · right: causal mask — a formal parallel"},
    }[lang]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(8.6, 3.4), gridspec_kw={"width_ratios": [2.1, 1.0]})
    # 좌: 진입 지도
    for v in range(6):
        ax1.axhline(v, color="#DDDDDD", lw=0.6, zorder=0)
    c_subj = "#B8770A" if color else "#2B2B2B"   # 청각 Amber 진함
    c_answ = "#EBC97F" if color else "#9A9A9A"   # 청각 Amber 연함 (명도차 확보)
    for m, p in subj:
        ax1.barh(row[p], theme_bars, left=m, height=0.52, color=c_subj, zorder=3)
    for m, p in answ:
        ax1.barh(row[p], theme_bars, left=m, height=0.52, color=c_answ, zorder=3)
    ax1.set_yticks(range(6), [f"{lab['voice']} {p + 1}" for p in expo_order])
    ax1.set_ylim(5.7, -0.7)
    ax1.set_xlim(0, total_m + 2)
    ax1.set_xlabel(lab["meas"])
    ax1.set_title(lab["left"], fontsize=10)
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(color=c_subj, label=lab["subj"]),
                        Patch(color=c_answ, label=lab["answ"])],
               loc="upper right", fontsize=8, frameon=False)
    # 우: 하삼각 인과 마스크
    n = 6
    M = np.tril(np.ones((n, n)))
    ax2.imshow(M, cmap=("BuGn" if color else "Greys"), vmin=0, vmax=1.6)
    ax2.set_xticks(range(n), [str(j + 1) for j in range(n)])
    ax2.set_yticks(range(n), [str(i + 1) for i in range(n)])
    ax2.set_xlabel(lab["xj"]); ax2.set_ylabel(lab["yi"])
    ax2.set_title(lab["right"], fontsize=10)
    for i in range(n):
        for j in range(n):
            if j > i:
                ax2.text(j, i, "·", ha="center", va="center", color="#BBBBBB", fontsize=7)
    fig.text(0.5, -0.04, lab["note"], ha="center", fontsize=8.2, color="#555555")
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"Fig12bR_리체르카레_진입지도_{lang}.{ext}", dpi=300,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"[bach_real] Fig12bR_리체르카레_진입지도_{lang}")


# ── 공통 헬퍼 (build_bach_music21의 embed/header 폭 변형) ────────────────
def embed_w(svg, iw, ih, x, y, w):
    return bm.embed(svg, iw, ih, x, y, w)


def header2(cxp, title, sub):
    return (text(cxp, 38, title, size=14, weight=600)
            + text(cxp, 60, sub, size=11, italic=True, fill=GRAY)
            + f'<line x1="{cxp - 300}" y1="76" x2="{cxp + 300}" y2="76" '
              f'stroke="{RULE}" stroke-width="0.8"/>')


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "crab"
    fn = {"crab": fig_crab, "pertonos": fig_pertonos,
          "cp14": fig_cp14, "entrymap": fig_entrymap,
          "entrymap-color": lambda lang: fig_entrymap(lang, color=True)}[which]
    for lang in ("ko", "en"):
        fn(lang)
