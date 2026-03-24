// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 导入3个投票页面
import VoteA from '../views/VoteA.vue'
import VoteB from '../views/VoteB.vue'
import VoteC from '../views/VoteC.vue'

const routes = [
    { path: '/', redirect: '/a' }, // 默认打开A类票
    { path: '/a', component: VoteA }, // A类票面
    { path: '/b', component: VoteB }, // B类票面
    { path: '/c', component: VoteC }, // C类票面
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router