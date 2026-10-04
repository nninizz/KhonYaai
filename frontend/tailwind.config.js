/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f4f7ff',
          500: '#3855f4',
          700: '#2337a6',
        },
      },
    },
  },
  plugins: [],
};
