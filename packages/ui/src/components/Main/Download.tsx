import { DownloadIcon, VideoIcon } from '@radix-ui/react-icons';
import { Box, Flex, IconButton, Spinner, TextField } from '@radix-ui/themes';
import { useMutation } from '@tanstack/react-query';
import { useCallback } from 'react';
import { messages } from '../../constants/messages';
import { useDownloaderStore } from '../../stores/downloaderStore';

type RequestDownloadData =
  | {
      error: false;
      data: {
        id: string;
      };
    }
  | {
      error: true;
      message: string;
    };

const postDownload = async (url: string) => {
  const response = await fetch('/api/v1/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  const data: RequestDownloadData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

export const Download = () => {
  const phase = useDownloaderStore((s) => s.phase);
  const url = useDownloaderStore((s) => s.url);
  const setUrl = useDownloaderStore((s) => s.setUrl);
  const setRequesting = useDownloaderStore((s) => s.setRequesting);
  const setDownloading = useDownloaderStore((s) => s.setDownloading);

  const { mutateAsync: download } = useMutation({
    mutationKey: ['download', url],
    mutationFn: () => postDownload(url),
  });

  const onClick = useCallback(async () => {
    setRequesting();
    const { id } = await download();
    setDownloading(id);
  }, [setRequesting, download, setDownloading]);

  return (
    <Flex direction="row" gap="4">
      <Box flexGrow="1">
        <TextField.Root
          placeholder={messages.download.placeholder}
          disabled={phase !== 'ready'}
          onChange={(event) => setUrl(event.currentTarget.value)}
          defaultValue={url}
          aria-label={messages.download.placeholder}
        >
          <TextField.Slot>
            <VideoIcon />
          </TextField.Slot>
        </TextField.Root>
      </Box>
      <IconButton
        disabled={url.length === 0 || phase !== 'ready'}
        onClick={onClick}
        aria-label={messages.download.buttonLabel}
        aria-busy={phase === 'requesting'}
      >
        {phase === 'requesting' ? <Spinner /> : <DownloadIcon />}
      </IconButton>
    </Flex>
  );
};
