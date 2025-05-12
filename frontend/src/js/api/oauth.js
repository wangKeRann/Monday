import request from '@/js/request';

export const githubCallback = (code) => {
    return request.post('/oauth/github', { code });
};

export const verifyToken = () => {
    return request.get('/api/user/verify');
}; 