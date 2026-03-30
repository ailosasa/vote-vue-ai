import os
import json
import re

# ====================== 【请修改这里】核心配置 ======================
# 替换为你的【总根文件夹路径】（包含所有部门文件夹的顶级目录）
# Windows路径示例：r"D:\公司资料\2025述职报告"
# Mac/Linux路径示例："/Users/xxx/公司资料/2025述职报告"
ROOT_FOLDER = r"./"
# ==================================================================

# 正则表达式：精准匹配文件名格式，提取括号内的人名
# 匹配规则：2025年度工作述职报告（任意字符）.pdf
NAME_PATTERN = re.compile(r"2025年度工作述职报告（(.+?)）\.pdf", re.IGNORECASE)

# 存储最终结果：key=人名，value=文件相对路径
person_report_map = {}

# 递归遍历根文件夹下的所有文件/子文件夹
for current_dir, _, file_list in os.walk(ROOT_FOLDER):
    for file_name in file_list:
        # 匹配述职报告的命名格式
        match_result = NAME_PATTERN.match(file_name)
        if match_result:
            # 提取括号内的人名（去除首尾多余空格）
            person_name = match_result.group(1).strip()
            # 拼接文件完整路径
            full_path = os.path.join(current_dir, file_name)
            # 计算【相对路径】（相对于根文件夹，符合你的要求）
            relative_path = os.path.relpath(full_path, ROOT_FOLDER)

            # 处理重名情况（不同部门同名员工，会提示并覆盖）
            if person_name in person_report_map:
                print(f"⚠️  警告：发现重名 {person_name}，已更新路径\n旧路径：{person_report_map[person_name]}\n新路径：{relative_path}\n")

            # 存入映射字典
            person_report_map[person_name] = relative_path

# 将结果保存为JSON文件（保存在根文件夹中）
json_save_path = os.path.join(ROOT_FOLDER, "述职报告人员映射.json")
with open(json_save_path, "w", encoding="utf-8") as json_file:
    # ensure_ascii=False：保证中文正常显示；indent=4：格式化JSON，方便查看
    json.dump(person_report_map, json_file, ensure_ascii=False, indent=4)

# 执行完成提示
print("="*50)
print(f"✅ 遍历完成！共匹配到 {len(person_report_map)} 份述职报告")
print(f"✅ 映射文件已保存至：{json_save_path}")
print("="*50)