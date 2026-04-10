import {
  ArrowDownIcon,
  CheckCircledIcon,
  CrossCircledIcon,
  UpdateIcon,
} from '@radix-ui/react-icons';
import { Badge, Flex, Progress, Text } from '@radix-ui/themes';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useMemo } from 'react';
import { messages } from '../../constants/messages';
import { useDownloaderStore } from '../../stores/downloaderStore';
import { useToast } from '../Toast';
import { convertFileSize } from '../../utilities/common';

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

const StatusIcon = ({ status }: { status: string }) => {
  switch (status) {
    case 'downloading':
      return <ArrowDownIcon width={14} height={14} />;
    case 'finished':
      return <CheckCircledIcon width={14} height={14} />;
    case 'error':
      return <CrossCircledIcon width={14} height={14} />;
    default:
      return <UpdateIcon width={14} height={14} />;
  }
};

export const DownloadProgress = () => {
  const downloadId = useDownloaderStore((s) => s.downloadId);
  const setFinished = useDownloaderStore((s) => s.setFinished);
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const { data: progressData } = useQuery({
    queryKey: ['info', downloadId],
    queryFn: () => getInfoID(downloadId!),
    enabled: !!downloadId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'finished' || data?.status === 'error') {
        return false;
      }
      return 1000;
    },
  });

  useEffect(() => {
    if (progressData?.status === 'finished') {
      setFinished();
      queryClient.invalidateQueries({ queryKey: ['downloaded'] });
      showToast('success', messages.download.complete);
    } else if (progressData?.status === 'error') {
      showToast('error', messages.download.error);
    }
  }, [progressData?.status, setFinished, queryClient, showToast]);

  const progressValue = useMemo(() => {
    if (
      !progressData ||
      !progressData.total_bytes ||
      progressData.total_bytes === 0
    ) {
      return null;
    }
    return progressData.downloaded_bytes / progressData.total_bytes;
  }, [progressData]);

  const eta = useMemo(() => {
    if (!progressData || !progressData.speed || progressData.speed <= 0)
      return null;
    const remainingBytes =
      progressData.total_bytes - progressData.downloaded_bytes;
    if (remainingBytes <= 0) return null;
    return remainingBytes / progressData.speed;
  }, [progressData]);

  if (!downloadId || progressData?.status === 'finished') {
    return null;
  }

  return (
    <Flex direction="column" gap="2" aria-live="polite" aria-busy="true">
      <Flex direction="row" align="center" gap="2">
        <StatusIcon status={progressData?.status ?? 'downloading'} />
        <Text size="2" weight="medium">
          {messages.download.progress}
        </Text>
        {eta !== null && (
          <Text size="1" color="gray">
            {messages.download.eta(eta)}
          </Text>
        )}
      </Flex>
      <Progress value={progressValue ?? undefined} max={1} />
      {progressData && (
        <Flex direction="row-reverse" gap="2">
          <Badge>{convertFileSize(progressData.speed)}/s</Badge>
          <Badge>{progressData.elapsed.toFixed(2)}s</Badge>
          {progressValue !== null && (
            <Badge>{(progressValue * 100).toFixed(2)}%</Badge>
          )}
        </Flex>
      )}
    </Flex>
  );
};
