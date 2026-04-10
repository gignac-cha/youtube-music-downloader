# 모바일 반응형, 접근성 및 경쟁 분석 리서치

> UI/UX 리서치 에이전트 #5 | 2026-04-10
> YouTube Music Downloader (React 19 + Radix UI Themes + TypeScript)

---

## 목차

1. [경쟁 분석](#1-경쟁-분석)
2. [모바일 반응형 디자인 패턴](#2-모바일-반응형-디자인-패턴)
3. [웹 접근성 (WCAG) 요구사항](#3-웹-접근성-wcag-요구사항)
4. [PWA 고려사항](#4-pwa-고려사항)
5. [성능 UX 패턴](#5-성능-ux-패턴)
6. [현재 앱 분석 및 구체적 권장사항](#6-현재-앱-분석-및-구체적-권장사항)

---

## 1. 경쟁 분석

### 1.1 경쟁 도구 비교표

| 기능/특성 | y2mate | yt1s | savefrom.net | cobalt.tools | 9convert | **본 앱 (현재)** |
|---|---|---|---|---|---|---|
| **모바일 반응형** | O (기본) | O (양호) | O (기본) | O (우수) | O (기본) | X (미구현) |
| **다크 모드** | X | X | X | O | X | O (기본) |
| **검색 내장** | X (URL만) | X (URL만) | X (URL만) | X (URL만) | X (URL만) | **O (차별점)** |
| **배치 다운로드** | X | X | X | O | X | X |
| **포맷 선택** | O (다양) | O (다양) | O (다양) | O (다양) | O (다양) | X (MP3만) |
| **광고** | 매우 많음 | 많음 | 많음 | 없음 | 많음 | 없음 |
| **PWA 지원** | X | X | X | O | X | X |
| **접근성** | 매우 낮음 | 낮음 | 낮음 | 보통 | 낮음 | 낮음 |
| **파일 관리** | X | X | X | X | X | **O (차별점)** |
| **재생 미리듣기** | X | X | X | X | X | **O (차별점)** |
| **진행률 표시** | 제한적 | 제한적 | X | O | 제한적 | **O (실시간)** |
| **오프라인 사용** | X | X | X | 부분적 | X | X |
| **키보드 내비게이션** | 매우 낮음 | 낮음 | 낮음 | 보통 | 낮음 | 부분적 |
| **스크린 리더** | X | X | X | 부분적 | X | X |
| **UI 품질** | 낮음 | 보통 | 보통 | **우수** | 낮음 | 보통 |
| **속도** | 보통 | 빠름 | 보통 | 빠름 | 보통 | 보통 |

### 1.2 경쟁사별 상세 분석

#### cobalt.tools (최고 벤치마크)
- **강점**: 깔끔한 미니멀 UI, 광고 없음, 오픈소스, PWA 지원, 다크/라이트 모드, 다양한 플랫폼 지원 (YouTube, Twitter, TikTok 등), 배치 다운로드, 우수한 모바일 경험
- **약점**: 내장 검색 없음 (URL 붙여넣기만), 파일 관리 없음, 재생 미리듣기 없음
- **교훈**: 단순하고 깔끔한 인터페이스가 사용자 만족도를 높임. 광고 없는 경험이 핵심 차별점

#### y2mate
- **강점**: 높은 인지도, 다양한 포맷/품질 옵션
- **약점**: 과도한 광고와 팝업, 악성 리다이렉트, 모바일에서 특히 사용 어려움, 접근성 전혀 고려 안 됨, CAPTCHA 빈번
- **교훈**: 광고가 UX를 완전히 파괴할 수 있음. 반면교사

#### yt1s
- **강점**: 비교적 깔끔한 UI, 빠른 변환 속도, 모바일 레이아웃 합리적
- **약점**: 광고 존재, URL만 지원, 파일 관리 없음
- **교훈**: 속도가 핵심 경쟁력. 변환 대기 시간 최소화 중요

#### savefrom.net
- **강점**: 브라우저 확장 프로그램 연동, 다양한 사이트 지원
- **약점**: 광고 많음, 모바일 경험 불량, 접근성 미고려
- **교훈**: 브라우저 통합이 편의성을 높일 수 있음

#### 9convert
- **강점**: 다국어 지원, 서버 사이드 변환
- **약점**: 과도한 광고, 느린 변환 속도, 모바일 UI 조악
- **교훈**: 다국어 지원은 글로벌 사용자 확보에 중요

### 1.3 본 앱의 경쟁 우위

현재 본 앱이 가진 **고유한 차별점**:
1. **내장 검색 기능**: 다른 도구들은 모두 URL 붙여넣기만 지원. 검색에서 다운로드까지 원스톱 경험
2. **파일 관리**: 다운로드된 파일 목록 조회, 재생, 삭제 기능
3. **인라인 재생**: 다운로드 전/후 미리듣기 가능
4. **광고 없음**: cobalt.tools 외에는 대부분 광고 과다
5. **다크 모드 기본**: 음악 앱에 적합한 분위기

**강화해야 할 영역**:
1. 모바일 반응형 (현재 전혀 미구현)
2. 접근성 (WCAG 미준수)
3. PWA 지원
4. 성능 UX (로딩 상태, 스켈레톤 등)

---

## 2. 모바일 반응형 디자인 패턴

### 2.1 터치 타겟 (Touch Targets)

**WCAG 2.2 Level AA 요구사항 (Success Criterion 2.5.8)**:
- 최소 터치 타겟 크기: **24x24 CSS px** (AA), **44x44 CSS px** (AAA 권장)
- Google Material Design 권장: **48x48dp** (터치 영역), 시각적 요소는 더 작을 수 있음
- Apple HIG 권장: **44x44pt**

**현재 앱 문제점**:
- `IconButton size={'1'}` (AudioPlayer, Delete 버튼): Radix UI의 size 1은 약 24px로, 모바일 터치에 너무 작음
- 검색 결과 항목의 선택 버튼 (`IconButton`): 기본 크기이나 모바일에서 정밀 터치 필요
- 삭제 확인/취소 버튼이 size 1로 매우 작음

**권장사항**:
```
모바일 환경:
- 모든 인터랙티브 요소 최소 44x44px
- 버튼 간 최소 간격 8px
- 터치 영역이 시각적 영역보다 클 수 있음 (padding으로 확장)
```

### 2.2 모바일 레이아웃 패턴

#### Bottom Sheet 패턴
음악/미디어 앱에서 가장 효과적인 모바일 패턴:
- **미니 플레이어**: 화면 하단에 현재 재생 중인 트랙 표시 (Spotify, Apple Music 패턴)
- **검색 결과**: Bottom Sheet로 올라오는 검색 결과 목록
- **다운로드 상세**: 스와이프 업으로 진행률 상세 보기

**구현 권장**:
```
- @radix-ui/react-dialog를 활용한 Bottom Sheet 커스텀 구현
- 또는 vaul 라이브러리 (Radix 기반 드로어 컴포넌트)
- 모바일에서 검색 결과를 Bottom Sheet으로 표시
- 현재 재생 중인 곡을 하단 미니 플레이어로 표시
```

#### 반응형 브레이크포인트

```
/* 권장 브레이크포인트 */
--mobile:   0 ~ 639px    (1열 레이아웃, 풀 너비)
--tablet:   640 ~ 1023px (여유 있는 1열, 패딩 증가)
--desktop:  1024px+      (현재 레이아웃 유지)

/* Radix UI Container size 매핑 */
모바일: Container size="1" (max-width: 448px에 100% 너비)
태블릿: Container size="2" (max-width: 688px)
데스크톱: Container size="2" (현재 유지)
```

#### 모바일 전용 고려사항

1. **검색 입력**: 모바일에서 전체 너비 사용, 키보드 올라올 때 스크롤 조정
2. **검색 결과 카드**: 세로 스택으로 변경 (현재 가로 배치는 모바일에서 비좁음)
3. **다운로드 목록**: 테이블 대신 카드 리스트로 변경 (모바일에서 테이블은 가독성 낮음)
4. **스와이프 제스처**: 목록 항목에서 좌로 스와이프하면 삭제 옵션 표시

### 2.3 검색 결과 카드 모바일 최적화

현재 구조 (가로 배치):
```
[썸네일] [제목 / 아티스트 / 메타] [선택 버튼]
```

모바일 권장 구조 (세로 스택):
```
[썸네일 (전체 너비 또는 큰 사이즈)]
[제목]
[아티스트 | 재생시간 | 조회수]
[선택 버튼 (전체 너비)]
```

### 2.4 다운로드 목록 모바일 최적화

현재 `Table` 컴포넌트 사용 --> 모바일에서 가독성 문제:

```
현재: [다운로드 링크 텍스트] [크기 뱃지] [재생] [삭제]
      → 가로 공간 부족, 텍스트 잘림

모바일 권장:
┌─────────────────────────┐
│ 제목                     │
│ 파일크기 | 재생시간       │
│ [재생] [다운로드] [삭제]  │
└─────────────────────────┘
```

### 2.5 제스처 내비게이션

| 제스처 | 동작 |
|---|---|
| 좌측 스와이프 (목록 항목) | 삭제 옵션 표시 |
| 우측 스와이프 (목록 항목) | 다운로드 |
| 아래로 당기기 (Pull-to-refresh) | 목록 새로고침 |
| 길게 누르기 (검색 결과) | 컨텍스트 메뉴 (YouTube에서 보기, 다운로드) |

---

## 3. 웹 접근성 (WCAG) 요구사항

### 3.1 현재 앱 접근성 감사 결과

#### 심각한 문제 (Level A 위반)

| 문제 | WCAG 기준 | 위치 | 심각도 |
|---|---|---|---|
| IconButton에 접근 가능한 이름 없음 | 1.1.1 (텍스트 대안) | 모든 IconButton | **치명적** |
| 검색 결과 선택 상태를 시각적으로만 전달 | 1.3.1 (정보와 관계) | Search.tsx | **높음** |
| 재생/일시정지 상태 스크린 리더 미전달 | 4.1.2 (이름, 역할, 값) | AudioPlayer | **높음** |
| `<details>` 요소의 접근 가능한 이름 없음 | 4.1.2 | Search.tsx | **중간** |
| 다운로드 진행률을 스크린 리더에 미전달 | 1.3.1 | DownloadProgress.tsx | **높음** |
| 삭제 확인 대화상자에 포커스 트랩 없음 | 2.4.3 (포커스 순서) | Downloaded.tsx | **중간** |
| 색상만으로 상태 구분 (다운로드됨 뱃지) | 1.4.1 (색상 사용) | Search.tsx | **중간** |

#### 개선 필요 (Level AA)

| 문제 | WCAG 기준 | 위치 |
|---|---|---|
| 포커스 표시기 커스터마이징 필요 | 2.4.7 (포커스 가시성) | 전체 |
| 오류 메시지 접근성 | 3.3.1 (오류 식별) | 검색, 다운로드 |
| 터치 타겟 크기 부족 | 2.5.8 (타겟 크기) | 소형 IconButton들 |
| skip navigation 링크 없음 | 2.4.1 (블록 건너뛰기) | Root.tsx |

### 3.2 ARIA 레이블 권장사항

#### IconButton 접근성

```tsx
// 현재 (접근성 없음)
<IconButton onClick={onClick}>
  <MagnifyingGlassIcon />
</IconButton>

// 권장
<IconButton onClick={onClick} aria-label="검색">
  <MagnifyingGlassIcon />
</IconButton>
```

**모든 IconButton에 필요한 aria-label**:

| 컴포넌트 | 버튼 | 필요한 aria-label |
|---|---|---|
| Search | 검색 버튼 | "검색" 또는 "YouTube 검색" |
| Search | 초기화 버튼 | "검색 초기화" (현재 title만 있음) |
| Search | 결과 선택 버튼 | "'{제목}' 선택" / "'{제목}' 선택됨" |
| Download | 다운로드 버튼 | "다운로드 시작" |
| Downloaded | 재생 버튼 | "'{제목}' 재생" / "'{제목}' 일시정지" |
| Downloaded | 삭제 버튼 | "'{제목}' 삭제" |
| Downloaded | 삭제 확인 | "삭제 확인" |
| Downloaded | 삭제 취소 | "삭제 취소" |
| Downloaded | 새로고침 | "다운로드 목록 새로고침" |

#### 오디오 플레이어 접근성

```tsx
// 현재 (최소한의 접근성)
<IconButton size={'1'} radius="full" onClick={toggle}>
  {isPlaying ? <PauseIcon /> : <PlayIcon />}
</IconButton>

// 권장
<IconButton
  size={'1'}
  radius="full"
  onClick={toggle}
  aria-label={isPlaying ? `${title} 일시정지` : `${title} 재생`}
  aria-pressed={isPlaying}
  role="button"
>
  {isPlaying ? <PauseIcon /> : <PlayIcon />}
</IconButton>
```

#### 다운로드 진행률 접근성

```tsx
// 현재
<Progress value={progressValue ?? undefined} max={1} />

// 권장
<Progress
  value={progressValue ?? undefined}
  max={1}
  aria-label="다운로드 진행률"
  aria-valuetext={progressValue !== null 
    ? `${(progressValue * 100).toFixed(0)}% 완료` 
    : '다운로드 준비 중'}
/>
// 또는 aria-live region 사용
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {progressValue !== null 
    ? `다운로드 ${(progressValue * 100).toFixed(0)}% 완료` 
    : '다운로드 진행 중'}
</div>
```

### 3.3 키보드 내비게이션

#### 현재 지원 상태
- Enter 키로 검색 실행: **O** (구현됨)
- Tab으로 요소 간 이동: **부분적** (Radix UI 기본 제공)
- 검색 결과 목록 키보드 탐색: **X**
- 다운로드 목록 키보드 탐색: **X**

#### 권장 키보드 단축키

| 키 | 동작 |
|---|---|
| `/` | 검색 입력란 포커스 |
| `Escape` | 검색 결과 닫기 / 입력 취소 |
| `Arrow Up/Down` | 검색 결과 목록 탐색 |
| `Enter` | 선택된 항목 다운로드 |
| `Space` | 재생/일시정지 토글 |
| `Delete` | 선택된 항목 삭제 |

#### 포커스 관리

```tsx
// 검색 결과가 나타났을 때 첫 번째 결과로 포커스 이동
useEffect(() => {
  if (list && list.length > 0) {
    const firstResult = document.querySelector('[data-search-result]');
    (firstResult as HTMLElement)?.focus();
  }
}, [list]);

// 삭제 확인 다이얼로그 포커스 트랩
// 현재: 포커스 관리 없음
// 권장: Radix AlertDialog 사용으로 교체
```

### 3.4 스크린 리더 지원

#### 시맨틱 HTML 개선

```tsx
// 현재 Root.tsx
<header></header>  // 빈 header
<nav></nav>        // 빈 nav
<Main />
<footer></footer>  // 빈 footer

// 권장: 빈 시맨틱 요소 제거 또는 의미 있는 콘텐츠 추가
// 빈 landmark는 스크린 리더 사용자를 혼란스럽게 함
<main>
  <h1>YouTube Music Downloader</h1>
  <section aria-label="검색">...</section>
  <section aria-label="다운로드">...</section>
  <section aria-label="다운로드된 파일">...</section>
</main>
```

#### Live Region 사용

```tsx
// 검색 결과 개수 알림
<div aria-live="polite" className="sr-only">
  검색 결과 {list?.length ?? 0}개를 찾았습니다
</div>

// 다운로드 완료 알림
<div aria-live="assertive" className="sr-only">
  다운로드가 완료되었습니다
</div>

// 삭제 완료 알림
<div aria-live="polite" className="sr-only">
  파일이 삭제되었습니다
</div>
```

### 3.5 시각적으로 숨긴 텍스트 유틸리티

```css
/* sr-only 클래스 (화면에 보이지 않지만 스크린 리더는 읽음) */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## 4. PWA 고려사항

### 4.1 PWA 구현 이점

음악 다운로더 앱에서 PWA가 특히 유용한 이유:
1. **홈 화면 설치**: 네이티브 앱처럼 빠른 접근
2. **오프라인 캐싱**: 앱 셸(UI)을 오프라인에서도 사용 가능
3. **푸시 알림**: 긴 다운로드 완료 시 알림
4. **Background Fetch API**: 앱이 백그라운드에 있어도 다운로드 계속

### 4.2 manifest.json 권장 설정

```json
{
  "name": "YouTube Music Downloader",
  "short_name": "YT Music DL",
  "description": "YouTube 음악을 검색하고 MP3로 다운로드하세요",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#111113",
  "theme_color": "#111113",
  "orientation": "any",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "categories": ["music", "utilities"],
  "shortcuts": [
    {
      "name": "검색",
      "url": "/?action=search",
      "description": "YouTube 음악 검색"
    }
  ]
}
```

### 4.3 Service Worker 전략

| 리소스 | 캐싱 전략 | 이유 |
|---|---|---|
| HTML/CSS/JS (앱 셸) | Cache First, 네트워크 업데이트 | 빠른 로드, 오프라인 지원 |
| API 응답 (검색) | Network First | 실시간 데이터 필요 |
| 썸네일 이미지 | Cache First (24시간) | 대역폭 절약 |
| MP3 파일 | Network Only | 대용량, 캐시 불필요 |
| 폰트/아이콘 | Cache First (영구) | 변경 거의 없음 |

### 4.4 설치 프롬프트 UX

```
권장 타이밍:
- 첫 다운로드 완료 후 (사용자가 앱 가치를 경험한 시점)
- 3번째 방문 시
- "앱으로 설치하면 더 빠르게 사용할 수 있어요" 배너

비권장:
- 첫 방문 즉시 (사용자 이탈 유발)
- 강제 팝업
```

### 4.5 알림 활용

```
다운로드 완료 알림:
- 브라우저가 백그라운드일 때 "다운로드 완료: {곡 제목}" 알림
- 클릭 시 앱으로 이동, 해당 파일 하이라이트

구현 고려사항:
- Notification API 권한은 다운로드 시작 시 요청
- 과도한 알림 방지 (배치 다운로드 시 완료 건만)
```

---

## 5. 성능 UX 패턴

### 5.1 스켈레톤 스크린

현재 앱은 `<Spinner />`만 사용 (Suspense fallback, 검색 중 등).

**스켈레톤이 스피너보다 우수한 이유** (연구 기반):
- 체감 로딩 시간이 평균 **15-30% 감소** (Luke Wroblewski, 2013)
- 사용자가 콘텐츠가 "로드되고 있다"는 인식을 가짐
- Spinner는 "기다리고 있다"는 부정적 인식

#### 검색 결과 스켈레톤

```
┌──────────────────────────────────┐
│ [░░░░] [░░░░░░░░░░░░░░░░░] [░]  │  ← 카드 형태 유지
│ [░░░░] [░░░░░░░░░░░░░░░░░] [░]  │
│ [░░░░] [░░░░░░░░░░░░░░░░░] [░]  │
│ [░░░░] [░░░░░░░░░░░░░░░░░] [░]  │
│ [░░░░] [░░░░░░░░░░░░░░░░░] [░]  │
└──────────────────────────────────┘
```

#### 다운로드 목록 스켈레톤

```
┌──────────────────────────────────┐
│ [░░░░░░░░░░░░░░░░░] [░░] [░] [░]│
│ [░░░░░░░░░░░░░░░░░] [░░] [░] [░]│
│ [░░░░░░░░░░░░░░░░░] [░░] [░] [░]│
└──────────────────────────────────┘
```

### 5.2 Optimistic UI

#### 삭제 동작

```tsx
// 현재: 서버 응답 대기 후 UI 업데이트
const handleConfirm = async () => {
  setIsLoading(true);
  await deleteDownloaded(id);
  queryClient.invalidateQueries({ queryKey: ['downloaded'] });
};

// 권장: 즉시 UI에서 제거, 실패 시 롤백
const handleConfirm = async () => {
  // 1. 즉시 UI에서 제거 (optimistic update)
  queryClient.setQueryData(['downloaded'], (old) =>
    old.filter(item => item.info_dict.id !== id)
  );
  
  try {
    await deleteDownloaded(id);
  } catch (error) {
    // 2. 실패 시 롤백
    queryClient.invalidateQueries({ queryKey: ['downloaded'] });
    toast.error('삭제에 실패했습니다');
  }
};
```

### 5.3 Lazy Loading

#### 썸네일 이미지

```tsx
// 현재: 모든 썸네일 즉시 로드
<Avatar src={item.thumbnail} fallback={<VideoIcon />} size={'4'} />

// 권장: IntersectionObserver 기반 lazy loading
<Avatar 
  src={item.thumbnail} 
  fallback={<VideoIcon />} 
  size={'4'}
  loading="lazy"  // 네이티브 lazy loading
/>
```

#### 다운로드 목록 가상화

파일이 많아질 경우 (50개 이상):
```
@tanstack/react-virtual 또는 react-window 사용
- 화면에 보이는 항목만 렌더링
- 수백 개 파일이 있어도 성능 유지
```

### 5.4 검색 디바운싱

```tsx
// 현재: Enter 또는 버튼 클릭으로만 검색
// 고려사항: 자동 검색 시 디바운싱 필수

// 향후 자동 검색 구현 시:
const debouncedSearch = useDeferredValue(query);
// 또는
useEffect(() => {
  const timer = setTimeout(() => {
    if (query.length >= 2) search();
  }, 300);
  return () => clearTimeout(timer);
}, [query]);
```

### 5.5 에러 상태 UX

현재 앱에는 사용자 친화적인 에러 표시가 없음:

```
권장 에러 상태:
1. 검색 실패: "검색 결과를 가져올 수 없습니다. 다시 시도해 주세요." + 재시도 버튼
2. 다운로드 실패: "다운로드에 실패했습니다. 영상이 제한되었을 수 있습니다." + 재시도 옵션
3. 네트워크 오류: "인터넷 연결을 확인해 주세요." (오프라인 감지)
4. 서버 오류: "서버에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."
```

---

## 6. 현재 앱 분석 및 구체적 권장사항

### 6.1 우선순위별 개선 과제

#### P0 - 즉시 수정 (접근성 법적 요구사항)

| # | 과제 | 파일 | 예상 작업량 |
|---|---|---|---|
| 1 | 모든 IconButton에 aria-label 추가 | Search, Download, Downloaded, DownloadProgress | 30분 |
| 2 | Root.tsx 빈 시맨틱 요소 제거 또는 채우기 | Root.tsx | 15분 |
| 3 | Progress 컴포넌트 aria 속성 추가 | DownloadProgress.tsx | 15분 |
| 4 | sr-only 유틸리티 클래스 추가 | 글로벌 CSS | 5분 |
| 5 | 색상만으로 상태 구분하는 부분에 텍스트/아이콘 보완 | Search.tsx | 15분 |

#### P1 - 단기 개선 (1~2주)

| # | 과제 | 설명 | 예상 작업량 |
|---|---|---|---|
| 6 | 모바일 반응형 레이아웃 | 브레이크포인트 기반 레이아웃 변경 | 2일 |
| 7 | 터치 타겟 크기 확대 | 모바일에서 44px 이상 보장 | 4시간 |
| 8 | 검색 결과 모바일 카드 레이아웃 | 세로 스택 레이아웃 | 1일 |
| 9 | 다운로드 목록 카드 변환 | Table -> Card (모바일) | 1일 |
| 10 | 키보드 내비게이션 강화 | `/` 단축키, 화살표 탐색 | 1일 |
| 11 | 스켈레톤 스크린 도입 | 검색, 목록 로딩 상태 | 4시간 |
| 12 | aria-live region 추가 | 상태 변경 알림 | 4시간 |

#### P2 - 중기 개선 (1개월)

| # | 과제 | 설명 |
|---|---|---|
| 13 | PWA manifest 및 Service Worker | 설치 가능한 앱 |
| 14 | 오프라인 앱 셸 캐싱 | Service Worker 캐싱 전략 |
| 15 | 푸시 알림 (다운로드 완료) | Notification API |
| 16 | Optimistic UI (삭제) | React Query mutation 최적화 |
| 17 | 에러 바운더리 및 사용자 친화적 에러 UI | ErrorBoundary, Toast |
| 18 | Bottom Sheet (모바일 검색 결과) | vaul 라이브러리 또는 커스텀 |

#### P3 - 장기 개선 (분기)

| # | 과제 | 설명 |
|---|---|---|
| 19 | 제스처 내비게이션 | 스와이프 삭제, Pull-to-refresh |
| 20 | 가상화 목록 | @tanstack/react-virtual |
| 21 | 다국어 지원 (i18n) | react-intl 또는 i18next |
| 22 | 고대비 모드 지원 | prefers-contrast 미디어 쿼리 |
| 23 | 모션 감소 지원 | prefers-reduced-motion |

### 6.2 구체적 코드 변경 권장사항

#### 6.2.1 Root.tsx 개선

```tsx
// 변경 전
<header></header>
<nav></nav>
<Main />
<footer></footer>

// 변경 후
<a href="#main-content" className="sr-only focus:not-sr-only">
  본문으로 건너뛰기
</a>
<Main />
```

#### 6.2.2 Search.tsx - 검색 결과 항목 접근성

```tsx
// 검색 결과 목록에 role="listbox" 추가
<Flex direction={'column'} gap={'1'} role="listbox" aria-label="검색 결과">
  {list?.map((item, index) => (
    <Card 
      size={'1'} 
      key={item.id}
      role="option"
      aria-selected={url.includes(item.id)}
      tabIndex={0}
      data-search-result
    >
```

#### 6.2.3 Downloaded.tsx - 테이블 접근성

```tsx
// 테이블에 caption 추가
<Table.Root>
  <caption className="sr-only">다운로드된 음악 파일 목록</caption>
  <Table.Body>
```

#### 6.2.4 반응형 CSS 미디어 쿼리

```css
/* 검색 결과 카드 */
@media (max-width: 639px) {
  .search-result-card {
    flex-direction: column;
  }
  
  .search-result-card .thumbnail {
    width: 100%;
    aspect-ratio: 16/9;
  }
  
  /* 터치 타겟 확대 */
  [data-radix-collection-item] {
    min-height: 44px;
    min-width: 44px;
  }
  
  /* 다운로드 목록 카드화 */
  .download-list-item {
    flex-direction: column;
    padding: 12px;
    gap: 8px;
  }
}

/* 모션 감소 지원 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 6.3 경쟁 포지셔닝 전략

본 앱이 cobalt.tools 수준의 UX를 달성하면서도 차별화할 수 있는 포인트:

```
핵심 가치 제안:
"광고 없는 올인원 YouTube 음악 다운로더"
- 검색 → 미리보기 → 다운로드 → 관리 → 재생까지 한 곳에서
- cobalt.tools보다 우수한 점: 내장 검색, 파일 관리, 인라인 재생
- 추가 차별점: PWA 설치, 접근성 준수, 한국어 지원
```

### 6.4 Radix UI 활용 최적화

현재 Radix UI Themes를 사용 중이므로, 추가 라이브러리 없이 활용 가능한 부분:

| Radix 컴포넌트 | 활용 방안 |
|---|---|
| `AlertDialog` | 삭제 확인 (현재 커스텀 구현 -> AlertDialog로 교체하면 포커스 트랩 자동 제공) |
| `Toast` | 성공/에러 알림 |
| `Tooltip` | 버튼 설명 (title 속성 대신) |
| `VisuallyHidden` | sr-only 텍스트 (@radix-ui/react-visually-hidden) |
| `Skeleton` | Radix Themes의 내장 Skeleton 컴포넌트 |
| `responsive props` | Radix Themes는 반응형 prop 지원 (예: `size={{ initial: '1', md: '2' }}`) |

**특히 중요**: Radix UI Themes는 반응형 prop을 기본 지원함:
```tsx
<Container size={{ initial: '1', sm: '2' }}>
<Heading size={{ initial: '5', md: '7' }}>
<Flex direction={{ initial: 'column', sm: 'row' }}>
```
이를 활용하면 별도의 CSS 미디어 쿼리 없이도 상당 부분 반응형 구현 가능.

---

## 참고 자료

### 웹 접근성 표준
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WCAG 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

### 모바일 디자인 가이드
- Google Material Design 3: https://m3.material.io/
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Radix UI Themes Responsive: https://www.radix-ui.com/themes/docs/theme/breakpoints

### PWA
- web.dev PWA Guide: https://web.dev/progressive-web-apps/
- MDN Service Worker API: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

### 경쟁 도구
- cobalt.tools: https://cobalt.tools/
- y2mate: https://www.y2mate.com/
- yt1s: https://yt1s.com/
- savefrom.net: https://savefrom.net/
- 9convert: https://9convert.com/

### 성능 UX 연구
- Nielsen Norman Group - Skeleton Screens: https://www.nngroup.com/articles/skeleton-screens/
- Luke Wroblewski - Mobile First: https://www.lukew.com/ff/entry.asp?933
