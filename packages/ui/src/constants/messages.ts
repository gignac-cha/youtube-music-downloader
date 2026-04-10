export const messages = {
  app: {
    title: 'YouTube Music Downloader',
    version: 'v0.2.0',
  },
  search: {
    placeholder: '검색어를 입력하세요...',
    results: (count: number) => `검색 결과 (${count}개)`,
    noResults: '검색 결과가 없습니다',
    error: '검색 중 오류가 발생했습니다',
    buttonLabel: '검색',
  },
  download: {
    placeholder: 'YouTube URL을 입력하세요...',
    buttonLabel: '다운로드 시작',
    progress: '다운로드 중...',
    complete: '다운로드 완료',
    error: '다운로드 실패',
    eta: (seconds: number) => `남은 시간: ${Math.ceil(seconds)}초`,
  },
  downloaded: {
    title: '다운로드 목록',
    empty: '다운로드한 파일이 없습니다',
    badge: '다운로드됨',
    deleteConfirm: '정말 삭제하시겠습니까?',
    sortByTitle: '제목순',
    sortBySize: '크기순',
    sortByNewest: '최신순',
  },
  common: {
    reset: '초기화',
    refresh: '새로고침',
    retry: '다시 시도',
    play: '재생',
    pause: '일시정지',
    delete: '삭제',
    confirm: '확인',
    cancel: '취소',
  },
  audio: {
    playLabel: (title: string) => `재생: ${title}`,
    pauseLabel: (title: string) => `일시정지: ${title}`,
  },
} as const;
