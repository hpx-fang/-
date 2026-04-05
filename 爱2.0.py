import tkinter as tk
import math
import random
import threading
import time
import ctypes
import queue

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

WINDOW_W, WINDOW_H = 320, 120
DESIRED_POINTS = 300
BASE_DISPLAY_TIME = 3000
DESTROY_INTERVAL = 10
TIPS_COUNT = 60

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

window_queue = queue.Queue()
all_windows_created = threading.Event()

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
    center_y = screen_h // 2 - 100
    
    effective_points = int(num_points * 0.7)
    
    for i in range(effective_points):
        t = i / effective_points * 2 * math.pi
        
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        
        scale_x = 30
        scale_y = 30
        
        x = center_x + int(x * scale_x)
        y = center_y + int(y * scale_y)
        
        x = max(0, min(x, screen_w - window_w))
        y = max(0, min(y, screen_h - window_h))
        
        points.append((x, y))
    
    while len(points) < num_points:
        t = random.random() * 2 * math.pi
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        
        scale_x = 30
        scale_y = 30
        
        x = center_x + int(x * scale_x)
        y = center_y + int(y * scale_y)
        
        x = max(0, min(x, screen_w - window_w))
        y = max(0, min(y, screen_h - window_h))
        
        if random.random() < 0.7:
            points.append((x, y))
    
    return points[:num_points]

def create_heart_window(x, y, index, total):
    window = tk.Tk()
    window.title(f"祝福-{index}")
    window.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
    
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    
    blessing = get_blessing(index-1)
    
    label = tk.Label(window, text=f"{blessing}\n——幽默旭芳", 
                     font=("微软雅黑", 20, "bold"), fg='#FF1493',
                     wraplength=WINDOW_W-20, justify='center')
    label.pack(expand=True, fill='both', padx=10, pady=10)
    
    colors = ['#FFB6C1', '#FF69B4', '#FF1493', '#DB7093', '#C71585']
    window.config(bg=colors[index % len(colors)])
    
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
    
    print("\n" + "=" * 40)
    print("❤️ 开始显示心形弹窗...")
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

def show_warm_tip():
    window = tk.Tk()
    window_width = 280
    window_height = 80
    x = random.randint(0, SCREEN_W - window_width)
    y = random.randint(0, SCREEN_H - window_height)
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
    
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen', 'lavender',
        'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine',
        'mistyrose', 'honeydew', 'lightcyan', 'thistle', 'peachpuff',
        'lightsalmon', 'lightblue', 'lightcoral', 'lightgoldenrodyellow',
    ]
    bg_color = random.choice(bg_colors)
    
    label = tk.Label(window, text=f"{tip}\n——幽默旭芳", font=("微软雅黑", 10), 
                     bg=bg_color, wraplength=window_width-20, 
                     padx=5, pady=5, justify='center')
    label.pack(expand=True, fill='both')
    
    window.after(5000, window.destroy)
    window.mainloop()

def show_warm_tips_series(tip_count=TIPS_COUNT, delay=0.3):
    print("\n" + "=" * 40)
    print("💌 开始显示温馨提醒弹窗...")
    print("=" * 40)
    
    for i in range(tip_count):
        t = threading.Thread(target=show_warm_tip)
        t.start()
        time.sleep(delay)
        
        if (i + 1) % 10 == 0:
            print(f"已显示 {i+1}/{tip_count} 个温馨提醒")
            time.sleep(0.5)
    
    print("\n" + "=" * 40)
    print("🎉 程序运行完成！")
    print("=" * 40)

def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║                                                   ║")
    print("║        ❤️  Python浪漫弹窗程序 ❤️           ║")
    print("║                                                   ║")
    print("╠═══════════════════════════════════════════════════╣")
    print("║                                                   ║")
    print("║             作者：幽默旭芳                        ║")
    print("║             制作时长：2个月                        ║")
    print("║             制作不易，点个赞吧❤️                  ║")
    print("║                                                   ║")
    print("╠═══════════════════════════════════════════════════╣")
    print("║                                                   ║")
    print("║   温馨提示：                                      ║")
    print("║   1. 程序运行时会创建大量弹窗                     ║")
    print("║   2. 如需提前结束请使用任务管理器关闭Python进程   ║")
    print("║   3. 本人数学不好，所以函数画的心有点难看         ║")
    print("║                                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    print("")
    input("按Enter键开始浪漫之旅...")
    
    try:
        show_heart_windows()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()