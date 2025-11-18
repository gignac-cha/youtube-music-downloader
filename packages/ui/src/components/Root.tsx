import { Theme } from '@radix-ui/themes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import { Main } from './Main/Main';

const client = new QueryClient();

export const Root = () => {
  return (
    <StrictMode>
      <Theme appearance="dark">
        <QueryClientProvider client={client}>
          <header></header>
          <nav></nav>
          <Main />
          <footer></footer>
        </QueryClientProvider>
      </Theme>
    </StrictMode>
  );
};
