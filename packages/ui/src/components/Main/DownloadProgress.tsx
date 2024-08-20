import { Badge, Flex, Progress } from '@radix-ui/themes';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useCallback, useContext, useEffect, useMemo } from 'react';
import { useAnimationFrame } from '../../hooks/useAnimationFrame';
import { convertFileSize } from '../../utilities/common';
import { timeout } from '../../utilities/timeout';
import { DownloaderContext } from './DownloaderContext';

type DownloadProgressData =
  | {
      error: false;
      data: {
        status: 'downloading' | 'finished' | 'error';
        info_dict: {
          id: string;
        };
        downloaded_bytes: number;
        total_bytes: number;
        speed: number;
        elapsed: number;
      };
    }
  | {
      error: true;
      message: string;
    };

const getInfoID = async (id: string) => {
  const response = await fetch(`/api/v1/info/${id}`);
  const data: DownloadProgressData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

export const DownloadProgress = () => {
  const { id } = useContext(DownloaderContext);

  const { data: progressData, refetch: getProgress } = useQuery({
    queryKey: ['info', id],
    queryFn: () => {
      if (id) {
        return getInfoID(id);
      }
    },
    enabled: false,
  });

  const queryClient = useQueryClient();

  const task = useCallback(async () => {
    const { data } = await getProgress();
    if (data) {
      if (data.status === 'finished') {
        stop();
        await queryClient.invalidateQueries({ queryKey: ['downloaded'] });
      }
    }
    await timeout(1000 / 60);
  }, [id]);

  const { start, stop } = useAnimationFrame(task);

  useEffect(() => {
    if (id) {
      start();
    }
    return () => stop();
  }, [id]);

  const progressValue = useMemo(
    () =>
      progressData
        ? progressData.downloaded_bytes / progressData.total_bytes
        : 0,
    [progressData],
  );

  return (
    <Flex direction={'column'} gap={'2'}>
      <Progress value={progressValue} max={1} />
      {progressData && (
        <Flex direction={'row-reverse'} gap={'2'}>
          <Badge>{convertFileSize(progressData.speed)}/s</Badge>
          <Badge>{progressData.elapsed.toFixed(2)}s</Badge>
          <Badge>{(progressValue * 100).toFixed(2)}%</Badge>
        </Flex>
      )}
    </Flex>
  );
};
