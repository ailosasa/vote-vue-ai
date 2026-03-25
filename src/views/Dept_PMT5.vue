<template>
  <div class="app-container">
    <h1>{{ data.deptName }} 综合评价评分</h1>
    <div class="vote-form">
      <div class="form-tip">
        ✅ 专业技术人员：每项 0-25 分 |
        ✅ 一般管理人员：每项 0-10 分 |
        🚫 同一IP仅可提交1次
      </div>

      <!-- 专业技术人员 -->
      <div class="section">
        <h3>专业技术人员评分</h3>
        <div v-for="name in data.technicalStaff" :key="name" class="person-box">
          <div class="person-header">
            <span>{{ name }}</span>
            <button class="preview-btn" @click="openReport(name)">查看述职报告</button>
          </div>
          <div class="score-items">
            <div>职业道德<input v-model.number="tech[name].moral" @input="handleTechInput(name, 'moral')" min="0" max="25"></div>
            <div>工作作风<input v-model.number="tech[name].work_style" @input="handleTechInput(name, 'work_style')" min="0" max="25"></div>
            <div>担当作为<input v-model.number="tech[name].responsibility" @input="handleTechInput(name, 'responsibility')" min="0" max="25"></div>
            <div>廉洁自律<input v-model.number="tech[name].integrity" @input="handleTechInput(name, 'integrity')" min="0" max="25"></div>
          </div>
          <div class="total">总分：{{ techTotal[name] }}</div>
        </div>
      </div>

      <!-- 一般管理人员 -->
      <div class="section">
        <h3>一般管理人员评分</h3>
        <div v-for="name in data.managementStaff" :key="name" class="person-box">
          <div class="person-header">
            <span>{{ name }}</span>
            <button class="preview-btn" @click="openReport(name)">查看述职报告</button>
          </div>
          <div class="score-items grid-10">
            <div>政治能力<input v-model.number="manage[name].political_ability" @input="handleManageInput(name, 'political_ability')" min="0" max="10"></div>
            <div>政治表现<input v-model.number="manage[name].political_performance" @input="handleManageInput(name, 'political_performance')" min="0" max="10"></div>
            <div>党建责任<input v-model.number="manage[name].party_duty" @input="handleManageInput(name, 'party_duty')" min="0" max="10"></div>
            <div>专业素养<input v-model.number="manage[name].professional" @input="handleManageInput(name, 'professional')" min="0" max="10"></div>
            <div>领导能力<input v-model.number="manage[name].leadership" @input="handleManageInput(name, 'leadership')" min="0" max="10"></div>
            <div>学习创新<input v-model.number="manage[name].innovation" @input="handleManageInput(name, 'innovation')" min="0" max="10"></div>
            <div>履职成效<input v-model.number="manage[name].performance" @input="handleManageInput(name, 'performance')" min="0" max="10"></div>
            <div>担当作为<input v-model.number="manage[name].act" @input="handleManageInput(name, 'act')" min="0" max="10"></div>
            <div>作风形象<input v-model.number="manage[name].style_image" @input="handleManageInput(name, 'style_image')" min="0" max="10"></div>
            <div>廉洁从业<input v-model.number="manage[name].integrity_work" @input="handleManageInput(name, 'integrity_work')" min="0" max="10"></div>
          </div>
          <div class="total">总分：{{ manageTotal[name] }}</div>
        </div>
      </div>

      <button class="submit-btn" @click="submitAll" :disabled="submitting">{{ submitting ? '提交中...' : '提交全部评分' }}</button>
      <div v-if="msg" class="message" :class="type">{{ msg }}</div>
    </div>
  </div>

  <!-- 原有代码不动，末尾加这个弹窗 -->
  <div v-if="showPdfPreview" class="pdf-modal" @click.self="closePdfPreview">
    <div class="pdf-wrapper">
      <div class="pdf-header">
        <h3>{{ currentPerson }} - 述职报告（禁止下载）</h3>
        <button class="close-btn" @click="closePdfPreview">关闭</button>
      </div>
      <!-- 内嵌PDF，隐藏工具栏+禁用打印 -->
      <iframe
          :src="pdfUrl + '#toolbar=0&navpanes=0&scrollbar=1&statusbar=0&view=FitH'"
          class="pdf-iframe"
          frameborder="0"
          oncontextmenu="return false" <!-- 禁止右键 -->
      onload="this.contentWindow.print=function(){}" <!-- 禁用打印 -->
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { supabase } from '../utils/supabase'
import { getClientIP } from '../utils/ip'
import data from '../data/PMT5.json'

const DEPT = data.deptName
const techPersons = data.technicalStaff
const managePersons = data.managementStaff

// 初始化评分数据
const tech = reactive({})
const techTotal = reactive({})
techPersons.forEach(n => tech[n] = { moral:0, work_style:0, responsibility:0, integrity:0 })
techPersons.forEach(n => techTotal[n] = 0)

const manage = reactive({})
const manageTotal = reactive({})
managePersons.forEach(n => manage[n] = {
  political_ability:0, political_performance:0, party_duty:0, professional:0, leadership:0,
  innovation:0, performance:0, act:0, style_image:0, integrity_work:0
})
managePersons.forEach(n => manageTotal[n] = 0)

const submitting = ref(false)
const msg = ref('')
const type = ref('')

// =============================================
// 🔥 核心：技术人员分数自动校验（0-25分）
// =============================================
const handleTechInput = (name, field) => {
  // 限制分数范围：0 ≤ 分数 ≤25
  tech[name][field] = Math.max(0, Math.min(25, tech[name][field] || 0))
  calcTech(name)
}

// =============================================
// 🔥 核心：管理人员分数自动校验（0-10分）
// =============================================
const handleManageInput = (name, field) => {
  // 限制分数范围：0 ≤ 分数 ≤10
  manage[name][field] = Math.max(0, Math.min(10, manage[name][field] || 0))
  calcManage(name)
}

// 计算总分（仅展示）
const calcTech = (name) => {
  const s = tech[name]
  techTotal[name] = s.moral + s.work_style + s.responsibility + s.integrity
}
const calcManage = (name) => {
  const s = manage[name]
  manageTotal[name] = s.political_ability + s.political_performance + s.party_duty + s.professional + s.leadership + s.innovation + s.performance + s.act + s.style_image + s.integrity_work
}

// PDF 预览控制
const showPdfPreview = ref(false)
const pdfUrl = ref('')
const currentPerson = ref('')

// =============================================
// 🔥 新版：仅预览、禁止下载、禁止右键、禁止打印
// =============================================
const openReport = (personName) => {
  currentPerson.value = personName
  const deptFolder = `$PMT5_shuzhi`
  // 拼接PDF地址
  pdfUrl.value = `${window.location.origin}/data/${deptFolder}/${personName}.pdf`
  // 打开弹窗
  showPdfPreview.value = true
}

// 关闭预览
const closePdfPreview = () => {
  showPdfPreview.value = false
  pdfUrl.value = ''
}

// 提交逻辑（新增：禁止任何人员打满分 100分）
const submitAll = async () => {
  submitting.value = true
  msg.value = ''
  const ip = await getClientIP()

  try {
    // =============================================
    // 🔥 核心新增：禁止任何人员打满分（总分=100 阻止提交）
    // =============================================
    // 检查专业技术人员
    for (const n of techPersons) {
      if (techTotal[n] === 100) {
        throw new Error(`提交失败：【${n}】不能打满分（总分100分），请调整分数！`)
      }
    }
    // 检查一般管理人员
    for (const n of managePersons) {
      if (manageTotal[n] === 100) {
        throw new Error(`提交失败：【${n}】不能打满分（总分100分），请调整分数！`)
      }
    }

    // 2. 批量提交至两张独立表（保留）
    const techData = techPersons.map(n => ({ dept_name: DEPT, person_name: n, ...tech[n], total_score: techTotal[n], ip }))
    const manageData = managePersons.map(n => ({ dept_name: DEPT, person_name: n, ...manage[n], total_score: manageTotal[n], ip }))

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
.app-container{max-width:1200px;margin:30px auto;padding:0 20px;font-family:Microsoft YaHei}
.vote-form{padding:25px;background:#f9fafb;border-radius:8px}
.form-tip{padding:12px;background:#eff6ff;border-left:4px solid #3b82f6;margin-bottom:20px}
.section{margin-bottom:30px}
.person-box{padding:15px;background:white;border-radius:6px;margin-bottom:15px}
.person-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.preview-btn{padding:4px 10px;background:#165DFF;color:white;border:none;border-radius:4px;font-size:12px;cursor:pointer}
.preview-btn:hover{background:#0E42D2}
.score-items{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0}
.grid-10{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
input{width:70px;padding:4px;margin-left:5px}
.total{color:#dc2626;font-weight:bold}
.submit-btn{width:100%;padding:14px;background:#2563eb;color:white;border:none;border-radius:6px;font-size:16px}
.message{padding:12px;margin-top:15px;text-align:center}
.success{background:#dcfce7}
.error{background:#fee2e2}
/* PDF 防下载预览弹窗 */
.pdf-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
}
.pdf-wrapper {
  width: 90%;
  height: 90%;
  background: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.pdf-header {
  padding: 12px 20px;
  background: #2563eb;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-btn {
  background: #fff;
  color: #2563eb;
  border: none;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.pdf-iframe {
  flex: 1;
  width: 100%;
  border: none;
}
</style>