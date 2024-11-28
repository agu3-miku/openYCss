import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont  # 引入tkFont用于设置字体

# 数据文件路径（与脚本文件在同一目录）
DATA_FILE = os.path.join(os.path.dirname(__file__), "storage_data.json")

def create_empty_file_if_not_exists():
    """如果数据文件不存在，则创建一个空的 JSON 文件."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4, ensure_ascii=False)

def load_data():
    """加载数据文件中的内容，并返回数据字典."""
    create_empty_file_if_not_exists()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        messagebox.showerror("错误", "数据文件格式错误或损坏，已创建新文件。")
        create_empty_file_if_not_exists()
        return {}
    except Exception as e:
        messagebox.showerror("错误", f"读取数据文件时发生错误: {e}")
        return {}

def save_data(data):
    """将数据字典保存到数据文件中."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("错误", f"保存数据文件时发生错误: {e}")

def add_item():
    """添加物品的窗口和逻辑处理."""
    def submit():
        room = entry_room.get().strip()
        storage = entry_storage.get().strip()
        items_string = entry_items.get().strip()
        if room and storage and items_string:
            items = [item.strip() for item in items_string.split('；') if item]
            data = load_data()
            existing_items = data.get(room, {}).get(storage, [])
            duplicates = [item for item in items if item in existing_items]

            if duplicates:
                response = messagebox.askyesno("重复物品", f"已存在以下物品：{', '.join(duplicates)}\n是否仍要添加？")
                if not response:
                    return  # 用户选择不添加，直接返回

            data.setdefault(room, {}).setdefault(storage, []).extend(items)
            save_data(data)
            messagebox.showinfo("成功", "物品已成功添加！")
        else:
            messagebox.showwarning("输入错误", "请填写所有字段。")

    add_window = tk.Toplevel(main_menu_window)
    add_window.title("添加物品")

    # 设置字体和背景色
    font = tkFont.Font(family="Helvetica", size=12)
    add_window.configure(bg="white")  # 设置背景为纯白

    tk.Label(add_window, text="房间：", anchor='e', font=font, bg="white").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_room = tk.Entry(add_window, font=font)
    entry_room.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    tk.Label(add_window, text="收纳处：", anchor='e', font=font, bg="white").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_storage = tk.Entry(add_window, font=font)
    entry_storage.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    tk.Label(add_window, text="物品（用中文分号隔开）：", anchor='e', font=font, bg="white").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    entry_items = tk.Entry(add_window, font=font)
    entry_items.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # 扁平化设计的按钮
    tk.Button(add_window, text="提交", command=submit, bg="#4CAF50", fg="white", font=font, relief="flat").grid(row=3, column=0, columnspan=2, pady=10)

def find_item():
    """查找物品的逻辑处理."""
    def search():
        search_term = entry_search.get().strip()
        if search_term:
            data = load_data()
            found_items = {room: {storage: items for storage, items in storages.items() if search_term in items} 
                           for room, storages in data.items()}

            if not any(found_items.values()):
                messagebox.showinfo("查找物品", "未找到任何匹配的物品。")
            else:
                result = json.dumps(found_items, indent=4, ensure_ascii=False)
                messagebox.showinfo("查找结果", result)
        else:
            messagebox.showwarning("输入错误", "请输入要查找的物品。")

    search_window = tk.Toplevel(main_menu_window)
    search_window.title("查找物品")

    font = tkFont.Font(family="Helvetica", size=12)
    search_window.configure(bg="white")

    tk.Label(search_window, text="请输入物品名称：", anchor='e', font=font, bg="white").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_search = tk.Entry(search_window, font=font)
    entry_search.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    tk.Button(search_window, text="搜索", command=search, bg="#4CAF50", fg="white", font=font, relief="flat").grid(row=1, column=0, columnspan=2, pady=10)

def show_statistics():
    """统计信息的逻辑处理."""
    data = load_data()
    total_items = sum(len(storage_items) for storages in data.values() for storage_items in storages.values())
    total_rooms = len(data)
    if total_rooms == 0:
        messagebox.showinfo("统计信息", "当前没有任何数据。")
    else:
        stats_info = f"房间总数: {total_rooms}\n物品总数: {total_items}"
        messagebox.showinfo("统计信息", stats_info)

def open_settings():
    """设置的逻辑处理."""
    settings_window = tk.Toplevel(main_menu_window)
    settings_window.title("设置")

    font = tkFont.Font(family="Helvetica", size=12)
    settings_window.configure(bg="white")

    # 数据文件路径显示和修改
    lbl_file_path = tk.Label(settings_window, text=f"当前数据文件路径：\n{DATA_FILE}", font=font, bg="white")
    lbl_file_path.pack(padx=10, pady=(10, 0))

    def change_file_path():
        new_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if new_path:
            global DATA_FILE
            DATA_FILE = new_path
            lbl_file_path.config(text=f"当前数据文件路径：\n{DATA_FILE}")  # 更新标签显示

    tk.Button(settings_window, text="修改数据文件路径", command=change_file_path, bg="#2196F3", fg="white", font=font, relief="flat").pack(pady=10)

    def clear_data():
        """清空数据文件中的所有数据."""
        if messagebox.askyesno("确认", "您确定要清空所有数据吗？这将删除所有记录！"):
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("成功", "数据已成功清空！")

    tk.Button(settings_window, text="清空数据", command=clear_data, bg="#F44336", fg="white", font=font, relief="flat").pack(pady=10)



def main_menu():
    """创建并显示主菜单."""
    global main_menu_window
    main_menu_window = tk.Toplevel()
    main_menu_window.title("YCss")

    # 设置主菜单的背景色
    main_menu_window.configure(bg="white")  # 设置背景为纯白

    font = tkFont.Font(family="Helvetica", size=12)
    
    tk.Button(main_menu_window, text="添加物品", command=add_item, width=40, bg="#2196F3", fg="white", font=font, relief="flat").grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="查找物品", command=find_item, width=40, bg="#2196F3", fg="white", font=font, relief="flat").grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="统计信息", command=show_statistics, width=40, bg="#2196F3", fg="white", font=font, relief="flat").grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="设置", command=open_settings, width=40, bg="#2196F3", fg="white", font=font, relief="flat").grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    # 设置列的权重，使按钮居中
    main_menu_window.grid_columnconfigure(0, weight=1)

# 创建并显示主菜单窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
main_menu()

root.mainloop()
