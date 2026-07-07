"""바흐 청각영역 도판 — music21 구조 생성 + verovio 정식 조판 + 구조 주석 (흑백 학술본 KO/EN).

논문 도판 목적에 맞춘 하이브리드: 정식 조판 악보(verovio) 위에
구판(build_music.py)의 구조 주석 체계(제목·부제·화살표·괄호·수식 라벨)를 결합.
  Fig10 무한상승: 블록별 이조 라벨(T, T+P4, …) + 되돌아가는 루프 화살표 + ad infinitum
  Fig11 BACH: 음명 매핑(B♭→B … B♮→H) + 자기서명 라벨
  Fig12 게 카논: 성부별 시간 방향 화살표 + P₂(t)=P₁(T−t) (주제+역행 — 회문 아님)
music21(Stream·이조·역행) → MusicXML → verovio(SVG) → 주석 합성 → Playwright PNG/PDF.
바흐=퍼블릭도메인 → 자체 보표 자유. 외부 LilyPond/MuseScore 불필요.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

import verovio
from music21 import clef, interval, key, meter, note, stream
from music21.musicxml.m21ToXml import GeneralObjectExporter

from style_academic import GRAY, GRAYL, INK, RULE, arrow_marker, render, svg_doc, text

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
RES = r"C:\verovio_data"   # ASCII 경로(한글 venv 경로를 verovio 네이티브가 못 읽음)

VEROVIO_OPTS = {
    "pageWidth": 2400, "scale": 55,
    "adjustPageHeight": True, "adjustPageWidth": True,
    "header": "none", "footer": "none", "breaks": "none",
    "pageMarginTop": 20, "pageMarginBottom": 20,
    "pageMarginLeft": 30, "pageMarginRight": 30,
}

# 도판별 한/영 라벨 — f12 부제는 음악학 정정 반영(회문 X, 주제+역행 O)
ANN = {
    "ko": {
        "f10_t": "무한상승 카논 (Canon per Tonos)",
        "f10_s": "동일 동기가 매 반복 완전4도(+P4)씩 상승 — 끝없이 오른다",
        "f10_loop": "반복 (ad infinitum)",
        "f11_t": "B–A–C–H 모티프",
        "f11_s": "작곡가의 이름이 음높이로 — 음악 안의 자기서명(self-signature)",
        "f11_map": "독일 음명:  B♭ = B,   A = A,   C = C,   B♮ = H",
        "f12_t": "게 카논 (Crab Canon)",
        "f12_s": "주제와 그 역행(retrograde)의 동시 결합 — 시간 역전 자기참조",
        "f12_fwd": "주제 (시간 순방향)",
        "f12_bwd": "역행 (시간 역방향)",
        "f12_rel": "P₂(t) = P₁(T − t)",
        "p_theme": "주제", "p_retro": "역행",
    },
    "en": {
        "f10_t": "Endlessly Rising Canon (Canon per Tonos)",
        "f10_s": "the same motif rises a perfect fourth (+P4) each cycle — ascending forever",
        "f10_loop": "repeat (ad infinitum)",
        "f11_t": "The B–A–C–H Motif",
        "f11_s": "the composer's name as pitch — a self-signature inside the music",
        "f11_map": "German note names:  B♭ = B,   A = A,   C = C,   B♮ = H",
        "f12_t": "Crab Canon",
        "f12_s": "the theme combined with its own retrograde — self-reference by time reversal",
        "f12_fwd": "theme (forward in time)",
        "f12_bwd": "retrograde (backward in time)",
        "f12_rel": "P₂(t) = P₁(T − t)",
        "p_theme": "theme", "p_retro": "retrograde",
    },
}


def _ensure_resources():
    """verovio data를 ASCII 경로로 복사(최초 1회). 한글 경로 네이티브 제약 회피."""
    if os.path.isdir(RES) and os.path.isfile(os.path.join(RES, "Bravura.xml")):
        return
    src = os.path.join(os.path.dirname(verovio.__file__), "data")
    if os.path.isdir(RES):
        shutil.rmtree(RES)
    shutil.copytree(src, RES)


def to_svg(s) -> tuple[str, float, float]:
    """music21 Stream → verovio SVG. (svg 본문, 원폭 px, 원높이 px) 반환."""
    _ensure_resources()
    xml = GeneralObjectExporter(s).parse().decode("utf-8")
    tk = verovio.toolkit(False)
    tk.setResourcePath(RES)
    tk.setOptions(VEROVIO_OPTS)      # dict 직접(json.dumps 아님)
    tk.loadData(xml)
    svg = tk.renderToSVG(1)
    svg = svg[svg.index("<svg"):]    # xml 프롤로그 제거
    m = re.search(r'width="([\d.]+)px"\s+height="([\d.]+)px"', svg)
    iw, ih = float(m.group(1)), float(m.group(2))
    return svg, iw, ih


def embed(svg: str, iw: float, ih: float, x: float, y: float, w: float) -> tuple[str, float]:
    """조판 SVG를 외부 문서 (x,y)에 폭 w로 벡터 스케일 삽입. (조각, 표시높이) 반환.

    주의: verovio CSS는 루트 svg의 id로 스코프됨(#id path{stroke:currentColor}) —
    id를 보존하지 않으면 오선·세로줄 등 스트로크 요소가 전부 사라진다."""
    h = ih * (w / iw)
    mid = re.search(r'^<svg[^>]*\bid="([^"]+)"', svg)
    id_attr = f'id="{mid.group(1)}" ' if mid else ""
    head = re.sub(r'^<svg[^>]*>',
                  f'<svg {id_attr}x="{x}" y="{y}" width="{w}" height="{h}" '
                  f'viewBox="0 0 {iw} {ih}" preserveAspectRatio="xMidYMid meet" '
                  f'xmlns="http://www.w3.org/2000/svg" '
                  f'xmlns:xlink="http://www.w3.org/1999/xlink" overflow="visible">',
                  svg, count=1)
    return head, h


def header(cxp: float, title: str, sub: str) -> str:
    """구판 build_music.py와 동일한 제목·부제·괘선 헤더."""
    return (text(cxp, 40, title, size=15, weight=600)
            + text(cxp, 62, sub, size=11.5, italic=True, fill=GRAY)
            + f'<line x1="{cxp - 290}" y1="76" x2="{cxp + 290}" y2="76" '
              f'stroke="{RULE}" stroke-width="0.8"/>')


def part(pitches, lyrics=None, ts="4/4", ql=1.0, name=None):
    s = stream.Part()
    if name:
        s.partName = name
        s.partAbbreviation = name
    s.append(clef.TrebleClef())
    s.append(key.KeySignature(0))
    s.append(meter.TimeSignature(ts))
    ns = []
    for p in pitches:
        n = note.Note(p, quarterLength=ql)
        s.append(n); ns.append(n)
    if lyrics:
        for n, ly in zip(ns, lyrics):
            if ly:
                n.addLyric(ly)
    return s


def _part_rhythm(pairs, name=None):
    """(pitch, quarterLength) 쌍으로 성부 생성."""
    s = stream.Part()
    if name:
        s.partName = name
        s.partAbbreviation = name
    s.append(clef.TrebleClef())
    s.append(key.KeySignature(0))
    s.append(meter.TimeSignature("4/4"))
    for p, ql in pairs:
        s.append(note.Note(p, quarterLength=ql))
    return s


# ── Fig11: BACH 모티프 — 조판 + 음명 매핑 주석 ─────────────────────────
def fig_bach(lang):
    L = ANN[lang]
    sc = part(["B-4", "A4", "C5", "B4"], lyrics=["B", "A", "C", "H"], ql=2.0)
    svg, iw, ih = to_svg(sc)
    W = 660
    piece, sh = embed(svg, iw, ih, (W - 480) / 2, 96, 480)
    y_after = 96 + sh
    body = (header(W / 2, L["f11_t"], L["f11_s"]) + piece
            + text(W / 2, y_after + 26, L["f11_map"], size=12, cls="mono", fill=GRAY)
            + text(W / 2, y_after + 50, "B – A – C – H", size=14, cls="mono",
                   weight=500, ls=2))
    H = y_after + 72
    render(svg_doc(W, H, body), f"Fig11_BACH_music21_{lang}", OUT, W, H)


# ── Fig12: 게 카논 — 조판(주제+역행 2성부) + 시간 방향 화살표 주석 ──────
def fig_crab(lang):
    L = ANN[lang]
    # 비대칭 주제(윤곽·리듬 비대칭) → 역행이 명확한 시간 거울상
    theme = [("C5", 1), ("E-5", 0.5), ("G5", 0.5), ("C6", 2),
             ("B-5", 1), ("A-5", 0.5), ("F5", 0.5), ("D5", 2)]      # 합=8 (2마디)
    retro = list(reversed(theme))                                    # 음정+리듬 역행
    sc = stream.Score()
    sc.insert(0, _part_rhythm(theme, L["p_theme"]))
    sc.insert(0, _part_rhythm(retro, L["p_retro"]))
    svg, iw, ih = to_svg(sc)
    W = 660
    piece, sh = embed(svg, iw, ih, (W - 560) / 2, 112, 560)
    y0, y1 = 112, 112 + sh
    cxp = W / 2
    ax0, ax1 = cxp - 180, cxp + 180
    body = (arrow_marker() + header(cxp, L["f12_t"], L["f12_s"]) + piece
            # 위 성부: 시간 순방향 →
            + f'<line x1="{ax0}" y1="{y0 - 12}" x2="{ax1}" y2="{y0 - 12}" '
              f'stroke="{INK}" stroke-width="1" marker-end="url(#ar)"/>'
            + text(cxp, y0 - 20, L["f12_fwd"], size=11, fill=GRAYL)
            # 아래 성부: 시간 역방향 ←
            + f'<line x1="{ax1}" y1="{y1 + 14}" x2="{ax0}" y2="{y1 + 14}" '
              f'stroke="{INK}" stroke-width="1" marker-end="url(#ar)"/>'
            + text(cxp, y1 + 34, L["f12_bwd"], size=11, fill=GRAYL)
            + text(cxp, y1 + 60, L["f12_rel"], size=12.5, cls="mono", fill=GRAY))
    H = y1 + 82
    render(svg_doc(W, H, body), f"Fig12_회문_music21_{lang}", OUT, W, H)


# ── Fig10: 무한상승 — 조판(+P4 연속 상승) + 블록 이조 라벨 + 루프 화살표 ─
def fig_rising(lang):
    L = ANN[lang]
    s = stream.Part()
    s.append(clef.TrebleClef())
    s.append(key.KeySignature(0))
    s.append(meter.TimeSignature("4/4"))
    motif = ["C5", "D5", "E5", "F5"]            # 상행 4음 동기(완전4도 폭)
    for blk in range(5):                          # 5회: 매번 +P4(5반음) → 연속 상승
        for m in motif:
            p = note.Note(m).transpose(interval.Interval(5 * blk))
            s.append(note.Note(p.nameWithOctave, quarterLength=1))
    svg, iw, ih = to_svg(s)
    W = 660
    sx, sw_ = 24, 612
    piece, sh = embed(svg, iw, ih, sx, 112, sw_)
    y0, y1 = 112, 112 + sh
    cxp = W / 2
    # 블록 라벨: 클레프·조표 리드 영역(약 7%) 이후를 5등분
    lead = sx + sw_ * 0.07
    bw = (sx + sw_ - lead) / 5
    tags = ["T", "T+P4", "T+2·P4", "T+3·P4", "T+4·P4"]
    labels = []
    for b, tag in enumerate(tags):
        x0, x1 = lead + b * bw + 4, lead + (b + 1) * bw - 4
        labels.append(
            f'<path d="M {x0} {y0 - 6} L {x0} {y0 - 12} L {x1} {y0 - 12} L {x1} {y0 - 6}" '
            f'fill="none" stroke="{GRAYL}" stroke-width="0.9"/>'
            + text((x0 + x1) / 2, y0 - 18, tag, size=10.5, cls="mono", fill=GRAY))
    # 루프 화살표: 마지막 블록 → 첫 블록 (점선, 악보 아래)
    loop = (f'<path d="M {lead + 4.6 * bw} {y1 + 6} C {lead + 4.6 * bw} {y1 + 40}, '
            f'{lead + 0.4 * bw} {y1 + 40}, {lead + 0.4 * bw} {y1 + 12}" fill="none" '
            f'stroke="{INK}" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#ar)"/>'
            + text(cxp, y1 + 56, L["f10_loop"], size=11, italic=True, fill=GRAYL))
    body = (arrow_marker() + header(cxp, L["f10_t"], L["f10_s"]) + piece
            + "".join(labels) + loop)
    H = y1 + 72
    render(svg_doc(W, H, body), f"Fig10_무한상승_music21_{lang}", OUT, W, H)


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "bach"
    fn = {"bach": fig_bach, "crab": fig_crab, "rising": fig_rising}[which]
    for lang in ("ko", "en"):
        fn(lang)
