---
name: ui-style-guide
description: 이 프로젝트(index.html)의 디자인 시스템과 UI 패턴 가이드. UI 수정, 새 컴포넌트 추가, 스타일 일관성 검토, 레이아웃 문제 진단 시 반드시 이 스킬을 먼저 읽을 것. ux-designer 에이전트가 사용하는 공유 기준.
---

## 디자인 토큰 (CSS Variables)

```css
:root {
  --primary    /* 주 액션색, 포커스, 활성 */
  --success    /* 성공/PASS */
  --danger     /* 오류/FAIL */
  --border     /* 모든 테두리 */
  --radius     /* 모든 모서리 반경 */
  --surface    /* 패널 배경 */
  --surface2   /* 입력 필드 배경 */
  --bg         /* 페이지 배경 */
  --text       /* 본문 */
  --text-muted /* 보조/label */
}
```

하드코딩 색상·크기 금지 — 반드시 변수 사용.

---

## 컴포넌트 높이 기준: **30px 통일**

```css
/* input */
.input-wrap input {
  height: 30px;
  padding: 0 10px;
  box-sizing: border-box;
}
.input-wrap input.has-eye { padding-right: 30px; } /* 눈 아이콘 여백 */

/* select */
select { height: 30px; box-sizing: border-box; }

/* env 버튼 */
.env-btn { height: 30px; box-sizing: border-box; }

/* 일반 버튼 (btn-sm) */
.btn-sm { padding: 4px 10px; font-size: 12px; } /* ~28px, flex-end 정렬로 시각적 통일 */
```

---

## 너비 클래스

| class | 너비 | 용도 |
|-------|------|------|
| `.wide` | 240px | Base URL, X-Auth-Token |
| `.medium` | 150px | Credential-ID, Credential-Secret |
| `.narrow` | 110px | Domain-ID, Project-ID |

---

## Auth Panel 레이아웃

```
┌─────────────────────────────────────────────────────────────────┐
│ Row 1: [Service ▾]  [Stage] [CBT] [Prod]  [Base URL_________] │
├─────────────────────────────────────────────────────────────────┤
│ Row 2: [Domain] [Project] [Cred-ID] [Cred-Sec] [Token____] 🔑💾│
└─────────────────────────────────────────────────────────────────┘
```

```css
.auth-panel-inner { display:flex; flex-direction:column; gap:8px; }
.auth-row         { display:flex; gap:10px; align-items:flex-end; flex-wrap:wrap; }
.auth-row+.auth-row { padding-top:6px; border-top:1px solid var(--border); }
```

---

## label 스타일

```css
.auth-field label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: .05em;
}
.auth-field { display:flex; flex-direction:column; gap:3px; }
```

---

## 환경 버튼 그룹 (env-btn-group)

```css
.env-btn-group { display:flex; gap:4px; }
.env-btn       { height:30px; padding:0 10px; font-size:12px; border:1px solid var(--border); ... }
.env-btn.active { background:var(--primary); color:#fff; border-color:var(--primary); }
.env-btn:disabled { opacity:0.38; pointer-events:none; }
```

Disabled 툴팁 — CSS `::after`로 구현 (`data-tip` 속성 사용):

```css
.env-opt-wrap[data-disabled="true"]:hover::after {
  content: attr(data-tip);
  /* 말풍선 스타일 */
}
```

---

## 새 컴포넌트 추가 체크리스트

새 서비스/필드를 추가할 때:

- [ ] 높이 30px + `box-sizing:border-box` 적용
- [ ] CSS 변수 사용 (하드코딩 금지)
- [ ] `.auth-row` 내 적절한 row에 배치
- [ ] 새 input에 `.has-eye` 또는 일반 padding 선택
- [ ] 너비 클래스(`.wide`/`.medium`/`.narrow`) 적용
- [ ] label이 10px uppercase 스타일인지 확인
