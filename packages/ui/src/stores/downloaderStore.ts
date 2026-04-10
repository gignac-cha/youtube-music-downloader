import { create } from 'zustand';

export type DownloaderPhase =
  | 'ready'
  | 'searching'
  | 'requesting'
  | 'downloading'
  | 'finished';

export type SearchResultItem = {
  id: string;
  title: string;
  artist: string;
  thumbnail: string;
  view_count?: string;
  duration?: string;
};

interface DownloaderState {
  phase: DownloaderPhase;
  query: string;
  searchResults: SearchResultItem[] | null;
  url: string;
  downloadId: string | null;
}

interface DownloaderActions {
  setQuery: (query: string) => void;
  setSearching: () => void;
  setSearchResults: (results: SearchResultItem[]) => void;
  setUrl: (url: string) => void;
  setRequesting: () => void;
  setDownloading: (id: string) => void;
  setFinished: () => void;
  reset: () => void;
}

const initialState: DownloaderState = {
  phase: 'ready',
  query: '',
  searchResults: null,
  url: '',
  downloadId: null,
};

export const useDownloaderStore = create<DownloaderState & DownloaderActions>()(
  (set) => ({
    ...initialState,

    setQuery: (query) => set({ query }),

    setSearching: () => set({ phase: 'searching' }),

    setSearchResults: (results) =>
      set({ phase: 'ready', searchResults: results }),

    setUrl: (url) =>
      set((state) => ({
        url,
        phase: state.phase === 'finished' ? 'ready' : state.phase,
      })),

    setRequesting: () => set({ phase: 'requesting' }),

    setDownloading: (id) => set({ phase: 'downloading', downloadId: id }),

    setFinished: () => set({ phase: 'finished' }),

    reset: () => set(initialState),
  }),
);
