import axios from 'axios';
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    DataZoomComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册必需的组件
echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    DataZoomComponent,
    BarChart,
    CanvasRenderer
]);

export const handleTrendAnalysis = async (params) => {
    try {
        const response = await axios.get('http://localhost:8001/api/health/trend-analysis', {
            params: {
                start_date: params.startDate,
                end_date: params.endDate,
                indicator_type: params.indicatorType,
                indicator_name: params.indicatorName
            },
            timeout: 5000,
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
            throw new Error(response.data.message || '获取趋势数据失败');
        }
    } catch (error) {
        console.error('趋势分析失败:', error);
        return {
            success: false,
            error: error.response?.data?.message || error.message
        };
    }
};

export const analyzeTrend = (trendData, selectedTrendIndicator) => {
    if (!trendData || trendData.length < 2) {
        return '数据点不足，无法进行趋势分析';
    }

    const values = trendData.map(item => {
        const indicatorData = item[selectedTrendIndicator];
        return Object.values(indicatorData)[0];
    });

    const average = values.reduce((a, b) => a + b, 0) / values.length;
    const firstValue = values[0];
    const lastValue = values[values.length - 1];
    const changeRate = ((lastValue - firstValue) / firstValue * 100).toFixed(2);

    let trendText = `分析结果：\n`;
    trendText += `1. 平均值：${average.toFixed(2)}\n`;
    trendText += `2. 总体变化：${changeRate}%\n`;

    if (changeRate > 5) {
        trendText += '3. 趋势判断：指标呈上升趋势，建议关注';
    } else if (changeRate < -5) {
        trendText += '3. 趋势判断：指标呈下降趋势，建议关注';
    } else {
        trendText += '3. 趋势判断：指标相对稳定';
    }

    return trendText;
};

export const initChart = (chartDom, data) => {
    if (!chartDom) return null;

    const chart = echarts.init(chartDom);

    const option = {
        title: {
            text: '指标趋势分析',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: data.dates
        },
        yAxis: {
            type: 'value',
            name: '指标值'
        },
        series: [{
            name: '指标值',
            type: 'line',
            data: data.values,
            smooth: true,
            markPoint: {
                data: [
                    { type: 'max', name: '最大值' },
                    { type: 'min', name: '最小值' }
                ]
            }
        }]
    };

    chart.setOption(option);
    return chart;
}; 