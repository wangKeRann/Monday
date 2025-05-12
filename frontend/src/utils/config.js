// API 配置
export const API_BASE_URL = 'http://localhost:8001';

// GitHub OAuth 配置
export const GITHUB_CONFIG = {
    clientId: 'Ov23li3GKMaVHuVeBVRY',
    redirectUri: 'http://localhost:8080/callback',
    scope: 'user:email'
};

// 路由配置
export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    CALLBACK: '/callback'
};