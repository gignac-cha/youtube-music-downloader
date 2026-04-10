# 음악 라이브러리 및 재생 UX 리서치 보고서

> 작성일: 2026-04-10  
> 에이전트: UI/UX 리서치 에이전트 #3  
> 대상: YouTube Music Downloader (React 19 + Radix UI + TypeScript)

---

## 목차

1. [리서치 개요](#1-리서치-개요)
2. [주요 뮤직 플레이어 분석](#2-주요-뮤직-플레이어-분석)
3. [음악 라이브러리 레이아웃 패턴](#3-음악-라이브러리-레이아웃-패턴)
4. [오디오 플레이어 UX 패턴](#4-오디오-플레이어-ux-패턴)
5. [앨범 아트 및 메타데이터 표시](#5-앨범-아트-및-메타데이터-표시)
6. [플레이리스트 및 컬렉션 관리](#6-플레이리스트-및-컬렉션-관리)
7. [키보드 단축키 및 접근성](#7-키보드-단축키-및-접근성)
8. [현재 앱 분석 및 구체적 권장사항](#8-현재-앱-분석-및-구체적-권장사항)

---

## 1. 리서치 개요

### 조사 대상 서비스 및 애플리케이션

| 카테고리 | 서비스/앱 | 특징 |
|---------|----------|------|
| 스트리밍 | Spotify, Apple Music, Tidal | 대규모 라이브러리, 큐레이션, 소셜 기능 |
| 데스크톱 플레이어 | foobar2000, MusicBee, Winamp | 고급 커스터마이징, 로컬 파일 관리 |
| 셀프호스팅 | Plexamp, Navidrome | 개인 서버 기반 스트리밍 |
| 웹 플레이어 | VLC Web, Museeks | 브라우저 기반 재생 |

### 리서치 소스

- [Tubik Studio - Music Streaming UI Design](https://blog.tubikstudio.com/feel-the-beat-ui-design-for-music-streaming-services/)
- [Tubik Studio - Echo Music App Case Study](https://blog.tubikstudio.com/case-study-echo-designing-uxui/)
- [Pixso - Music Player UI Design Examples](https://pixso.net/tips/music-player-ui/)
- [GeeksforGeeks - Music Streaming Web App UI Design](https://www.geeksforgeeks.org/websites-apps/ui-design-of-a-music-streaming-web-app/)
- [Hicks Design - My Perfect Music App](https://hicks.design/journal/my-perfect-music-app-doesnt-exist)
- [LogRocket - Building Audio Player in React](https://blog.logrocket.com/building-audio-player-react/)
- [Let's Build UI - Audio Player with React Hooks](https://www.letsbuildui.dev/articles/building-an-audio-player-with-react-hooks/)
- [Level Up Coding - Mini Audio Player in React](https://levelup.gitconnected.com/how-to-add-a-mini-audio-player-to-your-website-with-react-184046e17472)
- [W3C WAI-ARIA Practices Guide](https://wai-aria-practices.netlify.app/aria-practices/)
- [WCAG Audio Control Guidelines](https://wcag.dock.codes/documentation/wcag142/)
- [foobar2000 Columns UI](https://yuo.be/columns-ui)
- [Behance - Music Player Dark Theme](https://www.behance.net/gallery/94004549/Music-Player-App-UIUX-design-Dark-Theme)
- [Dribbble - Music Library Designs](https://dribbble.com/tags/music-library)
- [npm - react-h5-audio-player](https://www.npmjs.com/package/react-h5-audio-player)
- [npm - react-modern-audio-player](https://github.com/slash9494/react-modern-audio-player)
- [Psysonic - Navidrome Client](https://github.com/Psychotoxical/psysonic)

---

## 2. 주요 뮤직 플레이어 분석

### 2.1 Spotify Web Player

**레이아웃 구조:**
- 3단 구조: 좌측 사이드바(네비게이션 + 라이브러리) | 중앙 콘텐츠 영역 | 우측 패널(Now Playing 상세)
- 하단 고정 재생 바 (Persistent Bottom Bar)
- 다크 테마 기본, 앨범 아트 기반 동적 그라디언트 배경

**핵심 UX 패턴:**
- 재생 바가 항상 하단에 고정되어 브라우징 중에도 재생 제어 가능
- 좌측: 곡 정보 + 앨범 아트 썸네일
- 중앙: 재생 컨트롤 (셔플, 이전, 재생/일시정지, 다음, 반복) + 시크바 + 시간 표시
- 우측: 볼륨 슬라이더, 큐 보기, 디바이스 전환, 전체화면

**라이브러리 관리:**
- 리스트 뷰와 그리드 뷰 전환 가능
- 최근 재생, 내 플레이리스트, 저장한 앨범 등 자동 분류
- 검색 필터: 아티스트, 앨범, 곡, 팟캐스트

### 2.2 Apple Music

**레이아웃 구조:**
- 좌측 사이드바: 라이브러리 카테고리 (최근 추가, 아티스트, 앨범, 노래, 장르)
- 중앙: 콘텐츠 그리드/리스트
- 상단: 네비게이션 + 검색
- 하단: 미니 플레이어 (확장 가능)

**핵심 UX 패턴:**
- "몰입형 보기" (Immersive View): 전체화면 재생 시 앨범 아트 + 가사 + 크레딧 표시
- 탭 기반 네비게이션: For You, Browse, Radio, Library
- 다크/라이트 테마 지원
- iPad/macOS에서 전체화면 시 재생 큐 표시

### 2.3 foobar2000 / Columns UI

**레이아웃 구조:**
- 완전 커스터마이징 가능한 패널 시스템
- 수평/수직 분할자로 윈도우를 섹션으로 나누고 각 섹션에 패널 배치
- 주요 패널: Column Browser (아티스트/앨범/장르 계층 탐색), Playlist View, Album Art, Spectrum Analyzer

**핵심 UX 패턴:**
- "Column Browser": 아티스트 > 앨범 > 곡 순서로 필터링하는 다단 열 탐색
- 플레이리스트 트리 (foo_playlist_tree): 트리 기반 미디어 라이브러리
- 커스텀 열 정의 및 그룹핑 스킴 지원
- 고급 사용자를 위한 포맷팅 문자열 기반 표시 커스터마이징

### 2.4 Plexamp

**레이아웃 구조:**
- 컴팩트한 단일 컬럼 레이아웃 (모바일 우선)
- 라이브러리 그리드 뷰: 앨범 아트 중심의 그리드 표시
- 플레이리스트를 아티스트 또는 앨범 목록으로 표시 가능

**핵심 UX 패턴:**
- 비주얼 중심: 앨범 아트를 크게 표시
- Sonic Analysis 기반 자동 플레이리스트 생성
- 크로스페이드, 게인 정규화 등 오디오 품질 기능
- 데스크톱 대형 화면에서는 제한적인 레이아웃

### 2.5 Navidrome / Psysonic (웹 기반)

**레이아웃 구조:**
- Psysonic: Winamp에서 영감받은 Tauri + React 기반 데스크톱 클라이언트
- 웨이브폼 시크바, 캔버스 기반 렌더링
- 그라디언트와 글로우 효과로 시각적 피드백

**핵심 UX 패턴:**
- 자체 호스팅 서버와 동기화
- 서버사이드 큐 동기화
- 다양한 클라이언트 앱 지원 (웹, 데스크톱, 모바일)

---

## 3. 음악 라이브러리 레이아웃 패턴

### 3.1 그리드 뷰 vs 리스트 뷰

#### 그리드 뷰 (Grid View)

**적합한 경우:**
- 앨범 아트가 있는 콘텐츠 탐색
- 시각적 브라우징 선호 사용자
- 앨범/아티스트 단위 탐색

**구현 패턴:**
```
+------------------+------------------+------------------+
|  +-----------+   |  +-----------+   |  +-----------+   |
|  | 앨범 아트  |   |  | 앨범 아트  |   |  | 앨범 아트  |   |
|  |           |   |  |           |   |  |           |   |
|  +-----------+   |  +-----------+   |  +-----------+   |
|  곡 제목         |  곡 제목         |  곡 제목         |
|  아티스트        |  아티스트        |  아티스트        |
+------------------+------------------+------------------+
```

**장점:**
- 시각적으로 풍부하고 매력적
- 앨범 아트를 활용한 빠른 인식
- 탐색 모드에서 높은 참여도

**단점:**
- 한 화면에 표시할 수 있는 항목 수 제한
- 메타데이터 표시 공간 부족
- 긴 목록에서 스크롤 증가

#### 리스트 뷰 (List View)

**적합한 경우:**
- 세부 정보 확인 (파일 크기, 길이, 비트레이트)
- 대량의 항목 빠르게 스캔
- 정렬/필터링 작업

**구현 패턴:**
```
+------+------------------------------------------+----------+--------+
| 아트  | 제목 / 아티스트                           | 파일 크기 | 시간   |
+------+------------------------------------------+----------+--------+
| [img] | 노래 제목 1 - 아티스트 이름               | 4.2 MB   | 3:42   |
| [img] | 노래 제목 2 - 아티스트 이름               | 3.8 MB   | 3:15   |
| [img] | 노래 제목 3 - 아티스트 이름               | 5.1 MB   | 4:20   |
+------+------------------------------------------+----------+--------+
```

**장점:**
- 정보 밀도가 높음
- 열 기반 정렬 용이
- 대규모 라이브러리에 적합

**단점:**
- 시각적으로 단조로움
- 앨범 아트 크기 제한

### 3.2 권장: 하이브리드 접근법

**본 앱에 가장 적합한 방식은 기본 리스트 뷰 + 그리드 뷰 전환 옵션이다.**

이유:
1. 다운로드 관리 앱의 특성상 파일 크기, 다운로드 상태 등 메타데이터가 중요
2. YouTube 영상 썸네일이 있으므로 그리드 뷰에서 시각적 탐색 가능
3. 사용자가 뷰 모드를 전환할 수 있도록 토글 제공

### 3.3 정렬 (Sorting)

필수 정렬 옵션:
| 기준 | 설명 | 우선순위 |
|------|------|---------|
| 다운로드 날짜 | 최신순/오래된순 (기본값) | 높음 |
| 제목 | 가나다/알파벳순 | 높음 |
| 파일 크기 | 큰순/작은순 | 중간 |
| 아티스트 | 아티스트명 기준 | 중간 |

### 3.4 필터링 (Filtering)

| 필터 | 설명 | 우선순위 |
|------|------|---------|
| 텍스트 검색 | 제목/아티스트 검색 | 높음 |
| 날짜 범위 | 특정 기간 필터 | 낮음 |

### 3.5 그룹핑 (Grouping)

foobar2000의 Column Browser 패턴에서 영감을 받아:
- 다운로드 날짜별 그룹핑 (오늘, 이번 주, 이번 달, 이전)
- 아티스트별 그룹핑 (메타데이터가 있는 경우)

---

## 4. 오디오 플레이어 UX 패턴

### 4.1 Persistent Bottom Bar (고정 하단 재생 바)

**업계 표준 패턴으로, 본 앱에 반드시 도입해야 할 핵심 기능이다.**

모든 주요 뮤직 서비스 (Spotify, Apple Music, Tidal, YouTube Music)가 이 패턴을 채택하고 있다. 사용자가 라이브러리를 탐색하거나 검색하는 동안에도 재생 컨트롤에 항상 접근할 수 있어 끊김 없는 청취 경험을 제공한다.

#### 레이아웃 구조

```
+------------------------------------------------------------------+
|                        메인 콘텐츠 영역                            |
|  (검색, 다운로드 진행, 라이브러리 등)                               |
|                                                                    |
+------------------------------------------------------------------+
| [앨범아트] 곡 제목 - 아티스트 | ◀ ▶ ■ | ===●========== 1:23/3:45 | 🔊 ===●=== |
+------------------------------------------------------------------+
```

#### 3단 구성

| 영역 | 내용 | 설명 |
|------|------|------|
| 좌측 | 곡 정보 | 앨범 아트 썸네일 (40x40px) + 곡 제목 + 아티스트 |
| 중앙 | 재생 컨트롤 | 이전/재생-일시정지/다음 버튼 + 시크바 + 현재시간/총시간 |
| 우측 | 부가 컨트롤 | 볼륨 슬라이더 + 큐 보기 + 반복/셔플 |

#### 상태 관리

현재 앱은 `useAudio` 훅으로 개별 `Audio` 객체를 관리하고 있으나, Persistent Bottom Bar를 위해서는 **전역 오디오 상태 관리**가 필요하다:

- React Context API 또는 Zustand를 사용한 전역 오디오 상태
- 단일 `HTMLAudioElement` 인스턴스를 앱 전체에서 공유
- 재생 상태, 현재 곡, 큐, 볼륨 등을 중앙에서 관리

### 4.2 시크바 (Seekbar)

#### 기본 시크바 (Linear Progress Bar)
- 수평 막대 형태의 진행 표시
- 클릭/드래그로 원하는 위치로 이동
- 버퍼링 상태 표시 (로딩된 부분 시각화)
- 호버 시 미리보기 시간 툴팁 표시

#### 웨이브폼 시크바 (Waveform Seekbar)
- 오디오 파형을 시각적으로 렌더링
- Canvas 기반 렌더링으로 그라디언트, 글로우 효과 적용 가능
- 피크와 밸리를 시각적으로 확인하여 직관적 탐색
- SoundCloud에서 대중화된 패턴

**권장:** 기본 시크바를 우선 구현하고, 향후 웨이브폼 시크바를 선택적 기능으로 추가. 웨이브폼은 서버에서 오디오 분석 데이터를 미리 생성해야 하므로 구현 비용이 높다.

### 4.3 볼륨 컨트롤

- 슬라이더 + 음소거 토글 아이콘
- 볼륨 레벨에 따른 아이콘 변화 (음소거/저/중/고)
- 마우스 휠로 볼륨 조절 지원
- 볼륨 값 localStorage에 저장하여 세션 간 유지

### 4.4 재생 큐 (Queue)

**핵심 기능:**
- 현재 재생 중인 곡 하이라이트
- 다음 재생될 곡 목록 표시
- 드래그 앤 드롭으로 순서 변경
- 곡을 큐에서 제거하는 기능
- "다음에 재생" (Play Next) 기능
- "큐에 추가" (Add to Queue) 기능

**표시 방식:**
- 하단 재생 바에서 큐 아이콘 클릭 시 슬라이드업 패널
- 또는 우측 사이드 패널로 표시 (Spotify 스타일)

### 4.5 반복 및 셔플

| 모드 | 아이콘 | 동작 |
|------|--------|------|
| 반복 없음 | 🔁 (비활성) | 큐 끝에서 정지 |
| 전체 반복 | 🔁 (활성) | 큐 전체 반복 |
| 한 곡 반복 | 🔂 | 현재 곡만 반복 |
| 셔플 | 🔀 | 랜덤 순서 재생 |

---

## 5. 앨범 아트 및 메타데이터 표시

### 5.1 앨범 아트 표시 패턴

#### 썸네일 (40-60px)
- 리스트 뷰의 각 행에 표시
- 재생 바 좌측에 표시
- 원형 또는 사각형 (둥근 모서리)

#### 미디엄 (120-200px)
- 그리드 뷰 카드
- "Now Playing" 미니 뷰

#### 대형 (300px+)
- 전체화면 "Now Playing" 뷰
- 앨범 상세 페이지 헤더

#### 동적 배경
- 앨범 아트에서 주요 색상 추출 (color extraction)
- 추출한 색상으로 배경 그라디언트 생성
- Spotify, Apple Music에서 활용하는 패턴
- 라이브러리: `colorthief`, `vibrant.js` 등

### 5.2 메타데이터 표시

**필수 표시 정보:**
| 정보 | 표시 위치 | 우선순위 |
|------|----------|---------|
| 곡 제목 | 모든 곳 | 필수 |
| YouTube ID | 리스트 뷰 (작게) | 필수 |
| 파일 크기 | 리스트 뷰, 상세 | 필수 |
| 아티스트 | 재생 바, 리스트 | 높음 |
| 재생 시간 | 리스트 뷰, 시크바 | 높음 |
| 다운로드 날짜 | 리스트 뷰 | 중간 |
| 비트레이트/품질 | 상세 보기 | 낮음 |

### 5.3 다크 테마

현대 뮤직 플레이어의 사실상 표준:
- 어두운 배경 (#0a0a0a ~ #1a1a1a)이 앨범 아트의 색상을 더 돋보이게 함
- 눈의 피로를 줄여 장시간 사용에 적합
- Radix UI Themes의 다크 모드 지원 활용 가능
- 대비 비율 WCAG AA 기준 (4.5:1 이상) 준수 필요

---

## 6. 플레이리스트 및 컬렉션 관리

### 6.1 본 앱에서의 플레이리스트 개념

YouTube Music Downloader의 특성을 고려할 때, 전통적인 플레이리스트보다는 다음과 같은 **경량 컬렉션 관리**가 적합하다:

#### 자동 컬렉션
- "모든 다운로드" - 전체 라이브러리
- "최근 다운로드" - 최근 7일 이내
- "최근 재생" - 최근 재생한 곡 (LocalStorage 기반)

#### 사용자 정의 컬렉션 (향후 확장)
- 사용자가 직접 만드는 플레이리스트
- 드래그 앤 드롭으로 곡 추가
- 서버사이드 또는 LocalStorage 저장

### 6.2 큐 관리 vs 플레이리스트

| 특성 | 큐 (Queue) | 플레이리스트 (Playlist) |
|------|-----------|----------------------|
| 지속성 | 임시 (세션 기반) | 영구 저장 |
| 용도 | 즉석 재생 순서 | 큐레이션된 모음 |
| 편집 | 즉시 추가/제거/재정렬 | 이름, 설명 등 관리 |
| 우선순위 | 높음 (MVP 필수) | 중간 (향후 확장) |

### 6.3 일괄 작업 (Batch Operations)

- 다중 선택 (체크박스 또는 Shift+클릭)
- 선택한 곡 일괄 삭제
- 선택한 곡 일괄 다운로드 (ZIP)
- 선택한 곡 큐에 추가

---

## 7. 키보드 단축키 및 접근성

### 7.1 키보드 단축키

#### 필수 단축키

| 단축키 | 동작 | 우선순위 |
|--------|------|---------|
| `Space` | 재생/일시정지 토글 | 필수 |
| `→` | 5초 앞으로 | 높음 |
| `←` | 5초 뒤로 | 높음 |
| `↑` | 볼륨 증가 | 높음 |
| `↓` | 볼륨 감소 | 높음 |
| `M` | 음소거 토글 | 높음 |
| `N` | 다음 곡 | 중간 |
| `P` | 이전 곡 | 중간 |
| `/` 또는 `Ctrl+K` | 검색 포커스 | 높음 |
| `Escape` | 모달/패널 닫기 | 높음 |

#### 구현 시 주의사항
- 입력 필드에 포커스가 있을 때는 단축키 비활성화
- `event.preventDefault()`로 브라우저 기본 동작 방지
- 단축키 목록을 `?` 키로 표시하는 도움말 제공

### 7.2 WCAG 접근성 요구사항

#### ARIA 속성

```
재생 버튼: role="button", aria-label="재생" 또는 "일시정지", aria-pressed
시크바: role="slider", aria-valuemin, aria-valuemax, aria-valuenow, aria-label="재생 위치"
볼륨: role="slider", aria-label="볼륨", aria-valuemin="0", aria-valuemax="100"
```

#### WCAG 1.4.2 오디오 컨트롤
- 자동 재생되는 오디오가 3초 이상인 경우, 일시정지/정지 메커니즘 제공 필수
- 시스템 볼륨과 독립적으로 오디오 볼륨 제어 가능해야 함

#### 키보드 접근성
- 모든 오디오 컨트롤은 키보드로 완전히 조작 가능해야 함
- Tab 키로 컨트롤 간 이동, Enter/Space로 활성화
- 토글 버튼(음소거 등)은 `aria-pressed` 속성으로 상태 전달
- 포커스 표시기(focus indicator)가 명확하게 보여야 함

#### 색상 대비
- 텍스트: 최소 4.5:1 대비 비율 (WCAG AA)
- 비활성 컨트롤도 3:1 이상의 대비 비율
- 색상만으로 정보를 전달하지 않기 (아이콘 + 텍스트 병행)

### 7.3 스크린 리더 지원

- 곡 변경 시 `aria-live="polite"` 영역에 "현재 재생 중: [곡 제목]" 알림
- 재생 진행 상태를 주기적으로 업데이트하되 너무 자주 하지 않기 (5-10초 간격)
- 다운로드 완료 알림: `aria-live="assertive"`

---

## 8. 현재 앱 분석 및 구체적 권장사항

### 8.1 현재 상태 분석

현재 `Downloaded.tsx` 코드를 분석한 결과:

**현재 구현:**
- `Table.Root` + `Table.Body`로 단순 테이블 레이아웃
- 각 행: 다운로드 링크 + 파일 크기 Badge + 재생/삭제 버튼
- `useAudio` 훅: 개별 `Audio` 객체를 각 행마다 생성
- 재생 시 다른 곡이 함께 재생될 수 있는 문제 (단일 재생 제어 없음)
- 삭제 확인: 인라인 확인/취소 버튼 (좋은 패턴)

**문제점:**
1. **전역 재생 상태 부재**: 각 `AudioPlayer` 컴포넌트가 독립적으로 `new Audio()`를 생성. 여러 곡이 동시에 재생될 수 있음
2. **재생 컨트롤 부족**: 시크바, 볼륨, 시간 표시 없음. 재생/일시정지만 가능
3. **시각적 빈약함**: 앨범 아트/썸네일 없음, 텍스트 위주 표시
4. **라이브러리 관리 기능 없음**: 정렬, 필터, 검색 없음
5. **레이아웃이 테이블에 한정**: 그리드 뷰 옵션 없음
6. **접근성 부족**: ARIA 속성 미적용, 키보드 단축키 없음

### 8.2 단계별 개선 권장사항

#### Phase 1: 핵심 재생 경험 개선 (MVP, 높은 우선순위)

**1-1. 전역 오디오 컨텍스트 도입**

현재의 컴포넌트별 `useAudio`를 전역 `AudioContext`로 교체:

```
AudioPlayerContext:
  - currentTrack: { id, title, src }
  - isPlaying: boolean
  - currentTime: number
  - duration: number
  - volume: number
  - queue: Track[]
  - play(track): void
  - pause(): void
  - toggle(): void
  - seek(time): void
  - setVolume(level): void
  - next(): void
  - previous(): void
```

단일 `HTMLAudioElement` 인스턴스를 Context에서 관리하여 동시 재생 방지.

**1-2. Persistent Bottom Bar 추가**

앱 하단에 고정 재생 바를 추가. `Main.tsx`의 레이아웃을 수정하여:

```
<main>
  <Container>
    <Section>
      {/* 기존 콘텐츠 */}
    </Section>
  </Container>
  <PlayerBar />  {/* position: fixed; bottom: 0 */}
</main>
```

PlayerBar 구성:
- 좌측: 곡 제목 (YouTube 썸네일이 있으면 표시)
- 중앙: 재생/일시정지 + 이전/다음 + 시크바
- 우측: 볼륨 슬라이더

**1-3. 시크바 구현**

Radix UI의 `Slider` 컴포넌트를 활용:
- `requestAnimationFrame`으로 부드러운 진행 표시 (기존 `useAnimationFrame` 훅 활용 가능)
- 클릭/드래그로 위치 이동
- 현재 시간 / 총 시간 텍스트 표시

#### Phase 2: 라이브러리 관리 개선 (중간 우선순위)

**2-1. 리스트 뷰 개선**

현재 테이블을 개선된 리스트 뷰로 교체:
- YouTube 썸네일 표시 (`https://img.youtube.com/vi/{id}/mqdefault.jpg`)
- 곡 제목 / 파일 크기 / 다운로드 날짜
- 호버 시 재생 버튼 오버레이
- 현재 재생 중인 곡 하이라이트 (이퀄라이저 애니메이션 아이콘)

**2-2. 정렬 기능**

라이브러리 헤더에 정렬 드롭다운:
- 다운로드 날짜순 (기본)
- 제목순
- 파일 크기순

**2-3. 검색/필터**

라이브러리 내 텍스트 검색 입력 필드:
- 실시간 필터링 (debounce 적용)
- 제목 기준 검색

#### Phase 3: 고급 기능 (낮은 우선순위, 향후 확장)

**3-1. 그리드 뷰 옵션**

뷰 모드 전환 토글 (리스트/그리드):
- 그리드: YouTube 썸네일 카드 + 제목
- 반응형 그리드 (CSS Grid, auto-fill, minmax)

**3-2. 재생 큐 관리**

큐 패널 (하단 재생 바에서 큐 아이콘 클릭):
- 현재 재생 중인 곡 표시
- 다음 재생 목록
- 드래그 앤 드롭 순서 변경
- "다음에 재생" 컨텍스트 메뉴

**3-3. 키보드 단축키**

전역 키보드 이벤트 리스너:
- Space: 재생/일시정지
- 좌우 화살표: 시크
- 상하 화살표: 볼륨

**3-4. 접근성 개선**

- 모든 컨트롤에 적절한 ARIA 속성 추가
- 포커스 관리 및 포커스 트래핑 (모달/패널)
- `aria-live` 영역으로 재생 상태 알림

### 8.3 기술 구현 참고

#### 추천 라이브러리/도구

| 도구 | 용도 | 비고 |
|------|------|------|
| Radix UI Slider | 시크바, 볼륨 슬라이더 | 이미 Radix UI 사용 중 |
| Zustand 또는 Context API | 전역 오디오 상태 | Context API가 이미 사용 중이므로 일관성 있음 |
| `useAnimationFrame` | 시크바 실시간 업데이트 | 이미 프로젝트에 존재 |
| YouTube Thumbnail URL | 앨범 아트 대체 | `img.youtube.com/vi/{id}/mqdefault.jpg` |
| localStorage | 볼륨, 뷰 모드 설정 저장 | 서버 불필요 |

#### YouTube 썸네일 활용

YouTube 비디오 ID로 썸네일을 무료로 가져올 수 있음:
- `https://img.youtube.com/vi/{VIDEO_ID}/default.jpg` (120x90)
- `https://img.youtube.com/vi/{VIDEO_ID}/mqdefault.jpg` (320x180)
- `https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg` (480x360)
- `https://img.youtube.com/vi/{VIDEO_ID}/maxresdefault.jpg` (1280x720, 없을 수 있음)

이를 통해 별도의 이미지 저장 없이 앨범 아트를 표시할 수 있다.

### 8.4 최종 우선순위 요약

| 순위 | 기능 | 영향도 | 구현 복잡도 |
|------|------|--------|------------|
| 1 | 전역 오디오 컨텍스트 | 매우 높음 | 중간 |
| 2 | Persistent Bottom Bar | 매우 높음 | 중간 |
| 3 | 시크바 + 시간 표시 | 높음 | 낮음 |
| 4 | 볼륨 컨트롤 | 높음 | 낮음 |
| 5 | YouTube 썸네일 표시 | 높음 | 낮음 |
| 6 | 리스트 뷰 개선 | 중간 | 낮음 |
| 7 | 정렬 기능 | 중간 | 낮음 |
| 8 | 라이브러리 내 검색 | 중간 | 낮음 |
| 9 | 키보드 단축키 | 중간 | 낮음 |
| 10 | 그리드 뷰 | 중간 | 중간 |
| 11 | 재생 큐 관리 | 중간 | 높음 |
| 12 | 접근성 (ARIA) | 중간 | 중간 |
| 13 | 웨이브폼 시크바 | 낮음 | 높음 |
| 14 | 플레이리스트 관리 | 낮음 | 높음 |

---

## 부록: 참고 디자인 레퍼런스

### 웹 기반 뮤직 플레이어 레퍼런스

1. **Spotify Web Player** - 업계 표준 3단 레이아웃, persistent bottom bar
2. **Navidrome Web UI** - 셀프호스팅 웹 기반 뮤직 플레이어의 좋은 레퍼런스
3. **Psysonic** (Tauri + React) - Winamp 스타일의 현대적 재해석, 웨이브폼 시크바
4. **SoundCloud** - 웨이브폼 시크바의 원조, 심플한 재생 UX

### Figma 커뮤니티 레퍼런스

- [Spotify Music UI Design & Prototype](https://www.figma.com/community/file/1124449258211294515)
- [Music Player Web UI Design Concept](https://www.figma.com/community/file/1396367792083209260)
- [Music App Design](https://www.figma.com/community/file/1227220980074899885)

### React 오디오 플레이어 라이브러리

- [react-h5-audio-player](https://www.npmjs.com/package/react-h5-audio-player) - i18n, a11y, MSE/EME 지원
- [react-modern-audio-player](https://github.com/slash9494/react-modern-audio-player) - 위치 설정 가능, 접근성 내장
- [react-audio-play](https://github.com/riyaddecoder/react-audio-play) - 경량, 커스터마이징 용이
