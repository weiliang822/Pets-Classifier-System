<template>
  <router-view />
</template>

<style lang="less">
*,
*::after,
*::before {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  user-select: none;
}

@import "./assets/css/font.css";

#app {
  font-family: ezxq;
}
</style>

<!-- 看板娘 -->
<script>
export default {
  name: "App",
  /*看板娘初始化
参数说明
model 模型的配置
   json 文件资源路径，可以支持网络路径，此处使用的是相对路径
   scale 模型缩放系数
display 模型布局
   position 位置
   width 宽度
   height 高度
   hOffset 水平偏移量
   vOffset 垂直偏移量
mobile 移动端配置
   show 显示/隐藏
   scale 缩放比例
react 模型矩形框样式
   opacity 透明度
   opacityDefault 默认透明度
   opacityOnHover 鼠标悬浮透明度
*/
  mounted() {
    setTimeout(() => {
      window.L2Dwidget.init({
        pluginRootPath: "../public/live2dw/",
        pluginJsPath: "lib/",
        pluginModelPath: "live2d-widget-model-tororo/assets/", //中间这个haru_2就是人物,想换个人物,换这个就可以了
        tagMode: false,
        debug: false,
        model: {
          jsonPath:
            "/live2dw/live2d-widget-model-tororo/assets/tororo.model.json",
        },
        display: { position: "right", width: 300, height: 700 }, //调整大小,和位置
        mobile: { show: true }, //要不要盯着你的鼠标看
        log: false,
      });
    }, 1);
  },
};
</script>

