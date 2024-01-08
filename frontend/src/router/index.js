import { createRouter, createWebHashHistory } from 'vue-router'
import store from '@/store';

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
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
  },
  {
    path: '/search',
    name: 'search', 
    component: () => import( '../views/SearchView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import( '../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import( '../views/RegisterView.vue')
  },
  {
    path: '/perfil', 
    name: 'perfil',
    component: () => import( '../views/UserView.vue'),
    meta: { requiresAuth: true }
  }, 
  {
    path: '/crear-post',
    name: 'createPost',
    component: () => import( '../views/CreatePostView.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.access_token;
  console.log(isAuthenticated)

  // Verifica si la ruta requiere autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirige a la página de inicio de sesión si no está autenticado
    next('/login');
  } else {
    // Continúa con la navegación
    next();
  }
});


export default router
