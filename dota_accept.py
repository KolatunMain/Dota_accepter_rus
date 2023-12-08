import threading
from tkinter import *
from pyautogui import *
from time import *
from pygetwindow import *
import keyboard


target_image_path = "accept.png" #введение переменных
windows = getAllTitles()
skr_aktive = False
root = Tk()
toggle_button_var = IntVar()


def run_script():
    for window in windows:
        windows_with_title = getWindowsWithTitle(window)
        if windows_with_title and len(windows_with_title) > 0:
            if windows_with_title[0].isActive: #Ищу активное Окно с картинкой
                if skr_aktive:
                    try:
                        location = locateCenterOnScreen(target_image_path, confidence=0.6)
                        if location: #Ищу картинку
                            center_x, center_y = location
                            print(f'Найдено на: {center_x}, {center_y}')
                            sleep(0.5)
                            mouseDown(button='left', x=center_x, y=center_y)
                            sleep(0.1)
                            mouseUp(button='left') #Клик на найденую картинку
                        else:
                            print('Картинка не найдена')
                    except ImageNotFoundException:
                        print('Не нашел. Ищу снова...')
                        sleep(1)
                else:
                    return
    if skr_aktive: root.after(100,run_script)


def run_script_thread(): #Запуск в отдельном потоке осн скрипта (костыль)
    while skr_aktive:
        run_script()
    root.after(100, run_script)


def toggle_skr(): #вкл/выкл цыкла работы скрипта
    global skr_aktive
    skr_aktive = not skr_aktive
    toggle_button_var.set(1 if skr_aktive else 0)
    print(f"Акто-ацепт {'ВКЛ' if skr_aktive else 'выключен'}")
    if skr_aktive: threading.Thread(target=run_script_thread).start()


def on_chbx_change(): #Флажок в окне вкл/вкл
    toggle_skr()

toggle_button = Checkbutton(root, text='Включить/Выключить',variable=toggle_button_var, command=on_chbx_change)
toggle_button.pack(pady=10) #создание флажка вкл/вкл
keyboard.add_hotkey('F10', toggle_skr) #хоткей на вкл/выкл
root.protocol("WM_DELETE_WINDOW", root.destroy)  # Обработчик закрытия окна
root.mainloop()
