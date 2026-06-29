# 🎓 도판 학술본 — 흑백 학술지 스타일 (한/영 양판, bare diagram)

> 컬러 슬라이드본을 **학술지 논문 도판**으로 재제작 + **18-도판 전체 자체제작 완성**.
> 흑백(색 0) · bare diagram · 한글판/영문판 분리. 생성기: `09_CODE_코드/figures_academic/`.
> 갱신: 2026-06-11 (이전 8-도판 버전은 `_백업_20260611/`)

## 📐 스타일
```
색 없음(Ink #1A1A1A on white) · 강조=굵기·회색조 · 4영역=라벨+위치(색 X)
glow·그라데이션·이모지·둥근카드 0 · hairline 1.1px
Serif 본문 / Mono=실제 노테이션 전용 · bare(제목·캡션 chrome 없음, 「(도 N)」은 본문 식자)
```

## 📂 18-도판 전체 (× {ko,en} 또는 textless × {png 300dpi, svg, pdf})
| 파일 | 논문 | 내용 | 트랙 |
|------|------|------|------|
| `Fig01_3단계모델` | Fig 1 | 환원→자기참조→창발 | 개념 SVG |
| `Fig02_타일링` | Fig 2 | 주기 타일링(Truchet, 대칭) | 수학(textless) |
| `Fig03_평면결정군` | Fig 3 | 17 평면결정군 분류 | 차트 SVG |
| `Fig04_상호자기참조` | Fig 4 | Drawing Hands(상호 산출 루프) | 개념 SVG |
| `Fig05_드로스테` | Fig 5 | Print Gallery(무한 재귀 포함) | 개념 SVG |
| `Fig06_폭포루프` | Fig 6 | Waterfall(불가능 하강 루프) | 개념 SVG |
| `Fig07_계단루프` | Fig 7 | Ascending(끝없는 상승) | 개념 SVG |
| `Fig08_09_쌍곡타일링` | Fig 8-9 | Circle Limit(푸앵카레 원판) | 수학(textless) |
| `Fig10R_무한상승_실물` | Fig 10 | Canon per Tonos **실물**(제1주기+장2도 사다리) | 조판+주석 (구판→_백업_20260612) |
| `Fig11R_BACH_실물` | Fig 11 | Contrapunctus XIV mm.191–196 **실발췌**(B-A-C-H 마킹) | 조판+주석 |
| `Fig12R_게카논_실물` | Fig 12 | Crab Canon **실물 18마디 전체**+역행 | 조판+주석 |
| `Fig12bR_리체르카레_진입지도` | Fig 12b | Ricercar a 6 주제 진입 ↔ causal mask 평행 | matplotlib Greys |
| `Fig13_괴델G` | Fig 13 | 명제 G 자기참조 | 개념 SVG |
| `Fig14_어텐션` | Fig 14 | self-attention | matplotlib Greys |
| `Fig15_induction` | Fig 15 | gpt2 L5H5 실측(0.91) | matplotlib Greys |
| `Fig16_스케일링` | Fig 16 | 창발 곡선(Wei 2022) | matplotlib |
| `Fig18_TRIH통합` ⭐ | Fig 18 | 4영역 동형 통합 | 개념 SVG |
| `Table1_동형성매트릭스` | Table 1 | 4영역×3단계 | 괘선 표 |
| `Supp_바흐형식도식` | §4 보조 | 회문·상승·BACH 통합 | 보표 SVG |

⬜ **Fig 17** (attribution graph): Anthropic 2025 transformer-circuits **외부 인용** — 자체생성 X.
   → 본문 인용: `Anthropic (2025), https://transformer-circuits.pub/2025/attribution-graphs/biology.html`

D-018 정합: 에셔 작품 원본이미지 미사용 → Fig2-9 모두 **수학/개념 자체제작**(저작권 안전).

## 🌐 용도
```
_ko → 한국어 학위논문   |   _en → arxiv/Leonardo/CogSci
.png(.hwp 삽입 300dpi) · .pdf(인쇄) · .svg(LaTeX/arxiv 벡터)
textless(Fig02·08_09) = 언어 무관(한·영 공용)
```

## 🔁 vs 컬러 발표본
```
ClaudeDesign_변환본/  = 컬러(발표/슬라이드/Leonardo 비주얼) — 보존
도판_학술본/(여기)    = 흑백 학술지 — 논문 본문 채택
```

## ♻️ 재생성 (가이드: figures_academic/GUIDE_학술도판_제작.md)
```
<venv>\python.exe figures_academic\build_fig01.py / build_fig13.py / build_fig18.py /
   build_table1.py / build_bach.py / build_geom.py / build_hyper.py / build_music.py / build_data.py
```
