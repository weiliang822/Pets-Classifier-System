import axios from "axios";

// 创建 Axios 实例
const axiosInstance = axios.create({
    // baseURL: "http://localhost:8000", // 设置后端 API 的基本 URL
    withCredentials: true, // 允许发送跨域请求时携带 cookie
});

// 添加请求拦截器
axiosInstance.interceptors.request.use((config) => {
    config.headers["X-Requested-With"] = "XMLHttpRequest";
    const regex = /.*csrftoken=([^;.]*).*$/;
    config.headers["X-CSRFToken"] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    return config;
});

// 添加响应拦截器
axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosInstance;
