import { createRouter, createWebHashHistory } from "vue-router";
import store from "@/store";


import Error404View from "../views/Error404View.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
  },
  {
    path: "/explore-topics",
    name: "explore-topics",
    component: () => import("../views/ExploreTopicsView.vue"),
  },
  {
    path: "/posts/:slug(.*)-:id",
    name: "article",
    component: () => import("../views/ArticleView.vue"),
    props: true,
  },
  {
    path: "/search",
    name: "search",
    component: () => import("../views/SearchView.vue"),
    children: [
      {
        path: "",
        name: "search-posts",
        component: () => import("../views/SearchPostsView.vue"),
      },
      {
        path: "users",
        name: "search-users",
        component: () => import("../views/SearchUsersView.vue"),
      },
      {
        path: "tags",
        name: "search-tags",
        component: () => import("../views/SearchTagsView.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/profile/:id",
    name: "profile",
    component: () => import("../views/UserView.vue"),
  },
  {
    path: "/tag/:slug",
    name: "tag-detail",
    component: () => import("../views/TagDetailView.vue"),
  },
  {
    path: "/me",
    children: [
      {
        path: "stories",
        name: "my-stories",
        component: () => import("../views/UserStoriesView.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "following",
        name: "my-following",
        component: () => import("../views/UserFollowingView.vue"),
        meta: { requiresAuth: true },
        children: [
          {
            path: "suggestions",
            name: "my-suggestions",
            component: () => import("../views/UserSuggestionView.vue"),
          },
        ],
      },
    ],
    meta: { requiresAuth: true },
  },
  {
    path: "/crear-post",
    name: "create-post",
    component: () => import("../views/CreatePostView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/:catchAll(.*)",
    name: "error-404",
    component: Error404View,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

const redirectToLogin = (to, from, next) => {
  next("/login");
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
