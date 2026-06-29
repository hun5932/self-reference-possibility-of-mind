"""도판 17 — Emergent ability scaling curve (§6 계산).

듀얼트랙: 이 Python 트랙이 authoritative (실제 곡선 형태 재현).
Claude Design 트랙은 illustrative(매끈한 개념 곡선)로 별도 제작 후 comparison-framework.md 비교.

⚠️ 학술 주의: 아래는 emergent ability의 *형태*를 보여주는 재현 도식이다.
   본문에 실측 인용 시 Wei et al. (2022) 원자료/그림을 본인이 직접 확인·인용할 것
   (AI 생성 수치를 실측으로 제시 금지 — hallucination 주의).

실행: (1.7_Research_TRIH_연구/.venv 활성화 후)
    python fig17_scaling.py
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from trih_style import PALETTE, apply_style, save_fig


def main() -> None:
    apply_style()

    # 모델 규모(로그 스케일) vs 성능 — emergent 점프 형태 (개념 재현)
    scale = np.logspace(8, 12, 200)          # 파라미터 수 (10^8 ~ 10^12)
    threshold = 1e10                          # 임계 (TRIH '임계값' 시사)
    # 임계 부근 급격한 상승 (sigmoid)
    perf = 1 / (1 + np.exp(-(np.log10(scale) - np.log10(threshold)) * 3))

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.semilogx(scale, perf, color=PALETTE["compute"], lw=2.4)
    ax.axvline(threshold, color=PALETTE["emergence"], ls="--", lw=1.5, alpha=0.8)
    ax.annotate("임계 (threshold)", xy=(threshold, 0.5),
                xytext=(threshold * 3, 0.28), color=PALETTE["emergence"],
                fontsize=10,
                arrowprops=dict(arrowstyle="->", color=PALETTE["emergence"]))
    ax.set_xlabel("모델 규모 (파라미터 수, log)")
    ax.set_ylabel("창발 능력 (emergent ability)")
    ax.set_title("도판 17 — 임계 이후 창발 (개념 재현, 실측 X)")
    ax.set_ylim(0, 1.05)

    save_fig(fig, "fig17_scaling")
    plt.close(fig)


if __name__ == "__main__":
    main()
