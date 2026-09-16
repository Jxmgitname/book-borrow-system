<template>
  <div class="app-container">
    <!-- ========== 1. 查询栏 ========== -->
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <!--     1.1 按姓名搜 -->
      <el-form-item label="姓名">
        <el-input v-model="query.name" placeholder="姓名" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <!--     1.2 按钮 -->
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
      </el-form-item>
    </el-form>

    <!-- ========== 2. 表格 ========== -->
    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" width="80" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="max_borrow" label="可借数量" width="110" />
      <el-table-column label="操作" width="180" align="center">
        <template slot-scope="{ row }">
          <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- ========== 3. 分页 ========== -->
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

    <!-- ========== 4. 新增/编辑弹窗 ========== -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="420px">
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="form.gender" style="width: 100%;">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="可借数量" prop="max_borrow">
          <el-input-number v-model="form.max_borrow" :min="1" />
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
import { getReaderList, createReader, updateReader, deleteReader } from '@/api/library'

export default {
  name: 'Reader',
  data() {
    return {
      // ----- 列表 -----
      loading: false,
      list: [],
      total: 0,
      query: { name: '', page: 1, page_size: 10 },
      // ----- 弹窗 -----
      dialogVisible: false,
      dialogTitle: '新增读者',
      form: { id: null, name: '', gender: '男', phone: '', max_borrow: 5 },
      rules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    // ----- 列表 -----
    fetchData() {
      this.loading = true
      getReaderList(this.query).then(res => {
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
      this.query.name = ''
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
    // ----- 弹窗 -----
    handleAdd() {
      this.dialogTitle = '新增读者'
      this.form = { id: null, name: '', gender: '男', phone: '', max_borrow: 5 }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑读者'
      this.form = {
        id: row.id,
        name: row.name,
        gender: row.gender,
        phone: row.phone,
        max_borrow: row.max_borrow
      }
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        const data = {
          name: this.form.name,
          gender: this.form.gender,
          phone: this.form.phone,
          max_borrow: this.form.max_borrow
        }
        const req = this.form.id ? updateReader(this.form.id, data) : createReader(data)
        req.then(() => {
          this.$message.success('保存成功')
          this.dialogVisible = false
          this.fetchData()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除该读者吗？', '提示', { type: 'warning' }).then(() => {
        return deleteReader(row.id)
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