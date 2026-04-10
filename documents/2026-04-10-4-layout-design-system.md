# UI/UX 리서치 #4: 전체 레이아웃, 네비게이션 및 비주얼 디자인 시스템

> 작성일: 2026-04-10
> 대상: YouTube Music Downloader (React 19 + Radix UI Themes + TypeScript + SCSS)

---

## 1. 리서치 요약

### 1.1 조사한 앱 및 디자인 시스템

현대 SaaS/유틸리티 앱의 UI 패턴을 광범위하게 조사했다:

- **Linear**: 다크 모드 중심의 미니멀한 프로젝트 관리 도구. 커스텀 디자인 시스템 "Orbiter" 사용. Inter 폰트, #000000 배경, 보라색 그라데이션 악센트. 모듈러 컴포넌트 기반으로 전통적 그리드에 구애받지 않는 레이아웃.
  - 출처: [LogRocket - Linear Design Trend](https://blog.logrocket.com/ux-design/linear-design/)
  - 출처: [Linear UI Redesign](https://linear.app/now/how-we-redesigned-the-linear-ui)

- **Raycast**: 키보드 중심의 런처/유틸리티 앱. 볼드한 레드 악센트, 노이즈 오버레이 텍스처, 미니멀하면서도 고유한 비주얼 아이덴티티.
  - 출처: [Raycast](https://www.raycast.com/)

- **Arc Browser**: 사이드바 네비게이션, 탭 관리를 공간적으로 분리. 컬러 테마 커스터마이징 지원.
  - 출처: [SaaSUI - Arc Browser](https://www.saasui.design/application/arc-browser)

- **Material Design 3**: 다크 테마 가이드라인에서 #121212 배경, elevation을 밝기로 표현하는 패턴 제시.

- **Radix UI Themes**: 12단계 컬러 스케일, 25개 악센트 컬러, 6가지 그레이 스케일 제공. CSS 커스텀 프로퍼티 기반 토큰 시스템.
  - 출처: [Radix Themes - Color](https://www.radix-ui.com/themes/docs/theme/color)
  - 출처: [Radix Themes - Dark Mode](https://www.radix-ui.com/themes/docs/theme/dark-mode)

### 1.2 핵심 트렌드 (2025-2026)

1. **다크 모드 기본값**: 사용자 82%가 다크 모드 활성화 (Android Authority 2024 설문)
2. **Linear 스타일 디자인**: 미니멀, 고대비, 뉴트럴 톤 + 하나의 강렬한 악센트 컬러
3. **글래스모피즘의 실용화**: 복잡한 데이터를 정리하는 데 frosted-glass 효과 활용
4. **카드 기반 UI**: 관련 콘텐츠를 하나의 컨테이너에 그룹화하여 스캐닝 효율 향상
5. **GPU 가속 애니메이션**: transform/opacity 위주, 300ms 이하 전환 시간

---

## 2. 레이아웃 패턴 분석

### 2.1 레이아웃 유형 비교

| 패턴 | 장점 | 단점 | 적합한 앱 |
|------|------|------|-----------|
| **사이드바 네비게이션** | 많은 섹션 수용, 항상 노출 | 소규모 앱에는 과도 | Linear, Notion, Figma |
| **탑 네비게이션** | 직관적, 수평 공간 활용 | 항목 많아지면 복잡 | 마케팅 사이트, 블로그 |
| **싱글 컬럼 스택** | 단순, 모바일 친화적, 집중적 | 복잡한 상태 표현 제한 | 유틸리티 도구, 단일 작업 앱 |
| **스플릿 페인** | 목록+상세 동시 표시 | 좁은 화면에서 제약 | 메일, 채팅, 파일 매니저 |
| **카드 그리드** | 시각적 요소 강조, 스캐닝 용이 | 밀도 높은 데이터에 부적합 | 미디어 라이브러리, 대시보드 |

### 2.2 본 앱에 권장하는 레이아웃: "포커스드 싱글 컬럼 + 확장 가능한 섹션"

**근거:**
- 본 앱의 작업 흐름이 순차적(검색 → 선택 → 다운로드 → 관리)
- 동시에 여러 기능을 조작할 필요가 적음
- 사이드바는 5개 미만의 기능에 과도함
- 모바일 퍼스트 접근이 자연스러움

**제안 구조:**

```
┌─────────────────────────────────────────┐
│  ■ 헤더 (앱 로고 + 타이틀)              │
│    ─────────────────────────────────     │
│  ┌───────────────────────────────────┐  │
│  │  🔍 검색 영역                      │  │
│  │  - 검색 입력 + 버튼               │  │
│  │  - 검색 결과 (접이식)              │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  ⬇ 다운로드 진행 상황              │  │
│  │  - 현재 다운로드 프로그레스 바     │  │
│  │  - 상태 텍스트                     │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  🎵 다운로드된 파일 라이브러리     │  │
│  │  - 파일 목록/그리드 토글           │  │
│  │  - 재생/삭제 액션                  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ─ 푸터 (미니멀) ─                      │
└─────────────────────────────────────────┘
```

**현재 코드 분석:**

현재 `Main.tsx`에서 `Container size="2"` + `Section` + `Flex direction="column"`으로 이미 싱글 컬럼 스택을 사용 중이다. 이 기본 구조는 올바르지만, 다음 개선이 필요하다:

1. **헤더 분리**: 현재 `<header></header>`가 비어 있음 → 앱 로고/타이틀을 헤더로 분리
2. **섹션 간 시각적 구분 강화**: 현재 하나의 Card 안에 Search, Download, DownloadProgress가 모두 있음 → 기능별 독립 카드 또는 시각적 분리
3. **반응형 컨테이너 최대 너비 조정**: `Container size="2"`는 Radix 기본값 688px → 720px~800px로 확대 고려

---

## 3. 다크 모드 베스트 프랙티스

### 3.1 배경색 계층 구조

순수 검정(#000000) 대신 다크 그레이 계열을 사용하여 눈의 피로를 줄인다.

| 레이어 | 용도 | 권장 색상 | Radix 토큰 |
|--------|------|-----------|-----------|
| **L0 (기저)** | 페이지 배경 | #111113 | `--color-background` |
| **L1 (표면)** | 카드, 패널 | #18181B | `--gray-2` |
| **L2 (올린 표면)** | 호버 상태, 드롭다운 | #1F1F23 | `--gray-3` |
| **L3 (최상위)** | 모달, 툴팁 | #27272C | `--gray-4` |

- 출처: [UI Deploy - Dark Mode Design Guide](https://ui-deploy.com/blog/complete-dark-mode-design-guide-ui-patterns-and-implementation-best-practices-2025)
- 출처: [Graphic Eagle - Dark Mode UI](https://www.graphiceagle.com/dark-mode-ui/)

### 3.2 대비율(Contrast Ratio) 가이드라인

| 요소 | 최소 대비율 | 권장 대비율 |
|------|------------|------------|
| 본문 텍스트 (16px 이하) | 4.5:1 (WCAG AA) | 7:1 (WCAG AAA) |
| 대형 텍스트 (18px 이상) | 3:1 | 4.5:1 |
| UI 컴포넌트/아이콘 | 3:1 | 4.5:1 |
| 비활성 텍스트 | — | 최소 2.5:1 |
| 포커스 링 | 3:1 | — |

**다크 모드 특수 고려사항:**
- 100% 화이트(#FFFFFF) 텍스트는 다크 배경에서 과도한 대비를 유발 → **#EDEDEF** (Radix `--gray-12`) 또는 90% 밝기 사용 권장
- 악센트 컬러는 라이트 모드 대비 **채도를 10-20% 높여야** 동일한 시각적 무게감 유지
- 출처: [Uxcel - 12 Principles of Dark Mode Design](https://uxcel.com/blog/12-principles-of-dark-mode-design-627)

### 3.3 컬러 팔레트 구성

Radix UI Themes의 12단계 스케일을 활용한 권장 팔레트:

```
악센트 컬러 (Crimson 또는 Violet 권장 - 음악 앱의 감성적 특성):
  --accent-1:  배경 틴트
  --accent-2:  서브틀 배경
  --accent-3:  호버 배경
  --accent-4:  프레스 배경
  --accent-5:  -
  --accent-6:  보더 (서브틀)
  --accent-7:  보더
  --accent-8:  보더 (강조)
  --accent-9:  솔리드 배경 (버튼, 배지)  ← 주요 CTA
  --accent-10: 솔리드 배경 (호버)
  --accent-11: 텍스트 (로우 컨트라스트)
  --accent-12: 텍스트 (하이 컨트라스트)

그레이 (Slate 권장 - 블루 틴트가 테크 감성 부여):
  --gray-1 ~ --gray-12: 동일한 12단계 구조
```

### 3.4 Elevation 표현 방식

다크 모드에서는 그림자가 잘 보이지 않으므로, **표면 밝기**로 elevation을 표현한다:

```scss
// Elevation 시스템
--elevation-0: var(--gray-1);   // 기저 레벨
--elevation-1: var(--gray-2);   // 카드
--elevation-2: var(--gray-3);   // 드롭다운, 팝오버
--elevation-3: var(--gray-4);   // 모달, 다이얼로그
--elevation-4: var(--gray-5);   // 토스트, 알림

// 보조적으로 미세한 보더 사용
--border-subtle: 1px solid var(--gray-a3);
--border-default: 1px solid var(--gray-a4);
--border-strong: 1px solid var(--gray-a6);
```

- 출처: [Toptal - Dark UI Design Principles](https://www.toptal.com/designers/ui/dark-ui-design)
- 출처: [Netguru - Tips for Dark Theme Design](https://www.netguru.com/blog/tips-dark-mode-ui)

---

## 4. 타이포그래피 시스템

### 4.1 폰트 선택

Radix UI Themes 기본 폰트 스택을 유지하되, 음악 앱의 특성을 고려한 조정:

```css
/* 기본 (Radix 기본값) */
--default-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                       'Helvetica Neue', Arial, sans-serif;

/* 권장 대안: Inter 또는 Geist 폰트 */
--custom-font-family: 'Inter', var(--default-font-family);
```

**Inter 폰트 권장 이유:**
- Linear, Vercel, GitHub 등 현대 개발 도구에서 광범위하게 사용
- 작은 크기에서도 가독성 우수 (x-height이 높음)
- Variable font 지원으로 세밀한 weight 조절 가능

### 4.2 타입 스케일

Radix Themes의 기본 스케일을 기반으로 한 권장 시스템:

| 토큰 | 크기 | 줄 높이 | 용도 |
|------|------|---------|------|
| `--font-size-1` | 12px | 16px | 캡션, 메타데이터 |
| `--font-size-2` | 14px | 20px | 본문 (기본) |
| `--font-size-3` | 16px | 24px | 본문 (강조) |
| `--font-size-4` | 18px | 26px | 서브 헤딩 |
| `--font-size-5` | 20px | 28px | 섹션 제목 |
| `--font-size-6` | 24px | 30px | 페이지 제목 |
| `--font-size-7` | 28px | 36px | 히어로 텍스트 |
| `--font-size-8` | 35px | 40px | 디스플레이 |
| `--font-size-9` | 60px | 60px | 대형 디스플레이 |

**본 앱 권장 사용:**
- 앱 타이틀: `font-size-6` (24px), weight 700
- 섹션 헤딩: `font-size-4` (18px), weight 600
- 본문/레이블: `font-size-2` (14px), weight 400
- 보조 텍스트/메타: `font-size-1` (12px), weight 400, `--gray-11` 색상

- 출처: [Design Systems - Typography Guides](https://www.designsystems.com/typography-guides/)
- 출처: [UX Collective - Mastering Typography in Design Systems](https://uxdesign.cc/mastering-typography-in-design-systems-with-semantic-tokens-and-responsive-scaling-6ccd598d9f21)

---

## 5. 스페이싱 시스템

### 5.1 8px 그리드 시스템

모든 간격을 8px의 배수로 통일한다. 4px는 미세 조정용 하프 스텝으로 허용.

```
스페이싱 스케일:
  --space-1:  4px    (0.25rem)  - 인라인 요소 간격
  --space-2:  8px    (0.5rem)   - 아이콘과 텍스트 간격
  --space-3:  12px   (0.75rem)  - 관련 요소 그룹 내부
  --space-4:  16px   (1rem)     - 폼 필드 간격
  --space-5:  24px   (1.5rem)   - 섹션 내 그룹 간격
  --space-6:  32px   (2rem)     - 카드 내부 패딩
  --space-7:  40px   (2.5rem)   - 섹션 간 간격
  --space-8:  48px   (3rem)     - 주요 섹션 구분
  --space-9:  64px   (4rem)     - 페이지 레벨 간격
```

Radix Themes의 `gap` prop 값(1-9)이 이 스케일에 매핑된다.

- 출처: [Design Systems - Space, Grids, and Layouts](https://www.designsystems.com/space-grids-and-layouts/)
- 출처: [Cieden - Spacing Best Practices](https://cieden.com/book/sub-atomic/spacing/spacing-best-practices)
- 출처: [Atlassian Design - Spacing](https://atlassian.design/foundations/spacing/)

### 5.2 본 앱 스페이싱 권장

```
페이지 좌우 패딩:     --space-5 (24px), 모바일에서 --space-4 (16px)
카드 내부 패딩:       --space-5 (24px)
카드 간 간격:         --space-4 (16px)
폼 요소 간 간격:      --space-3 (12px) ~ --space-4 (16px)
인라인 요소 간격:     --space-2 (8px)
섹션(검색/다운로드/라이브러리) 간 간격: --space-6 (32px)
```

---

## 6. 반응형/적응형 디자인

### 6.1 브레이크포인트

```scss
// 모바일 퍼스트 접근
$breakpoint-sm: 520px;   // 소형 모바일
$breakpoint-md: 768px;   // 태블릿
$breakpoint-lg: 1024px;  // 데스크톱
$breakpoint-xl: 1280px;  // 대형 데스크톱
```

### 6.2 반응형 전략

| 화면 크기 | 레이아웃 | 컨테이너 너비 | 특이사항 |
|-----------|---------|--------------|---------|
| < 520px | 싱글 컬럼, 풀 와이드 | 100% - 32px | 검색 결과 풀스크린 오버레이 |
| 520-768px | 싱글 컬럼, 중앙 정렬 | 480px | 기본 레이아웃 |
| 768-1024px | 싱글 컬럼, 넉넉한 여백 | 640px | 다운로드 목록 2열 가능 |
| > 1024px | 싱글 컬럼, 최대 너비 제한 | 720px | 사이드 여백이 콘텐츠 집중 유도 |

**핵심 원칙:**
- 모바일 퍼스트 CSS: 기본 스타일이 모바일, `min-width` 미디어 쿼리로 확장
- 터치 타겟 최소 44x44px (모바일)
- Radix의 `Container` 컴포넌트와 `size` prop으로 반응형 너비 관리

- 출처: [SimplifyTechHub - Mobile-First Development Strategy](https://www.simplifytechhub.com.ng/2026/02/responsive-design-mobile-first.html)

### 6.3 적응형 컴포넌트 패턴

```
검색 결과:
  모바일 → 풀스크린 시트(bottom sheet) 또는 오버레이
  데스크톱 → 인라인 드롭다운 목록

다운로드 목록:
  모바일 → 간소화된 카드 (썸네일 + 제목 + 액션 버튼)
  데스크톱 → 테이블 형태 (썸네일 + 제목 + 아티스트 + 길이 + 액션)

프로그레스 표시:
  모바일 → 하단 고정 배너(sticky bottom)
  데스크톱 → 인라인 프로그레스 바
```

---

## 7. 애니메이션 및 전환 가이드라인

### 7.1 기본 원칙

1. **목적이 있는 애니메이션만 사용**: 상태 변화를 알리거나 공간적 관계를 설명할 때만
2. **성능 우선**: `transform`과 `opacity`만 애니메이션 (GPU 가속)
3. **`prefers-reduced-motion` 존중**: 시스템 설정에 따라 애니메이션 비활성화

- 출처: [Motion.dev](https://motion.dev/)
- 출처: [Web Animation Guide 2025](https://mmcommunications.vn/en/web-animation-motion-design-guide-n607)

### 7.2 타이밍 토큰

```css
/* Duration */
--duration-instant:  0ms;       /* 토글, 체크박스 */
--duration-fast:     100ms;     /* 호버, 포커스 링 */
--duration-normal:   200ms;     /* 대부분의 전환 */
--duration-moderate: 300ms;     /* 패널 열기/닫기 */
--duration-slow:     500ms;     /* 페이지 전환, 모달 */

/* Easing */
--ease-default:      cubic-bezier(0.25, 0.1, 0.25, 1.0);   /* 일반적인 전환 */
--ease-in:           cubic-bezier(0.42, 0, 1, 1);            /* 요소가 사라질 때 */
--ease-out:          cubic-bezier(0, 0, 0.58, 1);            /* 요소가 나타날 때 */
--ease-in-out:       cubic-bezier(0.42, 0, 0.58, 1);         /* 위치 이동 */
--ease-spring:       cubic-bezier(0.34, 1.56, 0.64, 1);      /* 바운스 효과 */
```

### 7.3 본 앱에서의 애니메이션 적용

| 인터랙션 | 애니메이션 | 지속 시간 | 이징 |
|----------|-----------|----------|------|
| 검색 결과 등장 | fadeIn + slideDown | 200ms | ease-out |
| 검색 결과 접기 | fadeOut + slideUp | 150ms | ease-in |
| 다운로드 프로그레스 바 | width 전환 | 300ms | ease-in-out |
| 다운로드 완료 | scale pulse + 체크 아이콘 | 400ms | ease-spring |
| 파일 삭제 | fadeOut + slideLeft + height collapse | 300ms | ease-in |
| 카드 호버 | border-color 전환 | 100ms | ease-default |
| 버튼 호버 | background-color 전환 | 100ms | ease-default |
| 버튼 프레스 | scale(0.98) | 100ms | ease-default |
| 토스트 알림 | slideIn from right | 300ms | ease-out |

### 7.4 CSS 구현 예시

```scss
// 기본 전환 믹스인
@mixin transition-default {
  transition-property: color, background-color, border-color, opacity, transform;
  transition-duration: var(--duration-normal);
  transition-timing-function: var(--ease-default);
}

// 리듀스드 모션 지원
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. 컴포넌트 디자인 토큰 및 테마

### 8.1 시맨틱 토큰 구조

Radix Themes의 CSS 커스텀 프로퍼티를 기반으로 시맨틱 레이어를 구축한다:

```css
:root {
  /* ── 표면(Surface) ── */
  --surface-background:     var(--color-background);
  --surface-primary:        var(--gray-2);
  --surface-secondary:      var(--gray-3);
  --surface-tertiary:       var(--gray-4);
  
  /* ── 텍스트(Text) ── */
  --text-primary:           var(--gray-12);
  --text-secondary:         var(--gray-11);
  --text-tertiary:          var(--gray-9);
  --text-disabled:          var(--gray-8);
  --text-accent:            var(--accent-11);
  
  /* ── 보더(Border) ── */
  --border-subtle:          var(--gray-a3);
  --border-default:         var(--gray-a5);
  --border-strong:          var(--gray-a7);
  --border-accent:          var(--accent-a7);
  
  /* ── 인터랙티브(Interactive) ── */
  --interactive-default:    var(--accent-9);
  --interactive-hover:      var(--accent-10);
  --interactive-active:     var(--accent-11);
  --interactive-disabled:   var(--gray-6);
  
  /* ── 상태(Status) ── */
  --status-success:         var(--green-9);
  --status-warning:         var(--amber-9);
  --status-error:           var(--red-9);
  --status-info:            var(--blue-9);
  
  /* ── 프로그레스(Progress) - 앱 특화 ── */
  --progress-track:         var(--gray-3);
  --progress-fill:          var(--accent-9);
  --progress-complete:      var(--green-9);
}
```

- 출처: [Penpot - Guide to Design Tokens and CSS Variables](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- 출처: [Fourzerothree - Crafting a Semantic Colour System](https://www.fourzerothree.in/p/crafting-a-semantic-colour-system)

### 8.2 컴포넌트별 토큰

```css
/* 카드 */
--card-background:      var(--surface-primary);
--card-border:          var(--border-subtle);
--card-border-hover:    var(--border-default);
--card-padding:         var(--space-5);
--card-radius:          var(--radius-3);     /* Radix: 8px */

/* 검색 입력 */
--input-background:     var(--gray-a2);
--input-border:         var(--border-default);
--input-border-focus:   var(--accent-a7);
--input-text:           var(--text-primary);
--input-placeholder:    var(--text-tertiary);

/* 테이블/목록 */
--table-header-bg:      var(--gray-2);
--table-row-bg:         transparent;
--table-row-hover:      var(--gray-a2);
--table-border:         var(--border-subtle);

/* 프로그레스 바 */
--progress-height:      8px;
--progress-radius:      var(--radius-full);
--progress-bg:          var(--progress-track);
--progress-fill-color:  var(--progress-fill);
```

### 8.3 Radix UI Themes 최적 설정

현재 `Root.tsx`의 `<Theme appearance="dark">`를 다음과 같이 확장 권장:

```tsx
<Theme
  appearance="dark"
  accentColor="violet"      // 음악 앱 감성 (또는 "crimson", "iris")
  grayColor="slate"         // 블루 틴트 → 테크/모던 느낌
  panelBackground="solid"   // 반투명 대신 솔리드 배경
  radius="medium"           // 적당히 둥근 코너 (4-8px)
  scaling="100%"             // 기본 스케일
>
```

**악센트 컬러 권장:**
- `violet` 또는 `iris`: 음악/크리에이티브 감성, 충분히 눈에 띄면서 과하지 않음
- `crimson`: 보다 에너지 넘치는 느낌, YouTube의 레드와 연관성
- 비추천: `blue` (너무 일반적), `green` (다운로드 완료 상태와 충돌)

---

## 9. 구체적인 앱 개선 제안

### 9.1 레이아웃 구조 개편

**현재 문제점:**
1. 빈 `<header>`, `<nav>`, `<footer>` 태그가 의미 없이 존재
2. 검색/다운로드/프로그레스가 하나의 Card에 과도하게 밀집
3. 섹션 간 시각적 계층 구조가 부족

**개선안:**

```tsx
// Root.tsx
<Theme appearance="dark" accentColor="violet" grayColor="slate" radius="medium">
  <QueryClientProvider client={client}>
    <Flex direction="column" minHeight="100vh">
      <AppHeader />       {/* 로고 + 앱 이름, 선택적 설정 버튼 */}
      <Main />            {/* flex: 1로 남은 공간 채움 */}
      <AppFooter />       {/* 미니멀: 버전 정보 정도 */}
    </Flex>
  </QueryClientProvider>
</Theme>

// Main.tsx
<main style={{ flex: 1 }}>
  <Container size="2" px={{ initial: '4', sm: '5' }}>
    <Flex direction="column" gap="5" py="6">
      
      {/* 섹션 1: 검색 - 항상 노출 */}
      <SearchSection />
      
      {/* 섹션 2: 다운로드 진행 - 조건부 렌더링 */}
      {isDownloading && <DownloadProgressSection />}
      
      {/* 섹션 3: 라이브러리 - 항상 노출 */}
      <LibrarySection />
      
    </Flex>
  </Container>
</main>
```

### 9.2 비주얼 향상 포인트

1. **헤더**: 앱 이름 좌측, 우측에 설정 아이콘(기어). `backdrop-filter: blur(8px)`로 스크롤 시 반투명 효과. `position: sticky; top: 0; z-index: 10;`

2. **검색 카드**: 서치 아이콘이 내장된 Input. 결과는 카드 아래로 `details/summary` 대신 `AnimatePresence`(motion 라이브러리) 또는 Radix `Collapsible`로 부드럽게 등장/퇴장.

3. **프로그레스 섹션**: 다운로드 중일 때만 보이도록 조건부 렌더링 + 진입/퇴장 애니메이션. 곡 제목 + 아티스트 + 프로그레스 바 + 퍼센트를 한 줄에 배치.

4. **라이브러리 섹션**: 각 다운로드된 곡을 카드 형태로 표시. 썸네일(앨범 아트) + 곡 정보 + 재생/삭제 버튼. 빈 상태(empty state) 디자인 추가: "아직 다운로드된 곡이 없습니다" + 일러스트.

5. **색상 체계 일관성**: 모든 상태 색상을 시맨틱 토큰으로 통일. 성공(초록), 진행중(악센트), 에러(빨강), 비활성(그레이).

### 9.3 마이크로 인터랙션 추가 포인트

```
✦ 검색 입력 포커스 → 보더 악센트 컬러 전환 (100ms)
✦ 검색 중 → 로딩 스피너 또는 스켈레톤 UI
✦ 검색 결과 항목 호버 → 배경 하이라이트 (100ms)
✦ 다운로드 버튼 클릭 → 리플 효과 또는 스케일 애니메이션
✦ 프로그레스 바 → 부드러운 width 전환 + 완료 시 색상 변경(accent → green)
✦ 다운로드 완료 → 체크마크 아이콘 스프링 애니메이션
✦ 파일 삭제 → 슬라이드 아웃 + 높이 축소 애니메이션
✦ 재생 버튼 → 재생/일시정지 아이콘 모프 애니메이션
```

---

## 10. 디자인 토큰 종합 정리 (구현 참조용)

### 10.1 CSS 커스텀 프로퍼티 전체 맵

```scss
// =============================================
// YouTube Music Downloader - Design Tokens
// Radix UI Themes 기반 확장
// =============================================

:root, .radix-themes {
  // ── 스페이싱 ──
  --app-space-xs:    4px;
  --app-space-sm:    8px;
  --app-space-md:    16px;
  --app-space-lg:    24px;
  --app-space-xl:    32px;
  --app-space-2xl:   48px;
  --app-space-3xl:   64px;
  
  // ── 컨테이너 ──
  --app-container-sm:   480px;
  --app-container-md:   640px;
  --app-container-lg:   720px;
  --app-container-xl:   960px;
  
  // ── 타이밍 ──
  --app-duration-fast:      100ms;
  --app-duration-normal:    200ms;
  --app-duration-moderate:  300ms;
  --app-duration-slow:      500ms;
  
  --app-ease-default:   cubic-bezier(0.25, 0.1, 0.25, 1.0);
  --app-ease-out:       cubic-bezier(0, 0, 0.58, 1);
  --app-ease-in:        cubic-bezier(0.42, 0, 1, 1);
  --app-ease-spring:    cubic-bezier(0.34, 1.56, 0.64, 1);
  
  // ── Z-인덱스 ──
  --app-z-dropdown:   100;
  --app-z-sticky:     200;
  --app-z-overlay:    300;
  --app-z-modal:      400;
  --app-z-toast:      500;
  
  // ── 보더 라디우스 ──
  --app-radius-sm:    4px;
  --app-radius-md:    8px;
  --app-radius-lg:    12px;
  --app-radius-xl:    16px;
  --app-radius-full:  9999px;
  
  // ── 그림자 (다크 모드용 미세한 그로우) ──
  --app-shadow-sm:    0 1px 2px rgba(0, 0, 0, 0.3);
  --app-shadow-md:    0 4px 8px rgba(0, 0, 0, 0.4);
  --app-shadow-lg:    0 8px 24px rgba(0, 0, 0, 0.5);
  --app-shadow-glow:  0 0 12px rgba(var(--accent-9-rgb), 0.3);
}
```

---

## 11. 참고 자료 종합

### 대시보드 및 레이아웃
- [Muzli - 50 Best Dashboard Design Examples for 2026](https://muz.li/blog/best-dashboard-design-examples-inspirations-for-2026/)
- [Art of Styleframe - Dashboard Design Patterns for Modern Web Apps 2026](https://artofstyleframe.com/blog/dashboard-design-patterns-web-apps/)
- [UXPin - Effective Dashboard Design Principles](https://www.uxpin.com/studio/blog/dashboard-design-principles/)
- [Justinmind - Dashboard Design Best Practices](https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux)
- [Mockplus - 20 Best Practices for Dashboard Designs](https://www.mockplus.com/blog/post/dashboard-design-best-practices-examples)

### 다크 모드
- [UI Deploy - Complete Dark Mode Design Guide 2025](https://ui-deploy.com/blog/complete-dark-mode-design-guide-ui-patterns-and-implementation-best-practices-2025)
- [Graphic Eagle - Dark Mode UI Best Practices 2025](https://www.graphiceagle.com/dark-mode-ui/)
- [Colorhero - Dark Mode Color Palettes](https://colorhero.io/blog/dark-mode-color-palettes-2025)
- [Netguru - 11 Tips for Dark Theme Design](https://www.netguru.com/blog/tips-dark-mode-ui)
- [Uxcel - 12 Principles of Dark Mode Design](https://uxcel.com/blog/12-principles-of-dark-mode-design-627)
- [Toptal - Principles of Dark UI Design](https://www.toptal.com/designers/ui/dark-ui-design)
- [Medium (Ravindi) - Dark Mode Design Systems: A Practical Guide](https://medium.com/design-bootcamp/dark-mode-design-systems-a-practical-guide-13bc67e43774)
- [Fourzerothree - Designing a Scalable Accessible Dark Theme](https://www.fourzerothree.in/p/scalable-accessible-dark-mode)

### Linear 스타일 및 SaaS UI
- [LogRocket - Linear Design SaaS Trend](https://blog.logrocket.com/ux-design/linear-design/)
- [Linear - How We Redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui)
- [SaaSUI - Real Interface Design Screenshots](https://www.saasui.design/)
- [Medium (Arlene Xu) - The Rise of Linear Style Design](https://medium.com/design-bootcamp/the-rise-of-linear-style-design-origins-trends-and-techniques-4fd96aab7646)
- [LogRocket - Linear Design UI Libraries](https://blog.logrocket.com/ux-design/linear-design-ui-libraries-design-kits-layout-grid/)

### Radix UI Themes
- [Radix Themes - Theme Overview](https://www.radix-ui.com/themes/docs/theme/overview)
- [Radix Themes - Color](https://www.radix-ui.com/themes/docs/theme/color)
- [Radix Themes - Dark Mode](https://www.radix-ui.com/themes/docs/theme/dark-mode)
- [Radix Themes - Styling](https://www.radix-ui.com/themes/docs/overview/styling)
- [Radix Colors - Palette Composition](https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette)

### 타이포그래피 및 스페이싱
- [Design Systems - Typography Guides](https://www.designsystems.com/typography-guides/)
- [Design Systems - Space, Grids, and Layouts](https://www.designsystems.com/space-grids-and-layouts/)
- [Cieden - Spacing Best Practices (8pt Grid)](https://cieden.com/book/sub-atomic/spacing/spacing-best-practices)
- [Atlassian Design - Spacing](https://atlassian.design/foundations/spacing/)
- [UX Collective - Mastering Typography with Semantic Tokens](https://uxdesign.cc/mastering-typography-in-design-systems-with-semantic-tokens-and-responsive-scaling-6ccd598d9f21)

### 애니메이션
- [Motion.dev - JavaScript & React Animation Library](https://motion.dev/)
- [M&M Communications - Web Animation 2025 Guide](https://mmcommunications.vn/en/web-animation-motion-design-guide-n607)
- [Shoaib Sid - Motion UI with Framer Motion 2025](https://www.shoaibsid.dev/blog/motion-ui-with-framer-motion-in-2025-more-than-just-animations)

### 디자인 토큰
- [Penpot - Developer's Guide to Design Tokens and CSS Variables](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- [Contentful - Design Tokens Explained](https://www.contentful.com/blog/design-token-system/)
- [Mavik Labs - Design Tokens That Scale in 2026](https://www.maviklabs.com/blog/design-tokens-tailwind-v4-2026)
- [Fourzerothree - Crafting a Semantic Colour System](https://www.fourzerothree.in/p/crafting-a-semantic-colour-system)
- [Imperavi - Designing Semantic Colors](https://imperavi.com/blog/designing-semantic-colors-for-your-system/)

### 반응형 디자인
- [SimplifyTechHub - Mobile-First Development Strategy](https://www.simplifytechhub.com.ng/2026/02/responsive-design-mobile-first.html)
- [MDN - Common Grid Layouts](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Common_grid_layouts)
