import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    redirect: '/library/category',
    hidden: true
  },
  {
    path: '/library',
    component: Layout,
    redirect: '/library/category',
    name: 'Library',
    meta: { title: '图书管理', icon: 'el-icon-reading' },
    children: [
      {
        path: 'category',
        name: 'BookCategory',
        component: () => import('@/views/library/category/index'),
        meta: { title: '图书分类', icon: 'el-icon-menu' }
      },
      {
        path: 'book',
        name: 'Book',
        component: () => import('@/views/library/book/index'),
        meta: { title: '图书列表', icon: 'el-icon-document' }
      },
      {
        path: 'reader',
        name: 'Reader',
        component: () => import('@/views/library/reader/index'),
        meta: { title: '读者管理', icon: 'el-icon-user' }
      },
      {
        path: 'borrow',
        name: 'Borrow',
        component: () => import('@/views/library/borrow/index'),
        meta: { title: '借还管理', icon: 'el-icon-tickets' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router
