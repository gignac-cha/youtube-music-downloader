import { Card, Container, Flex, Section } from '@radix-ui/themes';
import { Download } from './Download';
import { Downloaded } from './Downloaded';
import { DownloadProgress } from './DownloadProgress';
import { Search } from './Search';

export const Main = () => {
  return (
    <main style={{ flex: 1 }}>
      <Container size={'2'} px="0">
        <Section py="4">
          <Flex direction={'column'} gap={'4'}>
            <Card>
              <Flex direction={'column'} gap={'4'}>
                <Search />
                <Download />
                <DownloadProgress />
              </Flex>
            </Card>
            <Downloaded />
          </Flex>
        </Section>
      </Container>
    </main>
  );
};
