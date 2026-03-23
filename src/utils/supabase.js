// src/utils/supabase.js
import { createClient } from '@supabase/supabase-js'

// 从环境变量获取配置
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// 创建并导出Supabase客户端（全局复用）
export const supabase = createClient(supabaseUrl, supabaseAnonKey)