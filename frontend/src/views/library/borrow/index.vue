<template>
  <div class="app-container">
    <!-- ========== 1. 查询栏 ========== -->
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <!--     1.1 条件 -->
      <el-form-item label="读者">
        <el-input v-model="query.reader_name" placeholder="读者姓名" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item label="书名">
        <el-input v-model="query.book_name" placeholder="书名" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable placeholder="全部" style="width: 120px;">
          <el-option label="借出中" value="borrowed" />
          <el-option label="已还" value="returned" />
          <el-option label="已逾期" value="overdue" />
        </el-select>
      </el-form-item>
      <!--     1.2 按钮 -->
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="primary" icon="el-icon-plus" @click="handleBorrow">借书</el-button>
      </el-form-item>
    </el-form>

    <!-- ========== 2. 表格 ========== -->
    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="reader_name" label="读者" />
      <el-table-column prop="book_name" label="书名" />
      <el-table-column prop="borrow_date" label="借书日期" width="120" />
      <el-table-column prop="due_date" label="应还日期" width="120" />
      <el-table-column prop="return_date" label="还书日期" width="120" />
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="{ row }">
          <el-tag :type="statusType(row)" size="mini">{{ statusText(row) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" align="center">
        <template slot-scope="{ row }">
          <el-button v-if="!row.return_date" type="text" @click="handleReturn(row)">还书</el-button>
          <span v-else>-</span>
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

    <!-- ========== 4. 借书弹窗 ========== -->
    <el-dialog title="借书" :visible.sync="dialogVisible" width="420px">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="读者" prop="reader">
          <el-select v-model="form.reader" filterable placeholder="请选择读者" style="width: 100%;">
            <el-option
              v-for="item in readers"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="图书" prop="book">
          <el-select v-model="form.book" filterable placeholder="请选择图书" style="width: 100%;">
            <el-option
              v-for="item in books"
              :key="item.id"
              :label="item.name + '（剩余' + item.remaining + '）'"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBorrow">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getBorrowList, createBorrow, returnBorrow, getReaderList, getBookList } from '@/api/library'

export default {
  name: 'Borrow',
  data() {
    return {
      // ----- 列表 -----
      loading: false,
      list: [],
      total: 0,
      query: {
        reader_name: '',
        book_name: '',
        status: '',
        page: 1,
        page_size: 10
      },
      // ----- 下拉选项 -----
      readers: [],
      books: [],
      // ----- 借书弹窗 -----
      dialogVisible: false,
      form: { reader: null, book: null },
      rules: {
        reader: [{ required: true, message: '请选择读者', trigger: 'change' }],
        book: [{ required: true, message: '请选择图书', trigger: 'change' }]
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
      getBorrowList(this.query).then(res => {
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
      this.query.reader_name = ''
      this.query.book_name = ''
      this.query.status = ''
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
    // ----- 状态显示 -----
    statusText(row) {
      if (row.return_date) return '已还'
      if (row.due_date < this.today()) return '已逾期'
      return '借出中'
    },
    statusType(row) {
      if (row.return_date) return 'success'
      if (row.due_date < this.today()) return 'danger'
      return 'warning'
    },
    today() {
      const d = new Date()
      const m = (d.getMonth() + 1 < 10 ? '0' : '') + (d.getMonth() + 1)
      const day = (d.getDate() < 10 ? '0' : '') + d.getDate()
      return d.getFullYear() + '-' + m + '-' + day
    },
    // ----- 借书 -----
    handleBorrow() {
      this.form = { reader: null, book: null }
      this.dialogVisible = true
      getReaderList({ page_size: 100 }).then(res => {
        this.readers = res.data.results
      })
      getBookList({ page_size: 100 }).then(res => {
        this.books = res.data.results
      })
    },
    submitBorrow() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        createBorrow({ reader: this.form.reader, book: this.form.book }).then(() => {
          this.$message.success('借书成功')
          this.dialogVisible = false
          this.fetchData()
        })
      })
    },
    // ----- 还书 -----
    handleReturn(row) {
      this.$confirm('确认归还《' + row.book_name + '》吗？', '提示', { type: 'warning' }).then(() => {
        return returnBorrow(row.id)
      }).then(() => {
        this.$message.success('还书成功')
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