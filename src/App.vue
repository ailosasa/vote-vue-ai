<template>
  <div class="app-container">
    <h1>人员综合评分系统</h1>

    <div class="vote-form">
      <div class="form-tip">
        请对以下人员的10项指标进行打分（每项 0–10 分），完成后点击提交。
      </div>

      <div v-for="person in evaluatedPersons" :key="person.name" class="person-section">
        <h3>{{ person.name }}</h3>
        <div class="score-grid">
          <div v-for="item in scoreItems" :key="item.key" class="score-item">
            <label>{{ item.label }}：</label>
            <input
                type="number"
                v-model.number="person.scores[item.key]"
                min="0"
                max="10"
                required
                @input="validateScore(person, item.key)"
            >
          </div>
        </div>
      </div>

      <button
          class="submit-btn"
          @click="submitAllVotes"
          :disabled="isSubmitting || !isFormValid"
      >
        {{ isSubmitting ? '提交中...' : '提交所有评分' }}
      </button>

      <div v-if="message" class="message {{ messageType }}">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { supabase } from './utils/supabase'

const evaluatedPersons = ref([
  { name: '韩玉彪', scores: {} },
  { name: '蔡镇', scores: {} },
  { name: '李海涛', scores: {} },
  { name: '孙长昕', scores: {} },
  { name: '张烈', scores: {} },
  { name: '傅俊丰', scores: {} },
  { name: '丁占峰', scores: {} }
])

const scoreItems = ref([
  { key: 'political_leadership', label: '政治引领' },
  { key: 'team_building', label: '班子建设' },
  { key: 'harmonious_stability', label: '和谐稳定' },
  { key: 'integrity_in_employment', label: '廉洁从业' },
  { key: 'style_discipline', label: '作风纪律' },
  { key: 'grassroots_organizations', label: '基层组织' },
  { key: 'party_member_team', label: '党员队伍' },
  { key: 'mass_organizations', label: '群团组织' },
  { key: 'steady_development', label: '稳健发展' },
  { key: 'unit_image', label: '单位形象' }
])

// 默认分数改为 0
evaluatedPersons.value.forEach(person => {
  scoreItems.value.forEach(item => {
    person.scores[item.key] = 0
  })
})

const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')

const isFormValid = computed(() => {
  for (const person of evaluatedPersons.value) {
    for (const item of scoreItems.value) {
      const score = person.scores[item.key]
      if (isNaN(score) || score < 0 || score > 10) {
        return false
      }
    }
  }
  return true
})

// 验证 0–10
const validateScore = (person, key) => {
  let score = person.scores[key]
  if (isNaN(score)) score = 0
  if (score < 0) score = 0
  if (score > 10) score = 10
  person.scores[key] = score
}

// 批量提交7条
const submitAllVotes = async () => {
  try {
    isSubmitting.value = true
    message.value = ''

    const voteData = evaluatedPersons.value.map(person => ({
      evaluated_person: person.name,
      political_leadership: person.scores.political_leadership,
      team_building: person.scores.team_building,
      harmonious_stability: person.scores.harmonious_stability,
      integrity_in_employment: person.scores.integrity_in_employment,
      style_discipline: person.scores.style_discipline,
      grassroots_organizations: person.scores.grassroots_organizations,
      party_member_team: person.scores.party_member_team,
      mass_organizations: person.scores.mass_organizations,
      steady_development: person.scores.steady_development,
      unit_image: person.scores.unit_image
    }))

    const { error } = await supabase
        .from('vote_records')
        .insert(voteData)

    if (error) throw error

    message.value = '所有评分提交成功！'
    messageType.value = 'success'
    evaluatedPersons.value.forEach(person => {
      scoreItems.value.forEach(item => {
        person.scores[item.key] = 0
      })
    })

  } catch (error) {
    message.value = `提交失败：${error.message}`
    messageType.value = 'error'
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
  font-family: "Microsoft YaHei", sans-serif;
}

.vote-form {
  margin-top: 20px;
  padding: 30px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.form-tip {
  margin-bottom: 20px;
  padding: 10px;
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  color: #1e40af;
  font-size: 14px;
}

.person-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.person-section h3 {
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #3b82f6;
  color: #1e3a8a;
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.score-item {
  display: flex;
  flex-direction: column;
}

.score-item label {
  margin-bottom: 6px;
  font-size: 14px;
  color: #374151;
}

.score-item input {
  padding: 8px 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.score-item input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.2);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 6px;
  text-align: center;
}

.success {
  background: #dcfce7;
  color: #166534;
}

.error {
  background: #fee2e2;
  color: #b91c1c;
}

@media (max-width: 768px) {
  .score-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>