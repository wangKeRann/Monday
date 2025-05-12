import request from '@/js/request';

export const getUserInfo = () => {
    return request.get('/api/user/info');
};

export const updateUserInfo = (data) => {
    return request.put('/api/user/info', data);
};

export const logout = () => {
    return request.post('/api/user/logout');
}; 