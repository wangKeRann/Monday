<template>
    <div class="layout-root">
        <!-- 全局顶栏 -->
        <div class="global-header">
            <div class="header-left">健康管理系统</div>
            <div v-if="user" class="user-info">
                <img :src="user.avatar_url" :alt="user.username" class="avatar">
                <div class="user-details">
                    <h2>{{ user.login }}</h2>
                </div>
                <button @click="handleLogout" class="logout-button">退出</button>
            </div>
        </div>

        <!-- 主内容区 -->
        <div class="main-area">
            <div class="content-area">
                <div class="content-actions">
                    <template v-if="['历史体检报告', '关键指标检索', '报告详情', '指标趋势分析', '数据对比分析'].includes(activeNav)">
                        <template v-if="activeNav === '历史体检报告'">
                            <div class="date-range-container">
                                <div class="date-inputs">
                                    <div class="input-group">
                                        <label>开始日期：</label>
                                        <input type="date" v-model="startDate" class="date-input" />
                                    </div>
                                    <div class="input-group">
                                        <label>结束日期：</label>
                                        <input type="date" v-model="endDate" class="date-input" />
                                    </div>
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
                                    <template v-if="selectedRecord && selectedRecord.blood_routine">
                                        <tr v-for="(value, key) in selectedRecord.blood_routine" :key="key">
                                            <td>{{ getIndicatorLabel('blood_routine', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in INDICATOR_NAMES.blood_routine" :key="item.value">
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
                                    <template v-if="selectedRecord && selectedRecord.urine_routine">
                                        <tr v-for="(value, key) in selectedRecord.urine_routine" :key="key">
                                            <td>{{ getIndicatorLabel('urine_routine', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in INDICATOR_NAMES.urine_routine" :key="item.value">
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
                                    <template v-if="selectedRecord && selectedRecord.biochemistry">
                                        <tr v-for="(value, key) in selectedRecord.biochemistry" :key="key">
                                            <td>{{ getIndicatorLabel('biochemistry', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in INDICATOR_NAMES.biochemistry" :key="item.value">
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
                                    <template v-if="selectedRecord && selectedRecord.liver_fibrosis">
                                        <tr v-for="(value, key) in selectedRecord.liver_fibrosis" :key="key">
                                            <td>{{ getIndicatorLabel('liver_fibrosis', key) }}</td>
                                            <td :class="getValueClass(value, key)">{{ value }}</td>
                                            <td class="reference-range" @click="showArticle(key)">{{ getReferenceRange(key) }}</td>
                                            <td :class="getStatusClass(value, key)">{{ getStatus(value, key) }}</td>
                                        </tr>
                                    </template>
                                    <template v-else>
                                        <tr v-for="item in INDICATOR_NAMES.liver_fibrosis" :key="item.value">
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

        <!-- 底部导航栏 -->
        <div class="mobile-nav">
            <div v-for="section in navSections" :key="section.title" class="nav-section">
                <div v-for="item in section.items" 
                     :key="item.label"
                     :class="['nav-item', { active: activeNav === item.label }]"
                     @click="selectNav(item.label)">
                    <i class="nav-icon">{{ item.icon }}</i>
                    <span>{{ item.label }}</span>
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
import { REFERENCE_RANGES, INDICATOR_NAMES, SCORE_WEIGHTS, ARTICLE_MAPPING, QUICK_OPTIONS, NAV_SECTIONS } from '../config/constants';
import { getReferenceRange, getStatus, getStatusClass, getValueClass, getIndicatorLabel } from '../utils/healthUtils';
import { handleLogout, handleRecordIdClick, showArticle, handleChartResize } from '../utils/eventHandlers';

export default {
    name: 'Home',
    data() {
        return {
            user: null,
            activeNav: '历史体检报告',
            navSections: NAV_SECTIONS,
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
            selectedQuickType: '',
            quickOptions: QUICK_OPTIONS,
            INDICATOR_NAMES
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
        window.addEventListener('resize', () => handleChartResize(this.chartInstance, this.chartReady));
    },
    beforeDestroy() {
        window.removeEventListener('resize', () => handleChartResize(this.chartInstance, this.chartReady));
        if (this.chartInstance) {
            this.chartInstance.dispose();
            this.chartInstance = null;
        }
    },
    methods: {
        handleLogout: () => handleLogout(this.$router),
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
                        this.chartInstance.resize(); // 强制触发一次resize
                    }
                });
                this.chartReady = true;
            } else {
                alert(result.error);
            }
            this.loading = false;
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
        showArticle,
        getReferenceRange,
        getStatus,
        getStatusClass,
        getValueClass,
        getIndicatorLabel
    }
};
</script>

<style>
@import '../assets/styles/home.css';
</style> 