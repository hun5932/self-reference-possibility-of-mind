"""TRIH 논문 도판 — Python 트랙 공통 스타일 모듈.

목적
----
듀얼트랙(Claude Design vs Python)에서 **Python 도판이 디자인 시스템과 동일한
4영역 색·타이포·인쇄 규격을 공유**하도록 강제한다. 색 hex는
`05_FIG_도판/ClaudeDesign_셋팅/design-system/design-system.css`의 변수와 1:1 일치.

사용
----
    from trih_style import PALETTE, apply_style, save_fig
    apply_style()
    fig, ax = plt.subplots()
    ...
    save_fig(fig, "fig17_scaling")   # 300dpi PNG + SVG 동시 저장

마지막 확인: 2026-05-28 | 호환: S-CES-R v1.0.5
"""
from __future__ import annotations

from pathlib import Path

# ── 4영역 색코딩 (design-system.css와 동일) ──────────────────────────────
PALETTE: dict[str, str] = {
    "visual": "#2A4D8F",     # 에셔 (시각)        Indigo
    "auditory": "#C8860D",   # 바흐 (청각)        Amber
    "logical": "#A6243A",    # 괴델 (논리)        Crimson
    "compute": "#1F7A6B",    # 트랜스포머 (계산)  Teal
    "emergence": "#6B3FA0",  # 창발 통합          Violet
    "ink": "#1A1A1A",
    "paper": "#FAF8F3",
    "gray": "#6B6B6B",
    "gray_line": "#D8D4CC",
}

# 3단계 모티프 색 (환원 → 자기참조 → 창발)
STAGE = {"reduction": "#9A968C", "selfref": PALETTE["visual"], "emergence": PALETTE["emergence"]}

# 인쇄 규격
DPI = 300                                   # 학과 .hwp 삽입용
OUT_DIR = Path(__file__).resolve().parent / "_output"   # 산출물 (이후 05_FIG_도판으로 이동)


def apply_style() -> None:
    """matplotlib 전역 스타일을 학술 도판 톤으로 설정 (세리프·종이 배경·절제)."""
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.facecolor": PALETTE["paper"],
        "axes.facecolor": PALETTE["paper"],
        "axes.edgecolor": PALETTE["gray_line"],
        "axes.labelcolor": PALETTE["ink"],
        "text.color": PALETTE["ink"],
        "xtick.color": PALETTE["gray"],
        "ytick.color": PALETTE["gray"],
        "font.family": "serif",
        # Noto Serif KR/Source Serif가 설치돼 있으면 한·영 정합. 없으면 fallback.
        "font.serif": ["Noto Serif KR", "Source Serif 4", "DejaVu Serif"],
        "axes.grid": True,
        "grid.color": PALETTE["gray_line"],
        "grid.alpha": 0.5,
        "savefig.facecolor": PALETTE["paper"],
        "figure.dpi": 120,
    })


def save_fig(fig, name: str, *, svg: bool = True) -> list[Path]:
    """도판을 PNG(300dpi) + SVG(벡터)로 저장. arxiv/LaTeX는 SVG, .hwp는 PNG.

    반환: 저장된 파일 경로 목록.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    png = OUT_DIR / f"{name}.png"
    fig.savefig(png, dpi=DPI, bbox_inches="tight")
    paths.append(png)
    if svg:
        s = OUT_DIR / f"{name}.svg"
        fig.savefig(s, bbox_inches="tight")
        paths.append(s)
    print(f"[trih_style] 저장: {', '.join(p.name for p in paths)} → {OUT_DIR}")
    return paths
