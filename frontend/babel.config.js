module.exports = {
  presets: [
    // https://github.com/vuejs/vue-cli/tree/master/packages/@vue/babel-preset-app
    '@vue/cli-plugin-babel/preset'
  ],
  'env': {
    'development': {
      // 开发环境把 import() 转成 require()，加快热更新
      'plugins': ['dynamic-import-node']
    }
  }
}
