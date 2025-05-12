import request from './request';
import { GITHUB_CONFIG } from '../utils/config';

// GitHub OAuth 相关函数
export const getGitHubAuthUrl = () => {
    const { clientId, redirectUri, scope } = GITHUB_CONFIG;
    return `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
};

export const handleGitHubCallback = async (code) => {
    try {
        const response = await request.post('/api/auth/github/callback', { code });
        return response;
    } catch (error) {
        console.error('GitHub 回调处理失败:', error);
        throw new Error(error.response?.data?.message || 'GitHub 认证失败');
    }
}; 