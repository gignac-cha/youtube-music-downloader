import { Card, Container, Flex, Heading, Section } from '@radix-ui/themes';
import { Download } from './Download';
import { Downloaded } from './Downloaded';
import { DownloaderContextProvider } from './DownloaderContext';
import { DownloadProgress } from './DownloadProgress';
import { Search } from './Search';

export const Main = () => {
  return (
    <main>
      <Container size={'2'}>
        <Section>
          <Flex direction={'column'} gap={'4'}>
            <Card>
              <Flex direction={'column'} gap={'4'}>
                <Heading>YouTube Music Downloader</Heading>
                <DownloaderContextProvider>
                  <Search />
                  <Download />
                  <DownloadProgress />
                </DownloaderContextProvider>
              </Flex>
            </Card>
            <Downloaded />
          </Flex>
        </Section>
      </Container>
    </main>
  );
};
