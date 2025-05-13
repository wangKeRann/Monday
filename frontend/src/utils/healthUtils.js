import { REFERENCE_RANGES, INDICATOR_NAMES } from '../config/constants';

// 获取参考范围
export const getReferenceRange = (key) => {
    const range = REFERENCE_RANGES[key];
    if (!range) return '-';
    return `${range.min}-${range.max}`;
};

// 获取指标状态
export const getStatus = (value, key) => {
    const range = REFERENCE_RANGES[key];
    if (!range) return '未知';

    if (value < range.min) return '偏低';
    if (value > range.max) return '偏高';
    return '正常';
};

// 获取状态样式类
export const getStatusClass = (value, key) => {
    const status = getStatus(value, key);
    return {
        'status-normal': status === '正常',
        'status-high': status === '偏高',
        'status-low': status === '偏低',
        'status-unknown': status === '未知'
    };
};

// 获取数值样式类
export const getValueClass = (value, key) => {
    const status = getStatus(value, key);
    return {
        'value-normal': status === '正常',
        'value-high': status === '偏高',
        'value-low': status === '偏低',
        'value-unknown': status === '未知'
    };
};

// 获取指标标签
export const getIndicatorLabel = (type, key) => {
    const item = INDICATOR_NAMES[type].find(i => i.value === key);
    return item ? item.label : key;
}; 