"""도판별 한/영 라벨 사전 — KO판/EN판 생성용. (bare diagram: 제목·캡션 없음)"""

# 4영역 명 (공통 참조)
DOMAINS = {
    "ko": ["시각", "청각", "논리", "계산"],
    "en": ["Visual", "Auditory", "Logical", "Computational"],
}

FIG1 = {  # 3단계 모델
    "ko": {
        "stage_word": "단계",
        "stages": ["환원", "자기참조", "창발"],
        "subs": ["단순 규칙·요소", "체계가 자기 자신을 지시", "환원으로 설명되지 않는 새 속성"],
        "axis": "자기참조 깊이 · 복잡도 →",
        "threshold": "임계",
    },
    "en": {
        "stage_word": "STAGE",
        "stages": ["Reduction", "Self-Reference", "Emergence"],
        "subs": ["simple rules · primitives", "system refers to itself", "novel · irreducible properties"],
        "axis": "recursive depth · complexity →",
        "threshold": "threshold",
    },
}

# 단계 접두 (Fig18 사분면 내부 3줄)
STAGE3 = {"ko": ["환원", "자기참조", "창발"], "en": ["Reduction", "Self-Reference", "Emergence"]}

FIG18 = {  # TRIH 통합 — 4영역 재귀적 동형
    "ko": {
        "domains": ["시각 · 에셔", "청각 · 바흐", "논리 · 괴델", "계산 · 트랜스포머"],
        "cells": [
            ["17 평면결정군", "그리는 손 (Drawing Hands)", "시각적 무한"],
            ["단일 동기 · 대위법", "무한상승 카논", "무한감"],
            ["Principia 형식 체계", "⌜G⌝ 명제", "불완전성 (메타-진리)"],
            ["Q·K·V 행렬 연산", "self-attention", "창발적 능력"],
        ],
        "center": ["자기참조의 임계", "마음의 가능성", "조건부"],
    },
    "en": {
        "domains": ["Visual · Escher", "Auditory · Bach", "Logical · Gödel", "Computational · Transformer"],
        "cells": [
            ["17 wallpaper groups", "Drawing Hands", "visual infinity"],
            ["motif · counterpoint", "endlessly rising canon", "sense of the infinite"],
            ["Principia system", "the sentence ⌜G⌝", "incompleteness (meta-truth)"],
            ["Q·K·V operations", "self-attention", "emergent ability"],
        ],
        "center": ["threshold of self-reference", "Possibility of Mind", "conditional"],
    },
}

FIG13 = {  # 괴델 명제 G 자기참조
    "ko": {
        "sys_title": "형식 체계 P · Principia Mathematica",
        "sys_sub": "공리(axioms) + 추론규칙(inference rules)",
        "arith": "산술화 · arithmetization",
        "g_def": "G ≡ “이 명제는 P 안에서 증명 불가능하다”",
        "loop_sub": "G가 자신의 괴델수를 지시",
        "meta_title": "메타-진리 · Meta-Truth",
        "meta_line": "G는 참이다 — 그러나 P에서 증명 불가",
        "meta_sub": "제1 불완전성 정리",
        "rail": ["환원", "자기참조", "창발"],
    },
    "en": {
        "sys_title": "Formal System P · Principia Mathematica",
        "sys_sub": "axioms + inference rules",
        "arith": "arithmetization",
        "g_def": "G ≡ “G is not provable in P”",
        "loop_sub": "G refers to its own Gödel number",
        "meta_title": "Meta-Truth",
        "meta_line": "G is true — yet unprovable in P",
        "meta_sub": "First Incompleteness Theorem",
        "rail": ["Reduction", "Self-Reference", "Emergence"],
    },
}
# Fig13 노테이션(언어 공통, mono)
FIG13_N = {
    "sys_note": "증명가능성 술어  Prov(x) · ⊢",
    "arith_note": {"ko": "g : 기호열 → ℕ", "en": "g : strings → ℕ"},
    "g_title": "⌜G⌝",
    "g_formula": "G ⟺ ¬Prov(⌜G⌝)",
    "loop_note": "sub(13, 17, 13)",
    "meta_formula": {"ko": "True(G) ∧ ¬Prov(⌜G⌝)  ⟹  P는 불완전", "en": "True(G) ∧ ¬Prov(⌜G⌝)  ⟹  P is incomplete"},
}

TABLE1 = {  # 4영역 동형성 매트릭스
    "ko": {
        "corner": "단계 \\ 영역",
        "cols": ["시각 · 에셔", "청각 · 바흐", "논리 · 괴델", "계산 · 트랜스포머"],
        "rows": ["환원", "자기참조", "창발"],
        "cells": [
            [("평면결정군 17 · 쌍곡 기하", "wallpaper groups"), ("단일 동기 + 대위법", "motif + counterpoint"),
             ("Principia 형식 체계", "axioms · Prov(x)"), ("Q·K·V 행렬 연산", "QKᵀ/√d · softmax")],
            [("그림 속 그림 그리는 손", "Drawing Hands"), ("회문 · 무한상승 · BACH", "palindrome · canon"),
             ("괴델 수와 ⌜G⌝", "sub(13, 17, 13)"), ("self-attention · ICL", "induction head")],
            [("시각적 무한 · 불가능 도형", "visual infinity"), ("무한감 · 미완성의 의미", "sense of the infinite"),
             ("메타-진리 · 불완전성", "¬Prov(⌜G⌝) ∧ True(G)"), ("창발적 능력", "emergent abilities")],
        ],
    },
    "en": {
        "corner": "Stage \\ Domain",
        "cols": ["Visual · Escher", "Auditory · Bach", "Logical · Gödel", "Computational · Transformer"],
        "rows": ["Reduction", "Self-Reference", "Emergence"],
        "cells": [
            [("17 wallpaper groups · hyperbolic", "wallpaper groups"), ("single motif + counterpoint", "motif + counterpoint"),
             ("Principia formal system", "axioms · Prov(x)"), ("Q·K·V matrix operations", "QKᵀ/√d · softmax")],
            [("a hand drawing itself", "Drawing Hands"), ("palindrome · rising · BACH", "palindrome · canon"),
             ("Gödel numbering and ⌜G⌝", "sub(13, 17, 13)"), ("self-attention · ICL", "induction head")],
            [("visual infinity · impossible figures", "visual infinity"), ("the infinite · the unfinished", "sense of the infinite"),
             ("meta-truth · incompleteness", "¬Prov(⌜G⌝) ∧ True(G)"), ("emergent abilities", "emergent abilities")],
        ],
    },
}

BACH = {  # 바흐 자기참조 형식 (3 패널)
    "ko": {
        "panels": ["회문 — 게 카논", "무한상승 카논", "B–A–C–H 모티프"],
        "subs": ["순행 = 역행 (시간 대칭)", "끝없는 상승 → 시작 (셰퍼드)", "작곡가의 이름을 음높이로"],
        "axis_l": "정행", "axis_r": "역행", "rise": "상승", "loop": "되돌아옴",
    },
    "en": {
        "panels": ["Crab Canon — retrograde", "Endlessly Rising Canon", "B–A–C–H motif"],
        "subs": ["forward = backward (time symmetry)", "endless rise → start (Shepard)", "the composer's name as pitch"],
        "axis_l": "forward", "axis_r": "retrograde", "rise": "rising", "loop": "returns",
    },
}

# Escher 영역 자체제작 (D-018) — 개념·수학 도식
FIG3 = {  # 17 평면결정군 (IUC 명은 공통, 그룹 헤더만 KO/EN)
    "groups": ["p1", "p2", "pm", "pg", "cm", "pmm", "pmg", "pgg", "cmm",
               "p4", "p4m", "p4g", "p3", "p3m1", "p31m", "p6", "p6m"],
    "ko": {"header": "17 평면결정군 (벽지 대칭군)", "rot": "최대 회전 차수"},
    "en": {"header": "the 17 wallpaper groups", "rot": "highest rotation order"},
}
FIG4 = {  # Drawing Hands → 상호 자기참조
    "ko": {"a": "A", "b": "B", "rel": "각자가 상대를 산출한다", "note": "상호 자기참조 (그리는 손)"},
    "en": {"a": "A", "b": "B", "rel": "each produces the other", "note": "mutual self-reference (Drawing Hands)"},
}
FIG5 = {  # Print Gallery → 드로스테 (무한 재귀 포함)
    "ko": {"note": "그림이 자기 자신을 포함한다", "sub": "무한 재귀 (드로스테 효과)"},
    "en": {"note": "the image contains itself", "sub": "infinite recursion (Droste effect)"},
}
FIG6 = {  # Waterfall → 불가능한 하강 루프
    "ko": {"down": "하강", "note": "끝없이 하강하지만 시작으로 돌아오는 닫힌 루프", "imp": "불가능 도형"},
    "en": {"down": "down", "note": "always descending, yet returning to the start", "imp": "impossible figure"},
}
FIG7 = {  # Ascending/Descending → 끝없는 상승 계단
    "ko": {"up": "상승", "note": "네 변 모두 오르막 — 끝없는 상승 계단", "imp": "불가능 도형"},
    "en": {"up": "up", "note": "every side ascends — an endless staircase", "imp": "impossible figure"},
}
FIG89 = {  # Circle Limit → 쌍곡 평면 (푸앵카레 원판)
    "ko": {"note": "푸앵카레 원판 — 경계로 갈수록 무한히 작아짐", "bd": "경계 = 무한"},
    "en": {"note": "Poincaré disk — cells shrink to infinity at the boundary", "bd": "boundary = infinity"},
}
MUSIC = {  # Fig10-12 개별 보표 모티프
    "ko": {
        "f10_t": "무한상승 카논 (Canon per Tonos)", "f10_s": "조성이 끝없이 상승하다 처음으로",
        "f11_t": "푸가의 기법 Contrapunctus XIV", "f11_s": "B–A–C–H = 작곡가의 이름이 음높이로",
        "f12_t": "게 카논 (Crab Canon)", "f12_s": "순행과 역행이 동일 (시간 회문)",
        "rise": "상승", "loop": "처음으로", "fwd": "정행", "bwd": "역행", "axis": "대칭축",
    },
    "en": {
        "f10_t": "Endlessly Rising Canon (Canon per Tonos)", "f10_s": "the key rises forever, back to the start",
        "f11_t": "The Art of Fugue, Contrapunctus XIV", "f11_s": "B–A–C–H = the composer's name as pitch",
        "f12_t": "Crab Canon", "f12_s": "forward equals backward (a palindrome in time)",
        "rise": "rising", "loop": "to the start", "fwd": "forward", "bwd": "retrograde", "axis": "axis",
    },
}

FIG17 = {  # 자체생성 attribution graph (자기참조 회로)
    "ko": {
        "a_prev": "A · 이전", "b_prev": "B · 이전", "a_cur": "A · 현재",
        "prev_feat": "이전-토큰 특징", "ind_feat": "유도 특징 (induction)", "out": "다음 토큰 예측: B",
        "selfref": "자기참조: 이전 등장의 다음 토큰을 참조",
        "leg": ["정보 흐름", "간접", "억제"], "note": "자기참조 회로 (귀속 그래프 양식, gpt2 §6 재구성)",
    },
    "en": {
        "a_prev": "A · earlier", "b_prev": "B · earlier", "a_cur": "A · current",
        "prev_feat": "prev-token feature", "ind_feat": "induction feature", "out": "predict next: B",
        "selfref": "self-reference: attend to the token after the previous occurrence",
        "leg": ["information flow", "indirect", "inhibitory"], "note": "self-referential circuit (attribution-graph style)",
    },
}

# 데이터 figs (matplotlib) 축/주석 — KO/EN
DATA = {
    "ko": {
        "attn_x": "key — 참조 대상 (attended-to)", "attn_y": "query — 현재 토큰 (attending)",
        "attn_note": "도식(예시) — 실측은 Python 산출", "attn_w": "어텐션 가중치",
        "scal_x": "모델 규모 · parameters (log)", "scal_y": "능력 (capability)",
        "scal_plateau": "우연 수준 정체", "scal_emerg": "창발적 능력", "scal_thr": "임계",
        "ind_x": "key 위치 (attended-to)", "ind_y": "query 위치 (attending)", "ind_stripe": "induction 줄무늬",
    },
    "en": {
        "attn_x": "key — attended-to", "attn_y": "query — attending",
        "attn_note": "schematic — measured values from Python", "attn_w": "attention weight",
        "scal_x": "model scale · parameters (log)", "scal_y": "capability",
        "scal_plateau": "near-random plateau", "scal_emerg": "emergent ability", "scal_thr": "threshold",
        "ind_x": "key position (attended-to)", "ind_y": "query position (attending)", "ind_stripe": "induction stripe",
    },
}
