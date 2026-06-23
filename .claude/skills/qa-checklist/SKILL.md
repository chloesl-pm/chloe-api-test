---
name: qa-checklist
description: API 테스트 품질 검증 5개 항목의 체크리스트 방법론. qa-validator 에이전트가 사용하는 공유 검증 기준. 커버리지·assert품질·스키마·리소스누수·SLA 기준 정의.
---

## 목적

qa-validator가 테스트 결과를 평가할 때 참조하는 표준 체크리스트. 여러 서비스(Pub/Sub, Data Query 등)에 공통 적용 가능한 재사용 방법론.

---

## 체크리스트 5개 항목

### ① 커버리지 (Coverage) — 가중치 30%

| 등급 | 기준 |
|------|------|
| ✅ 양호 | 80% 이상 |
| ⚠️ 보통 | 50~79% |
| ❌ 불충분 | 50% 미만 |

미테스트 엔드포인트는 서비스 임팩트 등급(P0~P3)과 함께 목록화.

---

### ② Assert 품질 (Assert Quality) — 가중치 30%

| 등급 | 기준 | 점수 |
|------|------|------|
| GOOD | status + body 관련 assert 포함 | 100 |
| WEAK | status/statusRange assert만 있음 | 50 |
| NONE | assert 없음 | 0 |

GOOD 비율이 70% 이상이면 양호.

---

### ③ 스키마 검증 (Schema Validation) — 가중치 20%

응답 body 실제 필드 vs Swagger 정의 필수 필드 비교.
- 필수 필드가 모두 존재하면 PASS
- 누락 필드 1개 이상이면 FAIL

---

### ④ 리소스 누수 (Resource Leak) — 가중치 10%

teardown의 DELETE 스텝 성공 여부 확인.
- 누수 없음: 100점
- 누수 1건 이상: 0점 + 수동 삭제 필요 항목 목록 출력

---

### ⑤ SLA 준수 (SLA Compliance) — 가중치 10%

| API 유형 | 기준 시간 |
|----------|----------|
| console (dashboard/quota/service) | 2,000ms |
| pubsub (topics/subscriptions/publish/pull) | 3,000ms |
| 기타 | 3,000ms |

전체 스텝 중 SLA 준수 비율로 점수 산정.

---

## 종합 점수 산정

```
종합 점수 = 커버리지(30%) + Assert품질(30%) + 스키마(20%) + 누수(10%) + SLA(10%)
```

| 종합 점수 | 판정 |
|----------|------|
| 90 이상 | ✅ 우수 |
| 70~89 | ⚠️ 양호 |
| 70 미만 | ❌ 개선 필요 |

---

## 신규 서비스 적용 시

새 서비스(Data Query 등) 추가 시 SLA 기준만 서비스에 맞게 조정하고 나머지 항목은 동일하게 적용한다.
