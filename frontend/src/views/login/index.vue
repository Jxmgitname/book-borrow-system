<template>
  <div class="login-page">
    <header class="login-header">
      <div class="login-header-inner">
        <div class="brand">
          <span class="brand-mark" />
          <span class="brand-name">图书借阅管理系统</span>
          <span class="brand-split" />
          <span class="brand-sub">后台登录</span>
        </div>
      </div>
    </header>

    <main class="login-main">
      <section class="panel">
        <div class="login-card">
          <h2 class="login-title">账号登录</h2>

          <el-form
            ref="loginForm"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            autocomplete="on"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="账号名"
                prefix-icon="el-icon-user"
                tabindex="1"
                @keyup.enter.native="handleLogin"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                :type="passwordType"
                placeholder="登录密码"
                prefix-icon="el-icon-lock"
                tabindex="2"
                @keyup.enter.native="handleLogin"
              >
                <i
                  slot="suffix"
                  class="el-input__icon el-icon-view password-eye"
                  @click="showPwd"
                />
              </el-input>
            </el-form-item>
            <el-button
              class="submit-btn"
              type="primary"
              :loading="loading"
              @click.native.prevent="handleLogin"
            >
              登录
            </el-button>
            <p class="tips">演示账号：admin1 / 123456</p>
          </el-form>
        </div>
      </section>
    </main>

    <footer class="login-footer">
      <p>© 2026 图书借阅管理系统</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value || !value.trim()) {
        callback(new Error('请输入账号名'))
      } else if (value.trim().length < 3) {
        callback(new Error('账号名不少于 3 位'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码不能少于 6 位'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: 'admin1',
        password: '123456'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password'
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/login', this.loginForm).then(() => {
          this.$router.push({ path: this.redirect || '/' })
          this.loading = false
        }).catch(() => {
          this.loading = false
        })
      })
    }
  }
}
</script>

<style lang="scss">
.login-page {
  .el-input__inner {
    height: 40px;
    line-height: 40px;
    border-radius: 4px;
    border-color: #d9d9d9;
  }

  .el-input__inner:focus {
    border-color: #3b82f6;
  }

  .el-form-item {
    margin-bottom: 18px;
  }

  .el-button--primary {
    background: #3b82f6;
    border-color: #3b82f6;
    border-radius: 4px;
    height: 40px;
    font-size: 16px;
    letter-spacing: 4px;
  }

  .el-button--primary:hover,
  .el-button--primary:focus {
    background: #60a5fa;
    border-color: #60a5fa;
  }
}
</style>

<style lang="scss" scoped>
$orange: #3b82f6;

.login-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(rgba(247, 248, 250, .55), rgba(247, 248, 250, .55)),
    url('~@/assets/login-bg.jpg') no-repeat center center;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

.login-header,
.login-main,
.login-footer {
  position: relative;
  z-index: 1;
}

.login-header {
  height: 50px;
  background: transparent;
}

.login-header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  color: #111;
}

.brand-mark {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  background: $orange;
  clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%);
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
}

.brand-split {
  width: 1px;
  height: 16px;
  background: #ddd;
  margin: 0 12px;
}

.brand-sub {
  font-size: 14px;
  color: #666;
}

.login-main {
  flex: 1;
  width: 100%;
  padding: 32px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel {
  width: 400px;
  flex-shrink: 0;
}

.login-card {
  width: 100%;
  background: #fff;
  padding: 28px 32px 32px;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(80, 90, 140, .12);
}

.login-title {
  margin: 0 0 28px;
  font-size: 20px;
  font-weight: 600;
  color: #111;
  text-align: center;
}

.submit-btn {
  width: 100%;
  margin-top: 6px;
}

.tips {
  margin: 16px 0 0;
  font-size: 12px;
  color: #999;
  line-height: 1.6;
}

.password-eye {
  cursor: pointer;
  color: #c0c4cc;
}

.login-footer {
  padding: 16px 24px 24px;
  text-align: center;
  color: #8a8fa3;
  font-size: 12px;
}

@media (max-width: 960px) {
  .login-main {
    padding-top: 24px;
  }

  .panel,
  .login-card {
    width: 100%;
    max-width: 400px;
  }
}
</style>
