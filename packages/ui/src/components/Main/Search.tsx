import {
  CheckIcon,
  DownloadIcon,
  EyeOpenIcon,
  MagnifyingGlassIcon,
  ResetIcon,
  VideoIcon,
} from '@radix-ui/react-icons';
import {
  Avatar,
  Badge,
  Box,
  Card,
  Flex,
  IconButton,
  Popover,
  Spinner,
  Text,
  TextField,
} from '@radix-ui/themes';
import { useQuery } from '@tanstack/react-query';
import { useCallback, useContext, useMemo } from 'react';
import { getDownloaded } from '../../api/downloaded';
import { DownloaderContext } from './DownloaderContext';

type SearchResultItem = {
  id: string;
  title: string;
  artist: string;
  thumbnail: string;
  view_count?: string;
  duration?: string;
};

type SearchData =
  | {
      error: false;
      data: SearchResultItem[];
    }
  | {
      error: true;
      message: string;
    };

const formatViewCount = (viewCount: string): string => {
  // Extract numeric value from strings like "1,234,567 views" or "1234567"
  const numericString = viewCount.replace(/[^\d]/g, '');
  const number = parseInt(numericString, 10);
  
  if (isNaN(number)) return viewCount;
  
  if (number >= 1000000000) {
    return `${(number / 1000000000).toFixed(1)}B`;
  } else if (number >= 1000000) {
    return `${(number / 1000000).toFixed(1)}M`;
  } else if (number >= 1000) {
    return `${(number / 1000).toFixed(1)}K`;
  }
  
  return number.toString();
};

const postSearch = async (query: string) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  const response = await fetch('/api/v1/search', {
    method: 'POST',
    headers,
    body: JSON.stringify({ search_query: query }),
  });
  const data: SearchData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

export const Search = () => {
  const {
    state,
    updateQuery,
    query,
    requestSearch,
    setList,
    list,
    updateURL,
    url,
    reset,
  } = useContext(DownloaderContext);

  const { refetch: search } = useQuery({
    queryKey: ['search', query],
    queryFn: () => postSearch(query),
    enabled: false,
  });

  const { data: downloadedFiles = [] } = useQuery({
    queryKey: ['downloaded'],
    queryFn: getDownloaded,
  });

  const onClick = useCallback(async () => {
    requestSearch();
    const { data } = await search();
    if (data) {
      setList(data);
    }
  }, [requestSearch, search, setList]);

  const isOpened = useMemo(() => !!list && !url, [list, url]);

  const isDownloaded = useCallback((videoId: string) => {
    return downloadedFiles.some((file: any) => file.info_dict.id === videoId);
  }, [downloadedFiles]);

  return (
    <Flex direction={'column'} gap={'2'}>
      <Flex direction={'row'} gap={'2'}>
        <Box flexGrow={'1'}>
          <TextField.Root
            placeholder="Input query here..."
            disabled={state !== 'ready' && state !== 'finished'}
            value={query}
            onChange={(event) => updateQuery(event.currentTarget.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && query.length > 0 && (state === 'ready' || state === 'finished')) {
                if (state === 'finished') {
                  const currentQuery = query;
                  reset();
                  setTimeout(async () => {
                    requestSearch();
                    try {
                      const data = await postSearch(currentQuery);
                      setList(data);
                    } catch (error) {
                      console.error('Search failed:', error);
                    }
                  }, 0);
                } else {
                  onClick();
                }
              }
            }}
          >
            <TextField.Slot>
              <MagnifyingGlassIcon />
            </TextField.Slot>
          </TextField.Root>
        </Box>
        <IconButton
          disabled={query.length === 0 || (state !== 'ready' && state !== 'finished')}
          onClick={async () => {
            if (state === 'finished') {
              const currentQuery = query;
              reset();
              setTimeout(async () => {
                requestSearch();
                try {
                  const data = await postSearch(currentQuery);
                  setList(data);
                } catch (error) {
                  console.error('Search failed:', error);
                }
              }, 0);
            } else {
              onClick();
            }
          }}
        >
          {state === 'searching' ? <Spinner /> : <MagnifyingGlassIcon />}
        </IconButton>
        <IconButton
          variant="soft"
          onClick={reset}
          title="초기화"
          disabled={state === 'searching' || state === 'requesting' || state === 'downloading'}
        >
          <ResetIcon />
        </IconButton>
      </Flex>
      <details open={isOpened}>
        <summary>Search results ({list?.length ?? 0} results)</summary>
        <Flex direction={'column'} gap={'1'}>
          {list?.map((item: SearchResultItem) => (
            <Card size={'1'} key={item.id}>
              <Flex direction={'row'} gap={'2'} align={'center'}>
                <Popover.Root>
                  <Popover.Trigger>
                    <Avatar src={item.thumbnail} fallback={<VideoIcon />} size={'4'} />
                  </Popover.Trigger>
                  <Popover.Content>
                    <img src={item.thumbnail} width={640} />
                  </Popover.Content>
                </Popover.Root>
                <Flex direction={'column'} flexGrow={'1'} gap={'1'}>
                  <Flex direction={'row'} align={'center'} gap={'2'}>
                    <Text weight={'bold'} size={'2'} style={{ lineHeight: 1.3 }}>
                      {item.title}
                    </Text>
                    {isDownloaded(item.id) && (
                      <Badge color="green" size="1">
                        <DownloadIcon width={10} height={10} />
                        다운로드됨
                      </Badge>
                    )}
                  </Flex>
                  <Flex direction={'row'} gap={'2'} align={'center'}>
                    <Text size={'1'} color={'gray'}>
                      {item.artist}
                    </Text>
                    {item.duration && (
                      <Flex align={'center'} gap={'1'}>
                        <Box style={{ width: '3px', height: '3px', backgroundColor: 'var(--gray-8)', borderRadius: '50%' }} />
                        <Text size={'1'} color={'gray'}>
                          {item.duration}
                        </Text>
                      </Flex>
                    )}
                    {item.view_count && (
                      <Flex 
                        align={'center'} 
                        gap={'1'} 
                        title={`${item.view_count} views`}
                      >
                        <Box style={{ width: '3px', height: '3px', backgroundColor: 'var(--gray-8)', borderRadius: '50%' }} />
                        <EyeOpenIcon width={12} height={12} style={{ color: 'var(--gray-9)' }} />
                        <Text size={'1'} color={'gray'}>
                          {formatViewCount(item.view_count)}
                        </Text>
                      </Flex>
                    )}
                  </Flex>
                </Flex>
                <IconButton
                  onClick={() =>
                    updateURL(`https://www.youtube.com/watch?v=${item.id}`)
                  }
                  variant={url.includes(item.id) ? 'soft' : 'outline'}
                >
                  {url.includes(item.id) && <CheckIcon />}
                </IconButton>
              </Flex>
            </Card>
          ))}
        </Flex>
      </details>
    </Flex>
  );
};
