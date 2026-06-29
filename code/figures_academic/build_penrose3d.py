"""펜로즈 삼각형(불가능 tribar) — 실제 3D 객체의 직교투영 자체 렌더러 (흑백 학술본).

원리: 세 막대를 3D에서 x·y·z 축으로 배치(실제로는 닫히지 않음). (1,1,1) 방향으로
직교투영하면 C막대 끝 코너가 A막대 시작 코너에 '정확히' 겹쳐 닫힌 삼각형으로 보임 =
실제 불가능(에펠하르트/펜로즈 조각의 원리). 자체 painter 알고리즘(면 깊이 정렬 + 법선 음영).

좌표:  A=[0,L]×[0,w]×[0,w]  B=[L-w,L]×[0,L]×[0,w]  C=[L-w,L]×[L-w,L]×[0,L]
   C상단코너 [L-w,L]³ 중심 - A시작코너 [0,w]³ 중심 = (L-w)(1,1,1) ∥ 시선 → 투영 일치.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from style_academic import INK, render, svg_doc

OUT = Path(__file__).resolve().parents[2] / "05_FIG_도판" / "도판_학술본"
import os as _os                       # FIG_OUT 환경변수로 산출 폴더 오버라이드
if _os.environ.get("FIG_OUT"):
    OUT = Path(_os.environ["FIG_OUT"])

# 시선/스크린 기저 (직교투영, 시점 = +(1,1,1) 쪽에서 원점을 바라봄)
D = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)      # 시선축(클수록 카메라에 가까움)
U = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)     # 스크린 가로
T = np.array([1.0, 1.0, -2.0]) / np.sqrt(6)     # 스크린 세로
# 면 '방향(축)'별 고정 3톤 — 빔에 무관하게 같은 방향=같은 톤 (정합 조명, 캐논 tribar 음영)
TONE = {0: "#A6A6A6", 1: "#CFCFCF", 2: "#EDEDED"}   # x축면(어둠)·y축면(중간)·z축(윗면, 밝음)


def box(x0, x1, y0, y1, z0, z1):
    V = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                  [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], float)
    faces = [([0, 1, 2, 3], (0, 0, -1)), ([4, 5, 6, 7], (0, 0, 1)),
             ([0, 1, 5, 4], (0, -1, 0)), ([2, 3, 7, 6], (0, 1, 0)),
             ([1, 2, 6, 5], (1, 0, 0)), ([0, 3, 7, 4], (-1, 0, 0))]
    return V, faces


def grey(n):
    ax = int(np.argmax(np.abs(np.array(n, float))))   # 0=x,1=y,2=z 면 방향
    return TONE[ax]


def fig(L=3.3, w=0.52, canvas=600, sw=1.8):
    boxes = [box(0, L, 0, w, 0, w),               # A (x축)
             box(L - w, L, 0, L, 0, w),           # B (y축)
             box(L - w, L, L - w, L, 0, L)]        # C (z축)
    polys = []   # (depth, fill, [(sx,sy)..])
    for V, faces in boxes:
        for idx, n in faces:
            if np.array(n, float) @ D <= 1e-9:    # 후면 컬링(시선과 등돌린 면)
                continue
            pts3 = V[idx]
            sx = pts3 @ U; sy = pts3 @ T
            depth = float(pts3.mean(axis=0) @ D)
            polys.append((depth, grey(n), list(zip(sx, sy))))
    # 화면 좌표 정규화(중심 맞춤·뒤집기)
    allx = [p[0] for _, _, pl in polys for p in pl]
    ally = [p[1] for _, _, pl in polys for p in pl]
    minx, maxx, miny, maxy = min(allx), max(allx), min(ally), max(ally)
    span = max(maxx - minx, maxy - miny)
    s = (canvas - 90) / span
    ox = (canvas - (maxx + minx) * s) / 2
    oy = (canvas + (maxy + miny) * s) / 2     # +: y 뒤집기
    body = []
    for depth, fill, pl in sorted(polys, key=lambda z: z[0]):   # 먼 면(작은 depth) 먼저
        d = " ".join(f"{ox + x * s:.2f},{oy - y * s:.2f}" for x, y in pl)
        body.append(f'<polygon points="{d}" fill="{fill}" stroke="{INK}" '
                    f'stroke-width="{sw}" stroke-linejoin="round"/>')
    return svg_doc(canvas, canvas, "".join(body)), canvas, canvas


def view_basis(d):
    d = np.array(d, float); d = d / np.linalg.norm(d)
    u = np.array([1.0, -1.0, 0.0]); u = u - d * (u @ d); u = u / np.linalg.norm(u)
    t = np.cross(d, u); t = t / np.linalg.norm(t)
    return d, u, t


def _project_sort(polys3, canvas, sw, view=(1, 1, 1), pad=80):
    """3D 면 리스트[(verts(Nx3), normal)] → 투영·깊이정렬·음영 SVG body. view=직교 시선."""
    d, u, t = view_basis(view)
    polys = []
    for verts, n in polys3:
        if np.array(n, float) @ d <= 1e-9:
            continue
        v = np.array(verts, float)
        sx = v @ u; sy = v @ t
        polys.append((float(v.mean(axis=0) @ d), grey(n), list(zip(sx, sy))))
    allx = [p[0] for _, _, pl in polys for p in pl]
    ally = [p[1] for _, _, pl in polys for p in pl]
    span = max(max(allx) - min(allx), max(ally) - min(ally))
    s = (canvas - pad) / span
    ox = (canvas - (max(allx) + min(allx)) * s) / 2
    oy = (canvas + (max(ally) + min(ally)) * s) / 2
    body = []
    for _, fill, pl in sorted(polys, key=lambda z: z[0]):
        d = " ".join(f"{ox + x * s:.2f},{oy - y * s:.2f}" for x, y in pl)
        body.append(f'<polygon points="{d}" fill="{fill}" stroke="{INK}" '
                    f'stroke-width="{sw}" stroke-linejoin="round"/>')
    return "".join(body)


def fig_stairs(canvas=660, sw=1.5, extra=""):
    """펜로즈 무한계단(Penrose & Penrose 1958) — tribar와 동일한 투영 트릭의 3D 구현.

    원리: 직사각 둘레를 돌며 매 칸 일정하게 상승하는 계단을 실제 3D로 배치하되,
    한 바퀴의 총변위가 (D,D,D) = D·(1,1,1) 이 되도록 비대칭 플라이트를 설계.
    시선 (1,1,1) 직교투영에서 이 변위는 0으로 사라짐 → 마지막 칸 다음 위치(유령 칸)가
    첫 칸에 '정확히' 겹쳐, 한 바퀴 내내 올라가는데 제자리로 돌아오는 폐합 무한계단.

    폐합 조건: Dx = n1-n3 = Dy = n2-n4 = N·rise  (N = 총 칸수)
    여기선 플라이트 (8,7,4,3) → Dx=Dy=4, N=22, rise=2/11 (네 변이 모두 보이는 직사각 비례).
    렌더: 벽면은 플라이트별 단일 병합 폴리곤 윤곽(수직 기둥선 제거),
          디딤판(top)·라이저/끝단(진행축 면)만 개별 윤곽선 → 매끈한 벽체 + 또렷한 계단.
    """
    flights = [((1, 0), 8), ((0, 1), 7), ((-1, 0), 4), ((0, -1), 3)]
    D_ = 4.0                                     # = n1-n3 = n2-n4
    N = sum(cnt for _, cnt in flights)           # 22칸
    rise = D_ / N                                # 2/11 — N·rise = D 가 폐합 조건
    cube = 3.2                                   # 깊은 벽체(일체 구조물로 읽힘)
    d, u, t = view_basis((1, 1, 1))
    cells = []                                   # (i, j, flight, dx, dy)
    cx, cy = 0, 0
    for fi, ((dx, dy), cnt) in enumerate(flights):
        for _ in range(cnt):
            cells.append((cx, cy, fi, dx, dy))
            cx += dx; cy += dy
    # 검증: 유령 칸(다음 위치) - 시작 칸 = (D,D), 높이 N·rise = D → (D,D,D) ∥ 시선
    assert (cx, cy) == (cells[0][0] + D_, cells[0][1] + D_)

    items = []   # (depth, fill, stroke, stroke_w, verts3)
    def emit(pts3, nrm, fill, stroke, w_, depth=None):
        if np.array(nrm, float) @ d <= 1e-9:
            return
        v = np.array(pts3, float)
        items.append((depth if depth is not None else float(v.mean(axis=0) @ d),
                      fill, stroke, w_, v))

    # 1) 칸별 면 채움: 디딤판(z+)만 검정 윤곽, 측면(x/y)은 자기색 미세 스트로크(틈 메움)
    #    각 칸을 진입 방향 반대쪽으로 ov 연장(노징) → 코너 턴·시임의 관통 슬릿을
    #    윗단 칸의 벽체가 가림(직선 구간에선 painter 순서로 자연 처리).
    ov = 0.45
    for k, (i, j, fi, dx, dy) in enumerate(cells):
        din = (cells[k][0] - cells[k - 1][0], cells[k][1] - cells[k - 1][1]) if k else flights[-1][0]
        x0, x1, y0, y1 = float(i), i + 1.0, float(j), j + 1.0
        if din == (1, 0):
            x0 -= ov
        elif din == (-1, 0):
            x1 += ov
        elif din == (0, 1):
            y0 -= ov
        else:
            y1 += ov
        b = k * rise
        V, fs = box(x0, x1, y0, y1, b, b + cube)
        for idx, nrm in fs:
            ax = int(np.argmax(np.abs(np.array(nrm, float))))
            f = grey(nrm)
            if ax == 2:
                emit(V[idx], nrm, f, INK, sw)
            else:
                emit(V[idx], nrm, f, f, 1.0)
    # 1.5) 연속 칸 경계 패치: 칸 사이 단차(rise)로 코너 턴에서 생기는 관통 슬릿을
    #      공유 경계면 전체를 덮는 벽톤 쿼드로 봉합(깊이를 낮춰 슬릿 외엔 전부 가려짐).
    #      마지막 칸→유령 칸(시임)도 동일 처리 — 투영상 첫 칸 위치에 정확히 겹침.
    ext = cells + [(cells[0][0] + int(D_), cells[0][1] + int(D_), 0, 0, 0)]
    for k in range(N):
        i0, j0 = ext[k][0], ext[k][1]
        i1, j1 = ext[k + 1][0], ext[k + 1][1]
        b0, b1 = k * rise, (k + 1) * rise
        zlo, zhi = min(b0, b1), max(b0, b1) + cube
        if i0 != i1:                                   # x 방향 경계 → 평면 x=max(i0,i1)
            c = float(max(i0, i1))
            q = [(c, j0, zlo), (c, j0 + 1, zlo), (c, j0 + 1, zhi), (c, j0, zhi)]
            nrm = (1, 0, 0)
        else:                                          # y 방향 경계 → 평면 y=max(j0,j1)
            c = float(max(j0, j1))
            q = [(i0, c, zlo), (i0 + 1, c, zlo), (i0 + 1, c, zhi), (i0, c, zhi)]
            nrm = (0, 1, 0)
        v = np.array(q, float)
        emit(q, nrm, grey(nrm), grey(nrm), 1.0,
             depth=float(v.mean(axis=0) @ d) - 1.0)

    # 2) 투영·정렬·렌더 — 실루엣 언더레이(전 폴리곤 검정 두꺼운 스트로크 한 겹) 후
    #    painter 순서로 채움 → 전체 외곽만 검정 윤곽, 내부는 톤 경계 + 디딤판 윤곽
    polys = []
    for depth, fill, stroke, w_, v in items:
        sx = v @ u; sy = v @ t
        polys.append((depth, fill, stroke, w_, list(zip(sx, sy))))
    allx = [p[0] for *_, pl in polys for p in pl]
    ally = [p[1] for *_, pl in polys for p in pl]
    span = max(max(allx) - min(allx), max(ally) - min(ally))
    s = (canvas - 80) / span
    ox = (canvas - (max(allx) + min(allx)) * s) / 2
    oy = (canvas + (max(ally) + min(ally)) * s) / 2
    def pstr(pl):
        return " ".join(f"{ox + x * s:.2f},{oy - y * s:.2f}" for x, y in pl)
    body = [extra]                             # 자가 봉합 패치(있다면 최후방)
    for *_, pl in polys:                       # 실루엣 언더레이
        body.append(f'<polygon points="{pstr(pl)}" fill="{INK}" stroke="{INK}" '
                    f'stroke-width="{sw * 2.2}" stroke-linejoin="round"/>')
    for _, fill, stroke, w_, pl in sorted(polys, key=lambda z: z[0]):
        body.append(f'<polygon points="{pstr(pl)}" fill="{fill}" stroke="{stroke}" '
                    f'stroke-width="{w_}" stroke-linejoin="round"/>')
    return svg_doc(canvas, canvas, "".join(body)), canvas, canvas


def _hole_patches(png_path, scale=3, margin=3):
    """렌더 PNG에서 내부 흰 구멍 검출 → 이웃 톤 사각 패치 SVG 문자열(최후방 삽입용).

    코너 턴에서 세 칸 사이로 시선이 통과하는 미세 슬릿(정직한 3D의 부산물)을
    이웃 벽톤으로 봉합. 최후방에 그려져 구멍 외 영역은 구조물이 전부 덮음."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    im = np.array(Image.open(png_path).convert("RGB"))
    g = im.mean(axis=2)
    white = g > 245
    lab, n = ndimage.label(white)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    border.discard(0)
    out = []
    for i in range(1, n + 1):
        if i in border:
            continue
        mask = lab == i
        if int(mask.sum()) < 9:
            continue
        ys, xs = np.where(mask)
        # 구멍 주변 링에서 비백색 중앙값 톤 샘플
        ring = ndimage.binary_dilation(mask, iterations=4) & ~mask
        rpx = im[ring]
        rpx = rpx[rpx.mean(axis=1) < 245]
        col = "#CFCFCF" if len(rpx) == 0 else "#{:02X}{:02X}{:02X}".format(
            *np.median(rpx, axis=0).astype(int))
        x0 = (xs.min() - margin) / scale; x1 = (xs.max() + margin) / scale
        y0 = (ys.min() - margin) / scale; y1 = (ys.max() + margin) / scale
        out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" '
                   f'height="{y1 - y0:.1f}" fill="{col}"/>')
    return "".join(out)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stairs":
        svg, w, h = fig_stairs()
        render(svg, "Fig07_계단_펜로즈", OUT, w, h)
        print("[penrose3d] Fig07_계단_펜로즈 (3D 상승 링)")
    else:
        svg, w, h = fig()
        render(svg, "Fig06_폭포_펜로즈", OUT, w, h)
        print("[penrose3d] Fig06_폭포_펜로즈 (3D 직교투영)")
