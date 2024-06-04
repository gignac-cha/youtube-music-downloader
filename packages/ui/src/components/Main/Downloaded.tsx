import {
  DownloadIcon,
  PauseIcon,
  PlayIcon,
  ReloadIcon,
} from '@radix-ui/react-icons';
import {
  Badge,
  Box,
  Card,
  Flex,
  Heading,
  IconButton,
  Link,
  Spinner,
  Table,
} from '@radix-ui/themes';
import { useQueryClient, useSuspenseQuery } from '@tanstack/react-query';
import { Suspense, useCallback, useEffect, useRef, useState } from 'react';
import { convertFileSize } from '../../utilities/common';

type DownloadedData =
  | {
      error: false;
      data: {
        info_dict: {
          id: string;
          title: string;
        };
        total_bytes: number;
      }[];
    }
  | {
      error: true;
      message: string;
    };

const getDownloaded = async () => {
  const response = await fetch('/api/v1/downloaded');
  const data: DownloadedData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

const useAudio = (element: HTMLAudioElement) => {
  const [isPlaying, setPlaying] = useState(false);

  const play = useCallback(() => {
    element.play();
    setPlaying(!element.paused);
  }, [element]);
  const pause = useCallback(() => {
    element.pause();
    setPlaying(!element.paused);
  }, [element]);
  const toggle = useCallback(() => {
    if (!isPlaying) {
      play();
    } else {
      pause();
    }
  }, [element, isPlaying]);

  return { isPlaying, play, pause, toggle };
};

const AudioPlayer = ({ src }: { src: string }) => {
  const ref = useRef(new Audio(src));

  const { isPlaying, toggle } = useAudio(ref.current);

  useEffect(() => {
    ref.current.controls = true;
    ref.current.autoplay = false;
    ref.current.loop = false;
  }, []);

  return (
    <IconButton size={'1'} radius="full" onClick={toggle}>
      {isPlaying ? <PauseIcon /> : <PlayIcon />}
    </IconButton>
  );
};

const ListItem = ({
  id,
  title,
  total_bytes,
}: {
  id: string;
  title: string;
  total_bytes: number;
}) => {
  return (
    <Table.Row>
      <Table.Cell>
        <Flex direction={'row'} gap={'2'} align={'center'}>
          <Box flexGrow={'1'}>
            <Link href={`/download/${id}`} target="_blank">
              <DownloadIcon /> {title} [{id}].mp3
            </Link>
          </Box>
          <Badge>{convertFileSize(total_bytes)}</Badge>
          <AudioPlayer src={`/play/${id}`} />
        </Flex>
      </Table.Cell>
    </Table.Row>
  );
};

const List = () => {
  const { data = [] } = useSuspenseQuery({
    queryKey: ['downloaded'],
    queryFn: getDownloaded,
  });

  return (
    <Table.Root>
      <Table.Body>
        {data.map(({ info_dict: { id, title }, total_bytes }) => (
          <ListItem id={id} title={title} total_bytes={total_bytes} />
        ))}
      </Table.Body>
    </Table.Root>
  );
};

export const Downloaded = () => {
  const queryClient = useQueryClient();

  return (
    <Card>
      <Flex direction={'column'} gap={'4'}>
        <Flex direction={'row'} gap={'2'} justify={'between'}>
          <Heading>Downloaded List</Heading>
          <IconButton
            variant="ghost"
            onClick={() =>
              queryClient.invalidateQueries({ queryKey: ['downloaded'] })
            }
          >
            <ReloadIcon />
          </IconButton>
        </Flex>
        <Flex justify={'center'}>
          <Box flexGrow={'1'}>
            <Suspense fallback={<Spinner />}>
              <List />
            </Suspense>
          </Box>
        </Flex>
      </Flex>
    </Card>
  );
};
