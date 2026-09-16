<template>
  <div class="app-container">
    <!-- 上面：查询和按钮 -->
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <el-form-item label="分类名称">
        <el-input v-model="query.search" placeholder="分类名称" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
      </el-form-item>
    </el-form>

    <!-- 中间：表格 -->
    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column label="操作" width="180" align="center">
        <template slot-scope="{ row }">
          <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      class="pager"
      background
      layout="total, prev, pager, next, sizes"
      :total="total"
      :page-size="query.page_size"
      :current-page="query.page"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />

    <!-- 弹窗：新增/编辑 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="400px">
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getCategoryList, createCategory, updateCategory, deleteCategory } from '@/api/library'

export default {
  name: 'BookCategory',
  data() {
    return {
      loading: false,
      list: [],
      total: 0,
      query: {
        search: '',
        page: 1,
        page_size: 10
      },
      dialogVisible: false,
      dialogTitle: '新增分类',
      form: {
        id: null,
        name: ''
      },
      rules: {
        name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      getCategoryList(this.query).then(res => {
        this.list = res.data.results
        this.total = res.data.count
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleSearch() {
      this.query.page = 1
      this.fetchData()
    },
    resetQuery() {
      this.query.search = ''
      this.handleSearch()
    },
    handlePageChange(page) {
      this.query.page = page
      this.fetchData()
    },
    handleSizeChange(size) {
      this.query.page_size = size
      this.query.page = 1
      this.fetchData()
    },
    handleAdd() {
      this.dialogTitle = '新增分类'
      this.form = { id: null, name: '' }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑分类'
      this.form = { id: row.id, name: row.name }
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        const req = this.form.id
          ? updateCategory(this.form.id, { name: this.form.name })
          : createCategory({ name: this.form.name })
        req.then(() => {
          this.$message.success('保存成功')
          this.dialogVisible = false
          this.fetchData()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除该分类吗？', '提示', { type: 'warning' }).then(() => {
        return deleteCategory(row.id)
      }).then(() => {
        this.$message.success('删除成功')
        this.fetchData()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.pager {
  margin-top: 16px;
  text-align: right;
}
</style>