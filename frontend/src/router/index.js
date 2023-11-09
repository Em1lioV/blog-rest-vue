import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/blog',
    name: 'blog',
    component: () => import( '../views/BlogView.vue')
  }
  ,
  {
    path: '/login',
    name: 'login',
    component: () => import( '../views/LoginView.vue')
  }  ,
  {
    path: '/register',
    name: 'register',
    component: () => import( '../views/RegisterView.vue')
  }, {
    path: '/perfil', // Ruta para la vista de usuario
    name: 'perfil',
    component: () => import( '../views/UserView.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
