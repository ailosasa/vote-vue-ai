<template>
  <div class="app-container">
    <h1>{{ data.deptName }} PMT5综合评价评分</h1>
    <div class="vote-form">
      <!-- 修正提示语：匹配最新评分规则 -->
      <div class="form-tip">
        ✅ 专业技术人员：4项 × 25分 = 总分100分 |
        ✅ 一般管理人员：10项 × 10分 = 总分100分 |
        🚫 同一IP仅可提交1次
      </div>

      <!-- 板块1：专业技术人员（每项最高25分） -->
      <div class="section">
        <h3>专业技术人员评分</h3>
        <div v-for="name in data.technicalStaff" :key="name" class="person-box">
          <span>{{ name }}</span>
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
          <span>{{ name }}</span>
          <div class="score-items grid-10">
            <div>政治能力<input v-model.number="manage[name].political_ability" @input="calcManage(name)" min="0" max="10"></div>
            <div>政治表现<input v-model.number="manage[name].political_performance" @input="calcManage(name)" min="0" max="10"></div>
            <div>党建责任<input v-model.number="manage[name].party_duty" @input="calcManage(name)" min="0" max="10"></div>
            <div>专业素养<input v-model.number="manage[name].professional" @input="calcManage(name)" min="0" max="10"></div>
            <div>领导能力<input v-model.number="manage[name].leadership" @input="calcManage(name)" min="0" max="10">
            </div>
            <div>学习创新<input v-model.number="manage[name].innovation" @input="calcManage(name)" min="0" max="10">
            </div>
            <div>履职成效<input v-model.number="manage[name].performance" @input="calcManage(name)" min="0" max="10">
            </div>
            <div>担当作为<input v-model.number="manage[name].act" @input="calcManage(name)" min="0" max="10"></div>
            <div>作风形象<input v-model.number="manage[name].style_image" @input="calcManage(name)" min="0" max="10">
            </div>
            <div>廉洁从业<input v-model.number="manage[name].integrity_work" @input="calcManage(name)" min="0" max="10">
            </div>
          </div>
          <div class="total">总分：{{ manageTotal[name] }}</div>
        </div>
      </div>

      <button class="submit-btn" @click="submitAll" :disabled="submitting">{{
          submitting ? '提交中...' : '提交全部评分'
        }}
      </button>
      <div v-if="msg" class="message" :class="type">{{ msg }}</div>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive} from 'vue'
import {supabase} from '../utils/supabase'
import {getClientIP} from '../utils/ip'
// 从JSON文件读取人员数据
import data from '../data/dept_PMT5.json'

const DEPT = data.deptName
const techPersons = data.technicalStaff
const managePersons = data.managementStaff

// 初始化技术人员评分
const tech = reactive({})
const techTotal = reactive({})
techPersons.forEach(n => tech[n] = {moral: 0, work_style: 0, responsibility: 0, integrity: 0})
techPersons.forEach(n => techTotal[n] = 0)

// 初始化管理人员评分
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

// 计算技术人员总分
const calcTech = (name) => {
  const s = tech[name]
  techTotal[name] = s.moral + s.work_style + s.responsibility + s.integrity
}

// 计算管理人员总分
const calcManage = (name) => {
  const s = manage[name]
  manageTotal[name] = s.political_ability + s.political_performance + s.party_duty + s.professional + s.leadership + s.innovation + s.performance + s.act + s.style_image + s.integrity_work
}

// 提交逻辑（不变）
const submitAll = async () => {
  submitting.value = true
  msg.value = ''
  const ip = await getClientIP()

  try {

    // 批量提交至两张独立表
    const techData = techPersons.map(n => ({dept_name: DEPT, person_name: n, ...tech[n], total_score: 100, ip}))
    const manageData = managePersons.map(n => ({dept_name: DEPT, person_name: n, ...manage[n], total_score: 100, ip}))
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