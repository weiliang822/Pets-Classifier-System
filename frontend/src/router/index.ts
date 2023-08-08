import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router'


const routes = [
    {
        path: '/',
        name: 'login',
        component: () => import('@/views/login.vue')
    },
    {
        path: '/userpage',
        name: 'userpage',
        component: () => import('@/views/userpage.vue'),

        children:[
            {
                path: '/dashboard',
                name: 'dashboard',
                component: () => import('@/views/components/dashboard.vue'),
            },
            {
                path: "/model",
                name: "model",
                component: () => import("@/views/components/modelList.vue"),
            },
            {
                path: "/modeldetail",
                name: "modelDetail",
                component: () => import("@/views/components/modelDetail.vue"),
            },
            {
                path: "/user",
                name: "user",
                component: () => import("@/views/components/userList.vue"),
            },
        ]
    },
    // {
    //     path: '/userpage/dashboard',
    //     name: 'dashboard',
    //     component: () => import('@/views/components/dashboard.vue'),
    // },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})


export default router
