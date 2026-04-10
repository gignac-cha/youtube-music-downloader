import { GitHubLogoIcon } from '@radix-ui/react-icons';
import { Flex, IconButton, Text, Theme } from '@radix-ui/themes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import { messages } from '../constants/messages';
import { ErrorBoundary } from './ErrorBoundary';
import { Main } from './Main/Main';
import { ToastProvider } from './Toast';

const client = new QueryClient();

export const Root = () => {
  return (
    <StrictMode>
      <Theme appearance="dark">
        <QueryClientProvider client={client}>
          <ToastProvider>
            <Flex direction="column" style={{ minHeight: '100vh' }}>
              <header>
                <Flex
                  justify="between"
                  align="center"
                  px="4"
                  py="3"
                  style={{
                    borderBottom: '1px solid var(--gray-5)',
                  }}
                >
                  <Text size="3" weight="bold">
                    {messages.app.title}
                  </Text>
                  <Flex align="center" gap="2">
                    <Text size="1" color="gray">
                      {messages.app.version}
                    </Text>
                  </Flex>
                </Flex>
              </header>
              <ErrorBoundary>
                <Main />
              </ErrorBoundary>
              <footer>
                <Flex
                  justify="center"
                  align="center"
                  px="4"
                  py="3"
                  style={{
                    borderTop: '1px solid var(--gray-5)',
                    marginTop: 'auto',
                  }}
                >
                  <Text size="1" color="gray">
                    YouTube Music Downloader {messages.app.version}
                  </Text>
                </Flex>
              </footer>
            </Flex>
          </ToastProvider>
        </QueryClientProvider>
      </Theme>
    </StrictMode>
  );
};
