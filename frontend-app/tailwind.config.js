/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        plenergy: {
          blue: "#002D74",
          "blue-soft": "#E6EDF7",
          orange: "#FF8204",
          "orange-soft": "#FFF3E8",
          dark: "#1E282D",
          gray: "#69727D",
          "light-gray": "#F7F8FC",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}

