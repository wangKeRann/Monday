import axios from 'axios';
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册必需的组件
echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    BarChart,
    CanvasRenderer
]);

export const handleComparisonAnalysis = async (ageRange) => {
    try {
        const response = await axios.get('http://localhost:8001/api/health/comparison', {
            params: {
                age_range: ageRange
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
            throw new Error(response.data.message || '获取对比数据失败');
        }
    } catch (error) {
        console.error('数据对比分析失败:', error);
        return {
            success: false,
            error: error.response?.data?.message || error.message
        };
    }
};

export const initComparisonChart = (chartDom, data) => {
    if (!chartDom) return null;

    const chart = echarts.init(chartDom);

    const option = {
        title: {
            text: '性别分布统计',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['男性', '女性'],
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {
            type: 'value',
            name: '人数'
        },
        series: [{
            name: '检测人数',
            type: 'bar',
            data: [data.male_count, data.female_count],
            showBackground: true,
            backgroundStyle: {
                color: 'rgba(180, 180, 180, 0.2)'
            }
        }]
    };

    chart.setOption(option);
    return chart;
}; 