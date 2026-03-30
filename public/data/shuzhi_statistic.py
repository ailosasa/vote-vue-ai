import os
import json
import re

# ====================== 【请修改这里】核心配置 ======================
# 替换为你的【总根文件夹路径】
ROOT_FOLDER = r"./"
# ==================================================================

# ✅ 已修改正则：适配两种文件名格式
# 匹配：2025年度工作述职报告（xxx）.pdf  +  2025年度述职报告（xxx）.pdf
# (工作)? 表示“工作”两个字 可选（0次或1次）
NAME_PATTERN = re.compile(r"2025年度(工作)?述职报告（(.+?)）\.pdf", re.IGNORECASE)

# 存储最终结果：key=人名，value=文件相对路径
person_report_map = {}

# 递归遍历根文件夹下的所有文件/子文件夹
for current_dir, _, file_list in os.walk(ROOT_FOLDER):
    for file_name in file_list:
        # 匹配述职报告的命名格式
        match_result = NAME_PATTERN.match(file_name)
        if match_result:
            # 提取括号内的人名（去除首尾多余空格）
            person_name = match_result.group(2).strip()  # 分组索引改为2，对应正则里的第二个括号
            # 拼接文件完整路径
            full_path = os.path.join(current_dir, file_name)
            # 计算【相对路径】
            relative_path = os.path.relpath(full_path, ROOT_FOLDER)

            # 处理重名情况
            if person_name in person_report_map:
                print(f"⚠️  警告：发现重名 {person_name}，已更新路径\n旧路径：{person_report_map[person_name]}\n新路径：{relative_path}\n")
            
            # 存入映射字典
            person_report_map[person_name] = relative_path

# 将结果保存为JSON文件
json_save_path = os.path.join(ROOT_FOLDER, "述职报告人员映射.json")
with open(json_save_path, "w", encoding="utf-8") as json_file:
    json.dump(person_report_map, json_file, ensure_ascii=False, indent=4)

# 执行完成提示
print("="*50)
print(f"✅ 遍历完成！共匹配到 {len(person_report_map)} 份述职报告")
print(f"✅ 映射文件已保存至：{json_save_path}")
print("="*50)