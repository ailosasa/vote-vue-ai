<template>
  <div class="app-container">
    <h1>匿名投票评分系统</h1>

    <!-- 评分表单 -->
    <div class="vote-form">
      <!-- 选择被评人员 -->
      <div class="form-item">
        <label>选择被评人员：</label>
        <select v-model="selectedPerson" required>
          <option value="">请选择</option>
          <option v-for="person in evaluatedPersons" :key="person" :value="person">
            {{ person }}
          </option>
        </select>
      </div>

      <!-- 多个评分项打分 -->
      <div class="score-items">
        <div v-for="item in scoreItems" :key="item" class="score-item">
          <label>{{ item }}（1-5分）：</label>
          <input
              type="number"
              v-model="scores[item]"
              min="1"
              max="5"
              required
          >
        </div>
      </div>

      <!-- 提交按钮 -->
      <button
          class="submit-btn"
          @click="submitVote"
          :disabled="isSubmitting || !selectedPerson"
      >
        {{ isSubmitting ? '提交中...' : '提交评分' }}
      </button>

      <!-- 提交结果提示 -->
      <div v-if="message" class="message {{ messageType }}">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from './utils/supabase'

// 定义被评人员列表（可根据需求修改）
const evaluatedPersons = ref(['张三', '李四', '王五'])
// 定义评分项列表（可根据需求修改）
const scoreItems = ref(['工作态度', '专业能力', '沟通效率', '团队协作'])

// 表单绑定数据
const selectedPerson = ref('')
const scores = ref(Object.fromEntries(scoreItems.value.map(item => [item, 1]))) // 默认每项1分
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('') // success/error

// 提交评分到Supabase
const submitVote = async () => {
  try {
    isSubmitting.value = true
    message.value = ''

    // 遍历所有评分项，逐个提交（也可批量提交，这里简化）
    for (const item of scoreItems.value) {
      const score = scores.value[item]
      // 插入数据到Supabase的vote_records表
      const { error } = await supabase
          .from('vote_records')
          .insert([
            {
              evaluated_person: selectedPerson.value,
              score_item: item,
              score: Number(score)
            }
          ])

      if (error) throw error
    }

    // 提交成功提示
    message.value = '评分提交成功！'
    messageType.value = 'success'
    // 重置表单
    selectedPerson.value = ''
    scores.value = Object.fromEntries(scoreItems.value.map(item => [item, 1]))
  } catch (error) {
    // 提交失败提示
    message.value = `提交失败：${error.message}`
    messageType.value = 'error'
    console.error('提交评分失败：', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.app-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 0 20px;
  font-family: Arial, sans-serif;
}

.vote-form {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-item select, .score-item input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.score-items {
  margin-bottom: 20px;
}

.score-item {
  margin-bottom: 15px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #dcfce7;
  color: #166534;
}

.error {
  background-color: #fee2e2;
  color: #b91c1c;
}
</style>