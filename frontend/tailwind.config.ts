import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        rose: {
          50: '#fff1f2',
          100: '#ffe4e6',
          200: '#fecdd3',
          300: '#fda4af',
          400: '#fb7185',
          500: '#f43f5e',
          600: '#e11d48',
          700: '#be123c',
          800: '#9f1239',
          900: '#881337',
        },
        pink: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
        },
        brown: {
          50: '#fdf8f6',
          100: '#f2e8e5',
          200: '#eaddd7',
          300: '#e0cec7',
          400: '#d2bab0',
          500: '#bfa094',
          600: '#a18072',
          700: '#977669',
          800: '#846358',
          900: '#43302b',
        },
        cream: {
          50: '#fefdfb',
          100: '#fef9f5',
          200: '#fef3eb',
          300: '#fdeee1',
          400: '#fce8d7',
          500: '#fbe2cd',
          600: '#f9dcc3',
          700: '#f8d6b9',
          800: '#f7d0af',
          900: '#f5caa5',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-mesh': 'radial-gradient(at 40% 20%, rgba(251, 207, 232, 0.3) 0px, transparent 50%), radial-gradient(at 80% 0%, rgba(191, 160, 148, 0.3) 0px, transparent 50%), radial-gradient(at 0% 50%, rgba(254, 243, 235, 0.3) 0px, transparent 50%), radial-gradient(at 80% 50%, rgba(252, 231, 243, 0.3) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(251, 207, 232, 0.3) 0px, transparent 50%), radial-gradient(at 80% 100%, rgba(191, 160, 148, 0.3) 0px, transparent 50%), radial-gradient(at 0% 0%, rgba(254, 243, 235, 0.3) 0px, transparent 50%)',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.1))',
        'glass-gradient-hover': 'linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.2))',
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(251, 207, 232, 0.2)',
        'glass-lg': '0 12px 48px 0 rgba(251, 207, 232, 0.3)',
        'glass-xl': '0 20px 60px 0 rgba(251, 207, 232, 0.4)',
        'inner-glass': 'inset 0 2px 4px 0 rgba(255, 255, 255, 0.5)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'float-slow': 'float 8s ease-in-out infinite',
        'float-delayed': 'float 7s ease-in-out 1s infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 20s linear infinite',
        'spin-slower': 'spin 30s linear infinite',
        'gradient': 'gradient 8s ease infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-20px) rotate(5deg)' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        }
      }
    },
  },
  plugins: [],
}
export default config
