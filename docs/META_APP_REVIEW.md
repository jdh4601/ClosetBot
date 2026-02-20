# Meta App Review 준비 가이드

## 개요

Fashion Influencer Matcher는 Instagram Graph API의 Business Discovery 엔드포인트를 사용하여 공개 Instagram 비즈니스/크리에이터 계정의 데이터를 수집합니다. 이 문서는 Meta App Review 제출을 위한 준비 사항을 정리합니다.

---

## 필요한 권한 (Permissions)

### 필수 권한

| 권한 | 용도 | 데이터 접근 범위 |
|-----|------|----------------|
| `instagram_basic` | Instagram 프로필 데이터 읽기 | username, followers_count, media_count, biography |
| `pages_show_list` | 연결된 Facebook 페이지 목록 조회 | 페이지 ID 목록 |

### 검토 중인 권한 (App Review 시 확인 필요)

> **참고**: Business Discovery API 사용을 위해 추가 권한이 필요한지 Meta 공식 문서에서 재확인 필요

- `pages_read_engagement` - 페이지 참여도 데이터 읽기 (필요 시)
- `instagram_manage_insights` - 인사이트 데이터 접근 (필요 시)

---

## App Review 제출 체크리스트

### 사전 준비

- [ ] Facebook 개발자 계정 생성
- [ ] Facebook Business 계정 설정
- [ ] Instagram Business/Creator 계정 연결
- [ ] 개인정보처리방침 페이지 작성 (PRIVACY_POLICY.md 참고)
- [ ] 데이터 삭제 절차 문서화
- [ ] 앱 아이콘 및 설명 준비

### 제출 자료

- [ ] **동의 화면 스크린샷**: 사용자가 권한 요청을 확인하는 화면
- [ ] **앱 시연 동영상** (최대 5분):
  - 브랜드 계정 입력
  - 인플루언서 분석 요청
  - 분석 결과 조회
  - 데이터 삭제 기능 시연
- [ ] **사용 사례 설명**: 왜 이러한 데이터가 필요한지 상세 설명
- [ ] **데이터 사용 방식**: 수집된 데이터의 처리 및 저장 방식

---

## 스크린샷/동영상 가이드라인

### 권장 콘텐츠

1. **로그인/인증 화면**
   - Facebook 로그인 버튼
   - 권한 요청 화면 (scope 표시)
   - 사용자 동의 과정

2. **주요 기능 시연**
   ```
   [시나리오 1] 브랜드 프로필 분석
   1. 브랜드 Instagram username 입력
   2. "분석 시작" 버튼 클릭
   3. 분석 진행 상태 표시
   4. 분석 결과 대시보드 표시
   
   [시나리오 2] 인플루언서 비교
   1. 브랜드 + 5명 인플루언서 입력
   2. 분석 요청
   3. 점수순으로 정렬된 결과 테이블
   4. 상세 분석 페이지
   
   [시나리오 3] 데이터 삭제
   1. 설정 페이지 이동
   2. "내 데이터 삭제" 버튼 클릭
   3. 삭제 확인
   4. 삭제 완료 메시지
   ```

3. **개인정보 보호 화면**
   - Privacy Policy 링크
   - 데이터 삭제 요청 양식
   - 연락처 정보

### 촬영 요구사항

- **해상도**: 1280x720 이상
- **형식**: MP4 (비디오), PNG (스크린샷)
- **언어**: 한국어 (필요시 영어 자막 추가)
- **길이**: 동영상 3-5분, 스크린샷은 핵심 화면 5-10장

---

## 데이터 사용 설명

### 데이터 수집

```
수집 주체: Fashion Influencer Matcher
수집 방법: Instagram Graph API (Business Discovery)
수집 대상: 공개 Instagram 비즈니스/크리에이터 계정
수집 데이터:
  - 프로필: username, followers_count, media_count, biography, website
  - 미디어: caption, comments_count, like_count (optional), media_type, permalink, timestamp
```

### 데이터 처리

```
처리 목적: 브랜드-인플루언서 적합도 분석
처리 방법:
  1. 해시태그 추출 및 분석
  2. 참여율 (engagement rate) 계산
  3. 패션 카테고리 분류
  4. 브랜드와의 유사도 점수 산정
보관 기간: 90일 (자동 삭제)
처리 위치: AWS 서울 리전
```

### 사용자 제어

- 데이터 캐싱 비활성화 요청 가능
- 계정 삭제 시 모든 데이터 즉시 삭제
- 분석 결과는 90일 후 자동 삭제

---

## 데이터 삭제 절차

### 사용자 요청 시

1. **요청 접수**
   - 이메일: privacy@fasion.app
   - 처리 기간: 7영업일

2. **삭제 실행**
   - PostgreSQL에서 사용자 계정 삭제
   - 관련된 모든 분석 작업(job) 삭제
   - 관련된 모든 분석 결과 삭제
   - Redis 캐시에서 해당 계정 데이터 삭제

3. **삭제 확인**
   - 이메일로 삭제 완료 통보
   - 삭제 로그 보관 (법적 의무)

### 자동 삭제

```python
# 90일 보유 기간 만료 시 자동 삭제
SCHEDULED_TASK:
  - 매일 자정 실행
  - 만료된 profile 데이터 삭제
  - 만료된 media 데이터 삭제
  - 만료된 analysis_result 삭제
```

---

## App Review 심사 기준

### 합격 기준

- [ ] **데이터 최소화**: 필요한 데이터만 수집
- [ ] **명확한 사용 목적**: 데이터 사용 목적 명시
- [ ] **사용자 제어**: 데이터 삭제 기능 제공
- [ ] **보안**: 적절한 보안 조치 시행
- [ ] **정책 준수**: Meta Developer Policy 준수

### 주요 반려 사유

- 비즈니스/크리에이터가 아닌 개인 계정 접근
- 비공개 계정 데이터 수집
- 데이터 판매 또는 제3자 제공
- 불분명한 데이터 사용 목적
- 데이터 삭제 기능 미제공

---

## 제출 후 프로세스

### 타임라인

1. **제출**: 앱 및 동영상 업로드
2. **검토**: Meta 심사팀 검토 (3-5 영업일)
3. **피드백**: 추가 정보 요청 또는 승인/반려
4. **수정**: 피드백 반영 후 재제출 (필요시)
5. **승인**: 프로덕션 모드 사용 가능

### 승인 후

- [ ] 프로덕션 모드 전환
- [ ] 실제 Instagram 계정으로 테스트
- [ ] 모니터링 대시보드 설정
- [ ] 정기적인 API 사용량 체크

---

## 연락처 및 지원

### Meta Developer Support
- [Meta for Developers](https://developers.facebook.com/)
- [Instagram Graph API 문서](https://developers.facebook.com/docs/instagram-api)

### 서비스 문의
- **이메일**: support@fasion.app
- **개발팀**: dev@fasion.app

---

## 참고 자료

- [Meta Developer Policy](https://developers.facebook.com/policy/)
- [Instagram Graph API 사용약관](https://developers.facebook.com/terms/)
- [Business Discovery API 가이드](https://developers.facebook.com/docs/instagram-api/reference/ig-user/business-discovery)
