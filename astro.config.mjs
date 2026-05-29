import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  site: "https://intro-shlok.github.io/AutoTest",
  base: "/AutoTest/",
  output: "static",
  integrations: [mdx()],
  markdown: {
    shikiConfig: {
      theme: "github-dark",
      wrap: true,
    },
    remarkPlugins: [],
  },
  build: {
    format: "directory",
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: undefined,
        },
      },
    },
    server: {
      watch: {
        ignored: [
          "**/networking_resources/**",
          "**/www-project-web-security-testing-guide/**",
          "**/offline_networking_library/**",
          "**/pcap_datasets/**",
          "**/settings/**",
          "**/node_modules/**",
          "**/dist/**",
          "**/.git/**",
        ],
      },
    },
  },
});