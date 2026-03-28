// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 导入3个投票页面
import VoteA from '../views/VoteA.vue'
//import VoteB from '../views/VoteB.vue'
//import VoteC from '../views/VoteC.vue'
import Dept_PMT1 from "../views/Dept_PMT1.vue";
import Dept_PMT2 from "../views/Dept_PMT2.vue";
import Dept_PMT3 from "../views/Dept_PMT3.vue";
import Dept_PMT4 from "../views/Dept_PMT4.vue";
import Dept_PMT5 from "../views/Dept_PMT5.vue";
// import Dept_PMT6 from "../views/Dept_PMT6.vue";
import Dept_PMT7 from "../views/Dept_PMT7.vue";
import Dept_HSE from "../views/Dept_HSE.vue";
import Dept_bgs from "../views/Dept_bgs.vue";
import Dept_cg from "../views/Dept_cg.vue";
import Dept_cw from "../views/Dept_cw.vue";
import Dept_gc from "../views/Dept_gc.vue";
import Dept_jdy from "../views/Dept_jdy.vue";
import Dept_jw from "../views/Dept_jw.vue";
import Dept_kz from "../views/Dept_kz.vue";
import Dept_rl from "../views/Dept_rl.vue";
import Dept_sc from "../views/Dept_sc.vue";
import Dept_sj from "../views/Dept_sj.vue";
import Dept_zh from "../views/Dept_zh.vue";
import Dept_zl from "../views/Dept_zl.vue";
//import Dept_yja from "../views/yeji_A.vue";

const routes = [
    { path: '/', redirect: '/a' }, // 默认打开A类票
    { path: '/a', component: VoteA }, // A类票面
    //{ path: '/b', component: VoteB }, // B类票面
    //{ path: '/c', component: VoteC }, // C类票面
    { path: '/dept_PMT1', component: Dept_PMT1 },
    { path: '/dept_PMT2', component: Dept_PMT2 },
    { path: '/dept_PMT3', component: Dept_PMT3 },
    { path: '/dept_PMT4', component: Dept_PMT4 },
    { path: '/dept_PMT5', component: Dept_PMT5 },
    // { path: '/dept_PMT6', component: Dept_PMT6 },
    { path: '/dept_PMT7', component: Dept_PMT7 },
    { path: '/dept_HSE', component: Dept_HSE },
    { path: '/dept_bgs', component: Dept_bgs },
    { path: '/dept_cg', component: Dept_cg },
    { path: '/dept_cw', component: Dept_cw },
    { path: '/dept_gc', component: Dept_gc },
    { path: '/dept_jdy', component: Dept_jdy },
    { path: '/dept_jw', component: Dept_jw },
    { path: '/dept_kz', component: Dept_kz },
    { path: '/dept_rl', component: Dept_rl },
    { path: '/dept_sc', component: Dept_sc },
    { path: '/dept_sj', component: Dept_sj },
    { path: '/dept_zh', component: Dept_zh },
    { path: '/dept_zl', component: Dept_zl },
    //{ path: '/dept_yja', component: Dept_yja }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default createRouter({ history: createWebHistory(), routes })