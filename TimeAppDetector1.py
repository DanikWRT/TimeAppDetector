import psutil
import datetime
import pystray
import threading
from pystray import MenuItem as item
from pystray import Icon, Menu
from PIL import Image
import tkinter as tk
import traceback

# Глобальные переменные
uptime = ""
process_name = "Telegram.exe"
image = Image.open("icon.png")

# Функция для получения времени запуска процесса
def get_process_uptime(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            return datetime.datetime.now() - datetime.datetime.fromtimestamp(process.create_time())
    return None

# Функция для обновления времени иконки в трее
def update_time(icon):
    global uptime
    process_uptime = get_process_uptime(process_name)
    if process_uptime:
        uptime = process_uptime.total_seconds()
        icon.title = f"Время работы процесса: {datetime.timedelta(seconds=int(uptime))}"

# Функция для обновления информации с интервалом
def update_info_thread(icon):
    while True:
        update_time(icon)
        icon._update_icon()
        threading.Event().wait(1)  # Интервал в секундах для обновления информации

def on_click(icon, item):
    process_uptime = get_process_uptime(process_name)
    if process_uptime:
        print("on_click - сработал")
        try:
            app = tk.Tk()
            app.title("Информация о процессе")
            label = tk.Label(app, text=f"Название процесса: {process_name}\n"
                                        f"Время работы процесса: {datetime.timedelta(seconds=int(uptime))}")
            label.pack()
            app.mainloop()
        except Exception as e:
            traceback.print_exc()


menus = Menu(
    item('Открыть информацию', lambda _: on_click(icon, _),default=True),
    item('Выход', lambda: icon.stop())
)
icon = Icon("Process Watcher", image, menu=menus, onclick=on_click )

# Запуск потока с обновлением информации
info_thread = threading.Thread(target=update_info_thread, args=(icon,))
info_thread.daemon = True
info_thread.start()

icon.run()