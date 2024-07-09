import path from 'path'
import fs from 'fs'
export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'front',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico',
        href: '/fonts.googleapis.com/css?family=Anonymous+Pro',
        href: 'https://fonts.googleapis.com/css2?family=MuseoModerno:wght@200&display=swap',
      },
    ],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['~/styles/common.css'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ['~/plugins/liff-init.client.js', '~/plugins/common.js'],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/eslint-module',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/',
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  env: {
    LIFF_ID: process.env.LIFF_ID,
  },

  server: {
    port: 3000,
    host: "localhost",
    https: {
      key: fs.readFileSync(path.resolve(__dirname, "../localhost-key.pem")),
      cert: fs.readFileSync(path.resolve(__dirname, "../localhost.pem"))
    },
  },
}
