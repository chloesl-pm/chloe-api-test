# CLAUDE.md — Pub/Sub Swagger API 자동화 테스트 하네스

## 하네스: Pub/Sub Swagger API 자동화 테스트

**목표:** index.html의 시나리오·Swagger 스펙을 기반으로 Kakao Cloud Pub/Sub API를 CLI에서 자동 실행·검증·리포트

**트리거:** "테스트 실행", "시나리오 실행", "API 검증", "전체 실행", "s1/s2/s3 실행", "결과 리포트", "API 테스트해줘", "시나리오 돌려줘" 등 테스트 관련 요청 시 `orchestrator` 에이전트를 사용하라. 단순 질문은 직접 응답 가능.

**규칙:** git push는 사용자가 명시적으로 요청할 때만 실행. 작업 완료 후 자동 push 금지.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-06-15 | 초기 구성 | 전체 | index.html 분석 기반 신규 구축 |
| 2026-06-23 | QA 검증 에이전트·스킬 추가 | qa-validator | 테스트 품질 검증 역할 신규 추가 |
| 2026-06-23 | 기획 에이전트·스킬 추가 | service-planner | 유저 저니·우선순위·통합 시나리오 기획 역할 신규 추가 |
| 2026-06-23 | 에이전트/스킬 구조 재정의 | 전체 | 중복 제거 및 역할 분리 |

---

## 프로젝트 개요

Kakao Cloud Pub/Sub API Swagger 자동화 테스트 도구.

- `index.html`: 브라우저 기반 UI 테스트 도구 (수정 금지) — Claude Code와 함께 기획·제작한 하네스 이전의 원형 툴. 이 툴의 시나리오 구조(SCENARIOS, extract/inject/assert)와 인증 패턴을 기반으로 현재 CLI 하네스가 구축됨
- `swagger/`: API 스펙 파일 4종 (console_v1/v2, pubsub_v1/v2)
- `.claude/`: 하네스 에이전트·스킬 (CLI 기반 자동화)
- `_workspace/`: 테스트 실행 시 생성되는 중간/결과 파일 (런타임 생성)

## 에이전트 구성

에이전트 = 역할 주체 (누가, 판단과 책임)

| 에이전트 | 역할 |
|---------|------|
| `orchestrator` | 전체 워크플로우 지휘 (Phase 0~5 순차 파이프라인) |
| `spec-analyst` | Swagger JSON + index.html 시나리오 파싱 |
| `api-test-runner` | HTTP API 실행, extract/inject/assert 처리 |
| `qa-validator` | 실행 결과 리포트 생성 + 품질 교차 검증 |
| `service-planner` | 유저 저니·비즈니스 임팩트·통합 시나리오 기획 |

## 스킬 구성

스킬 = 재사용 방법론 (어떻게, 여러 에이전트가 공유)

| 스킬 | 사용 주체 | 역할 |
|------|---------|------|
| `swagger-spec-reader` | spec-analyst | Swagger JSON 파싱 패턴 |
| `scenario-executor` | api-test-runner | API 시나리오 실행 패턴 (extract/inject/assert) |
| `test-report-generator` | qa-validator | 결과 리포트 생성 패턴 |
| `qa-checklist` | qa-validator | 품질 검증 5개 항목 체크리스트 (커버리지·assert·스키마·누수·SLA) |
