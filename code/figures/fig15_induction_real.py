"""도판 15 — induction head 실측 (§6 계산). 진짜 데이터본.

transformer-lens로 GPT-2 small을 로드하고, 반복 토큰 시퀀스를 입력해
**실제 induction head**(직전 등장의 다음 토큰을 참조하는 자기참조 회로)를 탐지·시각화한다.

- 입력: BOS + 무작위 토큰열 R 을 두 번 반복 (R R).
- 2회차 위치 p(토큰 T)에서 induction head는 1회차 T 다음 토큰(p-seq_len+1)을 attend.
- 전 레이어·헤드를 스캔해 induction score 최대 헤드를 고르고 그 어텐션 행렬을 렌더.

⚠️ 최초 실행 시 GPT-2 가중치(~500MB) 다운로드. CPU로 동작.
출처: induction head 개념 = Olsson et al. (2022). 본 그림은 본인이 gpt2에서 직접 추출.
"""
from __future__ import annotations

import numpy as np
import torch
import matplotlib.pyplot as plt

from trih_style import PALETTE, apply_style, save_fig


def main() -> None:
    from transformer_lens import HookedTransformer

    apply_style()
    print("[fig15] GPT-2 small 로드 중 (최초 1회 다운로드)...")
    model = HookedTransformer.from_pretrained("gpt2")
    model.eval()

    torch.manual_seed(0)
    seq_len = 24
    rand = torch.randint(1000, 12000, (1, seq_len))
    bos = torch.tensor([[model.tokenizer.bos_token_id]])
    tokens = torch.cat([bos, rand, rand], dim=1)  # [1, 1 + 2*seq_len]
    n = tokens.shape[1]

    with torch.no_grad():
        _, cache = model.run_with_cache(tokens, remove_batch_dim=True)

    # ── induction score: 2회차 위치 p → (p - seq_len + 1) 에 대한 평균 어텐션 ──
    best = (-1.0, 0, 0)
    for L in range(model.cfg.n_layers):
        patt = cache["pattern", L]  # [heads, q, k]
        for H in range(model.cfg.n_heads):
            p = patt[H]
            vals = []
            for pos in range(1 + seq_len, n):
                tgt = pos - seq_len + 1
                if 0 <= tgt < p.shape[1]:
                    vals.append(p[pos, tgt].item())
            score = float(np.mean(vals)) if vals else 0.0
            if score > best[0]:
                best = (score, L, H)
    score, L, H = best
    print(f"[fig15] 최강 induction head: L{L}H{H}, induction score = {score:.3f}")

    patt = cache["pattern", L][H].numpy()

    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    im = ax.imshow(patt, cmap="BuGn", vmin=0, vmax=float(patt.max()))
    # induction 줄무늬 표시 (2회차 query → 1회차 다음 토큰)
    xs = [pos - seq_len + 1 for pos in range(1 + seq_len, n)]
    ys = list(range(1 + seq_len, n))
    ax.plot(xs, ys, ls="--", lw=1.2, color=PALETTE["emergence"], alpha=0.8,
            label="induction 줄무늬")
    ax.axhline(1 + seq_len - 0.5, color=PALETTE["gray"], lw=0.8, ls=":")
    ax.set_title(f"도판 15 — induction head 실측\nGPT-2 small  L{L}·H{H}  (induction score {score:.2f})")
    ax.set_xlabel("key 위치 — 참조 대상 (attended-to)")
    ax.set_ylabel("query 위치 — 현재 토큰 (attending)")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="attention weight")

    save_fig(fig, "fig15_induction_real")
    plt.close(fig)
    print("[fig15] done - real data (Olsson 2022 induction head, extracted from gpt2)")


if __name__ == "__main__":
    main()
