<template>
    <div class="layout-root">
        <!-- 全局顶栏 -->
        <div class="global-header">
            <div class="header-left">健康管理系统</div>
            <div v-if="user" class="user-info">
                <img :src="user.avatar_url" :alt="user.username" class="avatar">
                <div class="user-details">
                    <h2>{{ user.login }}</h2>
                    <p>{{ user.email }}</p>
                </div>
                <button @click="handleLogout" class="logout-button">退出登录</button>
            </div>
        </div>
        <!-- 左侧导航栏 -->
        <div class="sidebar">
            <div class="sidebar-logo">健康管理</div>
            <div class="nav-section" v-for="section in navSections" :key="section.title">
                <h3 class="nav-title">{{ section.title }}</h3>
                <ul class="nav-list">
                    <li v-for="item in section.items" :key="item.label"
                        :class="['nav-item', { active: activeNav === item.label }]"
                        @click="selectNav(item.label)">
                        <i class="nav-icon">{{ item.icon }}</i>
                        <span>{{ item.label }}</span>
                    </li>
                </ul>
            </div>
        </div>
        <!-- 右侧主内容区 -->
        <div class="main-area">
            <div class="content-area">
                <div class="content-actions">
                    <template v-if="['历史体检报告', '关键指标检索', '报告详情', '指标趋势分析', '数据对比分析'].includes(activeNav)">
                        <template v-if="activeNav === '历史体检报告'">
                            <div class="date-range-container">
                                <div class="date-inputs">
                                    <label style="margin-right:8px;">开始日期：</label>
                                    <input type="date" v-model="startDate" class="date-input" />
                                    <label style="margin:0 8px;">结束日期：</label>
                                    <input type="date" v-model="endDate" class="date-input" />
                                    <button class="action-button" @click="handleQuery">查询</button>
                                </div>
                                <div class="quick-actions">
                                    <button 
                                        v-for="option in quickOptions" 
                                        :key="option.type"
                                        class="quick-button"
                                        :class="{ active: selectedQuickType === option.type }"
                                        @click="handleQuickQuery(option.type)"
                                    >
                                        {{ option.label }}
                                    </button>
                                </div>
                            </div>
                        </template>
                        <template v-else-if="activeNav === '关键指标检索'">
                            <label style="margin-right:8px;">指标类型：</label>
                            <select v-model="selectedIndicator" class="indicator-select">
                                <option value="">请选择指标类型</option>
                                <option value="blood_routine">血常规</option>
                                <option value="urine_routine">尿常规</option>
                                <option value="biochemistry">生化指标</option>
                                <option value="ultrasound">超声检查</option>
                                <option value="liver_fibrosis">肝纤维化</option>
                            </select>
                            <button class="action-button" @click="handleQuery">查询</button>
                        </template>
                        <template v-else-if="activeNav === '报告详情'">
                            <label style="margin-right:8px;">记录ID：</label>
                            <input type="text" v-model="recordId" class="record-input" placeholder="请输入记录ID" />
                            <button class="action-button" @click="handleQuery">查询</button>
                        </template>
                        <template v-else-if="activeNav === '指标趋势分析'">
                            <label style="margin-right:8px;">开始日期：</label>
                            <input type="date" v-model="trendStartDate" class="date-input" />
                            <label style="margin:0 8px;">结束日期：</label>
                            <input type="date" v-model="trendEndDate" class="date-input" />
                            <label style="margin:0 8px;">指标类型：</label>
                            <select v-model="selectedTrendIndicator" class="indicator-select" @change="handleIndicatorTypeChange">
                                <option value="">请选择指标类型</option>
                                <option value="blood_routine">血常规</option>
                                <option value="urine_routine">尿常规</option>
                                <option value="biochemistry">生化指标</option>
                                <option value="liver_fibrosis">肝纤维化</option>
                            </select>
                            <div v-if="selectedTrendIndicator" style="display: inline-block; margin-left: 8px;">
                                <label style="margin-right:8px;">具体指标：</label>
                                <select v-model="selectedIndicatorName" class="indicator-select">
                                    <option value="">请选择具体指标</option>
                                    <option v-for="item in indicatorNames[selectedTrendIndicator]" 
                                            :key="item.value" 
                                            :value="item.value">
                                        {{ item.label }}
                                    </option>
                                </select>
                            </div>
                            <button class="action-button" @click="handleTrendAnalysis">查询</button>
                        </template>
                        <template v-else-if="activeNav === '数据对比分析'">
                            <label style="margin-right:8px;">年龄段：</label>
                            <select v-model="selectedAgeRange" class="age-range-select">
                                <option value="">请选择年龄段</option>
                                <option value="0-18">0-18岁</option>
                                <option value="19-30">19-30岁</option>
                                <option value="31-45">31-45岁</option>
                                <option value="46-60">46-60岁</option>
                                <option value="60+">60岁以上</option>
                            </select>
                            <button class="action-button" @click="handleComparisonAnalysis">开始分析</button>
                        </template>
                    </template>
                    <template v-else-if="activeNav === '健康评分'">
                        <label style="margin-right:8px;">记录ID：</label>
                        <input type="text" v-model="healthScoreRecordId" class="record-input" placeholder="请输入记录ID" style="width: 220px;" />
                        <button class="action-button" @click="calculateHealthScore">开始评分</button>
                    </template>
                </div>
                <div class="content-body">
                    <!-- 健康评分显示区域 -->
                    <div v-if="activeNav === '健康评分' && healthScore !== null" class="score-display">
                        <div class="score-circle">
                            <div class="score-value">{{ healthScore }}</div>
                            <div class="score-label">健康评分</div>
                        </div>
                        <div class="score-analysis">
                            <h3>健康分析</h3>
                            <p>{{ healthScoreAnalysis }}</p>
                        </div>
                    </div>

                    <!-- 指标趋势分析 -->
                    <div v-if="activeNav === '指标趋势分析'">
                        <div class="table-container">
                            <!-- 加载状态显示 -->
                            <div v-if="loading" class="loading-overlay">
                                <div class="loading-spinner"></div>
                                <div class="loading-text">数据加载中...</div>
                            </div>
                            <div v-else>
                                <div class="trend-chart" ref="trendChart">
                                    <!-- 这里可以添加图表组件 -->
                                </div>
                                <div class="trend-analysis" v-if="trendAnalysis">
                                    <h3>趋势分析</h3>
                                    <p>{{ trendAnalysis }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 表格展示区域 -->
                    <div class="table-container" v-if="activeNav === '历史体检报告' || activeNav === '关键指标检索'">
                        <!-- 加载状态显示 -->
                        <div v-if="loading" class="loading-overlay">
                            <div class="loading-spinner"></div>
                            <div class="loading-text">数据加载中...</div>
                        </div>
                        
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>报告日期</th>
                                    <th>性别</th>
                                    <th>年龄</th>
                                    <th>记录ID</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="record in healthRecords" :key="record.record_id">
                                    <td>{{ record.report_date }}</td>
                                    <td>{{ record.gender }}</td>
                                    <td>{{ record.age }}</td>
                                    <td class="record-id-cell" @click="handleRecordIdClick(record.record_id)">{{ record.record_id }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="table-info" v-if="total > 0">
                            共 {{ total }} 条记录
                        </div>
                        <div class="no-data" v-if="total === 0">
                            暂无数据
                        </div>
                    </div>

                    <!-- 报告详情查询区域 -->
                    <div class="detail-container" v-if="activeNav === '报告详情' && selectedRecord">
                        <div class="detail-header">
                            <h2>报告详情</h2>
                            <div class="detail-info">
                                <span>记录ID：{{ selectedRecord.record_id }}</span>
                                <span>报告日期：{{ selectedRecord.report_date }}</span>
                                <span>性别：{{ selectedRecord.gender }}</span>
                                <span>年龄：{{ selectedRecord.age }}</span>
                            </div>
                        </div>

                        <!-- 血常规数据 -->
                        <div class="detail-section">
                            <h3>血常规检查</h3>
                            <table class="detail-table">
                                <thead>
                                    <tr>
                                        <th>指标名称</th>
                                        <th>检测值</th>
                                        <th>参考范围</th>
                                        <th>状态</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="selectedRecord.blood_routine">
                                        <tr v-for="(value, key) in selectedRecord.blood_routine" :key="key">
                                            <td>{{ getIndicatorLabel('blood_routine', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in indicatorNames.blood_routine" :key="item.value">
                                            <td>{{ item.label }}</td>
                                            <td>-</td>
                                            <td class="reference-range" @click="showArticle(item.value)">{{ getReferenceRange(item.value) }}</td>
                                            <td>暂无</td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <!-- 尿常规数据 -->
                        <div class="detail-section">
                            <h3>尿常规检查</h3>
                            <table class="detail-table">
                                <thead>
                                    <tr>
                                        <th>指标名称</th>
                                        <th>检测值</th>
                                        <th>参考范围</th>
                                        <th>状态</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="selectedRecord.urine_routine">
                                        <tr v-for="(value, key) in selectedRecord.urine_routine" :key="key">
                                            <td>{{ getIndicatorLabel('urine_routine', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in indicatorNames.urine_routine" :key="item.value">
                                            <td>{{ item.label }}</td>
                                            <td>-</td>
                                            <td class="reference-range" @click="showArticle(item.value)">{{ getReferenceRange(item.value) }}</td>
                                            <td>暂无</td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <!-- 生化指标数据 -->
                        <div class="detail-section">
                            <h3>生化指标检查</h3>
                            <table class="detail-table">
                                <thead>
                                    <tr>
                                        <th>指标名称</th>
                                        <th>检测值</th>
                                        <th>参考范围</th>
                                        <th>状态</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="selectedRecord.biochemistry">
                                        <tr v-for="(value, key) in selectedRecord.biochemistry" :key="key">
                                            <td>{{ getIndicatorLabel('biochemistry', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in indicatorNames.biochemistry" :key="item.value">
                                            <td>{{ item.label }}</td>
                                            <td>-</td>
                                            <td class="reference-range" @click="showArticle(item.value)">{{ getReferenceRange(item.value) }}</td>
                                            <td>暂无</td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <!-- 超声检查数据 -->
                        <div class="detail-section">
                            <h3>超声检查</h3>
                            <table class="detail-table">
                                <thead>
                                    <tr>
                                        <th>检查项目</th>
                                        <th>检查结果</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="selectedRecord.ultrasound">
                                        <tr v-for="(value, key) in selectedRecord.ultrasound" :key="key">
                                            <td>{{ getIndicatorLabel('ultrasound', key) }}</td>
                                            <td>{{ value }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr>
                                            <td colspan="2" class="no-data-cell">暂无数据</td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <!-- 肝纤维化数据 -->
                        <div class="detail-section">
                            <h3>肝纤维化检查</h3>
                            <table class="detail-table">
                                <thead>
                                    <tr>
                                        <th>指标名称</th>
                                        <th>检测值</th>
                                        <th>参考范围</th>
                                        <th>状态</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-if="selectedRecord.liver_fibrosis">
                                        <tr v-for="(value, key) in selectedRecord.liver_fibrosis" :key="key">
                                            <td>{{ getIndicatorLabel('liver_fibrosis', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in indicatorNames.liver_fibrosis" :key="item.value">
                                            <td>{{ item.label }}</td>
                                            <td>-</td>
                                            <td class="reference-range" @click="showArticle(item.value)">{{ getReferenceRange(item.value) }}</td>
                                            <td>暂无</td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- 数据对比分析区域 -->
                    <div v-if="activeNav === '数据对比分析'" class="comparison-container">
                        <div class="table-container">
                            <!-- 加载状态显示 -->
                            <div v-if="loading" class="loading-overlay">
                                <div class="loading-spinner"></div>
                                <div class="loading-text">数据加载中...</div>
                            </div>
                            <div v-else>
                                <div v-if="comparisonData" class="comparison-content">
                                    <div class="comparison-chart" ref="comparisonChart"></div>
                                    <div class="comparison-summary">
                                        <h3>数据统计</h3>
                                        <div class="summary-content">
                                            <div class="summary-item">
                                                <span class="label">男性检测人数：</span>
                                                <span class="value">{{ comparisonData.male_count }}</span>
                                            </div>
                                            <div class="summary-item">
                                                <span class="label">女性检测人数：</span>
                                                <span class="value">{{ comparisonData.female_count }}</span>
                                            </div>
                                            <div class="summary-item">
                                                <span class="label">总检测人数：</span>
                                                <span class="value">{{ comparisonData.male_count + comparisonData.female_count }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div v-else class="no-data">
                                    请选择年龄段并点击"开始分析"按钮查看数据
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 异常人群排名区域 -->
                    <div v-if="activeNav === '异常人群排名'" class="abnormal-ranking-container">
                        <div class="filter-section">
                            <label style="margin-right:8px;">指标类型：</label>
                            <select v-model="selectedAbnormalIndicator" class="indicator-select">
                                <option value="">请选择指标类型</option>
                                <option value="blood_routine">血常规</option>
                                <option value="urine_routine">尿常规</option>
                                <option value="biochemistry">生化指标</option>
                                <option value="liver_fibrosis">肝纤维化</option>
                            </select>
                            <button class="action-button" @click="handleAbnormalAnalysis" :disabled="!selectedAbnormalIndicator">开始分析</button>
                        </div>
                        
                        <div class="table-container">
                            <!-- 加载状态显示 -->
                            <div v-if="loading" class="loading-overlay">
                                <div class="loading-spinner"></div>
                                <div class="loading-text">数据加载中...</div>
                            </div>
                            <div v-else>
                                <div v-if="abnormalData" class="abnormal-content">
                                    <table class="data-table">
                                        <thead>
                                            <tr>
                                                <th>年龄段</th>
                                                <th>异常人数</th>
                                                <th>总人数</th>
                                                <th>异常比例</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="item in abnormalData.age_distribution" :key="item.age_range">
                                                <td>{{ item.age_range }}岁</td>
                                                <td>{{ item.count }}</td>
                                                <td>{{ item.total }}</td>
                                                <td>{{ ((item.count / item.total) * 100).toFixed(2) }}%</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <div class="table-info">
                                        总检测人数：{{ abnormalData.total_count }} | 
                                        总异常人数：{{ abnormalData.abnormal_count }} | 
                                        总体异常比例：{{ ((abnormalData.abnormal_count / abnormalData.total_count) * 100).toFixed(2) }}%
                                    </div>
                                </div>
                                <div v-else class="no-data">
                                    请选择指标类型查看异常人群分布
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { handleQuery } from '../components/home/QueryHandler';
import { handleReportDetail } from '../components/home/ReportDetailHandler';
import { handleTrendAnalysis, analyzeTrend, initChart } from '../components/home/TrendAnalysisHandler';
import { calculateHealthScore } from '../components/home/HealthScoreHandler';
import { handleComparisonAnalysis, initComparisonChart } from '../components/home/ComparisonHandler';
import { handleAbnormalAnalysis } from '../components/home/AbnormalAnalysisHandler';

export default {
    name: 'Home',
    data() {
        return {
            user: null,
            activeNav: '历史体检报告',
            navSections: [
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
            ],
            startDate: '',
            endDate: '',
            selectedIndicator: '',
            healthRecords: [],
            total: 0,
            loading: false,
            recordId: '',
            selectedRecord: null,
            healthScoreRecordId: '',
            healthScore: null,
            healthScoreAnalysis: '',
            trendStartDate: '',
            trendEndDate: '',
            selectedTrendIndicator: '',
            selectedIndicatorName: '',
            trendData: [],
            trendAnalysis: '',
            selectedAgeRange: '',
            comparisonData: null,
            chartInstance: null,
            chartReady: false,
            selectedAbnormalIndicator: '',
            abnormalData: null,
            // 参考范围
            referenceRanges: {
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
            },
            // 指标名称映射
            indicatorNames: {
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
            },
            // 评分权重配置
            scoreWeights: {
                blood_routine: 0.3,
                urine_routine: 0.2,
                biochemistry: 0.3,
                liver_fibrosis: 0.2
            },
            selectedQuickType: '',
            quickOptions: [
                { type: 'last_month', label: '最近一个月' },
                { type: 'last_three_months', label: '最近三个月' },
                { type: 'last_six_months', label: '最近半年' },
                { type: 'last_year', label: '最近一年' }
            ],
            // 添加科普文章映射
            articleMapping: {
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
            },
        };
    },
    created() {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            this.user = JSON.parse(userStr);
            console.log('存储的用户数据:', this.user);
        } else {
            this.$router.push('/login');
        }
    },
    mounted() {
        window.addEventListener('resize', this.handleChartResize);
    },
    watch: {
        comparisonData: {
            handler(newVal) {
                if (newVal) {
                    this.$nextTick(() => {
                        // 删除 this.initChart() 调用
                    });
                }
            },
            deep: true
        }
    },
    methods: {
        handleLogout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.$router.push('/login');
        },
        selectNav(label) {
            this.activeNav = label;
        },
        async handleQuery() {
            if (this.activeNav === '历史体检报告') {
                if (!this.startDate || !this.endDate) {
                    alert('请选择开始和结束日期');
                    return;
                }
            } else if (this.activeNav === '关键指标检索') {
                if (!this.selectedIndicator) {
                    alert('请选择指标类型');
                    return;
                }
            } else if (this.activeNav === '报告详情') {
                this.handleReportDetail();
                return;
            } else if (this.activeNav === '指标趋势分析') {
                this.handleTrendAnalysis();
                return;
            }
            
            this.loading = true;
            
            const params = {
                startDate: this.startDate,
                endDate: this.endDate,
                selectedIndicator: this.selectedIndicator
            };
            
            const result = await handleQuery(this.activeNav, params);
            
            if (result.success) {
                this.healthRecords = result.data;
                this.total = result.total;
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        async handleReportDetail() {
            if (!this.recordId) {
                alert('请输入记录ID');
                return;
            }

            this.loading = true;
            
            const result = await handleReportDetail(this.recordId);
            
            if (result.success) {
                this.selectedRecord = result.data;
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        async handleTrendAnalysis() {
            if (!this.trendStartDate || !this.trendEndDate) {
                alert('请选择开始和结束日期');
                return;
            }
            if (!this.selectedTrendIndicator) {
                alert('请选择要分析的指标类型');
                return;
            }
            if (!this.selectedIndicatorName) {
                alert('请选择具体指标');
                return;
            }

            this.loading = true;
            
            const params = {
                startDate: this.trendStartDate,
                endDate: this.trendEndDate,
                indicatorType: this.selectedTrendIndicator,
                indicatorName: this.selectedIndicatorName
            };
            
            const result = await handleTrendAnalysis(params);
            
            if (result.success) {
                this.trendData = result.data;
                this.trendAnalysis = analyzeTrend(this.trendData, this.selectedTrendIndicator);
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        handleIndicatorTypeChange() {
            this.selectedIndicatorName = '';
        },
        async calculateHealthScore() {
            if (!this.healthScoreRecordId) {
                alert('请输入记录ID');
                return;
            }

            this.loading = true;
            
            const result = await calculateHealthScore(this.healthScoreRecordId);
            
            if (result.success) {
                this.healthScore = result.score;
                this.healthScoreAnalysis = result.analysis;
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        async handleComparisonAnalysis() {
            if (!this.selectedAgeRange) {
                alert('请选择年龄段');
                return;
            }

            this.loading = true;
            this.chartReady = false;
            
            const result = await handleComparisonAnalysis(this.selectedAgeRange);
            
            if (result.success) {
                this.comparisonData = result.data;
                this.$nextTick(() => {
                    const chartDom = this.$refs.comparisonChart;
                    if (chartDom) {
                        this.chartInstance = initComparisonChart(chartDom, this.comparisonData);
                    }
                });
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        handleChartResize() {
            if (this.chartInstance && this.chartReady) {
                this.chartInstance.resize();
            }
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.handleChartResize);
            if (this.chartInstance) {
                this.chartInstance.dispose();
                this.chartInstance = null;
            }
        },
        async handleAbnormalAnalysis() {
            if (!this.selectedAbnormalIndicator) {
                return;
            }

            this.loading = true;
            
            const result = await handleAbnormalAnalysis(this.selectedAbnormalIndicator);
            
            if (result.success) {
                this.abnormalData = result.data;
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        // 获取参考范围
        getReferenceRange(key) {
            const range = this.referenceRanges[key];
            if (!range) return '-';
            return `${range.min}-${range.max}`;
        },

        // 获取指标状态
        getStatus(value, key) {
            const range = this.referenceRanges[key];
            if (!range) return '未知';
            
            if (value < range.min) return '偏低';
            if (value > range.max) return '偏高';
            return '正常';
        },

        // 获取状态样式类
        getStatusClass(value, key) {
            const status = this.getStatus(value, key);
            return {
                'status-normal': status === '正常',
                'status-high': status === '偏高',
                'status-low': status === '偏低',
                'status-unknown': status === '未知'
            };
        },

        // 获取数值样式类
        getValueClass(value, key) {
            const status = this.getStatus(value, key);
            return {
                'value-normal': status === '正常',
                'value-high': status === '偏高',
                'value-low': status === '偏低',
                'value-unknown': status === '未知'
            };
        },
        async handleQuickQuery(type) {
            this.selectedQuickType = type;
            this.loading = true;
            const result = await handleQuery(this.activeNav, { quickType: type });
            
            if (result.success) {
                this.healthRecords = result.data;
                this.total = result.total;
            } else {
                alert(result.error);
            }
            
            this.loading = false;
        },
        handleRecordIdClick(recordId) {
            this.activeNav = '报告详情';
            this.recordId = recordId;
            this.handleReportDetail();
        },
        showArticle(key) {
            const articleUrl = this.articleMapping[key];
            if (articleUrl) {
                window.open(articleUrl, '_blank');
            } else {
                alert('暂无相关科普文章');
            }
        },
        getIndicatorLabel(type, key) {
            const item = this.indicatorNames[type].find(i => i.value === key);
            return item ? item.label : key;
        },
    }
};
</script>

<style>
@import '../assets/styles/home.css';
.table-container {
    margin: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.data-table th,
.data-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

.data-table th {
    background-color: #f5f7fa;
    font-weight: 600;
    color: #333;
}

.data-table tr:hover {
    background-color: #f5f7fa;
}

.table-info {
    color: #666;
    font-size: 14px;
    text-align: right;
}

.no-data {
    text-align: center;
    padding: 40px;
    color: #999;
    font-size: 16px;
}

.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.loading-text {
    margin-top: 10px;
    color: #666;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 趋势分析样式 */
.analysis-container {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 24px;
    margin: 20px;
}

.analysis-header {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    align-items: center;
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.trend-chart {
    height: 400px;
    margin: 24px 0;
    background: #f8f9fa;
    border-radius: 8px;
    padding: 16px;
}

.trend-analysis {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 16px;
    margin-top: 24px;
}

.trend-analysis h3 {
    color: #2c3e50;
    margin: 0 0 16px 0;
    font-size: 18px;
}

.trend-analysis p {
    color: #34495e;
    line-height: 1.6;
    white-space: pre-line;
    margin: 0;
}

/* 健康评分样式 */
.score-display {
    display: flex;
    gap: 32px;
    margin-top: 0;
    padding: 24px 0 0 0;
    background: none;
    border-radius: 0;
    box-shadow: none;
}

.score-circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4CAF50, #8BC34A);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
}

.score-value {
    font-size: 40px;
    font-weight: bold;
    line-height: 1;
}

.score-label {
    font-size: 15px;
    margin-top: 8px;
}

.score-analysis {
    flex: 1;
    padding: 0 0 0 32px;
    background: none;
    border-radius: 0;
}

.score-analysis h3 {
    color: #2c3e50;
    margin: 0 0 12px 0;
    font-size: 17px;
}

.score-analysis p {
    color: #34495e;
    line-height: 1.7;
    white-space: pre-line;
    margin: 0;
}

/* 数据对比分析样式 */
.comparison-container {
    padding: 20px;
}

.comparison-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.comparison-chart {
    height: 400px;
    width: 100%;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.comparison-summary {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.comparison-summary h3 {
    color: #2c3e50;
    margin: 0 0 16px 0;
    font-size: 18px;
}

.summary-content {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
}

.summary-item {
    flex: 1;
    min-width: 200px;
}

.summary-item .label {
    color: #666;
    margin-right: 8px;
}

.summary-item .value {
    color: #2c3e50;
    font-weight: bold;
    font-size: 18px;
}

.age-range-select {
    padding: 8px 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    font-size: 14px;
    color: #606266;
    background-color: #fff;
    min-width: 120px;
}

.age-range-select:focus {
    border-color: #409eff;
    outline: none;
}

.comparison-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.comparison-chart {
    height: 400px;
    width: 100%;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.no-data {
    text-align: center;
    padding: 40px;
    color: #999;
    font-size: 16px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 异常人群排名样式 */
.abnormal-ranking-container {
    padding: 20px;
}

.filter-section {
    margin-bottom: 20px;
    padding: 0 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.indicator-select {
    padding: 8px 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    font-size: 14px;
    color: #606266;
    background-color: #fff;
    min-width: 200px;
}

.indicator-select:focus {
    border-color: #409eff;
    outline: none;
}

.action-button {
    padding: 8px 20px;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.action-button:hover {
    background-color: #66b1ff;
}

.action-button:disabled {
    background-color: #a0cfff;
    cursor: not-allowed;
}

.abnormal-content {
    margin-top: 20px;
}

.table-info {
    margin-top: 20px;
    padding: 10px;
    background-color: #f5f7fa;
    border-radius: 4px;
    text-align: center;
    color: #606266;
}

.date-range-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}

.date-inputs {
    display: flex;
    align-items: center;
    gap: 8px;
}

.quick-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.quick-button {
    padding: 6px 12px;
    background-color: #f0f2f5;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    color: #606266;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.quick-button:hover {
    background-color: #e6e8eb;
    color: #409eff;
    border-color: #c6e2ff;
}

.quick-button.active {
    background-color: #ecf5ff;
    color: #409eff;
    border-color: #409eff;
    font-weight: 500;
}

.quick-button.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #409eff;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        transform: scaleX(0);
    }
    to {
        transform: scaleX(1);
    }
}

.no-data-cell {
    text-align: center;
    color: #999;
    padding: 20px;
    font-style: italic;
}

.reference-range {
    cursor: pointer;
    color: #409eff;
    text-decoration: underline;
    transition: color 0.3s;
}

.reference-range:hover {
    color: #66b1ff;
}
</style> 