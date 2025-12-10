/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#09090b",
                surface: "#18181b",
                primary: "#3b82f6",
                secondary: "#10b981",
                accent: "#f59e0b",
                danger: "#ef4444",
            },
        },
    },
    plugins: [],
}
