/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        content: {
          50: "#e6f0fe",
          100: "#cee2fd",
          200: "#9cc4fc",
          300: "#6ba7fa",
          400: "#3989f9",
          500: "#086cf7",
          600: "#0656c6",
          700: "#054194",
          800: "#032b63",
          900: "#021631",
          950: "#010b19",
        },
        base: {
          50: "#ebebfa",
          100: "#d6d6f5",
          200: "#adadeb",
          300: "#8585e0",
          400: "#5c5cd6",
          500: "#3333cc",
          600: "#2929a3",
          700: "#1f1f7a",
          800: "#141452",
          900: "#0a0a29",
          950: "#050514",
        },
        primary: {
          50: "#e5e8ff",
          100: "#ccd0ff",
          200: "#99a2ff",
          300: "#6673ff",
          400: "#3344ff",
          500: "#0015ff",
          600: "#0011cc",
          700: "#000d99",
          800: "#000866",
          900: "#000433",
          950: "#00021a",
        },
        secondary: {
          50: "#eaf1fa",
          100: "#d6e3f5",
          200: "#adc8eb",
          300: "#84ace1",
          400: "#5b91d7",
          500: "#3275cd",
          600: "#285ea4",
          700: "#1e467b",
          800: "#142f52",
          900: "#0a1729",
          950: "#050c15",
        },
        accent: {
          50: "#fff7e5",
          100: "#ffeecc",
          200: "#ffdd99",
          300: "#ffcc66",
          400: "#ffbb33",
          500: "#ffaa00",
          600: "#cc8800",
          700: "#996600",
          800: "#664400",
          900: "#332200",
          950: "#1a1100",
        },
      },
    },
  },
  // daisyui: {
  //   themes: ["fantasy", "light"],
  //   // dracula,
  // },
  // daisyUI config (optional - here are the default values)
  daisyui: {
    themes: false, // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: "dark", // name of one of the included themes for dark mode
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
  darkMode: "class",
  plugins: [require("daisyui")],
  purge: [],
};
