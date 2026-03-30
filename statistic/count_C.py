# -*- coding: utf-8 -*-
import csv
from collections import defaultdict

def analyze_vote_data():
    # 配置文件路径
    input_file = "vote_records_rows.csv"
    output_file = "投票统计结果.csv"

    # 统计数据结构：{人名: {票型: {票数:count, 总分:total}}}
    stats = defaultdict(lambda: {
        "A": {"count": 0, "total": 0},
        "B": {"count": 0, "total": 0},
        "C": {"count": 0, "total": 0}
    })

    # 分数列索引（根据你的CSV表头确定）
    score_columns = [
        3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ]

    try:
        # 读取原始投票数据
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头

            for row in reader:
                try:
                    # 提取核心数据
                    person = row[1].strip()          # 被评价人
                    ticket_type = row[2].strip()     # 票型 A/B/C

                    # 计算当前行的总分
                    total = 0
                    for idx in score_columns:
                        score = float(row[idx].strip())
                        total += score

                    # 累加统计数据
                    if ticket_type in ["A", "B", "C"]:
                        stats[person][ticket_type]["count"] += 1
                        stats[person][ticket_type]["total"] += total

                except Exception as e:
                    print(f"跳过异常行：{row}，错误：{str(e)}")

        # ===================== 输出统计结果 =====================
        print("=" * 80)
        print("📊 投票数据统计结果（按人员+票型）")
        print("=" * 80)
        print(f"{'姓名':<8}{'票型':<6}{'票数':<8}{'总分':<12}{'平均分':<10}")
        print("-" * 80)

        # 保存统计结果到CSV
        with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["被评价人", "票型", "票数", "总分", "平均分"])

            # 遍历每个人的统计数据
            for person, types in stats.items():
                for t in ["A", "B", "C"]:
                    count = types[t]["count"]
                    total = round(types[t]["total"], 2)
                    avg = round(total / count, 2) if count > 0 else 0

                    # 控制台打印
                    print(f"{person:<8}{t:<6}{count:<8}{total:<12}{avg:<10}")
                    # 写入文件
                    writer.writerow([person, t, count, total, avg])

        print("=" * 80)
        print(f"✅ 统计完成！结果已保存至：{output_file}")
        print("💡 可用Excel直接打开统计文件进行分析")

    except FileNotFoundError:
        print(f"❌ 错误：未找到文件 {input_file}，请将文件放在同一目录下")
    except Exception as e:
        print(f"❌ 程序异常：{str(e)}")

if __name__ == "__main__":
    analyze_vote_data()