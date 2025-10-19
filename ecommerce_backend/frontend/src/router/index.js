import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Main',
    // 🔹 Carga diferida (lazy load)
    component: () => import('../layouts/MainLayout.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
