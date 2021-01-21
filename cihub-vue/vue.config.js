module.exports = {
  configureWebpack: {
    devServer: {
      clientLogLevel: 'debug',
      proxy: {
        '/api': {
          target: 'https://ci.whq.gocept.com/api',
          changeOrigin: true,
          pathRewrite: {'^/api' : ''},
        }
      },
    },
  }
}
