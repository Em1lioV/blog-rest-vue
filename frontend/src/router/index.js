import { createRouter, createWebHashHistory } from 'vue-router'
import store, { emitter } from '@/store';

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
    path: '/post/:slug',
    name: 'article',
    component: () => import( '../views/ArticleView.vue'),
    props: true,
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

const redirectToLogin = (to, from, next) => {
  next('/login');
};

router.beforeEach(async (to, from, next) => {
  if (!to.meta.requiresAuth) {
    return next();
  }
  const accessToken = store.getters.accessToken;

  if (!accessToken) {
    return redirectToLogin(to, from, next);
  }
  next();
});

export default router;