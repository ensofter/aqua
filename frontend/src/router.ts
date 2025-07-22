import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Login from './components/Login.vue';
import Admin from './components/Admin.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    // Вложенные табы реализуем позже через внутренний роутинг или стейт
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router; 