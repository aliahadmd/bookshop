/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  daisyui: {
    themes: ["light"],
  },
  plugins: [
    require('daisyui'),
  ],
}

