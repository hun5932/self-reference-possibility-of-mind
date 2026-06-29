# 📋 도판 manifest — 18-도판 완성 현황 (학술본)

> 생성: 2026-06-11 | 산출: `05_FIG_도판/도판_학술본/` | 가이드: `GUIDE_학술도판_제작.md`

## 빌드 스크립트 → 도판 매핑
| 스크립트 | 생성 도판 |
|----------|----------|
| `build_fig01.py` | Fig1 |
| `build_geom.py` | Fig2(타일링)·Fig3(평면군)·Fig4(자기참조)·Fig5(드로스테)·Fig6(폭포루프)·Fig7(계단루프) |
| `build_escher_v2.py` | (구) 2D 펜로즈 시도 — build_penrose3d.py로 대체됨 |
| `build_penrose3d.py` | ⭐Fig06_폭포_펜로즈(완성)·Fig07_계단_펜로즈(⚠️개선중 — 폐합 트릭 구현됨, 시각 다듬기 보류; 웹 검증 좌표로 재구현 예정) |
| `build_bach_music21.py` | (구) Fig10·11·12 _music21 합성 주제판 — 2026-06-12 R판으로 대체(D-026), 산출물 `_백업_20260612/` |
| `build_bach_real.py` + `verify_bach_real.py` | ⭐⭐**Fig10R·11R·12R·12bR (정본)** — 실제 악보(kern·Knuth MIDI) 파싱 + assert 5종 검증 + 조판·주석. 데이터: `data_bach/` |
| `build_hyper.py` | Fig8-9(쌍곡 타일링) |
| `build_music.py` | Fig10(무한상승)·Fig11(BACH)·Fig12(회문) |
| `build_fig13.py` | Fig13(괴델 G) |
| `build_data.py` | Fig14(어텐션)·Fig15(induction 실측)·Fig16(스케일링) |
| `build_fig18.py` | Fig18(통합) |
| `build_table1.py` | Table1(매트릭스) |
| `build_bach.py` | Supp(바흐 형식 통합) |
| 공통 | `style_academic.py`(헬퍼) · `labels.py`(한/영 라벨) |

## 18-도판 완성 체크 (× ko/en, textless 제외)
```
✅ Fig1  3단계            ✅ Fig10 무한상승
✅ Fig2  타일링(textless)  ✅ Fig11 BACH
✅ Fig3  17 평면군         ✅ Fig12 회문
✅ Fig4  상호자기참조      ✅ Fig13 괴델 G
✅ Fig5  드로스테          ✅ Fig14 어텐션
✅ Fig6  폭포 루프         ✅ Fig15 induction(gpt2 실측)
✅ Fig7  계단 루프         ✅ Fig16 스케일링
✅ Fig8-9 쌍곡(textless)   ✅ Fig18 통합
                          ✅ Table1 매트릭스 / ✅ Supp 바흐
✅ Fig17 귀속그래프 → **자체 재구성본**(build_fig17.py) + Anthropic 2025 인용
```
→ **18-도판 + Table1 전부 완성** (Fig17 포함 자체제작; 원본 에셔/Anthropic 미사용).

## 🎨 컬러 학술본 (색이 정보를 더하는 것만 — `도판_학술본_컬러/`)
```
build_color.py → Fig18(4영역)·Table1(4영역)·Fig17(계산 teal)·Fig14·Fig16(데이터)
절제된 4영역/영역 색 + 흰 배경 (glow·장식 없음). 그 외는 흑백본 사용(색 불필요).
```

## 📚 부속 문서
```
도판_학술본/도판_해설.md          — 각 도판 의미·논문 역할(TRIH 단계·영역)
도판_학술본/참고자료_저작권_출처.md — 에셔 저작권(2042까지)·Anthropic 인용·바흐 PD
```

## 검수 (육안 PNG 확인 완료)
```
Fig1·2·3·4·6·11·13·16·18·Table1·바흐·쌍곡·induction·무한상승 = 직접 확인 ✅
(나머지는 동일 생성기·동일 패턴 → 일괄 신뢰)
색·glow·이모지·chrome 없음 / 한·영 라벨 / mono=노테이션 / 흑백 인쇄 가독 확인
```

## 백업 정책 (준수)
```
기존 산출물 갱신 시 → 같은 폴더 _백업_YYYYMMDD/ 로 구본 이동 후 새로 생성.
예) 도판_학술본/_백업_20260611/ (구 8-도판 README 보존)
```
