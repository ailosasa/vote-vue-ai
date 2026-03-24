<template>
  <div class="app-container">
    <h1>人员综合评分C类票</h1>
    <div class="vote-form">
      <div class="form-tip">票面类型：C | 打分范围：0-10分</div>
      <!-- 评分区域（和之前完全一致） -->
      <div v-for="person in evaluatedPersons" :key="person.name" class="person-section">
        <h3>{{ person.name }}</h3>
        <div class="score-grid">
          <div v-for="item in scoreItems" :key="item.key" class="score-item">
            <label>{{ item.label }}：</label>
            <input type="number" v-model.number="person.scores[item.key]" min="0" max="10" required @input="validateScore(person, item.key)" />
          </div>
        </div>
      </div>
      <button class="submit-btn" @click="submitAllVotes" :disabled="isSubmitting || !isFormValid">
        {{ isSubmitting ? '提交中...' : '提交C类评分' }}
      </button>
      <div v-if="message" class="message {{ messageType }}">{{ message }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { supabase } from '../utils/supabase'
// 固定配置
const evaluatedPersons = ref([{ name: '韩玉彪', scores: {} },{ name: '蔡镇', scores: {} },{ name: '李海涛', scores: {} },{ name: '孙长昕', scores: {} },{ name: '张烈', scores: {} },{ name: '傅俊丰', scores: {} },{ name: '丁占峰', scores: {} }])
const scoreItems = ref([{ key: 'political_leadership', label: '政治引领' },{ key: 'team_building', label: '班子建设' },{ key: 'harmonious_stability', label: '和谐稳定' },{ key: 'integrity_in_employment', label: '廉洁从业' },{ key: 'style_discipline', label: '作风纪律' },{ key: 'grassroots_organizations', label: '基层组织' },{ key: 'party_member_team', label: '党员队伍' },{ key: 'mass_organizations', label: '群团组织' },{ key: 'steady_development', label: '稳健发展' },{ key: 'unit_image', label: '单位形象' }])
// 默认分数
evaluatedPersons.value.forEach(p => { scoreItems.value.forEach(i => p.scores[i.key] = 0) })
const isSubmitting = ref(false), message = ref(''), messageType = ref('')
// 验证
const isFormValid = computed(() => { for(const p of evaluatedPersons.value){for(const i of scoreItems.value){const s=p.scores[i.key];if(isNaN(s)||s<0||s>10)return false}}return true})
  const validateScore = (p,k)=>{let s=p.scores[k];if(isNaN(s))s=0;if(s<0)s=0;if(s>10)s=10;p.scores[k]=s}
// 提交（自动标记 A 类型）
  const submitAllVotes = async ()=>{
    try{
      isSubmitting.value=true;message.value='';
      const data = evaluatedPersons.value.map(p=>({evaluated_person:p.name,ticket_type:'C',...p.scores}))
      const { error } = await supabase.from('vote_records').insert(data)
      if(error)throw error;message.value='A类评分提交成功！';messageType.value='success'
      evaluatedPersons.value.forEach(p=>scoreItems.value.forEach(i=>p.scores[i.key]=0))
    }catch(e){message.value=`失败：${e.message}`;messageType.value='error';console.error(e)}
    finally{isSubmitting.value=false}
  }
</script>
<style scoped>
/* 样式和之前完全一致，直接复制 */
.app-container{max-width:1200px;margin:30px auto;padding:0 20px;font-family:Microsoft YaHei,sans-serif}
.vote-form{margin-top:20px;padding:30px;border:1px solid #e5e7eb;border-radius:8px;background:#f9fafb}
.form-tip{margin-bottom:20px;padding:10px;background:#eff6ff;border-left:4px solid #3b82f6;color:#1e40af;font-size:14px}
.person-section{margin-bottom:30px;padding:20px;background:#fff;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.person-section h3{margin:0 0 15px 0;padding-bottom:10px;border-bottom:2px solid #3b82f6;color:#1e3a8a}
.score-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:15px}
.score-item{display:flex;flex-direction:column}
.score-item label{margin-bottom:6px;font-size:14px;color:#374151}
.score-item input{padding:8px 10px;border:1px solid #d1d5db;border-radius:4px;font-size:14px}
.submit-btn{width:100%;padding:12px;background:#2563eb;color:white;border:none;border-radius:6px;font-size:16px;font-weight:600;cursor:pointer}
.submit-btn:disabled{background:#94a3b8;cursor:not-allowed}
.message{margin-top:20px;padding:12px;border-radius:6px;text-align:center}
.success{background:#dcfce7;color:#166534}
.error{background:#fee2e2;color:#b91c1c}
</style>