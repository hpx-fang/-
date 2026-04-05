import tkinter as tk
import math
import random
import threading
import time
import ctypes
import queue
import sys

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

BASE_DESIRED_POINTS = 300
BASE_DISPLAY_TIME = 3000
BASE_DESTROY_INTERVAL = 10
BASE_TIPS_COUNT = 120
SPECIAL_TIP_DELAY = 0.08

def get_screen_size():
    try:
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except:
        return 1920, 1080

SCREEN_W, SCREEN_H = get_screen_size()

def calculate_scale_factor():
    base_width, base_height = 1920, 1080
    width_scale = SCREEN_W / base_width
    height_scale = SCREEN_H / base_height
    return min(width_scale, height_scale)

SCALE_FACTOR = calculate_scale_factor()

WINDOW_W = int(240 * SCALE_FACTOR)
WINDOW_H = int(80 * SCALE_FACTOR)
DESIRED_POINTS = BASE_DESIRED_POINTS
DESTROY_INTERVAL = BASE_DESTROY_INTERVAL
TIPS_COUNT = BASE_TIPS_COUNT

window_queue = queue.Queue()
all_windows_created = threading.Event()
special_blessing_shown = False
special_message_shown = False

blessings = [
    "前程似锦", "万事胜意", "平安喜乐", "熠熠生辉", "乘风破浪",
    "未来可期", "一切顺遂", "得偿所愿", "光芒万丈", "喜乐安康",
    "自在如风", "前程万里", "星途璀璨", "万事顺意", "坦途无忧",
    "锦绣前程", "百事从欢", "嘉言懿行", "云程发轫", "芳华自在",
    "清澈明朗", "无忧无虑", "温暖有光", "所行皆坦", "终成所愿",
    "生活明朗", "不负韶华", "人间值得", "我喜欢你", "天天快乐"
]

def get_blessing(index):
    return blessings[index % len(blessings)]

def generate_heart_points(num_points, screen_w, screen_h, window_w, window_h):
    points = []
    
    center_x = screen_w // 2
    center_y = screen_h // 2
    
    for i in range(num_points):
        t = i / num_points * 2 * math.pi
        
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        scale_factor = 25 * SCALE_FACTOR
        
        x_coord = center_x + int(x * scale_factor)
        y_coord = center_y - int(y * scale_factor)
        
        if i < 2:
            top_x = center_x
            top_y = center_y - int(8 * scale_factor)
            
            offset = 30 * SCALE_FACTOR
            if i == 0:
                x_coord = int(top_x - offset)
                y_coord = int(top_y)
            else:
                x_coord = int(top_x + offset)
                y_coord = int(top_y)
        
        x_coord = max(0, min(x_coord, screen_w - window_w))
        y_coord = max(0, min(y_coord, screen_h - window_h))
        
        points.append((x_coord, y_coord))
    
    return points

def create_heart_window(x, y, index, total):
    window = tk.Tk()
    window.title(f"祝福-{index}")
    window.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
    
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    
    blessing = get_blessing(index-1)
    
    font_size = int(16 * SCALE_FACTOR)
    
    if index <= 2:
        bg_color = '#FFD700'
        text_color = '#8B0000'
    else:
        bg_color = '#FFB6C1'
        text_color = '#FF1493'
    
    label = tk.Label(window, text=f"{blessing}\n——幽默旭芳", 
                     font=("微软雅黑", font_size, "bold"), fg=text_color,
                     wraplength=WINDOW_W-20, justify='center', bg=bg_color)
    label.pack(expand=True, fill='both', padx=10, pady=10)
    
    if index > 2:
        colors = ['#FFB6C1', '#FF69B4', '#FF1493', '#DB7093', '#C71585']
        window.config(bg=colors[(index-1) % len(colors)])
    else:
        window.config(bg=bg_color)
    
    window_queue.put((index, window))
    
    if index == total:
        all_windows_created.set()
    
    window.mainloop()

def destroy_windows_sequentially():
    all_windows_created.wait()
    
    time.sleep(BASE_DISPLAY_TIME / 1000)
    
    windows_to_destroy = []
    while not window_queue.empty():
        windows_to_destroy.append(window_queue.get())
    
    windows_to_destroy.sort(key=lambda x: x[0])
    
    print("\n" + "=" * 40)
    print("❤️ 心形弹窗开始关闭...")
    print("=" * 40)
    
    for i, (index, window) in enumerate(windows_to_destroy):
        try:
            window.after(0, window.destroy)
        except:
            pass
        time.sleep(DESTROY_INTERVAL / 1000)
        
        if (i + 1) % 30 == 0:
            progress = (i + 1) / len(windows_to_destroy) * 100
            print(f"已关闭 {i+1}/{len(windows_to_destroy)} 个弹窗 ({progress:.1f}%)")
    
    print("\n" + "=" * 40)
    print("✅ 心形弹窗已全部关闭")
    print("=" * 40)
    
    show_warm_tips_series()

def show_heart_windows():
    points = generate_heart_points(DESIRED_POINTS, SCREEN_W, SCREEN_H, WINDOW_W, WINDOW_H)
    
    print(f"\n" + "=" * 40)
    print(f"❤️ 开始显示心形弹窗 (分辨率: {SCREEN_W}x{SCREEN_H})...")
    print("=" * 40)
    
    destroy_thread = threading.Thread(target=destroy_windows_sequentially)
    destroy_thread.start()
    
    for i, (x, y) in enumerate(points):
        t = threading.Thread(target=create_heart_window, args=(x, y, i+1, DESIRED_POINTS))
        t.start()
        time.sleep(0.01)
        
        if (i + 1) % 30 == 0:
            progress = (i + 1) / DESIRED_POINTS * 100
            print(f"已创建 {i+1}/{DESIRED_POINTS} 个弹窗 ({progress:.1f}%)")

def show_special_message():
    global special_message_shown
    
    if special_message_shown:
        return
    
    window_width = int(350 * SCALE_FACTOR)
    window_height = int(140 * SCALE_FACTOR)
    
    x = SCREEN_W // 2 - window_width // 2
    y = SCREEN_H // 2 - window_height // 2
    
    window = tk.Tk()
    window.title('特别祝福')
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    window.attributes('-topmost', True)
    
    window.config(bg='gold')
    
    label = tk.Label(window, 
                     text="有些话，到了嘴边又咽了回去...\n但祝福一直都在心底\n——致 祝春归", 
                     font=("微软雅黑", int(16 * SCALE_FACTOR), "bold"), 
                     fg='#8B0000', bg='gold',
                     wraplength=window_width-40, justify='center',
                     padx=20, pady=20)
    label.pack(expand=True, fill='both')
    
    window.after(8000, window.destroy)
    window.mainloop()
    
    special_message_shown = True

def show_warm_tip():
    global special_blessing_shown
    
    window_width = int(240 * SCALE_FACTOR)
    window_height = int(70 * SCALE_FACTOR)
    
    x = random.randint(0, SCREEN_W - window_width)
    y = random.randint(0, SCREEN_H - window_height)
    
    window = tk.Tk()
    window.title('温馨提示')
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    window.attributes('-topmost', True)
    
    tips = [
        "记得按时吃饭",
        "今天天气冷，加件外套",
        "累了就歇会儿，别硬撑",
        "多喝温水，对身体好",
        "早点休息，别熬夜太久",
        "出门记得带伞，要下雨",
        "路上注意安全，慢慢走",
        "难过了可以听首歌",
        "太阳好的时候晒晒背",
        "书别看太久，眼睛累",
        "心情不好就看看云",
        "给自己买点喜欢的水果",
        "走路别总低头看手机",
        "清晨的粥比深夜的酒好",
        "记得给窗户留条缝通风",
        "压力大的时候深呼吸",
        "周末去晒晒太阳吧",
        "热水泡脚睡得香些",
        "阴天记得开盏暖光灯",
        "对着绿树发会儿呆也好",
        "热牛奶比咖啡安神",
        "难过时不妨哭一场",
        "穿那双最舒服的鞋",
        "晴天晒晒被子和心情",
        "对自己说声辛苦了",
        "流泪后的眼睛敷片刻",
        "孤单时就听点人声",
        "迷茫时先睡一觉",
        "虚度时光也没关系",
        "想家就打个电话",
        "好好吃饭是头等大事",
        "淋雨了要立刻擦干",
        "委屈不必都憋着",
        "偶尔赖床也没事",
        "楼梯要扶稳慢慢下",
        "洗完头发尽快吹干",
        "清晨喝杯温水润润",
        "下午三点记得起身走走",
        "旧伤处要注意保暖",
        "想笑就笑，想静就静",
        "你的感受都很重要",
        "不喜欢就别勉强自己",
        "偶尔吃块糖，甜的",
        "散步时看一朵花开",
        "手凉了就搓一搓",
        "重要的事先写下来",
        "被拒绝不是你的错",
        "世界吵，你可以静",
        "流泪不是软弱的事",
        "今天的你已经很好",
        "不需要总是说抱歉",
        "你的存在本就珍贵",
        "慢慢来，不用追赶谁",
        "偶尔麻烦别人也可以",
        "你值得被温柔以待",
        "不必时刻都在奔跑",
        "你的声音值得被听见",
        "不想笑时可以不笑",
        "你比想象中更坚强",
        "我一直都在这里"
    ]
    
    tip = random.choice(tips)
    
    if not special_blessing_shown and random.random() < 0.15:
        tip = "春风送暖，四季长安\n——致 祝春归"
        special_blessing_shown = True
    
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen', 'lavender',
        'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine',
        'mistyrose', 'honeydew', 'lightcyan', 'thistle', 'peachpuff',
        'lightsalmon', 'lightblue', 'lightcoral', 'lightgoldenrodyellow',
    ]
    bg_color = random.choice(bg_colors)
    
    tip_font_size = int(9 * SCALE_FACTOR)
    
    label = tk.Label(window, text=f"{tip}\n——幽默旭芳", font=("微软雅黑", tip_font_size), 
                     bg=bg_color, wraplength=window_width-20, 
                     padx=5, pady=5, justify='center')
    label.pack(expand=True, fill='both')
    
    window.after(5000, window.destroy)
    window.mainloop()

def show_warm_tips_series(tip_count=TIPS_COUNT, delay=SPECIAL_TIP_DELAY):
    print("\n" + "=" * 40)
    print(f"💌 开始显示{tip_count}个温馨提醒弹窗...")
    print("=" * 40)
    
    special_shown = False
    tips_shown = 0
    
    for i in range(tip_count):
        if tips_shown == tip_count // 3 and not special_shown:
            t = threading.Thread(target=show_special_message)
            t.start()
            special_shown = True
            time.sleep(0.5)
        
        t = threading.Thread(target=show_warm_tip)
        t.start()
        tips_shown += 1
        time.sleep(delay)
        
        if (i + 1) % 20 == 0:
            print(f"已显示 {i+1}/{tip_count} 个温馨提醒")
            time.sleep(0.2)
    
    if not special_shown:
        t = threading.Thread(target=show_special_message)
        t.start()
    
    print("\n" + "=" * 40)
    print("🎉 程序运行完成！")
    print("=" * 40)

def start_program():
    print("=" * 60)
    print("❤️ Python浪漫弹窗程序 ❤️")
    print("=" * 60)
    print(f"作者: 幽默旭芳")
    print(f"制作时长: 2个月")
    print(f"制作不易，点个赞吧❤️")
    print("=" * 60)
    print(f"当前分辨率: {SCREEN_W}x{SCREEN_H}")
    print(f"缩放因子: {SCALE_FACTOR:.2f}")
    print(f"温馨提醒弹窗: {TIPS_COUNT}个")
    print("=" * 60)
    print("温馨提示:")
    print("1. 程序运行时会创建大量弹窗")
    print("2. 如需提前结束请使用任务管理器关闭Python进程")
    print("3. 本人数学不好，所以函数画的心有点难看")
    print("4. 程序已适配全分辨率显示")
    print("5. 包含特别祝福弹窗，请留意屏幕中央")
    print("=" * 60)
    
    try:
        show_heart_windows()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")

def show_start_gui():
    start_window = tk.Tk()
    start_window.title("Python浪漫弹窗程序")
    
    window_width = 500
    window_height = 550
    
    screen_width = start_window.winfo_screenwidth()
    screen_height = start_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    start_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    start_window.resizable(False, False)
    
    start_window.configure(bg='#FFE4E1')
    
    canvas = tk.Canvas(start_window, bg='#FFE4E1', highlightthickness=0)
    scrollbar = tk.Scrollbar(start_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#FFE4E1')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    title_label = tk.Label(scrollable_frame, text="❤️ Python浪漫弹窗程序 ❤️", 
                          font=("微软雅黑", 20, "bold"), fg='#FF1493', bg='#FFE4E1')
    title_label.pack(pady=10)
    
    author_frame = tk.Frame(scrollable_frame, bg='#FFE4E1')
    author_frame.pack(pady=5)
    
    tk.Label(author_frame, text="作者: 幽默旭芳", font=("微软雅黑", 14), 
            fg='#8B0000', bg='#FFE4E1').pack(pady=2)
    tk.Label(author_frame, text="制作时长: 2个月", font=("微软雅黑", 14), 
            fg='#8B0000', bg='#FFE4E1').pack(pady=2)
    tk.Label(author_frame, text="制作不易，点个赞吧❤️", font=("微软雅黑", 14), 
            fg='#8B0000', bg='#FFE4E1').pack(pady=2)
    
    tk.Frame(scrollable_frame, height=2, bg='#FF69B4').pack(fill='x', padx=20, pady=10)
    
    info_frame = tk.Frame(scrollable_frame, bg='#FFE4E1')
    info_frame.pack(pady=5)
    
    tk.Label(info_frame, text=f"当前分辨率: {SCREEN_W}x{SCREEN_H}", 
            font=("微软雅黑", 12), fg='#4B0082', bg='#FFE4E1').pack(pady=2)
    tk.Label(info_frame, text=f"缩放因子: {SCALE_FACTOR:.2f}", 
            font=("微软雅黑", 12), fg='#4B0082', bg='#FFE4E1').pack(pady=2)
    tk.Label(info_frame, text=f"温馨提醒弹窗: {TIPS_COUNT}个", 
            font=("微软雅黑", 12), fg='#4B0082', bg='#FFE4E1').pack(pady=2)
    
    tk.Frame(scrollable_frame, height=2, bg='#FF69B4').pack(fill='x', padx=20, pady=10)
    
    tk.Label(scrollable_frame, text="温馨提示:", font=("微软雅黑", 16, "bold"), 
            fg='#8B0000', bg='#FFE4E1').pack(pady=5)
    
    tips_frame = tk.Frame(scrollable_frame, bg='#FFE4E1')
    tips_frame.pack(pady=5)
    
    tips = [
        "1. 程序运行时会创建大量弹窗",
        "2. 如需提前结束请使用任务管理器关闭Python进程",
        "3. 本人数学不好，所以函数画的心有点难看",
        "4. 程序已适配全分辨率显示",
        "5. 包含特别祝福弹窗，请留意屏幕中央"
    ]
    
    for tip in tips:
        tip_label = tk.Label(tips_frame, text=tip, font=("微软雅黑", 10), 
                fg='#4B0082', bg='#FFE4E1', justify='left', anchor='w', wraplength=460)
        tip_label.pack(pady=2, anchor='w')
    
    def on_start_button_click():
        start_window.destroy()
        start_program()
    
    button_frame = tk.Frame(scrollable_frame, bg='#FFE4E1')
    button_frame.pack(pady=15)
    
    start_button = tk.Button(button_frame, text="开始浪漫之旅", 
                            font=("微软雅黑", 16, "bold"), bg='#FF69B4', fg='white',
                            activebackground='#FF1493', activeforeground='white',
                            relief='raised', bd=3, padx=20, pady=8,
                            command=on_start_button_click)
    start_button.pack()
    
    def on_enter(e):
        start_button['background'] = '#FF1493'
        start_button['foreground'] = 'white'
    
    def on_leave(e):
        start_button['background'] = '#FF69B4'
        start_button['foreground'] = 'white'
    
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)
    
    start_window.mainloop()

if __name__ == "__main__":
    if sys.platform == "win32":
        if not hasattr(sys, 'frozen'):
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.GetConsoleWindow()
    
    show_start_gui()