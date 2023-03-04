import threading
from tkinter import *
import tkinter
import tkinter.messagebox
from tkinter import ttk, messagebox
import random
from hashlib import md5
import requests
from pynput.mouse import Listener, Button
from pynput.keyboard import Key, Controller
import pynput.keyboard
import pyperclip
from ctypes import windll
import time


class GUI:
    __press_xy = (0, 0)

    def __init__(self, appid, key):
        self.appid = appid
        self.key = key
        self.root = Tk()
        self.mod = 'mouse'  # 默认划词
        self.root.wm_attributes('-topmost', 1)
        self.v_name = StringVar()
        self.t = ''
        self.s = Text(self.root, width=50, height=10)
        self.r = Text(self.root, width=50, height=10)
        self.keyboard = Controller()
        self.listener = Listener(on_click=self.on_click)
        self.key_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.key_listener.start()

        self.setup()
        self.lis_close = threading.Thread(target=self.root.protocol('WM_DELETE_WINDOW', self.on_closing)).start()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.listener.stop()
            self.key_listener.stop()

    def setup(self):
        self.root.title("TinyTranslator")
        self.root.iconbitmap(default='Angel.ico')
        Label(self.root, text='Input:').grid(row=0, column=0, sticky=W)
        self.s.grid(row=1, sticky=W)
        Label(self.root, text='Translating to:').grid(row=2, sticky=W)
        cb = tkinter.ttk.Combobox(self.root, width=20, textvariable=self.v_name, )
        cb["values"] = ('Chinese', 'French', 'English', 'Classical Chinese', 'Japanese')
        cb.grid(row=2)
        cb.current(0)
        Label(self.root, text='Output:').grid(row=3, column=0, sticky=W)
        self.r.grid(row=4, sticky=W)
        tkinter.Button(self.root, text='translate', width=10, command=self.trans).grid(row=5, sticky=W)
        tkinter.Button(self.root, text='clear', width=10, command=self.del_t).grid(row=5)
        tkinter.Button(self.root, text='switch', width=10, command=self.shift).grid(row=5, sticky=E)

    def shift(self):
        if self.mod == 'mouse':
            self.mod = 'keyboard'
            tkinter.messagebox.showinfo('Info', 'Switch to mode:Ctrl+C')
        else:
            self.mod = 'mouse'
            tkinter.messagebox.showinfo('Info', 'Switch to mode:Mouse')

    def on_click(self, x, y, button, pressed):
        if button == Button.left:  # 左键点击
            try:
                temp = self.root.clipboard_get()
            except:
                temp = ' '
            if pressed:
                self.__press_xy = (x, y)
            else:
                if self.__press_xy != (x, y):
                    self.copy()
                    time.sleep(0.01)
                if self.root.clipboard_get() != temp and self.mod == 'mouse':
                    self.del_t()
                    self.s.insert(INSERT, self.paste())
                    self.trans()

    def on_press(self, key):
        try:
            temp = self.root.clipboard_get()
        except:
            temp = ' '
        if str(key) == r"'\x03'":
            time.sleep(0.01)
            if self.root.clipboard_get() != temp and self.mod != 'mouse':
                self.del_t()
                self.s.insert(INSERT, self.paste())
                self.trans()

    def get_l(self):
        tmp = self.v_name.get()
        if tmp == 'Chinese':
            self.t = 'zh'
        elif tmp == 'English':
            self.t = 'en'
        elif tmp == 'Classical Chinese':
            self.t = 'wyw'
        elif tmp == 'French':
            self.t = 'fra'
        elif tmp == 'Japanese':
            self.t = 'jp'

    def del_t(self):
        self.s.delete(1.0, "end")
        self.r.delete(1.0, END)

    def trans(self):
        self.get_l()
        tstr = self.s.get(1.0, END).replace('\n', ' ').replace('\r', ' ')
        URL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        from_lang = 'auto'
        salt = str(random.randint(32768, 65536))
        m = self.appid + tstr + salt + self.key
        sign = md5(m.encode('utf-8')).hexdigest()
        data = {
            "appid": self.appid,
            "q": tstr,
            "from": from_lang,
            "to": self.t,
            "salt": salt,
            "sign": sign
        }
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(URL, params=data, headers=header)  # 发送post请求
        text = response.json()
        results = text['trans_result'][0]['dst']

        self.r.delete(1.0, END)
        self.r.insert("insert", results)
        print(results)
        return results

    # 复制函数
    def copy(self):
        with self.keyboard.pressed(Key.ctrl):  # 按下ctrl，with语句结束后自动松开
            self.keyboard.press('c')  # 按下c
            self.keyboard.release('c')  # 松开c

    def clipboard_clear(self):
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()

    def paste(self):
        return pyperclip.paste()


if __name__ == '__main__':
    gui = GUI(appid='your_id', key='your_key')
    mainloop()
