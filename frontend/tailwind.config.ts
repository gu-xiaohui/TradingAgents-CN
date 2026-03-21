import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // 深色主题背景
        dark: {
          bg: '#0f172a',
          surface: '#1e293b',
          border: '#334155',
        },
        // 浅色主题背景
        light: {
          bg: '#f8fafc',
          surface: '#ffffff',
          border: '#e2e8f0',
        },
        // 股票涨跌颜色
        stock: {
          up: '#ef4444',   // 涨-红色
          down: '#22c55e', // 跌-绿色
        },
        // 主题色
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
} satisfies Config
