import {
  CheckIcon,
  MagnifyingGlassIcon,
  VideoIcon,
} from '@radix-ui/react-icons';
import {
  Avatar,
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
import { DownloaderContext } from './DownloaderContext';

type SearchData =
  | {
      error: false;
      data: {
        id: string;
        title: string;
        artist: string;
        thumbnail: string;
      }[];
    }
  | {
      error: true;
      message: string;
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
  } = useContext(DownloaderContext);

  const { refetch: search } = useQuery({
    queryKey: ['search', query],
    queryFn: () => postSearch(query),
    enabled: false,
  });

  const onClick = useCallback(async () => {
    requestSearch();
    const { data } = await search();
    if (data) {
      setList(data);
    }
  }, []);

  const isOpened = useMemo(() => !!list && !url, [list, url]);

  return (
    <Flex direction={'column'} gap={'2'}>
      <Flex direction={'row'} gap={'4'}>
        <Box flexGrow={'1'}>
          <TextField.Root
            placeholder="Input query here..."
            disabled={state !== 'ready'}
            onChange={(event) => updateQuery(event.currentTarget.value)}
            defaultValue={query}
          >
            <TextField.Slot>
              <MagnifyingGlassIcon />
            </TextField.Slot>
          </TextField.Root>
        </Box>
        <IconButton
          disabled={query.length === 0 || state !== 'ready'}
          onClick={onClick}
        >
          {state === 'searching' ? <Spinner /> : <MagnifyingGlassIcon />}
        </IconButton>
      </Flex>
      <details open={isOpened}>
        <summary>Search results ({list?.length ?? 0} results)</summary>
        <Flex direction={'column'} gap={'1'}>
          {list?.map(({ id, title, artist, thumbnail }) => (
            <Card size={'1'}>
              <Flex direction={'row'} gap={'2'} align={'center'}>
                <Popover.Root>
                  <Popover.Trigger>
                    <Avatar src={thumbnail} fallback={<VideoIcon />} />
                  </Popover.Trigger>
                  <Popover.Content>
                    <img src={thumbnail} width={640} />
                  </Popover.Content>
                </Popover.Root>
                <Flex direction={'column'} flexGrow={'1'}>
                  <Text weight={'bold'}>{title}</Text>
                  <Text>{artist}</Text>
                </Flex>
                <IconButton
                  onClick={() =>
                    updateURL(`https://www.youtube.com/watch?v=${id}`)
                  }
                  variant={url.includes(id) ? 'soft' : 'outline'}
                >
                  {url.includes(id) && <CheckIcon />}
                </IconButton>
              </Flex>
            </Card>
          ))}
        </Flex>
      </details>
    </Flex>
  );
};
