<template>
  <div class="main">
    <h2>Photos:</h2>
    <div class="button-bar">
      <el-button @click="handleAddPhotos" type="primary" plain
        ><el-icon><Plus /></el-icon>添加照片</el-button
      >
      <el-button type="info" @click="toggleSelectMode" plain>
        <span v-if="isSelectMode"
          ><el-icon><CloseBold /></el-icon>取消选中</span
        >
        <span v-else
          ><el-icon><Select /></el-icon>选择删除</span
        >
        <!-- {{ isSelectMode ? "取消选中" : "选择删除" }} -->
      </el-button>
      <el-button
        type="danger"
        @click="deleteSelectedPhotos"
        :disabled="selectedPhotos.length === 0"
        plain
      >
        <el-icon><Delete /></el-icon>删除选中
      </el-button>
    </div>
    <div class="photo-wall">
      <div v-for="photo in paginatedPhotos" :key="photo.id" class="photo-item">
        <img
          :src="photo.image"
          alt="Photo"
          @click="handlePhotoClick(photo)"
          :class="{ selected: isSelected(photo) }"
        />
      </div>
    </div>
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="model.photoCount"
    ></el-pagination>

    <el-dialog v-model="modalVisible" width="70%">
      <img :src="modalImage" alt="Modal Photo" class="modal-image" />
      <template #footer>
        <el-button @click="modalVisible = false">Close</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="addPhotosFormVisible" title="Add Photos">
      <el-form v-model="form">
        <el-form-item label="Upload Photos" :label-width="formLabelWidth">
          <el-upload
            v-model:file-list="fileList"
            :headers="{ 'X-CSRFToken': csrfToken }"
            :auto-upload="false"
            :on-success="handleUploadSuccess"
            multiple
            list-type="picture"
            accept="image/*"
          >
            <template v-slot:trigger>
              <el-button>Select Photos</el-button>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addPhotosFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submit">Submit</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { getModel, updateModel, deletePhoto } from "../../api/api.js";
import { Delete, Plus, Select, CloseBold } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";

export default {
  data() {
    return {
      id: 0,
      model: {
        name: "",
        photoCount: 0,
        photos: [],
      },
      itemsPerPage: 5 * 6,
      pageSize: 5 * 6,
      currentPage: 1,
      modalVisible: false,
      addPhotosFormVisible: false,
      fileList: [],
      csrfToken: "",
      formLabelWidth: "120px",
      form: {
        photos: [],
      },
      selectedPhotos: [], // 选中的照片数组
      isSelectMode: false, // 是否处于选择模式
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.model.photos.length / this.itemsPerPage);
    },
    paginatedPhotos() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.model.photos.slice(startIndex, endIndex);
    },
  },
  methods: {
    getRouterData() {
      this.id = this.$route.query.id;
    },
    getModel() {
      getModel(this.id)
        .then((response) => {
          this.model = response.data;
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    },
    openModal(imageUrl) {
      this.modalVisible = true;
      this.modalImage = imageUrl;
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    handleAddPhotos() {
      this.addPhotosFormVisible = true;
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
    handleUploadSuccess(response, file, fileList) {
      console.log(11);
      this.fileList.push({
        name: file.name,
        url: response.url,
      });
    },
    submit() {
      this.form.photos = this.fileList;
      if (this.form.photos.length === 0) {
        ElNotification({
          title: "提示",
          message: "未选择图片!",
          type: "error",
          duration: 3000,
        });
      } else {
        updateModel(this.id, this.form, this.csrfToken)
          .then(() => {
            this.addPhotosFormVisible = false;
            this.getModel();
            this.fileList = [];
            ElNotification({
              title: "提示",
              message: "上传成功!",
              type: "success",
              duration: 3000,
            });
          })
          .catch((error) => {
            console.error("Error creating model:", error);
          });
      }
    },
    isSelected(photo) {
      return this.selectedPhotos.includes(photo);
    },
    toggleSelect(photo) {
      const index = this.selectedPhotos.indexOf(photo);
      if (index !== -1) {
        this.selectedPhotos.splice(index, 1);
      } else {
        this.selectedPhotos.push(photo);
      }
    },
    deleteSelectedPhotos() {
      for (const photo of this.selectedPhotos) {
        const photoId = photo.id;
        deletePhoto(photoId)
          .then(() => {
            const index = this.model.photos.findIndex((p) => p.id === photoId);
            if (index !== -1) {
              this.model.photos.splice(index, 1);
              this.model.photoCount -= 1;
            }
          })
          .catch((error) => {
            console.error("Error deleting photo:", error);
          });
      }
      this.selectedPhotos = [];
    },
    handlePhotoClick(photo) {
      if (!this.isSelectMode) {
        this.openModal(photo.image);
      } else {
        this.toggleSelect(photo);
      }
    },
    toggleSelectMode() {
      this.isSelectMode = !this.isSelectMode;
      this.selectedPhotos = [];
    },
  },
  created: function () {
    this.getRouterData();
    this.getModel();
    this.csrfToken = this.getCSRFToken();
  },
};
</script>

<style scoped>
.photo-wall {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.photo-item {
  width: 15%;
  padding: 10px;
  box-sizing: border-box;
}

.photo-item img {
  width: 100%;
  aspect-ratio: 1/1;
  object-fit: cover;
}

.photo-item img.selected {
  border: 2px solid red;
}

.photo-item button {
  margin-top: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 5px;
}

.el-dialog {
  max-height: 20vh;
}
.el-dialog img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-bar {
  transform: translate(-142%, 0);
}
</style>