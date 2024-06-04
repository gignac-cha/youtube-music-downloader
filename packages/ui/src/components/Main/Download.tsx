import { DownloadIcon, VideoIcon } from '@radix-ui/react-icons';
import { Box, Flex, IconButton, Spinner, TextField } from '@radix-ui/themes';
import { useMutation } from '@tanstack/react-query';
import { useCallback, useContext } from 'react';
import { DownloaderContext } from './DownloaderContext';

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
  const headers = {
    'Content-Type': 'application/json',
  };
  const response = await fetch('/api/v1/download', {
    method: 'POST',
    headers,
    body: JSON.stringify({ url }),
  });
  const data: RequestDownloadData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

export const Download = () => {
  const { state, updateURL, url, requestDownload, watchProgress, id } =
    useContext(DownloaderContext);

  const { mutateAsync: download } = useMutation({
    mutationKey: ['download', url],
    mutationFn: () => postDownload(url),
  });

  const onClick = useCallback(async () => {
    requestDownload();
    const { id } = await download();
    watchProgress(id);
  }, []);

  return (
    <Flex direction={'row'} gap={'4'}>
      <Box flexGrow={'1'}>
        <TextField.Root
          placeholder="Input YouTube URL here..."
          disabled={state !== 'ready'}
          onChange={(event) => updateURL(event.currentTarget.value)}
          defaultValue={url}
        >
          <TextField.Slot>
            <VideoIcon />
          </TextField.Slot>
        </TextField.Root>
      </Box>
      <IconButton
        disabled={url.length === 0 || state !== 'ready'}
        onClick={onClick}
      >
        {state === 'requesting' ? <Spinner /> : <DownloadIcon />}
      </IconButton>
    </Flex>
  );
};
