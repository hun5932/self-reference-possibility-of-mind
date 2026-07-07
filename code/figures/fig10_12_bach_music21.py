"""도판 10-12 — 바흐 자기참조 보표 분석 (§4 청각).

듀얼트랙: Python(music21) = authoritative (실제 악보 정량·렌더).
CD = illustrative 형식 도식 (회문 축·상승 나선·BACH 노트헤드).

도판
----
- 도판 10: Crab Canon (BWV 1079) — 회문(palindrome) 대칭 분석
- 도판 11: Endlessly Rising Canon — 조성 상승(Shepard) 분석
- 도판 12: Art of Fugue Contrapunctus XIV — BACH 모티프(B♭-A-C-B♮) 탐지

⚠️ 악보 = public domain (바흐, 저작권 만료). MusicXML/MIDI는 IMSLP 등에서 확보 → assets-to-upload.md.
⚠️ music21은 보표 렌더에 MuseScore/LilyPond 백엔드가 필요할 수 있음 (README 참조).

실행: python fig10_12_bach_music21.py  (먼저 SCORE 경로 지정)
"""
from __future__ import annotations

from pathlib import Path

# music21은 venv에 설치됨 (1.7_Research_TRIH_연구). import는 main에서 (무거움).

SCORES = {
    "fig10_crab_canon": None,        # TODO: Path(".../bwv1079_crab.musicxml")
    "fig11_endlessly_rising": None,  # TODO
    "fig12_art_of_fugue_xiv": None,  # TODO
}


def bach_motif_present(stream) -> bool:
    """BACH 모티프(B♭=Bb, A, C, B♮=B) 음렬이 존재하는지 간단 탐지."""
    from music21 import note
    names = [n.name for n in stream.recurse().notes if isinstance(n, note.Note)]
    target = ["B-", "A", "C", "B"]   # music21 표기: B-=B♭, B=B♮
    return any(names[i:i + 4] == target for i in range(len(names) - 3))


def analyze(name: str, path: Path | None) -> None:
    if path is None:
        print(f"[{name}] SCORE 미지정 — assets-to-upload.md에서 MusicXML 확보 후 SCORES에 경로 지정")
        return
    from music21 import converter
    s = converter.parse(str(path))
    print(f"[{name}] 마디 수={len(s.recurse().getElementsByClass('Measure'))}, "
          f"음표 수={len(s.recurse().notes)}, BACH 모티프={bach_motif_present(s)}")
    # TODO: 회문/상승 정량 + s.write('musicxml.png', fp=...) 로 보표 PNG 렌더
    #       (trih_style 색은 보표 주석 오버레이에 활용)


def main() -> None:
    for name, path in SCORES.items():
        analyze(name, path)


if __name__ == "__main__":
    main()
