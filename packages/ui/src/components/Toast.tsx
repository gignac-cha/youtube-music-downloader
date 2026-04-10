import { CheckCircledIcon, CrossCircledIcon, InfoCircledIcon } from '@radix-ui/react-icons';
import * as ToastPrimitive from '@radix-ui/react-toast';
import { Flex, Text } from '@radix-ui/themes';
import { createContext, useCallback, useContext, useState, type ReactNode } from 'react';

type ToastType = 'success' | 'error' | 'info';

interface ToastItem {
  id: number;
  type: ToastType;
  message: string;
}

interface ToastContextValue {
  showToast: (type: ToastType, message: string) => void;
}

const ToastContext = createContext<ToastContextValue>({
  showToast: () => {},
});

export const useToast = () => useContext(ToastContext);

let toastIdCounter = 0;

const ToastIcon = ({ type }: { type: ToastType }) => {
  switch (type) {
    case 'success':
      return <CheckCircledIcon width={16} height={16} style={{ color: 'var(--green-9)' }} />;
    case 'error':
      return <CrossCircledIcon width={16} height={16} style={{ color: 'var(--red-9)' }} />;
    case 'info':
      return <InfoCircledIcon width={16} height={16} style={{ color: 'var(--blue-9)' }} />;
  }
};

export const ToastProvider = ({ children }: { children: ReactNode }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const showToast = useCallback((type: ToastType, message: string) => {
    const id = ++toastIdCounter;
    setToasts((prev) => [...prev, { id, type, message }]);
  }, []);

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      <ToastPrimitive.Provider swipeDirection="right">
        {children}
        {toasts.map((toast) => (
          <ToastPrimitive.Root
            key={toast.id}
            open
            onOpenChange={(open) => {
              if (!open) removeToast(toast.id);
            }}
            duration={4000}
            style={{
              backgroundColor: 'var(--color-surface)',
              border: '1px solid var(--gray-6)',
              borderRadius: 'var(--radius-3)',
              padding: '12px 16px',
              boxShadow: 'var(--shadow-3)',
            }}
          >
            <Flex gap="2" align="center">
              <ToastIcon type={toast.type} />
              <ToastPrimitive.Description asChild>
                <Text size="2">{toast.message}</Text>
              </ToastPrimitive.Description>
            </Flex>
          </ToastPrimitive.Root>
        ))}
        <ToastPrimitive.Viewport
          style={{
            position: 'fixed',
            bottom: 16,
            right: 16,
            display: 'flex',
            flexDirection: 'column',
            gap: 8,
            width: 320,
            maxWidth: '100vw',
            zIndex: 9999,
            listStyle: 'none',
            padding: 0,
            margin: 0,
          }}
        />
      </ToastPrimitive.Provider>
    </ToastContext.Provider>
  );
};
