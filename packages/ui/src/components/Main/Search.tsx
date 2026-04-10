import {
  CheckIcon,
  ChevronDownIcon,
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
  Skeleton,
  Spinner,
  Text,
  TextField,
} from '@radix-ui/themes';
import { useQuery } from '@tanstack/react-query';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { getDownloaded } from '../../api/downloaded';
import { messages } from '../../constants/messages';
import {
  type SearchResultItem,
  useDownloaderStore,
} from '../../stores/downloaderStore';

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
  const response = await fetch('/api/v1/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ search_query: query }),
  });
  const data: SearchData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

const SearchResultSkeleton = () => (
  <Flex direction="column" gap="1">
    {[1, 2, 3].map((i) => (
      <Card size="1" key={i}>
        <Flex direction="row" gap="2" align="center">
          <Skeleton width="48px" height="48px" style={{ borderRadius: '50%' }} />
          <Flex direction="column" flexGrow="1" gap="1">
            <Skeleton height="16px" width="80%" />
            <Skeleton height="12px" width="50%" />
          </Flex>
          <Skeleton width="32px" height="32px" style={{ borderRadius: 'var(--radius-2)' }} />
        </Flex>
      </Card>
    ))}
  </Flex>
);

const SearchResultItemCard = ({
  item,
  url,
  isDownloaded,
  onSelect,
}: {
  item: SearchResultItem;
  url: string;
  isDownloaded: boolean;
  onSelect: (url: string) => void;
}) => {
  const isSelected = url.includes(item.id);

  return (
    <Card
      size="1"
      role="listitem"
      style={{
        transition: 'background-color 0.15s ease',
        ...(isSelected
          ? { backgroundColor: 'var(--accent-3)' }
          : {}),
      }}
    >
      <Flex direction="row" gap="2" align="center">
        <Popover.Root>
          <Popover.Trigger>
            <Avatar
              src={item.thumbnail}
              fallback={<VideoIcon />}
              size="4"
              style={{ cursor: 'pointer' }}
            />
          </Popover.Trigger>
          <Popover.Content>
            <img src={item.thumbnail} width={640} alt={item.title} />
          </Popover.Content>
        </Popover.Root>
        <Flex direction="column" flexGrow="1" gap="1">
          <Flex direction="row" align="center" gap="2">
            <Text
              weight="bold"
              size="2"
              style={{
                lineHeight: 1.3,
                cursor: 'pointer',
                textDecoration: 'none',
              }}
              onClick={() =>
                window.open(
                  `https://www.youtube.com/watch?v=${item.id}`,
                  '_blank',
                )
              }
              onMouseEnter={(e) =>
                (e.currentTarget.style.textDecoration = 'underline')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.textDecoration = 'none')
              }
            >
              {item.title}
            </Text>
            {isDownloaded && (
              <Badge color="green" size="1">
                <DownloadIcon width={10} height={10} />
                {messages.downloaded.badge}
              </Badge>
            )}
          </Flex>
          <Flex direction="row" gap="2" align="center">
            <Text size="1" color="gray">
              {item.artist}
            </Text>
            {item.duration && (
              <Flex align="center" gap="1">
                <Box
                  style={{
                    width: '3px',
                    height: '3px',
                    backgroundColor: 'var(--gray-8)',
                    borderRadius: '50%',
                  }}
                />
                <Text size="1" color="gray">
                  {item.duration}
                </Text>
              </Flex>
            )}
            {item.view_count && (
              <Flex
                align="center"
                gap="1"
                title={`${item.view_count} views`}
              >
                <Box
                  style={{
                    width: '3px',
                    height: '3px',
                    backgroundColor: 'var(--gray-8)',
                    borderRadius: '50%',
                  }}
                />
                <EyeOpenIcon
                  width={12}
                  height={12}
                  style={{ color: 'var(--gray-9)' }}
                />
                <Text size="1" color="gray">
                  {formatViewCount(item.view_count)}
                </Text>
              </Flex>
            )}
          </Flex>
        </Flex>
        <IconButton
          onClick={() =>
            onSelect(`https://www.youtube.com/watch?v=${item.id}`)
          }
          variant={isSelected ? 'soft' : 'outline'}
          aria-label={`Select ${item.title}`}
        >
          {isSelected && <CheckIcon />}
        </IconButton>
      </Flex>
    </Card>
  );
};

export const Search = () => {
  const phase = useDownloaderStore((s) => s.phase);
  const query = useDownloaderStore((s) => s.query);
  const searchResults = useDownloaderStore((s) => s.searchResults);
  const url = useDownloaderStore((s) => s.url);
  const setQuery = useDownloaderStore((s) => s.setQuery);
  const setSearching = useDownloaderStore((s) => s.setSearching);
  const setSearchResults = useDownloaderStore((s) => s.setSearchResults);
  const setUrl = useDownloaderStore((s) => s.setUrl);
  const reset = useDownloaderStore((s) => s.reset);

  const { refetch: search } = useQuery({
    queryKey: ['search', query],
    queryFn: () => postSearch(query),
    enabled: false,
  });

  const { data: downloadedFiles = [] } = useQuery({
    queryKey: ['downloaded'],
    queryFn: getDownloaded,
    staleTime: 0,
  });

  const doSearch = useCallback(async () => {
    setSearching();
    const { data } = await search();
    if (data) {
      setSearchResults(data);
    }
  }, [setSearching, search, setSearchResults]);

  const handleSearchFromFinished = useCallback(
    async (currentQuery: string) => {
      reset();
      setTimeout(async () => {
        setQuery(currentQuery);
        setSearching();
        try {
          const data = await postSearch(currentQuery);
          setSearchResults(data);
        } catch (error) {
          console.error('Search failed:', error);
        }
      }, 0);
    },
    [reset, setQuery, setSearching, setSearchResults],
  );

  const handleSearchClick = useCallback(async () => {
    if (phase === 'finished') {
      await handleSearchFromFinished(query);
    } else {
      await doSearch();
    }
  }, [phase, query, doSearch, handleSearchFromFinished]);

  const isOpened = useMemo(
    () => !!searchResults && !url,
    [searchResults, url],
  );
  const [detailsOpen, setDetailsOpen] = useState(false);
  const detailsRef = useRef<HTMLDetailsElement>(null);

  useEffect(() => {
    if (detailsRef.current) {
      detailsRef.current.open = isOpened;
      setDetailsOpen(isOpened);
    }
  }, [isOpened]);

  const isDownloaded = useCallback(
    (videoId: string) => {
      if (!Array.isArray(downloadedFiles)) return false;
      return downloadedFiles.some(
        (file: { info_dict: { id: string } }) => file.info_dict.id === videoId,
      );
    },
    [downloadedFiles],
  );

  const canInteract = phase === 'ready' || phase === 'finished';
  const isSearching = phase === 'searching';

  return (
    <Flex direction="column" gap="2">
      <Flex direction="row" gap="2" role="search">
        <Box flexGrow="1">
          <TextField.Root
            placeholder={messages.search.placeholder}
            disabled={!canInteract}
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
            onKeyDown={(event) => {
              if (
                event.key === 'Enter' &&
                query.length > 0 &&
                canInteract
              ) {
                handleSearchClick();
              }
            }}
            aria-label={messages.search.buttonLabel}
          >
            <TextField.Slot>
              <MagnifyingGlassIcon />
            </TextField.Slot>
          </TextField.Root>
        </Box>
        <IconButton
          disabled={query.length === 0 || !canInteract}
          onClick={handleSearchClick}
          aria-label={messages.search.buttonLabel}
          aria-busy={isSearching}
        >
          {isSearching ? <Spinner /> : <MagnifyingGlassIcon />}
        </IconButton>
        <IconButton
          variant="soft"
          onClick={reset}
          title={messages.common.reset}
          aria-label={messages.common.reset}
          disabled={
            phase === 'searching' ||
            phase === 'requesting' ||
            phase === 'downloading'
          }
        >
          <ResetIcon />
        </IconButton>
      </Flex>
      <details
        ref={detailsRef}
        open={isOpened}
        onToggle={(e) => setDetailsOpen(e.currentTarget.open)}
      >
        <summary style={{ padding: '8px 0' }}>
          <Flex direction="row" align="center" gap="2">
            <ChevronDownIcon
              width={16}
              height={16}
              style={{
                transform: detailsOpen ? 'rotate(0deg)' : 'rotate(-90deg)',
                transition: 'transform 0.2s ease',
              }}
            />
            <Text size="2" weight="medium" aria-live="polite">
              {messages.search.results(searchResults?.length ?? 0)}
            </Text>
          </Flex>
        </summary>
        <div
          style={{
            maxHeight: '400px',
            overflowY: 'auto',
            paddingRight: '4px',
          }}
        >
          {isSearching ? (
            <SearchResultSkeleton />
          ) : searchResults && searchResults.length === 0 ? (
            <Flex justify="center" py="4">
              <Text size="2" color="gray">
                {messages.search.noResults}
              </Text>
            </Flex>
          ) : (
            <Flex
              direction="column"
              gap="1"
              role="list"
              aria-label="Search results"
            >
              {searchResults?.map((item) => (
                <SearchResultItemCard
                  key={item.id}
                  item={item}
                  url={url}
                  isDownloaded={isDownloaded(item.id)}
                  onSelect={setUrl}
                />
              ))}
            </Flex>
          )}
        </div>
      </details>
    </Flex>
  );
};
