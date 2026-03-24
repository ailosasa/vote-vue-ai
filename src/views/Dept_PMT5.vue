<template>
  <div class="app-container">
    <h1>{{ data.deptName }} 综合评价评分</h1>
    <div class="vote-form">
      <div class="form-tip">
        ✅ 专业技术人员：每项 0-25 分 |
        ✅ 一般管理人员：每项 0-10 分 |
        🚫 同一IP仅可提交1次
      </div>

      <!-- 板块1：专业技术人员（每项最高25分） -->
      <div class="section">
        <h3>专业技术人员评分</h3>
        <div v-for="name in data.technicalStaff" :key="name" class="person-box">
          <!-- 姓名 + 预览按钮 -->
          <div class="person-header">
            <span>{{ name }}</span>
            <button class="preview-btn" @click="openReport(DEPT, name)">查看述职报告</button>
          </div>
          <div class="score-items">
            <div>职业道德<input v-model.number="tech[name].moral" @input="calcTech(name)" min="0" max="25"></div>
            <div>工作作风<input v-model.number="tech[name].work_style" @input="calcTech(name)" min="0" max="25"></div>
            <div>担当作为<input v-model.number="tech[name].responsibility" @input="calcTech(name)" min="0" max="25"></div>
            <div>廉洁自律<input v-model.number="tech[name].integrity" @input="calcTech(name)" min="0" max="25"></div>
          </div>
          <div class="total">总分：{{ techTotal[name] }}</div>
        </div>
      </div>

      <!-- 板块2：一般管理人员（每项最高10分） -->
      <div class="section">
        <h3>一般管理人员评分</h3>
        <div v-for="name in data.managementStaff" :key="name" class="person-box">
          <!-- 姓名 + 预览按钮 -->
          <div class="person-header">
            <span>{{ name }}</span>
            <button class="preview-btn" @click="openReport(DEPT, name)">查看述职报告</button>
          </div>
          <div class="score-items grid-10">
            <div>政治能力<input v-model.number="manage[name].political_ability" @input="calcManage(name)" min="0" max="10"></div>
            <div>政治表现<input v-model.number="manage[name].political_performance" @input="calcManage(name)" min="0" max="10"></div>
            <div>党建责任<input v-model.number="manage[name].party_duty" @input="calcManage(name)" min="0" max="10"></div>
            <div>专业素养<input v-model.number="manage[name].professional" @input="calcManage(name)" min="0" max="10"></div>
            <div>领导能力<input v-model.number="manage[name].leadership" @input="calcManage(name)" min="0" max="10"></div>
            <div>学习创新<input v-model.number="manage[name].innovation" @input="calcManage(name)" min="0" max="10"></div>
            <div>履职成效<input v-model.number="manage[name].performance" @input="calcManage(name)" min="0" max="10"></div>
            <div>担当作为<input v-model.number="manage[name].act" @input="calcManage(name)" min="0" max="10"></div>
            <div>作风形象<input v-model.number="manage[name].style_image" @input="calcManage(name)" min="0" max="10"></div>
            <div>廉洁从业<input v-model.number="manage[name].integrity_work" @input="calcManage(name)" min="0" max="10"></div>
          </div>
          <div class="total">总分：{{ manageTotal[name] }}</div>
        </div>
      </div>

      <button class="submit-btn" @click="submitAll" :disabled="submitting">{{ submitting ? '提交中...' : '提交全部评分' }}</button>
      <div v-if="msg" class="message" :class="type">{{ msg }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { supabase } from '../utils/supabase'
import { getClientIP } from '../utils/ip'
import data from '../data/dept_PMT5.json'

const DEPT = data.deptName
const techPersons = data.technicalStaff
const managePersons = data.managementStaff

// 初始化评分数据
const tech = reactive({})
const techTotal = reactive({})
techPersons.forEach(n => tech[n] = { moral:0, work_style: 0, responsibility: 0, integrity: 0})
techPersons.forEach(n => techTotal[n] = 0)

const manage = reactive({})
const manageTotal = reactive({})
managePersons.forEach(n => manage[n] = {
  political_ability: 0, political_performance: 0, party_duty: 0, professional: 0, leadership: 0,
  innovation: 0, performance: 0, act: 0, style_image: 0, integrity_work: 0
})
managePersons.forEach(n => manageTotal[n] = 0)

const submitting = ref(false)
const msg = ref('')
const type = ref('')

// 计算总分（仅展示）
const calcTech = (name) => {
  const s = tech[name]
  techTotal[name] = s.moral + s.work_style + s.responsibility + s.integrity
}
const calcManage = (name) => {
  const s = manage[name]
  manageTotal[name] = s.political_ability + s.political_performance + s.party_duty + s.professional + s.leadership + s.innovation + s.performance + s.act + s.style_image + s.integrity_work
}

// =============================================
// 🔥 核心：打开述职报告（在线预览）
// =============================================
const openReport = (deptName, personName) => {
  // 自动匹配部门文件夹名称
  const deptFolder = 'PMT5_shuzhi'
  // 拼接文件公网地址（部署后自动生效）
  const fileUrl = `https://raw.githubusercontent.com/ailosasa/vote-vue-ai/main/public/data/${deptFolder}/2025年度工作述职报告（${personName}）.docx`
  // 微软官方预览地址
  const previewUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(fileUrl)}`
  // 新标签页打开
  window.open(previewUrl, '_blank')
}

// 提交逻辑
const submitAll = async () => {
  submitting.value = true
  msg.value = ''
  const ip = await getClientIP()

  try {
    const {data: hasTech} = await supabase.from('tech_scores').select('*').eq('dept_name', DEPT).eq('ip', ip)
    const {data: hasManage} = await supabase.from('manage_scores').select('*').eq('dept_name', DEPT).eq('ip', ip)
    if (hasTech.length > 0 || hasManage.length > 0) throw new Error('当前IP已提交，不可重复提交')

    const techData = techPersons.map(n => ({
      dept_name: DEPT,
      person_name: n, ...tech[n],
      total_score: techTotal[n],
      ip
    }))
    const manageData = managePersons.map(n => ({
      dept_name: DEPT,
      person_name: n, ...manage[n],
      total_score: manageTotal[n],
      ip
    }))

    await supabase.from('tech_scores').insert(techData)
    await supabase.from('manage_scores').insert(manageData)

    msg.value = '提交成功！'
    type.value = 'success'
  } catch (err) {
    msg.value = err.message
    type.value = 'error'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
  font-family: Microsoft YaHei
}

.vote-form {
  padding: 25px;
  background: #f9fafb;
  border-radius: 8px
}

.form-tip {
  padding: 12px;
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  margin-bottom: 20px
}

.section {
  margin-bottom: 30px
}

.person-box {
  padding: 15px;
  background: white;
  border-radius: 6px;
  margin-bottom: 15px
}

/* 人员头部：姓名 + 按钮 */
.person-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px
}

.preview-btn {
  padding: 4px 10px;
  background: #165DFF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer
}

.preview-btn:hover {
  background: #0E42D2
}

.score-items {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 10px 0
}

.grid-10 {
  display: grid;
  grid-template-columns:repeat(5, 1fr);
  gap: 8px
}

input {
  width: 70px;
  padding: 4px;
  margin-left: 5px
}

.total {
  color: #dc2626;
  font-weight: bold
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px
}

.message {
  padding: 12px;
  margin-top: 15px;
  text-align: center
}

.success {
  background: #dcfce7
}

.error {
  background: #fee2e2
}
</style>