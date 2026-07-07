"""흑백 학술지 도판 공통 — 색 0(hue), 회색조만. bare diagram.

색 대신 굵기·크기·회색단계로 강조. glow/그라데이션/이모지 금지.
SVG 문서 빌더 + SVG→PNG(300dpi)/PDF/SVG 렌더(Playwright).
"""
from __future__ import annotations

from pathlib import Path

# ── 흑백 팔레트 (확정) ───────────────────────────────────────────────
INK = "#1A1A1A"     # 선·글자
GRAY = "#555555"    # 보조 텍스트
GRAYL = "#888888"   # 약한 텍스트
RULE = "#C8C8C8"    # 괘선·grid·축
SOFT = "#F2F2F2"    # 옅은 채움(최소)
WHITE = "#FFFFFF"

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Noto+Serif+KR:wght@400;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400"
    "&family=IBM+Plex+Mono:wght@400;500&display=swap');"
)
SERIF = "'Noto Serif KR','Source Serif 4',serif"
MONO = "'IBM Plex Mono',monospace"

# ── 컬러 학술본용 4영역 도메인 색 (절제된 학술 색; 흑백본과 별도) ──────
DOMAIN = {
    "visual": "#2A4D8F", "auditory": "#C8860D", "logical": "#A6243A",
    "compute": "#1F7A6B", "emergence": "#6B3FA0",
}
DOMAIN_SOFT = {
    "visual": "#EAF0F8", "auditory": "#FBF3E2", "logical": "#F8E8EB",
    "compute": "#E6F2EF", "emergence": "#F1EAF8",
}


def svg_doc(w: float, h: float, body: str, extra_css: str = "") -> str:
    """흰 배경 + 흑백 텍스트 기본 스타일의 자기완결형 SVG 문서."""
    css = (
        FONT_IMPORT
        + f"text{{fill:{INK};font-family:{SERIF}}}"
        + f".mono{{font-family:{MONO}}}.serif{{font-family:{SERIF}}}"
        + extra_css
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f"<style>{css}</style>"
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{WHITE}"/>'
        f"{body}</svg>"
    )


def arrow_marker(mid: str = "ar", color: str = INK) -> str:
    """검정 화살촉 마커 def."""
    return (
        f'<defs><marker id="{mid}" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
        f'orient="auto"><path d="M0,1 L7,4.5 L0,8 Z" fill="{color}"/></marker></defs>'
    )


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, anchor="middle", fill=INK, weight=None, italic=False, cls="serif", ls=None) -> str:
    """학술 텍스트 헬퍼. cls='serif'(기본)/'mono'(노테이션 전용)."""
    a = f'x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" class="{cls}"'
    if weight:
        a += f' font-weight="{weight}"'
    if italic:
        a += ' font-style="italic"'
    if ls is not None:
        a += f' letter-spacing="{ls}"'
    return f"<text {a}>{esc(str(s))}</text>"


def box(x, y, w, h, sw=1.1, fill=WHITE, stroke=INK) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def harrow(x1, y, x2, sw=1.1) -> str:
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{INK}" stroke-width="{sw}" marker-end="url(#ar)"/>'


def varrow(x, y1, y2, sw=1.1) -> str:
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{INK}" stroke-width="{sw}" marker-end="url(#ar)"/>'


def render(svg_str: str, name: str, out_dir: str | Path, w: float, h: float) -> None:
    """SVG 문자열 → standalone .svg + PNG(300dpi급, dsf=3) + PDF(벡터)."""
    from playwright.sync_api import sync_playwright

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.svg").write_text(svg_str, encoding="utf-8")
    html = f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:#fff}}</style>{svg_str}'
    tmp = out / f"_tmp_{name}.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            ctx = b.new_context(viewport={"width": int(w), "height": int(h)}, device_scale_factor=3)
            pg = ctx.new_page()
            pg.goto(tmp.as_uri(), wait_until="networkidle", timeout=30000)
            try:
                pg.evaluate("()=>new Promise(r=>{if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>r(1));else r(1)})")
            except Exception:
                pass
            pg.wait_for_timeout(350)
            pg.locator("svg").first.screenshot(path=str(out / f"{name}.png"))
            pg.pdf(path=str(out / f"{name}.pdf"), width=f"{w}px", height=f"{h}px",
                   print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            ctx.close()
            b.close()
    finally:
        tmp.unlink(missing_ok=True)
    print(f"[academic] {name}: PNG+SVG+PDF ({int(w)}x{int(h)})")
