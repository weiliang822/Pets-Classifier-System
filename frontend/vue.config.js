const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
    assetsDir: "static",
    transpileDependencies: true,
    pluginOptions: {
        "style-resources-loader": {
            preProcessor: "scss",
            patterns: [],
        },
    },
    // devServer: {
    //     // public: "http://100.80.170.235:9000",
    //     // proxy: "http://100.80.170.235:8000/",
    //     // port: 9000,
    // },
});
