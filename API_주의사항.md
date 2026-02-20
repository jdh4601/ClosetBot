---
title: "Instagram API 정책 준수 분석 보고서"
date: 2026-02-19
category: "API Policy"
---

# Instagram API 정책 준수 분석 보고서

> **대상 제품**: Fashion Brand Influencer Matcher (SaaS)
> **분석 기준**: Instagram Graph API / Business Discovery API / Meta Developer Policy (2025-2026 기준)

---

## 전체 요약

| 항목 | 판정 | 위험도 |
|------|------|--------|
| Business Discovery API 사용 자격 | ✅ 문제없음 | 낮음 |
| 데이터 수집 범위 (대부분 필드) | ✅ 문제없음 | 낮음 |
| like_count 필드 | ⚠️ 주의 필요 | 중간 |
| 데이터 영구 저장 (DB) | ⚠️ 주의 필요 | 중간 |
| SaaS 모델 (멀티테넌트 구조) | ⚠️ 주의 필요 | 중간-높음 |
| 분석 결과 제공/판매 | ⚠️ 주의 필요 | 중간 |
| CSV 내보내기 | ⚠️ 주의 필요 | 중간 |
| Rate Limit (200콜/시간) | ✅ 문제없음 | 낮음 |
| 필요 권한 범위 | ⚠️ 권한 부족 가능 | 높음 |
| App Review 통과 가능성 | ⚠️ 조건부 가능 | 중간 |

---

## 1. Business Discovery API 사용 자격 — ✅ 문제없음

Business Discovery API는 **타인 비즈니스/크리에이터 계정 조회를 위해 공식 설계**된 API다. 인플루언서 마케팅 도구는 Meta가 명시적으로 허용하는 사용 사례에 포함된다.

**전제 조건:**
- 앱 운영자 본인이 Facebook Page에 연결된 Instagram Business 계정을 보유해야 함
- 조회 대상은 Business/Creator 계정만 가능 (개인 계정 불가)
- PRD에 이미 명시됨 → 정상

---

## 2. 데이터 수집 범위 — ✅ 대부분 문제없음 / ⚠️ 일부 주의

### 사용 가능 필드 (문제없음)
- `username`, `name`, `followers_count`, `follows_count`, `media_count`, `biography`, `website`, `is_verified`
- `caption`, `comments_count`, `media_type`, `timestamp`, `permalink`
- `media_url`, `thumbnail_url` (단, URL 만료 정책 존재 — 하단 참고)

### 주의 필드

**`like_count`**
- Business Discovery API에서 반환 가능하지만 **계정 설정에 따라 숨겨진 경우 null 반환**
- PRD에 이미 "미제공 시 comments 기반 대체" 로직이 명시되어 있어 올바른 대응 ✅

**`profile_picture_url`**
- 반환되지만 **해당 URL을 장기 저장하면 Meta CDN 만료로 broken link 발생**
- DB에 저장하지 말고 실시간 조회 권장

### 2025년 이후 제거된 필드 (참고)
`video_views`, `email_contacts`, `profile_views`, `website_clicks`, `phone_call_clicks`, `text_message_clicks` 등 일부 insights 메트릭 제거됨
(직접 소유 계정용 insights 메트릭이라 Business Discovery와 다소 다른 맥락이나 참고용으로 기록)

---

## 3. 데이터 영구 저장 (PostgreSQL) — ⚠️ 주의 필요

Meta Developer Policy 규정:

- **데이터 삭제 의무**: 사용자가 앱 연결을 해제하거나 데이터 삭제를 요청하면 **즉시 삭제** 해야 함
  - 2024년 11월 Meta가 이 요건을 강화함
- **목적 제한**: 수집한 데이터는 "앱 서비스 제공 목적"으로만 사용 가능

### PRD 보완 필요 사항
- [ ] 사용자 데이터 삭제 요청 처리 메커니즘 추가
- [ ] 브랜드가 서비스 탈퇴 시 수집된 인플루언서 데이터도 삭제하는 로직 구현
- [ ] `profile_picture_url` 등 Meta CDN URL을 DB에 영구 저장하지 않도록 주의
- [ ] 데이터 보유 기간 명시 및 Privacy Policy 작성 필수

---

## 4. SaaS 멀티테넌트 구조 — ⚠️ 가장 중요한 주의 항목

### 구조 설명
여러 브랜드(users)가 하나의 앱(Meta App)을 통해 타인 인플루언서 계정 조회

### 동작 방식
Business Discovery API는 **앱 운영자 본인의 IG Business 계정 토큰**으로 타인 계정을 조회하는 API다:
- 앱 운영자의 단일 Facebook Page + IG Business 계정 1개를 앱에 연결
- 그 토큰으로 모든 사용자(브랜드들)의 조회 요청을 처리

이 구조는 **기술적으로 가능**하며, 기존 인플루언서 마케팅 SaaS들(HypeAuditor 등)이 유사한 방식으로 운영 중이다. 단, App Review 시 이 구조를 명확히 설명하고 승인받아야 한다.

### Rate Limit 주의사항
- 200콜/시간은 **앱 단위**가 아닌 **앱 + 조회 대상 계정 조합**으로 적용
- 동시에 여러 브랜드가 같은 인플루언서를 조회하면 rate limit이 공유됨
- 캐시 전략(Redis TTL)으로 중복 조회 최소화 필수

---

## 5. 분석 결과 제공/판매 — ⚠️ 조건 있음

### Meta Policy 규정
> "User Data를 판매, 라이선스, 임대, 양도하는 행위 금지"

### 해석
인플루언서 분석 SaaS는 "데이터 판매"가 아닌 **"분석 서비스 제공"**으로 해석 가능:
- HypeAuditor, Modash, CreatorIQ 등 기존 서비스들이 정상 운영 중
- 핵심 차이: 원시 데이터(raw data)를 그대로 재판매하는 게 아닌, **분석/가공된 인사이트를 제공**하는 것

### 허용/위험 범위
| 데이터 유형 | 허용 여부 |
|------------|---------|
| 분석 점수, 참여율 계산값 등 가공된 인사이트 | ✅ 허용 |
| 팔로워 수, 게시물 수 등 집계 지표 | ✅ 허용 |
| 원시 캡션 텍스트 그대로 제공 | ⚠️ 위험 |
| 미디어 URL 그대로 제공/저장 | ⚠️ 위험 |

---

## 6. CSV 내보내기 — ⚠️ 범위 조정 필요

PRD: "현재 테이블 뷰 기준 CSV 내보내기"

**권장 방향**: CSV 내보내기는 분석 결과(점수, 집계값) 위주로 제한

| 내보내기 항목 | 허용 여부 |
|-------------|---------|
| 종합 점수, 등급 | ✅ 허용 |
| 참여율, 팔로워 수, 게시물 수 | ✅ 허용 |
| 브랜드 유사도 점수 | ✅ 허용 |
| 캡션 원문 텍스트 | ⚠️ 제한 권장 |
| 게시물 permalink | ⚠️ 제한 권장 |
| biography 원문 | ⚠️ 제한 권장 |
| profile_picture_url | ❌ 제외 권장 |

---

## 7. Rate Limit — ✅ PRD 설정 정확함

**200콜/시간 설정이 정책과 일치한다.** 단, 적용 단위를 정확히 이해해야 함:

| 항목 | 내용 |
|------|------|
| 적용 단위 | 앱 + 조회 대상 계정 조합 |
| 윈도우 방식 | Rolling 1-hour window |
| 리셋 주기 | 매 24시간 |
| 카운팅 범위 | 실패 요청 포함, 페이지네이션 각각 1콜 |

PRD의 **큐잉 + 토큰 버킷 + 캐시 전략**이 올바른 접근이다.

---

## 8. 필요 권한 — ⚠️ 재확인 필요

### PRD 명시 권한
```
instagram_basic
pages_show_list
```

### 실제 필요 가능한 권한
| 권한 | 필요 이유 | 필수 여부 |
|------|----------|----------|
| `instagram_basic` | 기본 IG 계정 접근 | ✅ 필수 |
| `pages_show_list` | Facebook Page 목록 접근 | ✅ 필수 |
| `pages_read_engagement` | Page 접근 시 필요할 수 있음 | 확인 필요 |
| `instagram_manage_insights` | 상세 미디어 데이터 접근 시 필요 가능 | 확인 필요 |

**Action**: App Review 전에 Meta 공식 문서의 Business Discovery API 권한 요건 재확인 필수

---

## 9. App Review 통과 가능성 — ✅ 충분히 가능

유사 서비스들(HypeAuditor, Modash 등)이 App Review를 통과하여 운영 중이므로 **인플루언서 마케팅 분석 SaaS는 Meta가 허용하는 사용 사례**에 해당한다.

### App Review 제출 필수 항목
- [ ] 명확한 Privacy Policy (데이터 보유/삭제 정책 포함)
- [ ] 데이터 사용 목적 설명 (인플루언서 마케팅 분석)
- [ ] 앱 사용 데모 영상
- [ ] Data Use Checkup (DUC) 완료
- [ ] 멀티테넌트 구조 명확히 설명

---

## 10. 신규 API 검토 권장 (v2 로드맵)

Meta가 2025년 10월에 **Instagram Creator Marketplace API**와 **Facebook Creator Discovery API**를 공식 출시했다.

### 특징
- 브랜드가 크리에이터를 키워드로 검색
- 오디언스 demographics, 평균 참여율 확인
- Business Discovery API보다 **인플루언서 마케팅에 특화**

PRD v1의 Business Discovery 기반 접근도 유효하지만, Creator Marketplace API가 이 제품의 목적에 더 부합할 수 있다. **v2 로드맵에 검토 추가 권장**.

---

## 결론 및 필수 보완 사항

PRD의 핵심 방향은 **정책 위반이 아니다.** 안전한 운영을 위해 아래 3가지를 반드시 보완해야 한다:

### 필수 보완 (Must)
1. **데이터 삭제 정책 추가**: 사용자 탈퇴/요청 시 수집된 데이터 삭제 메커니즘 구현
2. **CSV 내보내기 범위 제한**: 가공된 분석값만 내보내기 (원시 캡션/URL 제외)
3. **App Review 전 권한 재확인**: Business Discovery API 실제 요구 권한 목록 검토

### 권장 보완 (Recommended)
4. `profile_picture_url` DB 저장 제거 → 실시간 조회 방식으로 변경
5. Privacy Policy 문서 작성 (App Review 필수 제출 서류)
6. Creator Marketplace API v2 로드맵 추가 검토

---

## 참고 자료

- [Instagram Graph API: Complete Developer Guide for 2026](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/)
- [Why Instagram is Cracking Down on Third-Party Apps in 2025](https://blog.postly.ai/why-instagram-is-cracking-down-on-third-party-apps-in-2025/)
- [Navigating Instagram API Rate Limit Errors | Phyllo](https://www.getphyllo.com/post/navigating-instagram-api-rate-limit-errors-a-comprehensive-guide)
- [Meta Developer Data Use Policy](https://developers.meta.com/horizon/policy/data-use/)
- [Instagram and Facebook launch new creator marketplace and discovery APIs](https://web.swipeinsight.app/posts/instagram-and-facebook-launch-new-creator-marketplace-and-discovery-apis-19339)
- [Is Instagram Scraping Legal? The 2025 Developer's Guide](https://sociavault.com/blog/instagram-scraping-legal-2025)
- [Meta enhances Developer Platform with new user data deletion requirements](https://ppc.land/meta-enhances-developer-platform-with-new-user-data-deletion-requirements/)
