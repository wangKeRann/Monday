import axios from 'axios';

export const handleAbnormalAnalysis = async (indicatorType) => {
    try {
        const response = await axios.get('http://localhost:8001/api/health/abnormal-ranking', {
            params: {
                indicator_type: indicatorType
            },
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.data.code === 200 && response.data.data) {
            return {
                success: true,
                data: response.data.data
            };
        } else {
            throw new Error(response.data.message || '获取异常人群数据失败');
        }
    } catch (error) {
        console.error('异常人群分析失败:', error);
        return {
            success: false,
            error: error.response?.data?.message || error.message
        };
    }
}; 