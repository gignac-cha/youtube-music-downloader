import { PropsWithChildren, Reducer, createContext, useReducer } from 'react';

const initialState: {
  state: 'ready' | 'searching' | 'requesting' | 'downloading' | 'finished';
  query: string;
  list?: {
    id: string;
    title: string;
    artist: string;
    thumbnail: string;
  }[];
  url: string;
  id?: string;
} = {
  state: 'ready',
  query: '',
  url: '',
};

type DownloaderAction =
  | { type: 'update-query'; query: string }
  | { type: 'request-search' }
  | { type: 'searched'; list: NonNullable<(typeof initialState)['list']> }
  | { type: 'update-url'; url: string }
  | { type: 'request-download' }
  | { type: 'progress'; id: string }
  | { type: 'finish' }
  | { type: 'reset' };

const reducer: Reducer<typeof initialState, DownloaderAction> = (
  prevState,
  action,
) => {
  switch (action.type) {
    case 'update-query':
      return { ...prevState, query: action.query };
    case 'request-search':
      return { ...prevState, state: 'searching' };
    case 'searched':
      return { ...prevState, state: 'ready', list: action.list };
    case 'update-url':
      return { ...prevState, url: action.url };
    case 'request-download':
      return { ...prevState, state: 'requesting' };
    case 'progress':
      return { ...prevState, state: 'downloading', id: action.id };
    case 'finish':
      return { ...prevState, state: 'finished' };
    case 'reset':
      return initialState;
  }
};

const defaultValue = {
  ...initialState,
  updateQuery: (query: string) => {},
  requestSearch: () => {},
  setList: (list: NonNullable<(typeof initialState)['list']>) => {},
  updateURL: (url: string) => {},
  requestDownload: () => {},
  watchProgress: (id: string) => {},
  finish: () => {},
  reset: () => {},
};

export const DownloaderContext = createContext(defaultValue);

export const DownloaderContextProvider = ({ children }: PropsWithChildren) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <DownloaderContext.Provider
      value={{
        ...state,
        updateQuery: (query: string) =>
          dispatch({ type: 'update-query', query }),
        requestSearch: () => dispatch({ type: 'request-search' }),
        setList: (list: NonNullable<(typeof initialState)['list']>) =>
          dispatch({ type: 'searched', list }),
        updateURL: (url: string) => dispatch({ type: 'update-url', url }),
        requestDownload: () => dispatch({ type: 'request-download' }),
        watchProgress: (id: string) => dispatch({ type: 'progress', id }),
        finish: () => dispatch({ type: 'finish' }),
        reset: () => dispatch({ type: 'reset' }),
      }}
    >
      {children}
    </DownloaderContext.Provider>
  );
};
