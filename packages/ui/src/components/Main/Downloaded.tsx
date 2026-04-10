import {
  ArrowDownIcon,
  ArrowUpIcon,
  CheckIcon,
  Cross2Icon,
  DownloadIcon,
  ReloadIcon,
  TrashIcon,
} from '@radix-ui/react-icons';
import {
  Badge,
  Box,
  Button,
  Card,
  Flex,
  Heading,
  IconButton,
  Link,
  Spinner,
  Table,
  Text,
} from '@radix-ui/themes';
import { useQueryClient, useSuspenseQuery } from '@tanstack/react-query';
import { Suspense, useCallback, useMemo, useState } from 'react';
import { deleteDownloaded, getDownloaded } from '../../api/downloaded';
import { messages } from '../../constants/messages';
import { convertFileSize } from '../../utilities/common';
import { AudioPlayer } from './AudioPlayer';

type SortKey = 'title' | 'size';
type SortDirection = 'asc' | 'desc';

const ListItem = ({
  id,
  title,
  total_bytes,
}: {
  id: string;
  title: string;
  total_bytes: number;
}) => {
  const queryClient = useQueryClient();
  const [isDeleting, setIsDeleting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleDelete = () => {
    setIsDeleting(true);
  };

  const handleConfirm = async () => {
    setIsLoading(true);
    try {
      await deleteDownloaded(id);
      queryClient.invalidateQueries({ queryKey: ['downloaded'] });
    } catch (error) {
      console.error('Failed to delete:', error);
      setIsLoading(false);
    }
    setIsDeleting(false);
  };

  const handleCancel = () => {
    setIsDeleting(false);
  };

  return (
    <Table.Row>
      <Table.Cell>
        <Flex direction="row" gap="2" align="center">
          <Box flexGrow="1">
            <Link href={`/download/${id}`} target="_blank">
              <DownloadIcon /> {title} [{id}].mp3
            </Link>
          </Box>
          <Badge>{convertFileSize(total_bytes)}</Badge>
          <AudioPlayer src={`/play/${id}`} title={title} compact />

          {!isDeleting ? (
            <IconButton
              size="1"
              color="red"
              variant="soft"
              onClick={handleDelete}
              disabled={isLoading}
              aria-label={`${messages.common.delete}: ${title}`}
            >
              <TrashIcon />
            </IconButton>
          ) : (
            <Flex gap="1" role="alertdialog" aria-label={messages.downloaded.deleteConfirm}>
              <IconButton
                size="1"
                color="red"
                variant="solid"
                onClick={handleConfirm}
                disabled={isLoading}
                aria-label={messages.common.confirm}
              >
                <CheckIcon />
              </IconButton>
              <IconButton
                size="1"
                color="gray"
                variant="soft"
                onClick={handleCancel}
                disabled={isLoading}
                aria-label={messages.common.cancel}
              >
                <Cross2Icon />
              </IconButton>
            </Flex>
          )}
        </Flex>
      </Table.Cell>
    </Table.Row>
  );
};

const SortButton = ({
  label,
  sortKey,
  currentKey,
  direction,
  onClick,
}: {
  label: string;
  sortKey: SortKey;
  currentKey: SortKey;
  direction: SortDirection;
  onClick: (key: SortKey) => void;
}) => {
  const isActive = sortKey === currentKey;

  return (
    <Button
      size="1"
      variant={isActive ? 'soft' : 'ghost'}
      onClick={() => onClick(sortKey)}
      aria-label={`Sort by ${label}`}
    >
      {label}
      {isActive &&
        (direction === 'asc' ? (
          <ArrowUpIcon width={12} height={12} />
        ) : (
          <ArrowDownIcon width={12} height={12} />
        ))}
    </Button>
  );
};

const List = ({
  sortKey,
  sortDirection,
}: {
  sortKey: SortKey;
  sortDirection: SortDirection;
}) => {
  const { data = [] } = useSuspenseQuery({
    queryKey: ['downloaded'],
    queryFn: getDownloaded,
  });

  const sorted = useMemo(() => {
    const copy = [...data];
    copy.sort((a, b) => {
      let cmp = 0;
      if (sortKey === 'title') {
        cmp = a.info_dict.title.localeCompare(b.info_dict.title);
      } else if (sortKey === 'size') {
        cmp = a.total_bytes - b.total_bytes;
      }
      return sortDirection === 'asc' ? cmp : -cmp;
    });
    return copy;
  }, [data, sortKey, sortDirection]);

  if (sorted.length === 0) {
    return (
      <Flex justify="center" py="4">
        <Text size="2" color="gray">
          {messages.downloaded.empty}
        </Text>
      </Flex>
    );
  }

  return (
    <Table.Root>
      <Table.Body>
        {sorted.map(({ info_dict: { id, title }, total_bytes }) => (
          <ListItem key={id} id={id} title={title} total_bytes={total_bytes} />
        ))}
      </Table.Body>
    </Table.Root>
  );
};

export const Downloaded = () => {
  const queryClient = useQueryClient();
  const [sortKey, setSortKey] = useState<SortKey>('title');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  const handleSort = useCallback(
    (key: SortKey) => {
      if (key === sortKey) {
        setSortDirection((d) => (d === 'asc' ? 'desc' : 'asc'));
      } else {
        setSortKey(key);
        setSortDirection('asc');
      }
    },
    [sortKey],
  );

  return (
    <Card>
      <Flex direction="column" gap="4">
        <Flex direction="row" gap="2" justify="between" align="center">
          <Heading size="4">{messages.downloaded.title}</Heading>
          <Flex gap="2" align="center">
            <SortButton
              label={messages.downloaded.sortByTitle}
              sortKey="title"
              currentKey={sortKey}
              direction={sortDirection}
              onClick={handleSort}
            />
            <SortButton
              label={messages.downloaded.sortBySize}
              sortKey="size"
              currentKey={sortKey}
              direction={sortDirection}
              onClick={handleSort}
            />
            <IconButton
              variant="ghost"
              onClick={() =>
                queryClient.invalidateQueries({ queryKey: ['downloaded'] })
              }
              aria-label={messages.common.refresh}
            >
              <ReloadIcon />
            </IconButton>
          </Flex>
        </Flex>
        <Flex justify="center">
          <Box flexGrow="1">
            <Suspense fallback={<Spinner />}>
              <List sortKey={sortKey} sortDirection={sortDirection} />
            </Suspense>
          </Box>
        </Flex>
      </Flex>
    </Card>
  );
};
