---
name: qa-validator
description: 테스트 결과와 Swagger 스펙을 교차 검증해 품질 리포트를 생성한다. "QA 검증", "커버리지 확인", "품질 검사", "스키마 검증", "QA 리포트" 요청 시 사용.
---

## 목적

`_workspace/test-results.json`과 `_workspace/spec-analysis.json`을 교차 분석해 테스트 품질을 5가지 관점에서 평가하고 `_workspace/qa-report.md`를 생성한다.

---

## QA 검증 실행 시점

| 상황 | 처리 |
|------|------|
| `test-results.json` 있음 | 즉시 QA 검증 실행 |
| `test-results.json` 없음 | "시나리오를 먼저 실행하세요" 안내 후 종료 |
| `spec-analysis.json` 없음 | 커버리지 검증 스킵, 나머지만 수행 |

---

## 5가지 검증 항목

### ① 커버리지 (Coverage)

Swagger 전체 엔드포인트 대비 실제 테스트된 엔드포인트 비율.

```
커버율 = 테스트된 엔드포인트 수 / 전체 엔드포인트 수 × 100
```

- 80% 이상: ✅ 양호
- 50~79%: ⚠️ 보통
- 50% 미만: ❌ 불충분

### ② Assert 품질 (Assert Quality)

각 스텝의 assert 규칙 충실도 평가:

| 등급 | 기준 |
|------|------|
| ✅ GOOD | status + body 관련 assert 포함 |
| ⚠️ WEAK | status/statusRange assert만 있음 |
| ❌ NONE | assert 없음 |

### ③ 응답 스키마 검증 (Schema Validation)

실제 응답 body 필드가 Swagger 정의 스키마와 일치하는지 확인.

### ④ 리소스 누수 탐지 (Resource Leak)

DELETE 스텝 실패 시 리소스가 정리되지 않은 것으로 판단, 수동 삭제 필요 항목 목록화.

### ⑤ SLA 준수 (SLA Compliance)

| API 유형 | 기준 |
|----------|------|
| console (dashboard/quota/service) | 2,000ms |
| pubsub (topics/subscriptions/publish/pull) | 3,000ms |

---

## 실행 방법

qa-validator 에이전트를 서브 에이전트로 호출:

```
Agent(
  description="QA 검증 및 품질 리포트 생성",
  subagent_type="qa-validator",
  prompt="""
  _workspace/test-results.json과 _workspace/spec-analysis.json을 교차 검증한다.
  5가지 항목(커버리지, assert품질, 스키마, 누수, SLA)을 평가하고
  _workspace/qa-report.md를 생성한 뒤 종합 점수를 콘솔에 출력한다.
  작업 경로: /Users/kakao_ent/chloe_workspace/api_test_tool/analytics-api-test-tool
  """
)
```

---

## 종합 점수 산정

| 항목 | 가중치 |
|------|--------|
| 커버리지 | 30% |
| Assert 품질 (GOOD 비율) | 30% |
| 스키마 준수율 | 20% |
| 리소스 누수 없음 | 10% |
| SLA 준수율 | 10% |

**종합 점수 = 각 항목 점수 × 가중치 합산 (100점 만점)**

---

## 출력

- `_workspace/qa-report.md`: 전체 QA 리포트
- 콘솔: 종합 점수 1줄 요약 (`QA 종합: {score}/100 — 커버리지 {rate}% | GOOD assert {good}% | SLA {sla}%`)
