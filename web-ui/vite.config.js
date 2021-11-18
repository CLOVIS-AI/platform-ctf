import {defineConfig} from "vite";

export default defineConfig({
    build: {
        rollupOptions: {
            input: "js/index.js",
            output: {
                chunkFileNames: "[name].js",
                assetFileNames: "[name][extname]",
                entryFileNames: "[name].js"
            },
            sourceMap: true,
        }
    }
})
