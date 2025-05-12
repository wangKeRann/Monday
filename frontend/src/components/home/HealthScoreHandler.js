import axios from 'axios';

// 参考范围配置
const referenceRanges = {
    white_blood_cell: { min: 4.0, max: 10.0 },
    red_blood_cell: { min: 3.5, max: 5.5 },
    platelet: { min: 100, max: 300 },
    urine_sugar: { min: 0, max: 0 },
    urine_protein: { min: 0, max: 0 },
    alt: { min: 0, max: 40 },
    ast: { min: 0, max: 40 },
    creatinine: { min: 44, max: 133 },
    urea: { min: 2.9, max: 8.2 },
    cholesterol: { min: 2.8, max: 5.17 },
    triglyceride: { min: 0.56, max: 1.7 },
    fibrosis_index: { min: 0, max: 2.0 }
};

// 评分权重配置
const scoreWeights = {
    blood_routine: 0.3,
    urine_routine: 0.2,
    biochemistry: 0.3,
    liver_fibrosis: 0.2
};

export const calculateHealthScore = async (recordId) => {
    try {
        const response = await axios.get(`http://localhost:8001/api/health/detail/${recordId}`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.data.code === 200) {
            const record = response.data.data;
            if (!record) {
                throw new Error('未找到相关记录');
            }

            const scores = {};
            const sectionTypes = ['blood_routine', 'urine_routine', 'biochemistry', 'liver_fibrosis'];

            for (const section of sectionTypes) {
                scores[section] = calculateSectionScore(record[section], section);
            }

            let totalScore = 0;
            for (const [section, score] of Object.entries(scores)) {
                totalScore += score * scoreWeights[section];
            }

            const healthScore = Math.round(totalScore);
            const analysis = generateHealthAnalysis(scores, healthScore);

            return {
                success: true,
                score: healthScore,
                analysis: analysis
            };
        } else {
            throw new Error(response.data.message || '获取报告详情失败');
        }
    } catch (error) {
        console.error('评分计算失败:', error);
        return {
            success: false,
            error: error.response?.data?.message || error.message
        };
    }
};

const calculateSectionScore = (sectionData, sectionType) => {
    if (!sectionData) return 100;

    let totalScore = 0;
    let validIndicators = 0;

    for (const [key, value] of Object.entries(sectionData)) {
        const range = referenceRanges[key];
        if (!range) continue;

        validIndicators++;
        if (value >= range.min && value <= range.max) {
            totalScore += 100;
        } else {
            const deviation = Math.min(
                Math.abs(value - range.min),
                Math.abs(value - range.max)
            );
            const maxDeviation = Math.max(range.max - range.min, 1);
            const score = Math.max(0, 100 - (deviation / maxDeviation) * 100);
            totalScore += score;
        }
    }

    return validIndicators > 0 ? totalScore / validIndicators : 100;
};

const generateHealthAnalysis = (scores, totalScore) => {
    let analysis = '健康评分分析：\n\n';

    const sectionNames = {
        blood_routine: '血常规',
        urine_routine: '尿常规',
        biochemistry: '生化指标',
        liver_fibrosis: '肝纤维化'
    };

    for (const [section, score] of Object.entries(scores)) {
        analysis += `${sectionNames[section]}得分：${Math.round(score)}分\n`;
    }

    analysis += '\n总体评价：\n';
    if (totalScore >= 90) {
        analysis += '您的健康状况优秀，各项指标都在正常范围内。建议继续保持良好的生活习惯。';
    } else if (totalScore >= 80) {
        analysis += '您的健康状况良好，但部分指标略有异常。建议关注异常指标，适当调整生活方式。';
    } else if (totalScore >= 70) {
        analysis += '您的健康状况一般，存在一些异常指标。建议及时就医检查，并注意改善生活习惯。';
    } else {
        analysis += '您的健康状况需要关注，多项指标异常。建议尽快就医进行详细检查，并遵医嘱进行治疗。';
    }

    return analysis;
}; 