# -*- coding: utf-8 -*-
"""IMSLP MIDI 4종 분석 — 게 카논 역행 대칭 + 두 시퀀서 교차 일치 + per tonos 상행 구조."""
from pathlib import Path

from music21 import converter

DATA = Path(__file__).resolve().parent


def load(name):
    s = converter.parse(str(DATA / name))
    parts = list(s.parts)
    out = []
    for p in parts:
        ns = []
        for n in p.flatten().notes:
            if n.isNote:
                ns.append((n.pitch.nameWithOctave, float(n.offset), float(n.quarterLength)))
            else:  # 화음이면 최고음
                top = max(n.pitches, key=lambda x: x.midi)
                ns.append((top.nameWithOctave, float(n.offset), float(n.quarterLength)))
        ns.sort(key=lambda t: t[1])
        out.append(ns)
    return out


def names(seq):
    return [t[0] for t in seq]


def pcs(seq):
    """피치 클래스 이름(옥타브 무시)."""
    return [t[0].rstrip("0123456789") for t in seq]


print("=" * 70)
for f in ["crab_lanoiselee.mid", "crab_knuth.mid"]:
    ps = load(f)
    print(f"\n[{f}] 파트 {len(ps)}개, 노트수 {[len(p) for p in ps]}")
    for i, p in enumerate(ps):
        print(f"  part{i} 첫 10: {names(p)[:10]}")
        print(f"  part{i} 끝 10: {names(p)[-10:]}")

print("\n" + "=" * 70)
print("[게 카논 역행 대칭 검사 — 두 파일 모두]")
for f in ["crab_lanoiselee.mid", "crab_knuth.mid"]:
    ps = [p for p in load(f) if len(p) > 4]
    if len(ps) != 2:
        print(f"  {f}: 성부 수 {len(ps)} — 스킵")
        continue
    v1, v2 = ps
    a = pcs(v1)
    b = list(reversed(pcs(v2)))
    eq = a == b
    print(f"  {f}: v1({len(a)}) vs reverse(v2)({len(b)}) 피치클래스 일치 = {eq}")
    if not eq:
        for k, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"    첫 불일치 idx {k}: {x} vs {y}  (전후: {a[max(0,k-2):k+3]} | {b[max(0,k-2):k+3]})")
                break

print("\n" + "=" * 70)
print("[두 시퀀서 교차 일치 — 게 카논 voice1]")
l = [p for p in load("crab_lanoiselee.mid") if len(p) > 4]
k = [p for p in load("crab_knuth.mid") if len(p) > 4]
if len(l) == 2 and len(k) == 2:
    for vi in range(2):
        a, b = pcs(l[vi]), pcs(k[vi])
        print(f"  voice{vi+1}: Lanoiselée({len(a)}) vs Knuth({len(b)}) 일치 = {a == b}")
        if a != b:
            for idx, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"    첫 불일치 idx {idx}: {x} vs {y}")
                    break

print("\n" + "=" * 70)
for f in ["pertonos_lanoiselee.mid", "pertonos_knuth.mid"]:
    ps = load(f)
    print(f"\n[{f}] 파트 {len(ps)}개, 노트수 {[len(p) for p in ps]}")
    for i, p in enumerate(ps):
        print(f"  part{i} 첫 12: {names(p)[:12]}")
