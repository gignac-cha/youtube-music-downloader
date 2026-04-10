import { ExclamationTriangleIcon } from '@radix-ui/react-icons';
import { Button, Callout, Flex } from '@radix-ui/themes';
import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <Callout.Root color="red" role="alert">
          <Callout.Icon>
            <ExclamationTriangleIcon />
          </Callout.Icon>
          <Callout.Text>
            <Flex direction="column" gap="2">
              <span>Something went wrong: {this.state.error?.message}</span>
              <Button
                size="1"
                variant="soft"
                color="red"
                onClick={() => this.setState({ hasError: false, error: null })}
                style={{ alignSelf: 'flex-start' }}
              >
                Retry
              </Button>
            </Flex>
          </Callout.Text>
        </Callout.Root>
      );
    }

    return this.props.children;
  }
}
