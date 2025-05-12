import axios from 'axios';

// 时间格式化函数
const formatDate = (date) => {
    if (!date) return '';
    const d = new Date(date);
    return d.toISOString().split('T')[0];
};

// 获取快捷时间范围
const getQuickDateRange = (type) => {
    const now = new Date();
    const endDate = formatDate(now);
    let startDate;

    switch (type) {
        case 'last_exam':
            // 获取最近一次体检记录
            return {
                type: 'last_exam',
                endDate
            };
        case 'last_month':
            startDate = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
            break;
        case 'last_three_months':
            startDate = new Date(now.getFullYear(), now.getMonth() - 3, now.getDate());
            break;
        case 'last_six_months':
            startDate = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate());
            break;
        case 'last_year':
            startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
            break;
        default:
            return null;
    }

    return {
        type: 'date_range',
        startDate: formatDate(startDate),
        endDate
    };
};

// 验证时间范围
const validateDateRange = (startDate, endDate) => {
    if (!startDate || !endDate) {
        return {
            valid: false,
            error: '请选择开始和结束日期'
        };
    }

    const start = new Date(startDate);
    const end = new Date(endDate);
    const now = new Date();

    // 检查日期是否有效
    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
        return {
            valid: false,
            error: '日期格式无效'
        };
    }

    // 检查日期范围是否合理
    if (start > end) {
        return {
            valid: false,
            error: '开始日期不能晚于结束日期'
        };
    }

    // 检查是否超过当前日期
    if (end > now) {
        return {
            valid: false,
            error: '结束日期不能超过当前日期'
        };
    }

    // 检查时间范围是否超过一年
    const oneYear = 365 * 24 * 60 * 60 * 1000;
    if (end - start > oneYear) {
        return {
            valid: false,
            error: '查询时间范围不能超过一年'
        };
    }

    return {
        valid: true
    };
};

export const handleQuery = async (activeNav, params) => {
    try {
        let endpoint = '';
        let queryParams = {};

        switch (activeNav) {
            case '历史体检报告':
                // 处理快捷查询
                if (params.quickType) {
                    const quickRange = getQuickDateRange(params.quickType);
                    if (!quickRange) {
                        return {
                            success: false,
                            error: '无效的快捷查询类型'
                        };
                    }

                    if (quickRange.type === 'last_exam') {
                        // 获取最近一次体检记录
                        endpoint = 'http://localhost:8001/api/health/last-exam';
                    } else {
                        // 使用日期范围查询
                        endpoint = 'http://localhost:8001/api/health/history';
                        queryParams = {
                            startDate: quickRange.startDate,
                            endDate: quickRange.endDate
                        };
                    }
                } else {
                    // 验证时间范围
                    const validation = validateDateRange(params.startDate, params.endDate);
                    if (!validation.valid) {
                        return {
                            success: false,
                            error: validation.error
                        };
                    }

                    endpoint = 'http://localhost:8001/api/health/history';
                    queryParams = {
                        startDate: formatDate(params.startDate),
                        endDate: formatDate(params.endDate)
                    };
                }
                break;
            case '关键指标检索':
                endpoint = 'http://localhost:8001/api/health/indicators';
                queryParams = {
                    type: params.selectedIndicator
                };
                break;
            default:
                throw new Error('未知的导航类型');
        }

        const response = await axios.get(endpoint, {
            params: queryParams,
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.data.code === 200) {
            // 对历史体检报告数据进行时间排序
            let data = response.data.data;
            if (activeNav === '历史体检报告') {
                data = data.sort((a, b) => {
                    return new Date(b.report_date) - new Date(a.report_date);
                });
            }

            return {
                success: true,
                data: data,
                total: response.data.total
            };
        } else {
            throw new Error(response.data.message || '请求失败');
        }
    } catch (error) {
        console.error('查询失败:', error);
        let errorMessage = '查询失败';

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