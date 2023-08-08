<template>
  <div class="table-container">
    <div class="bar">
      <div>
        <el-input
          class="search"
          v-model="searchQuery"
          placeholder="请输入用户名"
          clearable
          style="width: 200px; margin-bottom: 10px"
        ></el-input>
        <el-button type="primary" @click="searchUser" class="search-button"
          >搜索</el-button
        >
      </div>

      <el-button type="danger" @click="deleteSelectedMembers" class="delete"
        ><el-icon><Delete /></el-icon>删除选中</el-button
      >
    </div>
    <el-table
      @selection-change="handleSelectionChange"
      :data="currentPageData"
      style="width: 50%; display: flex; align-items: center"
    >
      <el-table-column size="small" type="selection"></el-table-column>
      <el-table-column label="邮箱" width="220">
        <template #default="scope">
          <div style="display: flex; align-items: center">
            <span style="margin-left: 10px">{{ scope.row.email }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="用户名" width="180">
        <template #default="scope">
          <el-popover
            effect="light"
            trigger="hover"
            placement="top"
            width="auto"
          >
            <template #default>
              <div>name: {{ scope.row.username }}</div>
              <div>superuser: {{ scope.row.is_superuser }}</div>
            </template>
            <template #reference>
              <el-tag>{{ scope.row.username }}</el-tag>
            </template>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
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
    <el-dialog v-model="dialogFormVisible" @close="handleCloseDialog">
      <span>Edit User</span>
      <el-form v-model="editingUser">
        <el-form-item label="User Name" :label-width="formLabelWidth">
          <el-input v-model="editedUserName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Super User" :label-width="formLabelWidth">
          <el-select
            v-model="editedUserSuper"
            placeholder="Please select an option"
          >
            <el-option label="Yes" value="true" />
            <el-option label="No" value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseDialog">Cancel</el-button>
          <el-button type="primary" @click="handleSaveEdit">Save</el-button>
        </span>
      </template>
    </el-dialog>
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="tableData.length"
    ></el-pagination>
  </div>
</template>


<script>
import { Delete, Edit } from "@element-plus/icons-vue";
import { getUsers, deleteUser, customUpdateUser } from "../../api/api.js";
import { ElNotification } from "element-plus";

export default {
  name: "UserList",
  data() {
    return {
      tableData: this.tableData,
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示的数量
      dialogFormVisible: false, // 对话框可见性
      editedUserName: "", // 编辑后的用户名
      editedUserSuper: "", // 编辑后的用户名
      editingUser: null, // 正在编辑的用户对象
      selectedMembers: [],
      searchQuery: "",
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
    handleEdit(index, row) {
      this.editingUser = row;
      this.editedUserName = row.username;
      this.editedUserSuper = row.is_superuser;
      this.dialogFormVisible = true;
    },

    handleCloseDialog() {
      this.dialogFormVisible = false;
      this.editedUserName = "";
      this.editedUserSuper = "";
      this.editingUser = null;
    },

    handleSaveEdit() {
      if (this.editingUser) {
        const updatedUser = {
          ...this.editingUser,
          username: this.editedUserName,
          is_superuser: this.editedUserSuper,
        };
        customUpdateUser(this.editingUser.id, updatedUser)
          .then(() => {
            // 更新成功后，刷新用户列表
            this.loadUsers();
            this.handleCloseDialog();
            ElNotification({
              title: "提示",
              message: "更新成功!",
              type: "success",
              duration: 3000,
            });
          })
          .catch((error) => {
            console.error("Error updating user:", error);
          });
      }
    },
    handleDelete(index, row) {
      const userId = row.id; // 假设用户对象中有一个 id 属性表示用户的唯一标识
      deleteUser(userId)
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
          ElNotification({
            title: "提示",
            message: "删除失败!",
            type: "error",
            duration: 3000,
          });
        });
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    fetchUsers() {
      getUsers()
        .then((response) => {
          this.tableData = response.data;
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    },

    loadUsers() {
      if (this.searchQuery) {
        this.searchUser();
      } else {
        this.fetchUsers();
      }
    },
    searchUser() {
      if (this.searchQuery.trim() === "") {
        this.resetSearch();
      } else {
        // 根据搜索关键字进行筛选
        const filteredUsers = this.tableData.filter((user) =>
          user.username.includes(this.searchQuery)
        );
        // 更新表格数据
        this.currentPage = 1;
        this.tableData = filteredUsers;
      }
    },
    resetSearch() {
      this.searchQuery = "";
      this.loadUsers();
    },
    handleSelectionChange(selectedRows) {
      this.selectedMembers = selectedRows;
    },
    deleteSelectedMembers() {
      for (const member of this.selectedMembers) {
        const userId = member.id; // 假设用户对象中有一个 id 属性表示用户的唯一标识
        deleteUser(userId)
          .then(() => {
            // 删除成功后更新表格数据
            const index = this.tableData.findIndex(
              (user) => user.id === userId
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
      if (this.selectedMembers.length === 0) {
        ElNotification({
          title: "提示",
          message: "未选中用户!",
          type: "error",
          duration: 3000,
        });
      }
      // 清空选中的成员列表
      this.selectedMembers = [];
    },
  },
  created: function () {
    this.tableData = [];
    this.loadUsers();
  },
};
</script>

<style>
.table-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: center;
}

.bar {
  width: 50%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.delete {
  /* margin-bottom: 2vh; */
  /* transform: translate(130%, 0%);
  right: 0; */
}

.search {
  /* transform: translate(-60%, 15%); */
}

.search-button {
  margin-left: 0.5vw;
  margin-bottom: 1.2vh;
}

.el-table {
  margin-bottom: 2vh;
}
</style>