/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './404.html',
    './src/template.html',
    './src/build.py',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      colors: {
        ink: {
          950: '#06080b',
          900: '#0a0d12',
          850: '#0d1117',
          800: '#121720',
          700: '#1a212c',
        },
        accent: {
          DEFAULT: '#34d399',
          deep: '#10b981',
          soft: 'rgba(52,211,153,0.10)',
          line: 'rgba(52,211,153,0.32)',
        },
      },
    },
  },
  plugins: [],
};
