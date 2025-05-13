// 参考范围配置
export const REFERENCE_RANGES = {
    // 血常规参考范围
    white_blood_cell: { min: 4.0, max: 10.0 },
    red_blood_cell: { min: 3.5, max: 5.5 },
    platelet: { min: 100, max: 300 },
    // 尿常规参考范围
    urine_sugar: { min: 0, max: 0 },
    urine_protein: { min: 0, max: 0 },
    // 生化指标参考范围
    alt: { min: 0, max: 40 },
    ast: { min: 0, max: 40 },
    creatinine: { min: 44, max: 133 },
    urea: { min: 2.9, max: 8.2 },
    cholesterol: { min: 2.8, max: 5.17 },
    triglyceride: { min: 0.56, max: 1.7 },
    // 肝纤维化参考范围
    fibrosis_index: { min: 0, max: 2.0 }
};

// 指标名称映射
export const INDICATOR_NAMES = {
    blood_routine: [
        { value: 'white_blood_cell', label: '白细胞计数' },
        { value: 'red_blood_cell', label: '红细胞计数' },
        { value: 'platelet', label: '血小板计数' }
    ],
    urine_routine: [
        { value: 'urine_sugar', label: '尿糖' },
        { value: 'urine_protein', label: '尿蛋白' }
    ],
    biochemistry: [
        { value: 'alt', label: '谷丙转氨酶' },
        { value: 'ast', label: '谷草转氨酶' },
        { value: 'creatinine', label: '肌酐' },
        { value: 'urea', label: '尿素' },
        { value: 'cholesterol', label: '胆固醇' },
        { value: 'triglyceride', label: '甘油三酯' }
    ],
    liver_fibrosis: [
        { value: 'fibrosis_index', label: '肝纤维化指数' }
    ]
};

// 评分权重配置
export const SCORE_WEIGHTS = {
    blood_routine: 0.3,
    urine_routine: 0.2,
    biochemistry: 0.3,
    liver_fibrosis: 0.2
};

// 科普文章映射
export const ARTICLE_MAPPING = {
    // 血常规
    white_blood_cell: '/articles/blood-routine/white-blood-cell',
    red_blood_cell: '/articles/blood-routine/red-blood-cell',
    platelet: '/articles/blood-routine/platelet',
    // 尿常规
    urine_sugar: '/articles/urine-routine/sugar',
    urine_protein: '/articles/urine-routine/protein',
    // 生化指标
    alt: '/articles/biochemistry/alt',
    ast: '/articles/biochemistry/ast',
    creatinine: '/articles/biochemistry/creatinine',
    urea: '/articles/biochemistry/urea',
    cholesterol: '/articles/biochemistry/cholesterol',
    triglyceride: '/articles/biochemistry/triglyceride',
    // 肝纤维化
    fibrosis_index: '/articles/liver-fibrosis/index'
};

// 快捷选项配置
export const QUICK_OPTIONS = [
    { type: 'last_month', label: '最近一个月' },
    { type: 'last_three_months', label: '最近三个月' },
    { type: 'last_six_months', label: '最近半年' },
    { type: 'last_year', label: '最近一年' }
];

// 导航配置
export const NAV_SECTIONS = [
    {
        title: '数据查询',
        items: [
            { label: '历史体检报告', icon: '📊' },
            { label: '关键指标检索', icon: '🔍' },
            { label: '报告详情', icon: '📝' }
        ]
    },
    {
        title: '统计分析',
        items: [
            { label: '指标趋势分析', icon: '📈' },
            { label: '数据对比分析', icon: '📊' },
            { label: '健康评分', icon: '⭐' },
            { label: '异常人群排名', icon: '🏆' }
        ]
    }
]; 