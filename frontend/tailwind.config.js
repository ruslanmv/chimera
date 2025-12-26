/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        chimera: {
          950: "#05050a",
          900: "#0a0a0f",
          800: "#12121a",
          700: "#1c1c2e",
          accent: "#7c3aed" 
        }
      }
    }
  },
  plugins: []
}
