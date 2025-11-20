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

export const getDownloaded = async () => {
  const response = await fetch('/api/v1/downloaded');
  const data: DownloadedData = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data.data;
};

type DeleteResponse =
  | {
      error: false;
      message: string;
      deleted_files: string[];
    }
  | {
      error: true;
      message: string;
    };

export const deleteDownloaded = async (id: string) => {
  const response = await fetch(`/api/v1/download/${id}`, {
    method: 'DELETE',
  });
  const data: DeleteResponse = await response.json();
  if (data.error) {
    throw new Error(data.message);
  }
  return data;
};