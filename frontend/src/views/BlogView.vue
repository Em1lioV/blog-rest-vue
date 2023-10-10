<template>
    <div class="py-24 sm:py-25">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl ">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">From the blog</h2>
          <p class="mt-2 text-lg leading-8 text-gray-600">Learn how to grow your business with our expert advice.</p>
        </div>
        <div class="mx-auto  mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          <article v-for="post in posts" :key="post.id" class="flex max-w-xl flex-col items-start justify-between  border border-gray-200 rounded-lg shadow">
            <img :src="'http://127.0.0.1:8000' +  post.thumbnail " alt="" 
            class="max-h-48 w-full object-cover rounded-t-md ">
            <div class="flex items-center gap-x-4 text-xs pt-3 px-3">
              <time :datetime="post.published" class="text-gray-500">
                {{ new Date(post.published).toLocaleDateString("es-ES", {month: "short",day: "2-digit",year: "numeric"}) }}
                </time>
              <a class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">categori</a>
            </div>
            <div class="group relative p-3">
            <h3 class="mt-3  text-lg text-start font-semibold leading-6 text-gray-900 group-hover:text-gray-600">
                {{ post.title }} Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            </h3>
            <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">{{ post.content }}</p>
          </div>
            <div class=" text-start relative mt-8 flex items-center gap-x-4 pb-3 px-3">
              <img :src="'http://127.0.0.1:8000'  +  post.thumbnail " alt="" class="h-10 w-10 rounded-full bg-gray-50" />
              <div class="text-sm leading-6">
                <p class="font-semibold text-gray-900">
                  autor
                </p>
                <p class="text-gray-600">autor tag</p>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>

  import { getAPI } from '@/axios-api'

  export default {
    name: 'Blog',
    data () {
      return {
        posts: []
      }
    },
    created(){
        getAPI.get('/blog/posts/',)
            .then((response) => {
                this.posts = response.data
            }).catch((err) => {
                console.log(err);
            })
    }
  
  }
  </script>