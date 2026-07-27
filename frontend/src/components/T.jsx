import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

export function T({ it, en }) {
  const { lang } = useLanguage();
  return <>{lang === 'it' ? it : en}</>;
}
