/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './pages/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#007AFF',
        secondary: '#66BB6A',
        background: '#2E1065',
        textTitle: '#111827',
        textLabel: '#6B7280'
      },
      borderRadius: {
        'xl': '1rem'
      },
      boxShadow: {
        card: '0 6px 20px rgba(0,0,0,0.06)'
      }
    }
  },
  plugins: []
}
