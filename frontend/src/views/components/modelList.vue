<template>
  <div class="table-container">
    <div class="button-bar">
      <el-button type="danger" @click="deleteSelectedMembers"
        ><el-icon><Delete /></el-icon>删除选中</el-button
      >
      <el-button @click="handleAddModel" type="primary"
        ><el-icon><Plus /></el-icon>添加模型</el-button
      >
      <el-button @click="handleUploadModel" type="success"
        ><el-icon><UploadFilled /></el-icon>上传模型配置</el-button
      >
      <el-button @click="downloadModel" type="info"
        ><el-icon><Download /></el-icon>下载配置文件</el-button
      >
      <el-button @click="downloadPhotos" type="warning"
        ><el-icon><Picture /></el-icon>下载选中图片集</el-button
      >
    </div>
    <el-table
      @selection-change="handleSelectionChange"
      :data="currentPageData"
      style="width: 50%; display: flex; align-items: center"
    >
      <el-table-column size="small" type="selection"></el-table-column>
      <el-table-column label="图片数" width="220">
        <template #default="scope">
          <div style="display: flex; align-items: center">
            <span style="margin-left: 10px">{{ scope.row.photoCount }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="名称" width="180">
        <template #default="scope">
          <el-popover
            effect="light"
            trigger="hover"
            placement="top"
            width="auto"
          >
            <template #default>
              <div>name: {{ scope.row.name }}</div>
            </template>
            <template #reference>
              <el-tag>{{ scope.row.name }}</el-tag>
            </template>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="routerTo(scope.row.id)"
            ><el-icon><Edit /></el-icon>编辑</el-button
          >
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            ><el-icon><Delete /></el-icon>删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="tableData.length"
    ></el-pagination>
    <el-dialog v-model="dialogFormVisible" title="Add Model">
      <el-form v-model="form">
        <el-form-item label="Model Name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>

        <el-form-item label="Upload Photos" :label-width="formLabelWidth">
          <el-upload
            v-model:file-list="fileList"
            :headers="{ 'X-CSRFToken': csrfToken }"
            :auto-upload="false"
            accept=".zip"
          >
            <template v-slot:trigger>
              <el-button>Select Photos</el-button>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitModel">Submit</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 上传模型文件 -->
    <el-dialog v-model="uploadModelVisible" title="Upload Model Settings">
      <el-form v-model="modelForm">
        <el-form-item label="settingFile" :label-width="formLabelWidth">
          <el-upload
            v-model:file-list="modelForm.settingsFile"
            :headers="{ 'X-CSRFToken': csrfToken }"
            :auto-upload="false"
          >
            <template v-slot:trigger>
              <el-button>settingsFile</el-button>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="modelFile" :label-width="formLabelWidth">
          <el-upload
            v-model:file-list="modelForm.modelFile"
            :headers="{ 'X-CSRFToken': csrfToken }"
            :auto-upload="false"
          >
            <template v-slot:trigger>
              <el-button>modelFile</el-button>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadModelVisible = false">Cancel</el-button>
          <el-button type="primary" @click="uploadModel">Submit</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>


<script>
import {
  Delete,
  Plus,
  UploadFilled,
  Download,
  Picture,
  Edit,
} from "@element-plus/icons-vue";
import {
  getModels,
  deleteModel,
  createModel,
  uploadModel,
  downloadModel,
  downloadPhotos,
} from "../../api/api.js";
import saveAs from "file-saver";
import { ElNotification } from "element-plus";

export default {
  name: "modelList",
  data() {
    return {
      tableData: this.tableData,
      currentPage: 1,
      pageSize: 10,
      dialogFormVisible: false,
      form: {
        name: "",
        photos: [],
      },
      formLabelWidth: "120px",
      csrfToken: "",
      fileList: [],
      uploadModelVisible: false,
      modelForm: {
        settingsFile: [],
        modelFile: [],
      },
      selectedMembers: [],
    };
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.tableData.slice(startIndex, endIndex);
    },
  },
  methods: {
    handleDelete(index, row) {
      const modelId = row.id; // 假设用户对象中有一个 id 属性表示用户的唯一标识
      deleteModel(modelId)
        .then(() => {
          // 删除成功后更新表格数据
          this.tableData.splice(index, 1);
          ElNotification({
            title: "提示",
            message: "删除成功!",
            type: "success",
            duration: 3000,
          });
        })
        .catch((error) => {
          console.error("Error deleting user:", error);
        });
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    loadModels() {
      getModels()
        .then((response) => {
          this.tableData = response.data;
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    },
    handleAddModel() {
      this.dialogFormVisible = true;
    },
    submitModel() {
      // 提交模型数据
      this.form.photos = this.fileList;
      if (this.form.name === "") {
        ElNotification({
          title: "提示",
          message: "请输入名称!",
          type: "error",
          duration: 3000,
        });
      } else if (this.fileList.length === 0) {
        ElNotification({
          title: "提示",
          message: "请选择文件!",
          type: "error",
          duration: 3000,
        });
      } else {
        createModel(this.form, this.csrfToken)
          .then(() => {
            this.dialogFormVisible = false;
            this.loadModels();
            this.fileList = [];
            ElNotification({
              title: "提示",
              message: "创建成功!",
              type: "success",
              duration: 3000,
            });
          })
          .catch((error) => {
            console.error("Error creating model:", error);
          });
      }
    },
    beforeUpload(file) {
      return false;
    },
    handleUploadSuccess(response, file, fileList) {
      // 处理上传成功的回调
      console.log(11);
      this.fileList.push({
        name: file.name,
        url: response.url,
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
    routerTo(id) {
      this.$router.push({
        name: `modelDetail`,
        query: {
          id: id,
        },
      });
    },
    uploadModel() {
      if (this.modelForm.settingsFile.length === 0) {
        ElNotification({
          title: "提示",
          message: "请选择配置文件!",
          type: "error",
          duration: 3000,
        });
      } else if (this.modelForm.modelFile.length === 0) {
        ElNotification({
          title: "提示",
          message: "请选择模型文件!",
          type: "error",
          duration: 3000,
        });
      } else {
        uploadModel(this.modelForm, this.csrfToken)
          .then(() => {
            this.uploadModelVisible = false;
            this.modelForm.settingsFile = [];
            this.modelForm.modelFile = [];
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
    downloadModel() {
      downloadModel()
        .then((response) => {
          const settingsFile = new File([response.data], "settings.py", {
            type: "text/plain",
          });
          saveAs(settingsFile, "settings.py");
          ElNotification({
            title: "提示",
            message: "下载成功!",
            type: "success",
            duration: 3000,
          });
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    handleUploadModel() {
      this.uploadModelVisible = true;
    },
    handleSelectionChange(selectedRows) {
      this.selectedMembers = selectedRows;
    },
    deleteSelectedMembers() {
      if (this.selectedMembers.length === 0) {
        ElNotification({
          title: "提示",
          message: "未选中模型!",
          type: "error",
          duration: 3000,
        });
      }
      for (const member of this.selectedMembers) {
        const modelId = member.id; // 假设用户对象中有一个 id 属性表示用户的唯一标识
        deleteModel(modelId)
          .then(() => {
            // 删除成功后更新表格数据
            const index = this.tableData.findIndex(
              (model) => model.id === modelId
            );
            if (index !== -1) {
              this.tableData.splice(index, 1);
            }
            ElNotification({
              title: "提示",
              message: "删除成功!",
              type: "success",
              duration: 3000,
            });
          })
          .catch((error) => {
            console.error("Error deleting user:", error);
          });
      }
      // 清空选中的成员列表
      this.selectedMembers = [];
    },
    downloadPhotos() {
      var ids = [];
      for (const member of this.selectedMembers) {
        ids.push(member.id);
      }
      if (ids.length !== 0) {
        downloadPhotos(ids, this.csrfToken)
          .then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "photos.zip");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            ElNotification({
              title: "提示",
              message: "下载成功!",
              type: "success",
              duration: 3000,
            });
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        ElNotification({
          title: "提示",
          message: "未选中模型!",
          type: "error",
          duration: 3000,
        });
      }
    },
  },
  created: function () {
    this.tableData = [];
    this.loadModels();
    // 获取CSRF Token
    this.csrfToken = this.getCSRFToken(); // 替换为获取CSRF Token的实际代码
  },
};
</script>

<style>
.table-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-bar {
  margin-bottom: 2vh;
}

.el-table {
  margin-bottom: 2vh;
}
</style>