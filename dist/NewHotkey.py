import tkinter
import time
import win32api
import win32con
import ctypes  
import PyHook3
import pythoncom
import threading

check_ing = 0
check_end = 0
#定义左右按键标志位
MouseL_flag = 0  
MouseR_flat = 0
 
def Hotkey_gui():
    window = tkinter.Tk()
    window.title("Auto-Key")
    window.geometry("300x200")



    label_title1 = tkinter.Label(window,text="按顺序输入需要按下的键",font=('宋体',15,'italic'),anchor='center')
    label_title1.place(x=10,y=30,height=25,width =280)

    label_tile2 = tkinter.Label(window,text="通过空格分隔",font=('宋体',15,'italic'),anchor='center')
    label_tile2.place(x=10,y=60,height=25,width =245)
    #5个快捷键标题
    label_key1 = tkinter.Label(window,text="输入框",font=('宋体',13,'italic'),anchor='center')
    label_key1.place(x=30,y=100,height=25,width=70)

    Key1 = tkinter.StringVar(value=0)

    entry_key1 = tkinter.Entry(window,textvariable=Key1)
    entry_key1.place(x=110,y=100,height=25,width=150)

    button_yes = tkinter.Button(window,text="启动",command = lambda:[Hot_key(entry_key1.get())])
    button_no = tkinter.Button(window,text="退出",command = lambda:[exit()])

    button_yes.place(x=50,y=150,height=25,width=50)
    button_no.place(x=200,y=150,height=25,width=50)

    window.mainloop()

def Hot_key(string_keys):
    print("keys:".format(string_keys))
    str(string_keys)
    #此处分割后为列表
    keys = string_keys.split()
    #创建钩子管理器
    hm = PyHook3.HookManager()

    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()

    hm.SubscribeMouseAll(OnMouseEvent(keys))
    hm.HookMouse()

    pythoncom.PumpMessages()
def OnKeyboardEvent(event):
    if event.Key == 'End':
        exit()
    # print(event.Key)
    return True
#此处使用闭包传递外部参数
def OnMouseEvent(keys):
    def OnMouseEvent_dev(event):
        global MouseL_flag
        global MouseR_flat
        global check_end
        global check_ing
        print(event.MessageName)
        if event.MessageName == "mouse left down" : 
            MouseL_flag = 1
        if event.MessageName == "mouse right down" :
            MouseR_flat = 1
            print("+++++++++")
        if event.MessageName == "mouse left up" :
            MouseL_flag = 0
        if event.MessageName == "mouse right up" :
            MouseR_flat = 0
            print("---------")
                    
        check_ing = time.perf_counter()
        print("当前时间{}".format(check_ing))
        print("当前按键数目{}".format(MouseL_flag+MouseR_flat))
        print("one-time:{}".format(check_ing))
        print("two-tiem:{}".format(check_end))
        print("abs{}".format(abs(check_end-check_ing)))
        if check_end == 0 or abs(check_ing-check_end) > 1.5:
            A_Z =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            if MouseL_flag == 1 and MouseR_flat == 1:
                print("左右键按下开始执行！")
                for key in keys:
                    if key in A_Z:
                        # print(key.lower())
                        What_key('caps_lock')
                        What_key(key.lower())
                        What_key('caps_lock')
                    else:
                        What_key(key)
                check_end = time.perf_counter()
        return True
    return OnMouseEvent_dev


def What_key(key):
    MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    key_dict={
   #大写字母
    'A':65,
    'B':66,
    'C':67,
    'D':68,
    'E':69,
    'F':70,
    'G':71,
    'H':72,
    'I':73,
    'J':74,
    'K':75,
    'L':76,
    'M':77,
    'N':78,
    'O':79,
    'P':80,
    'Q':81,
    'R':82,
    'S':83,
    'T':84,
    'U':85,
    'V':86,
    'W':87,
    'X':88,
    'Y':89,
    'Z':90,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'spacebar':0x20,
    'caps_lock':0x14,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    '.':0xBE,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
   }

    try:
        now_key = key_dict[key]
        win32api.keybd_event(now_key,MapVirtualKey(now_key,0),0,0)
        win32api.keybd_event(now_key,MapVirtualKey(now_key,0),win32con.KEYEVENTF_KEYUP,0)
        print("按键{}按下成功！".format(key))
    except:
        print("错误输入，请重新输入！")



class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()
        
        self.func = func
        self.args = args
        
        self.setDaemon(True)
        self.start()    # 在这里开始
        
    def run(self):
        self.func(*self.args)


if __name__ == '__main__':
    Hotkey_gui()



