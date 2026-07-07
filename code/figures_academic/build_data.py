"""데이터 도판 (Fig14 어텐션 · Fig15 induction 실측 · Fig16 scaling) — 흑백 학술본 KO/EN.

matplotlib 회색조(cmap=Greys / 흑백 곡선), 제목 없음(bare), 축라벨 KO/EN.
한글: Batang/Malgun fallback. 영문: serif.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])
OUT.mkdir(parents=True, exist_ok=True)


def setup(lang: str) -> None:
    serif = (["Noto Serif KR", "Batang", "Malgun Gothic", "DejaVu Serif"] if lang == "ko"
             else ["Source Serif 4", "DejaVu Serif", "Times New Roman"])
    mpl.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "font.family": "serif", "font.serif": serif,
        "axes.edgecolor": "#1A1A1A", "axes.labelcolor": "#1A1A1A", "text.color": "#1A1A1A",
        "xtick.color": "#1A1A1A", "ytick.color": "#1A1A1A", "axes.linewidth": 0.8,
        "axes.unicode_minus": False, "svg.fonttype": "none",
    })


def save(fig, name: str) -> None:
    for ext in ("png", "svg", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[data] {name}")


def attention(lang):
    from labels import DATA
    D = DATA[lang]
    toks = ["The", "cat", "sat", "on", "the", "cat"]
    n = len(toks)
    rng = np.random.default_rng(7)
    a = rng.uniform(0, 0.08, (n, n))
    for i in range(n):
        a[i, max(0, i - 1)] += 0.5
        if toks[i] in toks[:i]:
            a[i, toks.index(toks[i])] += 0.6
    a = np.tril(a)
    a = a / a.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(4.6, 4.3))
    im = ax.imshow(a, cmap="Greys", vmin=0, vmax=a.max())
    ax.set_xticks(range(n), toks, rotation=45, ha="right")
    ax.set_yticks(range(n), toks)
    ax.set_xlabel(D["attn_x"]); ax.set_ylabel(D["attn_y"])
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(D["attn_w"]); cb.outline.set_linewidth(0.6)
    ax.text(0.5, -0.34, D["attn_note"], transform=ax.transAxes, ha="center", fontsize=8, color="#555")
    save(fig, f"Fig14_어텐션_{lang}")


def scaling(lang):
    from labels import DATA
    D = DATA[lang]
    x = np.logspace(8, 12, 200)
    thr = 1e10
    y = 1 / (1 + np.exp(-(np.log10(x) - np.log10(thr)) * 3))
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    ax.semilogx(x, y, color="#1A1A1A", lw=2)
    ax.axvline(thr, color="#888888", ls="--", lw=1)
    ax.text(thr * 1.25, 0.04, D["scal_thr"], color="#555", fontsize=9)
    ax.text(x[35], 0.13, D["scal_plateau"], color="#555", fontsize=9)
    ax.text(x[150], 0.88, D["scal_emerg"], color="#1A1A1A", fontsize=9)
    ax.set_xlabel(D["scal_x"]); ax.set_ylabel(D["scal_y"]); ax.set_ylim(0, 1.05)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, f"Fig16_스케일링_{lang}")


def induction_both(cmap="Greys"):
    import torch
    from transformer_lens import HookedTransformer
    from labels import DATA
    print("[data] GPT-2 로드 (induction 실측)...")
    model = HookedTransformer.from_pretrained("gpt2")
    model.eval()
    torch.manual_seed(0)
    sl = 24
    rand = torch.randint(1000, 12000, (1, sl))
    bos = torch.tensor([[model.tokenizer.bos_token_id]])
    toks = torch.cat([bos, rand, rand], 1)
    n = toks.shape[1]
    with torch.no_grad():
        _, cache = model.run_with_cache(toks, remove_batch_dim=True)
    best = (-1.0, 0, 0)
    for Lr in range(model.cfg.n_layers):
        pat = cache["pattern", Lr]
        for Hh in range(model.cfg.n_heads):
            pp = pat[Hh]
            vals = [pp[pos, pos - sl + 1].item() for pos in range(1 + sl, n) if 0 <= pos - sl + 1 < pp.shape[1]]
            sc = float(np.mean(vals)) if vals else 0.0
            if sc > best[0]:
                best = (sc, Lr, Hh)
    sc, Lr, Hh = best
    pat = cache["pattern", Lr][Hh].numpy()
    xs = [pos - sl + 1 for pos in range(1 + sl, n)]
    ys = list(range(1 + sl, n))
    for lang in ("ko", "en"):
        setup(lang)
        D = DATA[lang]
        fig, ax = plt.subplots(figsize=(5, 4.7))
        im = ax.imshow(pat, cmap=cmap, vmin=0, vmax=float(pat.max()))
        ax.plot(xs, ys, ls="--", lw=1, color="#1A1A1A", alpha=0.75, label=D["ind_stripe"])
        ax.set_xlabel(D["ind_x"]); ax.set_ylabel(D["ind_y"])
        ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
        ax.text(0.02, 1.02, f"GPT-2 small · L{Lr}H{Hh} · induction {sc:.2f}",
                transform=ax.transAxes, fontsize=8, color="#555")
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.outline.set_linewidth(0.6)
        save(fig, f"Fig15_induction_{lang}")


def main() -> None:
    for lang in ("ko", "en"):
        setup(lang)
        attention(lang)
        scaling(lang)
    induction_both()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "induction-color":
        induction_both(cmap="BuGn")   # 컬러 학술본(도14 컬러판과 동일 계열)
    else:
        main()
