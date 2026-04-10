# UI/UX 완전 재설계 플랜

## 현재 상태 진단

### 기술 스택 (유지)
- React 19 + TypeScript + Vite 7
- Radix UI Themes (dark) + Radix Icons
- Zustand (상태 관리) + TanStack React Query (서버 상태)
- SCSS

### 현재 문제점
1. **단일 다운로드만 지원** — `downloadId`가 string 하나, 큐/동시 다운로드 불가
2. **오디오 플레이어가 각 행마다 독립** — 동시 재생 가능, 글로벌 컨트롤 없음
3. **검색 결과가 `<details>` 접힘** — 불필요한 인터랙션, 결과 접근성 저하
4. **모바일 미대응** — 터치 타겟 24px (최소 44px 필요), 테이블 레이아웃
5. **접근성 부재** — IconButton에 aria-label 없음, 라이브 리전 없음
6. **레거시 코드** — DownloaderContext 미사용, useAnimationFrame 미사용

---

## 재설계 아키텍처

### 컴포넌트 트리 (신규)

```
Root
├── Theme (dark, accent: violet)
├── QueryClientProvider
├── ToastProvider
├── AudioProvider (NEW - 글로벌 오디오 상태)
│
└── App (NEW - 레이아웃 컨테이너)
    ├── Header (최소화: 타이틀 + 버전)
    ├── SearchSection (NEW)
    │   ├── SearchBar (통합 검색 입력)
    │   ├── RecentSearches (NEW - localStorage)
    │   └── SearchResults (NEW - 카드 리스트, 직접 다운로드 버튼)
    ├── DownloadQueue (NEW - 다중 다운로드 큐)
    │   └── DownloadQueueItem (NEW - 개별 진행률)
    ├── Library (NEW - 기존 Downloaded 대체)
    │   ├── LibraryHeader (정렬/필터/뷰 토글)
    │   ├── LibraryList / LibraryGrid (NEW - 뷰 모드 전환)
    │   └── LibraryItem (썸네일 + 메타 + 액션)
    └── PlayerBar (NEW - 하단 고정 플레이어)
        ├── NowPlaying (썸네일 + 제목 + 아티스트)
        ├── PlaybackControls (이전/재생/다음 + 시크바)
        └── VolumeControl (볼륨 슬라이더)
```

---

## Phase 1: 기반 구조 (P0)

### 1.1 글로벌 오디오 컨텍스트

**파일:** `src/stores/audioStore.ts`

```
audioStore (Zustand)
├── currentTrack: { id, title, artist, thumbnail } | null
├── isPlaying: boolean
├── currentTime: number
├── duration: number
├── volume: number (0-1)
├── queue: Track[]
│
├── play(track)    — 트랙 재생 (기존 정지 후)
├── pause()
├── resume()
├── seek(time)
├── setVolume(vol)
├── next() / prev()
└── addToQueue(track)
```

- HTML5 Audio 인스턴스를 store 내부에서 단일 관리
- 어떤 컴포넌트에서든 `play(track)` 호출 시 글로벌 재생

### 1.2 하단 고정 플레이어

**파일:** `src/components/PlayerBar.tsx`

```
┌─────────────────────────────────────────────────────────┐
│ [48px art] Title          ◀  ▶||  ▶  ====●======  3:45 │
│            Artist                        🔊 ===●===     │
└─────────────────────────────────────────────────────────┘
```

- `position: fixed; bottom: 0` — 항상 보임
- 트랙 없으면 숨김
- 썸네일: `img.youtube.com/vi/{id}/mqdefault.jpg`
- Radix Slider로 시크바/볼륨
- 키보드: Space(재생/일시정지), 좌우(5초 이동)

### 1.3 다운로드 큐 시스템

**파일:** `src/stores/downloadQueueStore.ts`

```
downloadQueueStore (Zustand)
├── items: Map<string, QueueItem>
│   QueueItem: { id, title, thumbnail, status, progress, speed, eta }
│   status: 'queued' | 'downloading' | 'converting' | 'done' | 'error'
│
├── enqueue(id, title, thumbnail)
├── updateProgress(id, data)
├── retry(id)
├── remove(id)
└── MAX_CONCURRENT = 2
```

- 동시 다운로드 2개, 나머지 대기
- 완료 시 토스트 알림 + 라이브러리 자동 갱신

### 1.4 접근성 수정 (즉시)

- 모든 `IconButton`에 `aria-label` 추가
- 검색 결과에 `role="listbox"`, 각 항목 `role="option"`
- 다운로드 상태 변경 시 `aria-live="polite"` 라이브 리전
- 포커스 관리: 검색 결과 → 화살표 키 네비게이션
- 최소 터치 타겟 44x44px

---

## Phase 2: 검색 & 결과 개편 (P1)

### 2.1 검색 바 재설계

**파일:** `src/components/SearchSection/SearchBar.tsx`

```
┌──────────────────────────────────────────────┐
│  🔍  검색어를 입력하세요...            [검색] │
└──────────────────────────────────────────────┘
```

- `<details>` 제거 — 결과는 항상 표시
- 300ms 디바운스 (입력 중 자동 검색 아님, Enter/버튼으로 실행)
- 최근 검색어 표시 (localStorage, 최대 10개)
- 빈 상태(zero state): "YouTube에서 음악을 검색하세요"
- 스켈레톤 로딩: 3개 카드 placeholder

### 2.2 검색 결과 카드

**파일:** `src/components/SearchSection/SearchResultCard.tsx`

```
┌────────────────────────────────────────────────────┐
│ [120x68 thumb]  Song Title                    [⬇]  │
│                 Artist • 3:45 • 👁 1.5M  [다운로드됨]│
└────────────────────────────────────────────────────┘
```

변경점:
- **직접 다운로드 버튼** — 선택 → URL 입력 → 다운로드 3단계를 1클릭으로
- 썸네일 크기 확대 (48px → 120x68px, 16:9)
- 다운로드 중이면 카드 내 미니 프로그레스 표시
- 이미 다운로드된 항목은 재생 버튼으로 전환

### 2.3 URL 직접 입력 (유지, 축소)

- 검색 카드 아래 접이식 "URL로 직접 다운로드" 링크
- 클릭 시 URL 입력 필드 토글

---

## Phase 3: 라이브러리 개편 (P1)

### 3.1 뷰 모드 전환

**파일:** `src/components/Library/Library.tsx`

```
다운로드 목록 (12곡)        [≡ 리스트] [⊞ 그리드] [정렬 ▼] [⟳]
─────────────────────────────────────────────────────────
```

리스트 뷰:
```
┌─────────────────────────────────────────────────────┐
│ [thumb] Title                    3.2MB  [▶] [⬇] [🗑]│
│         Artist • 3:45                                │
└─────────────────────────────────────────────────────┘
```

그리드 뷰:
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ [thumb]  │ │ [thumb]  │ │ [thumb]  │
│ Title    │ │ Title    │ │ Title    │
│ Artist   │ │ Artist   │ │ Artist   │
│ [▶] [🗑] │ │ [▶] [🗑] │ │ [▶] [🗑] │
└──────────┘ └──────────┘ └──────────┘
```

### 3.2 정렬 & 필터

- 정렬: 제목순, 크기순, 최신순 (다운로드 시간)
- 필터: 검색 (라이브러리 내)

### 3.3 썸네일 활용

- YouTube 썸네일 URL: `https://img.youtube.com/vi/{id}/mqdefault.jpg`
- 리스트: 60x34px, 그리드: 전체 너비
- 로드 실패 시 음표 아이콘 폴백

---

## Phase 4: 다운로드 큐 UI (P1)

### 4.1 Google Drive식 하단 드로어

**파일:** `src/components/DownloadQueue/DownloadQueue.tsx`

```
┌──────────────────────────────────────────┐
│ ▼ 다운로드 (2/5 완료)              [최소화]│
├──────────────────────────────────────────┤
│ ✓ Song A ──────────────────── 완료       │
│ ▶ Song B ████████░░░░░ 67% 2.1MB/s ETA 3s│
│ 🔄 Song C ──────────────── 변환 중        │
│ ⏳ Song D ──────────────── 대기           │
│ ✗ Song E ──────────────── 실패 [재시도]   │
└──────────────────────────────────────────┘
```

- 하단 드로어 (PlayerBar 위)
- 접기/펼치기 토글
- 각 항목: 상태 아이콘 + 제목 + 프로그레스 바 + 속도/ETA
- 완료 시 자동 접힘 (3초 후)
- 실패 시 재시도 버튼

### 4.2 상태별 시각 피드백

| 상태 | 아이콘 | 색상 | 프로그레스 |
|------|--------|------|-----------|
| 대기 | ⏳ | gray | 없음 |
| 다운로드 | ⬇ | blue (애니메이션) | 진행 바 |
| 변환 | 🔄 | orange | indeterminate |
| 완료 | ✓ | green | 100% |
| 실패 | ✗ | red | 없음 + 재시도 |

---

## Phase 5: 디자인 시스템 & 반응형 (P2)

### 5.1 디자인 토큰

```css
:root {
  /* 배경 레이어 (어두운 → 밝은) */
  --surface-0: #111113;  /* 전체 배경 */
  --surface-1: #18181b;  /* 카드 */
  --surface-2: #1f1f23;  /* 호버 */
  --surface-3: #27272c;  /* 활성 */

  /* 간격 (8px 그리드) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;

  /* 애니메이션 */
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-moderate: 300ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 5.2 반응형 브레이크포인트

| 브레이크포인트 | 너비 | 레이아웃 변경 |
|--------------|------|-------------|
| Mobile | < 640px | 단일 컬럼, 카드 스택, 하단 시트 |
| Tablet | 640-1024px | 단일 컬럼, 넓은 카드 |
| Desktop | > 1024px | 고정 max-width 720px |

모바일 변경:
- 검색 결과 → 풀스크린 하단 시트
- 라이브러리 테이블 → 카드 스택
- PlayerBar → 미니 모드 (썸네일 + 제목 + 재생 버튼만)
- 스와이프: 좌(삭제), 우(다운로드)

### 5.3 키보드 단축키

| 키 | 동작 |
|----|------|
| `/` | 검색 포커스 |
| `Escape` | 모달/패널 닫기 |
| `Space` | 재생/일시정지 |
| `←` / `→` | 5초 되감기/앞감기 |
| `↑` / `↓` | 볼륨 조절 |

---

## 파일 구조 (신규)

```
src/
├── components/
│   ├── App.tsx                    (레이아웃 컨테이너)
│   ├── Header.tsx                 (최소 헤더)
│   ├── ErrorBoundary.tsx          (유지)
│   ├── Toast.tsx                  (유지)
│   ├── PlayerBar/
│   │   ├── PlayerBar.tsx          (하단 고정 플레이어)
│   │   ├── NowPlaying.tsx         (현재 트랙 정보)
│   │   ├── PlaybackControls.tsx   (컨트롤 + 시크바)
│   │   └── VolumeControl.tsx      (볼륨)
│   ├── Search/
│   │   ├── SearchSection.tsx      (검색 섹션 래퍼)
│   │   ├── SearchBar.tsx          (검색 입력)
│   │   ├── RecentSearches.tsx     (최근 검색어)
│   │   └── SearchResultCard.tsx   (결과 카드 + 직접 다운로드)
│   ├── DownloadQueue/
│   │   ├── DownloadQueue.tsx      (큐 드로어)
│   │   └── DownloadQueueItem.tsx  (개별 항목)
│   └── Library/
│       ├── Library.tsx            (라이브러리 래퍼)
│       ├── LibraryHeader.tsx      (정렬/필터/뷰 토글)
│       ├── LibraryList.tsx        (리스트 뷰)
│       ├── LibraryGrid.tsx        (그리드 뷰)
│       └── LibraryItem.tsx        (개별 항목)
├── stores/
│   ├── audioStore.ts              (글로벌 오디오)
│   ├── downloadQueueStore.ts      (다운로드 큐)
│   └── uiStore.ts                 (UI 상태: 뷰 모드, 정렬)
├── api/
│   ├── search.ts                  (검색 API)
│   ├── download.ts                (다운로드 API)
│   └── library.ts                 (라이브러리 API)
├── constants/
│   └── messages.ts                (유지, 확장)
├── hooks/
│   ├── useKeyboardShortcuts.ts    (전역 키보드 단축키)
│   └── useRecentSearches.ts       (localStorage 검색 기록)
├── utilities/
│   ├── common.ts                  (유지)
│   └── format.ts                  (시간, 크기 포맷)
├── style.scss                     (글로벌 + 토큰)
└── script.ts                      (엔트리)
```

---

## 삭제 대상

- `src/components/Main/DownloaderContext.tsx` — 미사용 레거시
- `src/hooks/useAnimationFrame.ts` — 미사용
- `src/components/Main/` 디렉토리 구조 → `Search/`, `Library/` 등으로 분리

---

## 구현 순서

| 순서 | 작업 | 예상 규모 | 의존성 |
|------|------|----------|--------|
| 1 | 접근성 수정 (aria-label, 터치 타겟) | 소 | 없음 |
| 2 | 레거시 코드 삭제 | 소 | 없음 |
| 3 | audioStore + PlayerBar | 중 | 없음 |
| 4 | downloadQueueStore + DownloadQueue UI | 중 | 없음 |
| 5 | 검색 섹션 재설계 (details 제거, 직접 다운로드) | 중 | #4 |
| 6 | 라이브러리 재설계 (뷰 모드, 썸네일) | 중 | #3 |
| 7 | API 레이어 분리 | 소 | 없음 |
| 8 | 디자인 토큰 + 스타일 시스템 | 소 | 없음 |
| 9 | 반응형 레이아웃 | 중 | #5, #6 |
| 10 | 키보드 단축키 | 소 | #3 |

---

## 최종 와이어프레임

### Desktop (> 1024px)

```
┌─────────────────────────────────────────────────────────┐
│  YouTube Music Downloader                      v0.2.0   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  🔍  검색어를 입력하세요...              [검색]  │    │
│  └─────────────────────────────────────────────────┘    │
│  최근: Skid Row | AC/DC | Metallica                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ [thumb] Youth Gone Wild           3:45    [⬇]   │    │
│  │         Skid Row • 👁 50M                        │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ [thumb] 18 and Life              3:42    [▶]    │    │
│  │         Skid Row • 👁 80M        다운로드됨      │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ [thumb] I Remember You           5:12    [⬇]   │    │
│  │         Skid Row • 👁 30M                        │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  다운로드 목록 (12곡)    [≡] [⊞] [정렬▼] [⟳]          │
│  ┌─────────────────────────────────────────────────┐    │
│  │ [thumb] 18 and Life        3.2MB  [▶] [⬇] [🗑]  │    │
│  │ [thumb] Monkey Business    2.8MB  [▶] [⬇] [🗑]  │    │
│  │ [thumb] Slave to the Grind 4.1MB  [▶] [⬇] [🗑]  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [art] 18 and Life - Skid Row  ◀ ▶|| ▶ ==●===== 2:15   │
│                                          🔊 ====●==     │
└─────────────────────────────────────────────────────────┘

┌─ 다운로드 큐 (1/3 완료) ────────────────── [최소화] ─┐
│ ✓ Youth Gone Wild ─────────────────── 완료            │
│ ▶ I Remember You ████████░░░░ 67% 2.1MB/s ETA 3s     │
│ ⏳ Big Guns ──────────────────────── 대기              │
└──────────────────────────────────────────────────────┘
```

### Mobile (< 640px)

```
┌──────────────────────┐
│ YT Music DL   v0.2.0 │
├──────────────────────┤
│ 🔍 검색...    [검색] │
│                      │
│ ┌──────────────────┐ │
│ │[thumb]           │ │
│ │ Title      [⬇]  │ │
│ │ Artist • 3:45    │ │
│ ├──────────────────┤ │
│ │[thumb]           │ │
│ │ Title      [▶]  │ │
│ │ Artist • 4:12    │ │
│ └──────────────────┘ │
│                      │
│ 라이브러리 (12) [⟳]  │
│ ┌──────────────────┐ │
│ │[t] Title   [▶][🗑]│ │
│ │[t] Title   [▶][🗑]│ │
│ └──────────────────┘ │
│                      │
├──────────────────────┤
│[art] Title  ▶||  ●══│
└──────────────────────┘
```
