/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          400: '#00c8f0',
          500: '#00aed6',
        },
        dark: {
          900: '#070710',
          800: '#0e0e1a',
          700: '#16162a',
          600: '#1e1e36',
          500: '#2a2a4a',
        },
      },
    },
  },
  plugins: [],
};
