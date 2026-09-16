<template>
  <div class="app-container">
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <el-form-item label="书名">
        <el-input v-model="query.name" placeholder="书名" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="name" label="书名" />
      <el-table-column prop="author" label="作者" />
      <el-table-column prop="publisher" label="出版社" />
      <el-table-column prop="category_name" label="分类" />
      <el-table-column prop="inventory" label="库存" />
      <el-table-column prop="remaining" label="剩余" />
      <el-table-column label="操作" width="180" align="center">
        <template slot-scope="{ row }">
          <el-button type="text" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="480px">
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="书名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="出版社" prop="publisher">
          <el-input v-model="form.publisher" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
            <el-option
              v-for="item in categories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="库存" prop="inventory">
          <el-input-number v-model="form.inventory" :min="0" />
        </el-form-item>
        <el-form-item label="剩余" prop="remaining">
          <el-input-number v-model="form.remaining" :min="0" />
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
import { getBookList, createBook, updateBook, deleteBook, getCategoryList } from '@/api/library'

export default {
  name: 'Book',
  data() {
    return {
      loading: false,
      list: [],
      total: 0,
      categories: [],
      query: {
        name: '',
        page: 1,
        page_size: 10
      },
      dialogVisible: false,
      dialogTitle: '新增图书',
      form: {
        id: null,
        name: '',
        author: '',
        publisher: '',
        category: null,
        inventory: 0,
        remaining: 0
      },
      rules: {
        name: [{ required: true, message: '请输入书名', trigger: 'blur' }],
        author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
        category: [{ required: true, message: '请选择分类', trigger: 'change' }]
      }
    }
  },
  created() {
    this.fetchData()
    getCategoryList({ page_size: 100 }).then(res => {
      this.categories = res.data.results
    })
  },
  methods: {
    fetchData() {
      this.loading = true
      getBookList(this.query).then(res => {
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
    handleAdd() {
      this.dialogTitle = '新增图书'
      this.form = {
        id: null,
        name: '',
        author: '',
        publisher: '',
        category: null,
        inventory: 0,
        remaining: 0
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑图书'
      this.form = {
        id: row.id,
        name: row.name,
        author: row.author,
        publisher: row.publisher,
        category: row.category,
        inventory: row.inventory,
        remaining: row.remaining
      }
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        const data = {
          name: this.form.name,
          author: this.form.author,
          publisher: this.form.publisher,
          category: this.form.category,
          inventory: this.form.inventory,
          remaining: this.form.remaining
        }
        const req = this.form.id ? updateBook(this.form.id, data) : createBook(data)
        req.then(() => {
          this.$message.success('保存成功')
          this.dialogVisible = false
          this.fetchData()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除该图书吗？', '提示', { type: 'warning' }).then(() => {
        return deleteBook(row.id)
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