/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../templates/**/*.{html,js}'],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ['dracula'],
  },
  plugins: [require('daisyui')],
};
