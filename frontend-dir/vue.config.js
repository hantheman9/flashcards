module.exports = {
  devServer: {
    proxy: 'https://be-static-ip-service-uhrgp63gla-uc.a.run.app/',
    /*
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://backend:5000/'
      }
    }*/
    // https://github.com/vuejs/vue-cli/issues/4557
    progress: false,
  },
}
