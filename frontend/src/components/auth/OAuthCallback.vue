<template>
    <div class="oauth-callback">
        <div v-if="loading" class="loading">
            <div class="spinner"></div>
            <p>正在处理登录...</p>
        </div>
        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <button @click="retryLogin">重试</button>
        </div>
    </div>
</template>

<script>
import { handleGitHubCallback } from '@/api/oauth';
import { ROUTES } from '@/utils/config';
import '@/assets/styles/auth.css';

export default {
    name: 'OAuthCallback',
    data() {
        return {
            loading: true,
            error: null
        };
    },
    async created() {
        try {
            const code = new URLSearchParams(window.location.search).get('code');
            if (!code) {
                throw new Error('未收到授权码');
            }

            const response = await handleGitHubCallback(code);
            
            // 存储用户信息和 token
            localStorage.setItem('token', response.access_token);
            localStorage.setItem('user', JSON.stringify(response.user));

            // 跳转到首页
            this.$router.push(ROUTES.HOME);
        } catch (error) {
            this.error = error.message || '登录失败，请重试';
            this.loading = false;
        }
    },
    methods: {
        retryLogin() {
            this.$router.push(ROUTES.LOGIN);
        }
    }
};
</script> 