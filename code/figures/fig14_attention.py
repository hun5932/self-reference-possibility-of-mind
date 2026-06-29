"""도판 14 — 어텐션 행렬 시각화 (§6 계산).

듀얼트랙: Python = authoritative (실제 attention weights). CD = illustrative 개념 그리드.

두 모드
------
- DEMO=True  : 합성(synthetic) 자기참조 패턴 — 환경만 있으면 즉시 실행 (구조 시연용).
- DEMO=False : 실제 모델 활성화 추출 (transformer-lens/transformers 필요).
               TODO 부분에 모델·토큰 지정 후 실행. ⚠️ 실제 weights만 본문 인용.

실행: python fig14_attention.py
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from trih_style import PALETTE, apply_style, save_fig

DEMO = True   # 실제 모델 추출 시 False로 바꾸고 아래 TODO 채우기


def get_attention_matrix() -> tuple[np.ndarray, list[str]]:
    """어텐션 행렬과 토큰 라벨 반환."""
    if DEMO:
        # 합성 자기참조 패턴: induction-like (직전 토큰 + 자기 위치 강조)
        tokens = ["The", "cat", "sat", "on", "the", "cat"]
        n = len(tokens)
        rng = np.random.default_rng(7)
        a = rng.uniform(0, 0.1, (n, n))
        for i in range(n):
            a[i, max(0, i - 1)] += 0.5          # 직전 토큰
            if tokens[i] in tokens[:i]:          # 반복 토큰 → 이전 등장 위치 attend (induction)
                a[i, tokens.index(tokens[i])] += 0.6
        a = a / a.sum(axis=1, keepdims=True)     # 행 정규화
        return a, tokens
    # TODO(실제): transformer_lens.HookedTransformer 로 모델 로드 →
    #   cache["pattern", layer] 에서 head 선택 → numpy 변환.
    raise NotImplementedError("DEMO=False: 모델·토큰·layer/head 지정 필요")


def main() -> None:
    apply_style()
    attn, tokens = get_attention_matrix()

    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(attn, cmap="BuGn", vmin=0, vmax=attn.max())
    ax.set_xticks(range(len(tokens)), tokens, rotation=45, ha="right")
    ax.set_yticks(range(len(tokens)), tokens)
    ax.set_xlabel("attend to (key)")
    ax.set_ylabel("query")
    title = "도판 14 — self-attention (DEMO 합성)" if DEMO else "도판 14 — self-attention (실측)"
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="attention weight")

    save_fig(fig, "fig14_attention")
    plt.close(fig)


if __name__ == "__main__":
    main()
