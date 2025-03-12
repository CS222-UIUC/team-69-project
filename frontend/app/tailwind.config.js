/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'], // Ensures Tailwind scans your React files
  theme: {
    extend: {
      colors: {
        primary: '#0077b6', // Custom blue
        secondary: '#00b4d8', // Light blue
        accent: '#48cae4', // Cyan
        dark: '#023e8a', // Dark blue
        light: '#caf0f8', // Light cyan
      },
    },
  },
  plugins: [],
};
