# -*- coding: utf-8 -*-
"""바흐 실물 도판 데이터 검증 + 기보용 인코딩 생성 (Phase 1).

소스:
  data_bach/crab_knuth.mid      — 게 카논 (IMSLP #221462, Knuth, c단조 원조성)
  data_bach/pertonos_knuth.mid  — 무한상승 카논 (IMSLP #221466, Knuth, 6주기 전체)
  data_bach/artfugue-019.krn    — Cp.XIV (craigsapp, BGA 1878/1926 기반)
  data_bach/offering-002.krn    — Ricercar a 6 (craigsapp)

검증(assert):
  ① 게 카논: voice2 == retrograde(voice1) (피치클래스+리듬)
  ② 게 카논: 주제 머리 = C E♭ G A♭ B♮ (리체르카레 kern 주제와 교차 일치)
  ③ per tonos: 주기마다 장2도(+2 semitone) 상행, 6주기 후 +12(옥타브)
  ④ Cp.XIV: B♭-A-C-B♮ 첫 진입 m.193 (테너)
  ⑤ Ricercar a 6: 주제 진입 ≥6회 검출(엄격+완화)

산출:
  data_bach/crab_encoded.json      — 게 카논 voice1 (이름/옥타브/박, c단조 재철자)
  data_bach/pertonos_encoded.json  — per tonos 1주기 3성부 + 6주기 조성 사다리
  data_bach/ricercar_entries.json  — 리체르카레 주제 진입 (성부, 마디)
  실행 결과 → 콘솔 (체크리스트 md에 기록)
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from music21 import converter, interval

DATA = Path(__file__).resolve().parent / "data_bach"

# c단조 문맥 이명동음 재철자 (MIDI는 샤프 기본 → 플랫측 보정; F#/B는 유지)
RESPELL = {"G#": "A-", "C#": "D-", "D#": "E-", "A#": "B-"}


def respell(name: str) -> str:
    for k, v in RESPELL.items():
        if name.startswith(k):
            return v + name[len(k):]
    return name


def load_midi_notes(path: Path):
    """MIDI → 파트별 [(이름, 옥타브포함 이름, offset, ql)] (이름은 재철자)."""
    s = converter.parse(str(path))
    parts = []
    for p in s.parts:
        ns = []
        for n in p.flatten().notes:
            pit = n.pitch if n.isNote else max(n.pitches, key=lambda x: x.midi)
            nm = respell(pit.nameWithOctave)
            ns.append((nm, float(n.offset), float(n.quarterLength), pit.midi))
        ns.sort(key=lambda t: t[1])
        parts.append(ns)
    return parts


def pc(nm: str) -> str:
    return nm.rstrip("0123456789")


results = {}

# ── ① ② 게 카논 ─────────────────────────────────────────────────────
crab = [p for p in load_midi_notes(DATA / "crab_knuth.mid") if len(p) > 4]
assert len(crab) == 2, f"게 카논 성부 수 {len(crab)} != 2"
v1, v2 = crab
# 리듬 포함 역행 대칭: (피치클래스, ql) 열이 역순 일치
a = [(pc(t[0]), round(t[2], 3)) for t in v1]
b = [(pc(t[0]), round(t[2], 3)) for t in v2][::-1]
assert a == b, "① 실패: voice2 != retrograde(voice1)"
results["①_역행대칭"] = f"PASS — {len(a)}음 피치클래스+리듬 역순 완전 일치"

head = [pc(t[0]) for t in v1[:5]]
assert head == ["C", "E-", "G", "A-", "B"], f"② 실패: 주제 머리 {head}"
# 리체르카레 kern 주제와 교차 일치 (독립 소스)
ric = converter.parse(str(DATA / "offering-002.krn"), format="humdrum")
ric_parts = list(ric.parts)
ric_theme = None
for p in ric_parts:
    ns = [n for n in p.flatten().notes if n.isNote]
    if ns and ns[0].measureNumber == 1:
        ric_theme = [n.name for n in ns[:5]]
        break
assert ric_theme == ["C", "E-", "G", "A-", "B"], f"리체르카레 주제 {ric_theme}"
results["②_주제머리"] = f"PASS — 게카논 {head} == 리체르카레 kern {ric_theme} (독립 소스 교차)"

# 총 길이 → 마디 수 (4/4 가정)
total_ql = max(t[1] + t[2] for t in v1) - min(t[1] for t in v1)
results["게카논_길이"] = f"voice1 {len(v1)}음, 총 {total_ql} ql ≈ {total_ql / 4:.1f}마디(4/4)"

# 인코딩 저장 (voice1만 — voice2는 역행 생성이 정의)
enc = [{"n": t[0], "off": t[1], "ql": t[2]} for t in v1]
(DATA / "crab_encoded.json").write_text(
    json.dumps({"source": "IMSLP#221462 (Knuth) / 검증: 역행대칭+kern주제교차+Goodman PDF",
                "voice1": enc}, ensure_ascii=False, indent=1), encoding="utf-8")

# ── ③ per tonos ─────────────────────────────────────────────────────
pt = load_midi_notes(DATA / "pertonos_knuth.mid")
assert len(pt) == 3, f"per tonos 파트 수 {len(pt)} != 3"
# 가장 노트 많은 파트 = 카논 성부(전체 6주기). 주기 시작 = 개시 8음형
# (반음계 상승 C D E♭ E F F♯ G G♯)의 이조 등장 지점
lead = max(pt, key=len)
midis = [t[3] for t in lead]
offs = [t[1] for t in lead]
open8 = midis[:8]
iv8 = [open8[k + 1] - open8[k] for k in range(7)]
starts = []
for i in range(len(midis) - 7):
    if [midis[i + k + 1] - midis[i + k] for k in range(7)] == iv8:
        if not starts or offs[i] - starts[-1][1] > 8:   # 주기 간 최소 간격
            starts.append((midis[i], offs[i]))
trans = [s[0] - starts[0][0] for s in starts]
results["③_주기시작_이조"] = f"감지 {len(starts)}회, 누적 반음 {trans}"
assert len(starts) >= 6, f"③ 실패: 주기 {len(starts)} < 6"
assert trans[:6] == [0, 2, 4, 6, 8, 10], f"③ 실패: 장2도 사다리 아님 {trans[:6]}"
results["③_장2도상행"] = "PASS — 주기마다 +2 반음, 6주기 누적 +10→옥타브 회귀(+12) 구조"

# 1주기 추출 (모든 파트, 주기2 시작 전까지) — 도판용
cyc2_off = starts[1][1]
cycle1 = []
for pi, p in enumerate(pt):
    cycle1.append([{"n": t[0], "off": t[1], "ql": t[2]}
                   for t in p if t[1] < cyc2_off - 1e-6])
keys = ["c", "d", "e", "f♯", "g♯(a♭)", "b♭"]   # 누적 반음 [0,2,4,6,8,10]의 단조 표기
(DATA / "pertonos_encoded.json").write_text(
    json.dumps({"source": "IMSLP#221466 (Knuth) / 검증: 장2도 사다리 assert",
                "cycle1_parts": cycle1, "cycle_semitones": trans[:6],
                "key_ladder": keys, "cycle_len_ql": cyc2_off - starts[0][1]},
               ensure_ascii=False, indent=1), encoding="utf-8")

# ── ④ Cp.XIV ────────────────────────────────────────────────────────
af = converter.parse(str(DATA / "artfugue-019.krn"), format="humdrum")
af_parts = list(af.parts)
target = ["B-", "A", "C", "B"]
first_hit = None
for pi, p in enumerate(af_parts):
    ns = [n for n in p.flatten().notes if n.isNote]
    for i in range(len(ns) - 3):
        if [ns[i + k].name for k in range(4)] == target:
            if first_hit is None or ns[i].measureNumber < first_hit[1]:
                first_hit = (pi, ns[i].measureNumber)
assert first_hit and first_hit[1] == 193, f"④ 실패: 첫 BACH {first_hit}"
maxm = max(m.number for m in af_parts[0].getElementsByClass("Measure"))
assert maxm == 239, f"④ 실패: 최종 마디 {maxm}"
results["④_CpXIV"] = f"PASS — B♭-A-C-B♮ 첫 진입 m.193(part{first_hit[0]}), 중단 m.{maxm}"

# ── ⑤ Ricercar a 6 진입 ─────────────────────────────────────────────
ric_iv = None
entries_strict, entries_relax = [], []
for p in ric_parts:
    ns = [n for n in p.flatten().notes if n.isNote]
    if ns and ns[0].measureNumber == 1 and ric_iv is None:
        ths = ns[:9]
        ric_iv = [interval.Interval(ths[k], ths[k + 1]).semitones for k in range(8)]
for pi, p in enumerate(ric_parts):
    ns = [n for n in p.flatten().notes if n.isNote]
    for i in range(len(ns) - 8):
        iv = [interval.Interval(ns[i + k], ns[i + k + 1]).semitones for k in range(8)]
        if iv == ric_iv:
            entries_strict.append((ns[i].measureNumber, pi))
        elif iv[3:] == ric_iv[3:]:
            # 조적 응답: 머리(처음 3간격) 변형, 꼬리(뒤 5간격) 보존 — 푸가 응답 검출
            entries_relax.append((ns[i].measureNumber, pi))
entries_strict.sort(); entries_relax.sort()
assert len(entries_strict) >= 6, f"⑤ 실패: 엄격 진입 {len(entries_strict)}"
all_entries = sorted(entries_strict + entries_relax)
expo = [e for e in all_entries if e[0] <= 25]
assert sorted(pi for _, pi in expo) == [0, 1, 2, 3, 4, 5], f"⑤ 실패: 제시부 6성부 미완 {expo}"
results["⑤_리체르카레"] = (f"PASS — 주제 {len(entries_strict)}회 {entries_strict}, "
                        f"응답 {len(entries_relax)}회 {entries_relax} | 제시부 6성부 전원 진입 {expo}")
(DATA / "ricercar_entries.json").write_text(
    json.dumps({"source": "offering-002.krn (craigsapp)",
                "subject": entries_strict, "answer": entries_relax,
                "all": all_entries, "exposition": expo,
                "total_measures": 103, "voices": 6}, ensure_ascii=False, indent=1),
    encoding="utf-8")

print("=" * 64)
for k, v in results.items():
    print(f"{k}: {v}")
print("=" * 64)
print("모든 assert 통과 — 인코딩 JSON 3종 저장 완료")
