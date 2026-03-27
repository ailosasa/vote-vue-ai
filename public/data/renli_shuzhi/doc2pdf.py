import os
import win32com.client as win32

# 【修改这里】填入你的文件夹路径
folder_path = r"./"

# 初始化Word
word = win32.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0  # 关闭弹窗提示

# 遍历转换所有doc/docx
for filename in os.listdir(folder_path):
    if filename.lower().endswith((".doc", ".docx")):
        file_path = os.path.abspath(os.path.join(folder_path, filename))
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"
        
        try:
            # 打开Word文件
            doc = word.Documents.Open(file_path)
            # 另存为PDF
            doc.SaveAs(pdf_path, FileFormat=17)
            doc.Close()
            print(f"✅ 转换成功：{filename}")
        except Exception as e:
            print(f"❌ 转换失败：{filename}，错误：{str(e)}")

# 退出Word
word.Quit()
print("\n🎉 所有文件转换完成！")