import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        electric: {
          DEFAULT: "#2F8EFF",
          dark: "#1B5ED6"
        },
        background: {
          DEFAULT: "#0b0f1a",
          lighter: "#101624"
        }
      }
    }
  },
  plugins: []
};

export default config;
