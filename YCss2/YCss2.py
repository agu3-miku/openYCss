import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog

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
                # 如果存在重复物品，通知用户
                response = messagebox.askyesno("重复物品", f"已存在以下物品：{', '.join(duplicates)}\n是否仍要添加？")
                if not response:
                    return  # 用户选择不添加，直接返回

            # 添加物品
            data.setdefault(room, {}).setdefault(storage, []).extend(items)
            save_data(data)
            messagebox.showinfo("成功", "物品已成功添加！")
        else:
            messagebox.showwarning("输入错误", "请填写所有字段。")

    add_window = tk.Toplevel(main_menu_window)
    add_window.title("添加物品")

    tk.Label(add_window, text="房间：", anchor='e').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_room = tk.Entry(add_window)
    entry_room.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    tk.Label(add_window, text="收纳处：", anchor='e').grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_storage = tk.Entry(add_window)
    entry_storage.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    tk.Label(add_window, text="物品（用中文分号隔开）：", anchor='e').grid(row=2, column=0, padx=10, pady=10, sticky='e')
    entry_items = tk.Entry(add_window)
    entry_items.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    tk.Button(add_window, text="提交", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

def find_item():
    """查找物品的窗口和逻辑处理."""
    def search():
        room_name = entry_room.get().strip()
        item_name = entry_search.get().strip()
        data = load_data()
        result = "未找到该物品。"
        
        # 查找特定房间或所有房间
        if room_name:
            storages = data.get(room_name, {})
            for storage, items in storages.items():
                if item_name in items:
                    result = f"物品在房间'{room_name}'的收纳处'{storage}'中。"
                    break
        else:
            for room, storages in data.items():
                for storage, items in storages.items():
                    if item_name in items:
                        result = f"物品在房间'{room}'的收纳处'{storage}'中。"
                        break

        messagebox.showinfo("查找结果", result)

    search_window = tk.Toplevel(main_menu_window)
    search_window.title("查找物品")

    tk.Label(search_window, text="房间（可选）：", anchor='e').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_room = tk.Entry(search_window)
    entry_room.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    tk.Label(search_window, text="输入要查找的物品：", anchor='e').grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_search = tk.Entry(search_window)
    entry_search.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    tk.Button(search_window, text="查找", command=search).grid(row=2, column=0, columnspan=2, pady=10)

def show_statistics():
    """显示物品的统计信息."""
    data = load_data()
    room_count = len(data)
    statistics = f"房间总数: {room_count}\n"
    for room, storages in data.items():
        statistics += f"房间: {room}\n"
        for storage, items in storages.items():
            statistics += f"  收纳处: {storage} - {len(items)} 个物品\n"
    messagebox.showinfo("统计信息", statistics)

def clear_data():
    """清空数据的窗口和逻辑处理."""
    def submit():
        option = var.get()
        data = load_data()
        if option == "all":
            os.remove(DATA_FILE)
            messagebox.showinfo("成功", "所有数据已清空。")
            create_empty_file_if_not_exists()  # 创建新文件
        elif option == "room":
            room = entry_clear_room.get().strip()
            if room in data:
                del data[room]
                save_data(data)
                messagebox.showinfo("成功", f"房间'{room}'的数据已清空。")
            else:
                messagebox.showwarning("错误", "未找到该房间。")
        elif option == "storage":
            room = entry_clear_room.get().strip()
            storage = entry_clear_storage.get().strip()
            if room in data and storage in data[room]:
                del data[room][storage]
                if not data[room]:
                    del data[room]
                save_data(data)
                messagebox.showinfo("成功", f"房间'{room}'中的收纳处'{storage}'的数据已清空。")
            else:
                messagebox.showwarning("错误", "未找到该房间或收纳处。")
        clear_window.destroy()

    clear_window = tk.Toplevel(main_menu_window)
    clear_window.title("清空数据")

    tk.Label(clear_window, text="选择操作：", anchor='e').grid(row=0, column=0, padx=10, pady=10, sticky='e')

    var = tk.StringVar(value="all")
    tk.Radiobutton(clear_window, text="清空所有数据", variable=var, value="all").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')
    tk.Radiobutton(clear_window, text="清空特定房间", variable=var, value="room").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')
    tk.Radiobutton(clear_window, text="清空特定收纳处", variable=var, value="storage").grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='w')

    tk.Label(clear_window, text="房间（如适用）：", anchor='e').grid(row=4, column=0, padx=10, pady=10, sticky='e')
    entry_clear_room = tk.Entry(clear_window)
    entry_clear_room.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    tk.Label(clear_window, text="收纳处（如适用）：", anchor='e').grid(row=5, column=0, padx=10, pady=10, sticky='e')
    entry_clear_storage = tk.Entry(clear_window)
    entry_clear_storage.grid(row=5, column=1, padx=10, pady=10, sticky='w')

    tk.Button(clear_window, text="提交", command=submit).grid(row=6, column=0, columnspan=2, pady=10)

def backup_data():
    """备份数据的窗口和逻辑处理."""
    def submit():
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON 文件", "*.json")])
        if file_path:
            data = load_data()
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("成功", f"数据已备份到 {file_path}")
        backup_window.destroy()

    backup_window = tk.Toplevel(main_menu_window)
    backup_window.title("备份数据")

    tk.Button(backup_window, text="备份", command=submit).grid(row=0, column=0, padx=10, pady=10)

def open_settings():
    """打开设置窗口."""
    settings_window = tk.Toplevel(main_menu_window)
    settings_window.title("设置")

    tk.Button(settings_window, text="清空数据", command=clear_data).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(settings_window, text="备份数据", command=backup_data).grid(row=1, column=0, padx=10, pady=10)

def main_menu():
    """创建并显示主菜单."""
    global main_menu_window
    main_menu_window = tk.Toplevel()
    main_menu_window.title("YCss")

    # 创建主菜单窗口的布局
    tk.Button(main_menu_window, text="添加物品", command=add_item, width=40).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="查找物品", command=find_item, width=40).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="统计信息", command=show_statistics, width=40).grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    tk.Button(main_menu_window, text="设置", command=open_settings, width=40).grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    # 设置列的权重，使按钮居中
    main_menu_window.grid_columnconfigure(0, weight=1)

# 创建并显示主菜单窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
main_menu()

root.mainloop()
