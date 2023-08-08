<template>
  <div class="bgimage"></div>
  <el-container class="layout-container" style="height: 100vh">
    <el-aside width="250px">
      <el-row class="title">
        <el-avatar
          src="https://img.zcool.cn/community/019cd45c823360a80120af9a8d777c.jpg@2o.jpg"
          style="margin: 10px 2px 10px"
        />
        <span>宠物识别系统</span>
      </el-row>
      <el-menu :default-openeds="['1', '3']" :router="true">
        <el-menu-item index="/dashboard">
          <el-icon>
            <Reading />
          </el-icon>
          工作台
        </el-menu-item>
        <el-sub-menu v-if="isSuper" index="2">
          <template #title>
            <el-icon>
              <User />
            </el-icon>
            用户管理
          </template>
          <el-menu-item-group>
            <el-menu-item index="/user">用户列表</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>
        <el-sub-menu v-if="isSuper" index="3">
          <template #title>
            <el-icon>
              <Files />
            </el-icon>
            模型管理
          </template>
          <el-menu-item-group>
            <el-menu-item index="/model">模型列表</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <el-icon @click="fullscreen()" size="large" style="margin-right: 5px">
            <FullScreen />
          </el-icon>
          <el-dropdown>
            <span class="dropdown-link">
              <!-- <el-icon style="margin-right: 8px; margin-top: 1px" size="20">
                                <UserFilled />
                            </el-icon> -->
              <el-avatar
                src="https://i03piccdn.sogoucdn.com/61e4527afc58bf63"
                style="margin: 3px 2px 5px"
              />
              {{ username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :icon="UserFilled" @click="profile()"
                  >用户资料</el-dropdown-item
                >
                <el-dropdown-item :icon="Remove" @click="logout()"
                  >退出登录</el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <!-- <el-text>weiliang</el-text> -->
        </div>
      </el-header>
      <el-divider />
      <el-main>
        <router-view></router-view>
      </el-main>

      <el-footer class="footer">
        author:Tongji University 微凉 & 张博文
      </el-footer>
    </el-container>
  </el-container>
</template>

<script>
import { ref } from "vue";
import {
  Menu as IconMenu,
  Reading,
  Remove,
  FullScreen,
  UserFilled,
  User,
  Files,
} from "@element-plus/icons-vue";
import { ElAvatar, ElNotification } from "element-plus";
import screenfull from "screenfull";

export default {
  name: "userpage",
  data() {
    return {
      username: "", //应从后台获取
      UserFilled: UserFilled,
      FullScreen: FullScreen,
      Remove: Remove,
      Reading: Reading,
      User: User,
      Files: Files,
      isSuper: false,
      init: false,
    };
  },
  methods: {
    fullscreen() {
      if (!screenfull.isEnabled) {
        // 此时全屏不可用
        alert("此时全屏组件不可用");
        return;
      }
      //   如果可用 就可以全屏
      screenfull.toggle();
    },
    logout() {
      ElNotification({
        message: "您已退出登录",
        type: "warning",
      });
      this.$router.replace({ name: "login" });
    },
    profile() {},
    getRouterData() {
      this.username = this.$route.query.username;
      this.isSuper = this.$route.query.isSuper === "true" ? true : false;
      this.init = true;
    },
  },
  created: function () {
    if (this.init === false) this.getRouterData();
    console.log(this.isSuper);
  },
};
</script>

<style scoped>
.bgimage {
  background-image: url("../assets/images/VCG211250822095.jpg");
  background-size: cover;
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0.7;
}

.layout-container .el-header {
  position: relative;
  /* background-color: var(--el-color-primary-light-7); */
  color: var(--el-text-color-primary);
}

.layout-container .el-aside {
  color: var(--el-text-color-primary);
  /* color: black; */
  /* background: var(--el-color-primary-light-8); */
  /* background: linear-gradient(rgb(13, 250, 159), rgb(55, 172, 236)); */
}

.layout-container .el-aside .title {
  display: inline-flex;
  align-items: center;
  font-weight: bold;
}

.layout-container .el-menu {
  background: transparent;
  border-right: none;
}

.layout-container .el-main {
  padding: 0;
  /* background: transparent; */
  z-index: 1;
}

.toolbar {
  /* background: var(--el-color-primary-light-8); */
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
  width: 15%;
  opacity: 1;
}

.toolbar .dropdown-link {
  /* color: var(--el-color-primary); */
  display: flex;
  align-items: center;
}

.footer {
  display: inline-flex;
  align-items: center;
}
</style>
