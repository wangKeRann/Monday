import axios from 'axios';

export const handleReportDetail = async (recordId) => {
    try {
        const response = await axios.get(`http://localhost:8001/api/health/detail/${recordId}`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.data.code === 200) {
            return {
                success: true,
                data: response.data.data
            };
        } else {
            throw new Error(response.data.message || '获取报告详情失败');
        }
    } catch (error) {
        console.error('获取报告详情失败:', error);
        let errorMessage = '获取报告详情失败';

        if (error.response) {
            switch (error.response.status) {
                case 404:
                    errorMessage = '未找到相关记录';
                    break;
                case 401:
                    errorMessage = '未授权，请重新登录';
                    break;
                case 403:
                    errorMessage = '没有权限访问该资源';
                    break;
                case 500:
                    errorMessage = '服务器内部错误';
                    break;
                default:
                    errorMessage = error.response.data?.message || '请求失败';
            }
        } else if (error.code === 'ERR_NETWORK') {
            errorMessage = '无法连接到服务器，请检查网络连接';
        } else if (error.code === 'ECONNABORTED') {
            errorMessage = '请求超时，请稍后重试';
        }

        return {
            success: false,
            error: errorMessage
        };
    }
}; 