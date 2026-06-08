import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f0fdff',
          100: '#ccf7fe',
          200: '#99edfd',
          300: '#4ddefa',
          400: '#00c8f0',
          500: '#00aed6',
          600: '#008bb4',
          700: '#006f92',
          800: '#005a77',
          900: '#004a64',
        },
        dark: {
          900: '#070710',
          800: '#0e0e1a',
          700: '#16162a',
          600: '#1e1e36',
          500: '#2a2a4a',
        },
      },
      fontFamily: {
        arabic: ['Cairo', 'Tajawal', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
