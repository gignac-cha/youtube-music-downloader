import '@radix-ui/themes/styles.css';
import { createElement } from 'react';
import { createRoot } from 'react-dom/client';
import { Root } from './components/Root';

const initializeRoot = () =>
  createRoot(
    document.querySelector('#root') ??
      document.body.appendChild(document.createElement('div')),
  ).render(createElement(Root));

window.addEventListener('load', () => {
  initializeRoot();
});
