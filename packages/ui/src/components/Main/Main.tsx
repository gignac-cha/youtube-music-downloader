import { Card, Container, Flex, Heading, Section } from '@radix-ui/themes';
import { messages } from '../../constants/messages';
import { Download } from './Download';
import { Downloaded } from './Downloaded';
import { DownloadProgress } from './DownloadProgress';
import { Search } from './Search';

export const Main = () => {
  return (
    <main style={{ flex: 1 }}>
      <Container size={'2'} px="4">
        <Section>
          <Flex direction={'column'} gap={'4'}>
            <Card>
              <Flex direction={'column'} gap={'4'}>
                <Heading size="5">{messages.app.title}</Heading>
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
