import { Badge, Flex, Progress } from '@radix-ui/themes';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useCallback, useContext, useEffect, useMemo, useRef } from 'react';
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
  const { id, finish } = useContext(DownloaderContext);

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

  const taskRef = useRef<(() => void) | null>(null);
  
  const task = useCallback(async () => {
    const { data } = await getProgress();
    if (data) {
      if (data.status === 'finished') {
        taskRef.current?.(); // Stop the animation frame
        finish();

        // Invalidate queries to trigger automatic refetch
        await queryClient.invalidateQueries({ queryKey: ['downloaded'] });
      }
    }
    await timeout(1000 / 60);
  }, [id, getProgress, finish, queryClient]);

  const { start, stop } = useAnimationFrame(task);
  taskRef.current = stop;

  useEffect(() => {
    if (id) {
      start();
    }
    return () => stop();
  }, [id]);

  const progressValue = useMemo(
    () => {
      if (!progressData || !progressData.total_bytes || progressData.total_bytes === 0) {
        return null;  // indeterminate state
      }
      return progressData.downloaded_bytes / progressData.total_bytes;
    },
    [progressData],
  );

  // Don't render progress bar if there's no active download or if it's finished
  if (!id || progressData?.status === 'finished') {
    return null;
  }

  return (
    <Flex direction={'column'} gap={'2'}>
      <Progress value={progressValue ?? undefined} max={1} />
      {progressData && (
        <Flex direction={'row-reverse'} gap={'2'}>
          <Badge>{convertFileSize(progressData.speed)}/s</Badge>
          <Badge>{progressData.elapsed.toFixed(2)}s</Badge>
          {progressValue !== null && <Badge>{(progressValue * 100).toFixed(2)}%</Badge>}
        </Flex>
      )}
    </Flex>
  );
};
