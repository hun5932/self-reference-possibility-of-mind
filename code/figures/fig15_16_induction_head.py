"""도판 15-16 — Induction head 회로 시각화 (§6 계산).

듀얼트랙: Python(circuitsvis + transformer-lens) = authoritative (실제 회로).
CD = illustrative 회로 흐름 개념도.

⚠️ 실제 induction head는 transformer-lens(HookedTransformer)로 모델 로드 후
   prev-token head → induction head 경로를 cache에서 추출해야 한다.
   circuitsvis는 HTML 위젯을 출력하므로(정적 PNG 아님) →
   export 시 HTML → 브라우저 캡처 또는 핸드오프 변환 (README ⑥ 경로).

학술 주의: 회로 인용은 Olsson et al. (2022) 원자료 본인 확인 (hallucination 주의).

실행 개요 (TODO 채운 뒤):
    python fig15_16_induction_head.py   # circuitsvis HTML을 _output/에 저장
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "_output"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print(
        "[fig15_16] 스캐폴딩. 실제 추출 절차:\n"
        "  1) from transformer_lens import HookedTransformer; model = HookedTransformer.from_pretrained('gpt2')\n"
        "  2) 반복 토큰 시퀀스로 run_with_cache → cache['pattern', layer]\n"
        "  3) prev-token head & induction head 식별 (오프셋 -1 / 반복 패턴)\n"
        "  4) import circuitsvis as cv; html = cv.attention.attention_patterns(...)\n"
        "  5) (OUT / 'fig15_induction_head.html').write_text(str(html))\n"
        "  → HTML → 브라우저 캡처/핸드오프로 인쇄해상도 PNG/SVG 변환 (README ⑥)\n"
        "  ⚠️ 회로 해석은 Olsson 2022 원자료 본인 확인."
    )
    # TODO: 위 절차 구현


if __name__ == "__main__":
    main()
