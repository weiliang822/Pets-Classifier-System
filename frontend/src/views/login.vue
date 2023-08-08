<!-- 参考模板：https://codepen.io/ricardoolivaalonso/full/YzyaRPN -->
<!-- 参考教程：https://blog.csdn.net/Wind_AN/article/details/125539939 -->
<!-- 参考教程：https://blog.csdn.net/qq_41045128/article/details/125651144 -->
<template>
  <div class="body">
    <div class="main-box">
      <div :class="['container', 'container-register', { 'is-txl': isLogin }]">
        <form>
          <h2 class="title">注册</h2>
          <div class="form__icons">
            <img
              class="form__icon"
              src="@/assets/images/wechat.png"
              alt="微信登录"
            />
            <img
              class="form__icon"
              src="@/assets/images/alipay.png"
              alt="支付宝登录"
            />
            <img class="form__icon" src="@/assets/images/QQ.png" alt="QQ登录" />
          </div>
          <span class="text">或使用邮箱进行注册</span>
          <input
            class="form__input"
            type="text"
            placeholder="请输入用户名"
            v-model="registerForm.name"
          />
          <input
            class="form__input"
            type="text"
            placeholder="请输入邮箱"
            v-model="registerForm.email"
          />
          <input
            class="form__input"
            type="password"
            placeholder="请输入密码"
            v-model="registerForm.password"
          />
          <input
            class="form__input"
            type="password"
            placeholder="重复密码"
            v-model="registerForm.repeat_password"
          />
          <button class="form__button" @click="register">立即注册</button>
        </form>
      </div>
      <div
        :class="['container', 'container-login', { 'is-txl is-z200': isLogin }]"
      >
        <form>
          <h2 class="title">登录</h2>
          <div class="form__icons">
            <img
              class="form__icon"
              src="@/assets/images/wechat.png"
              alt="微信登录"
            />
            <img
              class="form__icon"
              src="@/assets/images/alipay.png"
              alt="支付宝登录"
            />
            <img class="form__icon" src="@/assets/images/QQ.png" alt="QQ登录" />
          </div>
          <span class="text">或使用用户名登录</span>
          <input
            class="form__input"
            type="text"
            placeholder="用户名"
            v-model="loginForm.name"
          />
          <input
            class="form__input"
            type="password"
            placeholder="请输入密码"
            v-model="loginForm.password"
          />
          <button class="form__button" @click="login">立即登录</button>
        </form>
      </div>
      <div :class="['switch', { login: isLogin }]">
        <div class="switch__circle"></div>
        <div class="switch__circle switch__circle_top"></div>
        <div class="switch__container">
          <h2>{{ isLogin ? "您好 !" : "欢迎回来 !" }}</h2>
          <p>
            {{
              isLogin
                ? "如果您还没有账号，请点击下方立即注册按钮进行账号注册"
                : "如果您已经注册过账号，请点击下方立即登录按钮进行登录"
            }}
          </p>
          <div class="form__button" @click="isLogin = !isLogin">
            {{ isLogin ? "立即注册" : "立即登录" }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { postLogin, postSignup } from "../api/api.js";
import { ElNotification } from "element-plus";

export default {
  name: "Login",
  data() {
    return {
      isLogin: true,
      loginForm: {
        name: "",
        password: "",
      },
      registerForm: {
        name: "",
        email: "",
        password: "",
        repeat_password: "",
      },
      csrfToken: "",
    };
  },
  methods: {
    login() {
      // post方法
      console.log(this.loginForm.name, this.loginForm.password);
      postLogin(this.loginForm.name, this.loginForm.password, this.csrfToken)
        .then((response) => {
          var res = response.data;
          console.log(res.msg);
          if (res.msg !== "管理员" && res.msg !== "普通用户") {
            ElNotification({
              message: res.msg,
              type: "warning",
            });
          } else {
            this.$router.push({
              name: "userpage",
              query: {
                username: this.loginForm.name,
                isSuper: res.msg === "管理员" ? true : false,
              },
            });
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    register() {
      console.log(this.registerForm);
      postSignup(this.registerForm, this.csrfToken)
        .then((response) => {
          var res = response.data;
          console.log(res);
          if (res.msg != "success") {
            ElNotification({
              message: res.msg,
              type: "warning",
            });
          } else {
            ElNotification({
              message: "注册成功，即将跳转登录页面",
              type: "success",
            });
            this.isLogin = !this.isLogin;
            //this.$router.replace();
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getCSRFToken() {
      const cookieName = "csrftoken";
      const cookie = document.cookie;
      if (cookie !== "") {
        const cookieValue = cookie
          .split(";")
          .find((cookie) => cookie.trim().startsWith(cookieName));
        if (cookieValue) {
          const value = cookieValue.split("=")[1];
          return value;
        }
      }

      return null;
    },
  },
  created: function () {
    this.csrfToken = this.getCSRFToken();
  },
};
</script>

<style lang="scss" scoped>
.body {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Montserrat", sans-serif;
  font-size: 12px;
  background-image: url("@/assets/images/background.jpg");
  color: #a0a5a8;
}

.main-box {
  position: relative;
  width: 1000px;
  min-width: 1000px;
  min-height: 600px;
  height: 600px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 1px 1px 100px 10px #ecf0f3;
  border-radius: 12px;
  overflow: hidden;

  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: all 1.25s;

    form {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 100%;
      height: 100%;
      color: #a0a5a8;

      .form__icon {
        object-fit: contain;
        width: 30px;
        margin: 0 5px;
        opacity: 0.5;
        transition: 0.15s;

        &:hover {
          opacity: 1;
          transition: 0.15s;
          cursor: pointer;
        }
      }

      .title {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }

      .text {
        margin-top: 30px;
        margin-bottom: 12px;
      }

      .form__input {
        width: 350px;
        height: 40px;
        margin: 4px 0;
        padding-left: 25px;
        font-size: 13px;
        letter-spacing: 0.15px;
        border: none;
        outline: none;
        // font-family: 'Montserrat', sans-serif;
        background-color: #ecf0f3;
        transition: 0.25s ease;
        border-radius: 8px;
        box-shadow: inset 2px 2px 4px #d1d9e6, inset -2px -2px 4px #f9f9f9;

        &::placeholder {
          color: #a0a5a8;
        }
      }
    }
  }

  .container-register {
    z-index: 100;
    left: calc(100% - 600px);
  }

  .container-login {
    left: calc(100% - 600px);
    z-index: 0;
  }

  .is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right;
  }

  .is-z200 {
    z-index: 200;
    transition: 1.25s;
  }

  .switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6, -4px -4px 10px #f9f9f9;
    color: #a0a5a8;

    .switch__circle {
      position: absolute;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      background-color: #ecf0f3;
      box-shadow: inset 8px 8px 12px #d1d9e6, inset -8px -8px 12px #f9f9f9;
      bottom: -60%;
      left: -60%;
      transition: 1.25s;
    }

    .switch__circle_top {
      top: -30%;
      left: 60%;
      width: 300px;
      height: 300px;
    }

    .switch__container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      position: absolute;
      width: 400px;
      padding: 50px 55px;
      transition: 1.25s;

      h2 {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }

      p {
        font-size: 14px;
        letter-spacing: 0.25px;
        text-align: center;
        line-height: 1.6;
      }
    }
  }

  .login {
    left: calc(100% - 400px);

    .switch__circle {
      left: 0;
    }
  }

  .form__button {
    width: 180px;
    height: 50px;
    border-radius: 25px;
    border: 0px solid rgba(255, 255, 255, 0.999);
    margin-top: 50px;
    text-align: center;
    line-height: 50px;
    font-size: 14px;
    letter-spacing: 2px;
    background-color: #4b70e2;
    color: #f9f9f9;
    cursor: pointer;
    box-shadow: 8px 8px 8px #d1d9e6, -8px -8px 8px #f9f9f9;

    &:hover {
      box-shadow: 2px 2px 3px 0 rgba(255, 255, 255, 50%),
        -2px -2px 3px 0 rgba(116, 125, 136, 50%),
        inset -2px -2px 3px 0 rgba(255, 255, 255, 20%),
        inset 2px 2px 3px 0 rgba(0, 0, 0, 30%);
    }
  }
}
</style>