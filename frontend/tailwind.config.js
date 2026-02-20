/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: '#f5f5eb',
          dark: '#e8e8dd',
        },
        lime: {
          DEFAULT: '#c4ff0e',
          dark: '#a8dd0a',
        },
        'brand-black': '#000000',
        'brand-gray': {
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        'pill': '9999px',
      },
    },
  },
  plugins: [],
}
