import { ARTICLE_MAPPING } from '../config/constants';

// 处理登出
export const handleLogout = (router) => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
};

// 处理记录ID点击
export const handleRecordIdClick = (recordId, activeNav, recordIdRef, handleReportDetail) => {
    activeNav = '报告详情';
    recordIdRef = recordId;
    handleReportDetail();
};

// 显示科普文章
export const showArticle = (key) => {
    const articleUrl = ARTICLE_MAPPING[key];
    if (articleUrl) {
        window.open(articleUrl, '_blank');
    } else {
        alert('暂无相关科普文章');
    }
};

// 处理图表大小调整
export const handleChartResize = (chartInstance, chartReady) => {
    if (chartInstance && chartReady) {
        chartInstance.resize();
    }
}; 