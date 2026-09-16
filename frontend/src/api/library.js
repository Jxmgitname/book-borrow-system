import request from '@/utils/request'

// 图书分类
  // 获取分类列表
export function getCategoryList(params) {
  return request({
    url: '/book-categories/',
    method: 'get',
    params
  })
}
  // 创建分类
export function createCategory(data) {
  return request({
    url: '/book-categories/',
    method: 'post',
    data
  })
}
  // 更新分类
export function updateCategory(id, data) {
  return request({
    url: '/book-categories/' + id + '/',
    method: 'put',
    data
  })
}
  // 删除分类
export function deleteCategory(id) {
  return request({
    url: '/book-categories/' + id + '/',
    method: 'delete'
  })
}

// 图书
    // 获取图书列表
export function getBookList(params) {
    return request({
      url: '/books/',
      method: 'get',
      params
    })
  }
    // 创建图书
  export function createBook(data) {
    return request({
      url: '/books/',
      method: 'post',
      data
    })
  }
  // 更新图书
  export function updateBook(id, data) {
    return request({
      url: '/books/' + id + '/',
      method: 'put',
      data
    })
  }
  // 删除图书
  export function deleteBook(id) {
    return request({
      url: '/books/' + id + '/',
      method: 'delete'
    })
  }

// =====================================================
// 读者
// =====================================================
  //   列表
export function getReaderList(params) {
    return request({
      url: '/readers/',
      method: 'get',
      params
    })
  }
  //   新增
  export function createReader(data) {
    return request({
      url: '/readers/',
      method: 'post',
      data
    })
  }
  //   修改
  export function updateReader(id, data) {
    return request({
      url: '/readers/' + id + '/',
      method: 'put',
      data
    })
  }
  //   删除
  export function deleteReader(id) {
    return request({
      url: '/readers/' + id + '/',
      method: 'delete'
    })
  }

// =====================================================
// 借还
// =====================================================
//   列表（可按读者、书名、状态筛选）
export function getBorrowList(params) {
    return request({
      url: '/borrows/',
      method: 'get',
      params
    })
  }
  //   借书
  export function createBorrow(data) {
    return request({
      url: '/borrows/',
      method: 'post',
      data
    })
  }
  //   还书（某一条记录）
  export function returnBorrow(id) {
    return request({
      url: '/borrows/' + id + '/return/',
      method: 'post'
    })
  }