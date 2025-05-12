import { createRouter, createWebHistory } from 'vue-router'
import GitHubLogin from '@/components/auth/GitHubLogin.vue'
import OAuthCallback from '@/components/auth/OAuthCallback.vue'
import { ROUTES } from '@/utils/config'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: GitHubLogin
    },
    {
        path: '/callback',
        name: 'Callback',
        component: OAuthCallback
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router