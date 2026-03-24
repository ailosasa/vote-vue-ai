# -*- coding: utf-8 -*-
"""
Word 批量转 PDF 工具
功能：自动转换当前目录下所有 .docx 文件为同名 PDF
使用：放在Word文件所在文件夹，直接运行
"""
import os
import win32com.client as win32
from pathlib import Path

def docx_to_pdf():
    # 获取当前脚本所在的文件夹（就是你的Word文件目录）
    current_dir = Path(__file__).parent
    print(f"✅ 当前工作目录：{current_dir}")
    print("="*50)

    # 启动Word程序（后台运行，不显示窗口）
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # 关闭弹窗警告

    try:
        # 遍历当前目录所有文件
        for file in os.listdir(current_dir):
            # 只处理 .docx 文件，跳过临时文件（~$开头）
            if file.endswith(".docx") and not file.startswith("~$"):
                docx_path = os.path.join(current_dir, file)
                pdf_path = os.path.splitext(docx_path)[0] + ".pdf"

                print(f"正在转换：{file}")
                
                # 打开Word文件
                doc = word.Documents.Open(docx_path)
                # 保存为PDF（格式代码：17 代表PDF）
                doc.SaveAs(pdf_path, FileFormat=17)
                # 关闭文档
                doc.Close()
                
                print(f"✅ 转换完成：{Path(pdf_path).name}")
                print("-"*30)

        print("\n🎉 全部转换完成！")

    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        print("💡 请检查：1.已安装Word/WPS 2.文件未被占用 3.不是.doc旧格式")

    finally:
        # 彻底关闭Word进程（防止后台残留）
        word.Quit()

if __name__ == "__main__":
    docx_to_pdf()
    input("\n按回车键退出...")