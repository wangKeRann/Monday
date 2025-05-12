<template>
    <div class="github-login">
        <button @click="handleLogin" class="github-button">
            <i class="fab fa-github"></i>
            使用 GitHub 登录
        </button>
    </div>
</template>

<script>
import { getGitHubAuthUrl } from '@/api/oauth';
import '@/assets/styles/auth.css';

export default {
    name: 'GitHubLogin',
    methods: {
        handleLogin() {
            window.location.href = getGitHubAuthUrl();
        }
    }
};
</script> 