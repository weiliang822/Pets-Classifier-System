<template>
  <!--action换成要传给的url-->
  <el-upload
    class="upload"
    v-model:file-list="fileList"
    action="http://localhost:8000/user/pets_classify/"
    list-type="picture-card"
    :on-preview="handlePictureCardPreview"
    :on-success="handleUploadSuccess"
    :on-remove="handleRemove"
    accept="image/*"
  >
    <el-icon>
      <Plus />
    </el-icon>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full :src="dialogImageUrl" alt="" />
  </el-dialog>
</template>

<script>
import { ElNotification } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
// import type { UploadProps, UploadUserFile } from 'element-plus'

export default {
  name: "dashboard",
  data() {
    return {
      dialogImageUrl: "",
      dialogVisible: false,
      resForm: {
        pet_cls: "",
        probability: "",
      },
    };
  },
  methods: {
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      console.log(this.dialogImageUrl);
    },
    handleUploadSuccess(response, file, fileList) {
      console.log(response);
      this.resForm = response;
      ElNotification({
        title: "识别结果",
        message: `${this.resForm.probability}的可能是${this.resForm.pet_cls}`, //这里为什么不用.data?
        type: "success",
        duration: 0,
      });
    },
  },
};
</script>

<style scoped>
.upload {
  margin: 20px;
}
</style>