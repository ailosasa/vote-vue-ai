// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 导入3个投票页面
import VoteA from '../views/VoteA.vue'
import VoteB from '../views/VoteB.vue'
import VoteC from '../views/VoteC.vue'
import Dept_PMT1 from "../views/Dept_PMT1.vue";
import Dept_PMT2 from "../views/Dept_PMT2.vue";
import Dept_PMT3 from "../views/Dept_PMT3.vue";
import Dept_PMT4 from "../views/Dept_PMT4.vue";
import Dept_PMT5 from "../views/Dept_PMT5.vue";
import Dept_PMT6 from "../views/Dept_PMT6.vue";
import Dept_PMT7 from "../views/Dept_PMT7.vue";
import Dept_bgs from "../views/Dept_bgs.vue";

const routes = [
    { path: '/', redirect: '/a' }, // 默认打开A类票
    { path: '/a', component: VoteA }, // A类票面
    { path: '/b', component: VoteB }, // B类票面
    { path: '/c', component: VoteC }, // C类票面
    { path: '/dept_PMT1', component: Dept_PMT1 },
    { path: '/dept_PMT2', component: Dept_PMT2 },
    { path: '/dept_PMT3', component: Dept_PMT3 },
    { path: '/dept_PMT4', component: Dept_PMT4 },
    { path: '/dept_PMT5', component: Dept_PMT5 },
    { path: '/dept_PMT6', component: Dept_PMT6 },
    { path: '/dept_PMT7', component: Dept_PMT7 },
    { path: '/dept_bgs', component: Dept_bgs }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default createRouter({ history: createWebHistory(), routes })