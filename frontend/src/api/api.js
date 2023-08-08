import axiosInstance from "./index.js";

const axios = axiosInstance;
const baseUrl = `http://localhost:8000`;

export const getUsers = () => {
    return axios.get(baseUrl + `/api/admini/user/`);
};

export const deleteUser = (userId) => {
    return axios.delete(baseUrl + `/api/admini/user/${userId}/`);
};

export const customUpdateUser = (userId, newData) => {
    console.log(userId);
    return axios.post(baseUrl + `/api/admini/user/${userId}/custom-update/`, newData);
};

export const getModels = () => {
    return axios.get(baseUrl + `/api/admini/model/`);
};

export const getModel = (modelId) => {
    return axios.get(baseUrl + `/api/admini/model/${modelId}/`);
};

export const deleteModel = (modelId) => {
    return axios.delete(baseUrl + `/api/admini/model/${modelId}/`);
};

export const updateModel = (modelId, newData, csrfToken) => {
    // 构建 FormData 对象
    const formData = new FormData();

    // 将每个上传的文件对象添加到 FormData
    newData.photos.forEach((file) => {
        formData.append("photos", file.raw);
    });
    console.log(formData);
    // 发送请求给后端
    return axios.patch(baseUrl + `/api/admini/model/${modelId}/`, formData, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "multipart/form-data",
        },
    });
};

export function createModel(data, csrfToken) {
    // 构建 FormData 对象
    const formData = new FormData();
    formData.append("name", data.name);

    // 将每个上传的文件对象添加到 FormData
    data.photos.forEach((file) => {
        formData.append("photos", file.raw);
    });
    console.log(formData);
    // 发送请求给后端
    return axios.post(baseUrl + "/api/admini/model/", formData, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "multipart/form-data",
        },
    });
}

export function uploadModel(data, csrfToken) {
    const formData = new FormData();
    formData.append("settingsFile", data.settingsFile[0].raw);
    formData.append("modelFile", data.modelFile[0].raw);
    console.log(formData);
    return axios.post(baseUrl + `/api/admini/upload-model/`, formData, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "multipart/form-data",
        },
    });
}

export function downloadModel() {
    return axios.get(baseUrl + `/api/admini/download-model/`);
}

export function deletePhoto(photoId) {
    return axios.delete(baseUrl + `/api/admini/photo/${photoId}/`);
}

export function postLogin(username, password, csrfToken) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    return axios.post(baseUrl + `/system/login/`, formData, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "multipart/form-data",
        },
    });
}

export function postSignup(data, csrfToken) {
    const formData = new FormData();
    formData.append("username", data.name);
    formData.append("password", data.password);
    formData.append("email", data.email);
    formData.append("repeat_password", data.repeat_password);
    return axios.post(baseUrl + `/system/signup/`, formData, {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "multipart/form-data",
        },
    });
}

export function downloadPhotos(data, csrfToken) {
    const formData = new FormData();
    formData.append("ids", data);
    console.log(typeof data);
    return axios.post(baseUrl + `/api/admini/download-photos/`, formData, {
        responseType: "blob",
        headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json; application/octet-stream" },
    });
}
