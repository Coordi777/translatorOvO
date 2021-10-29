from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from urllib import request
from urllib import parse
import json
import hashlib
import random

root = Tk()
root.title("小小翻译器")
root.iconbitmap(default='Angel.ico')
v_name = StringVar()
t = ''
Label(root, text='输入要翻译的内容：').grid(row=0, column=0, sticky=W)
s = Text(root, width=50, height=10)
s.grid(row=1, sticky=W)
Label(root, text='选择翻译语言：').grid(row=2, sticky=W)
cb = tkinter.ttk.Combobox(root, width=20, textvariable=v_name)
cb["values"] = ('中文', '法语', '英语', '文言文', '日语')
cb.grid(row=2)
Label(root, text='翻译结果如下：').grid(row=3, column=0, sticky=W)
r = Text(root, width=50, height=10)
r.grid(row=4, sticky=W)


def get_l():
    global t
    tmp = v_name.get()
    if tmp == '中文':
        t = 'zh'
    elif tmp == '英语':
        t = 'en'
    elif tmp == '文言文':
        t = 'wyw'
    elif tmp == '法语':
        t = 'fra'
    elif tmp == '日语':
        t = 'jp'


def del_t():
    s.delete(1.0, "end")
    r.delete(1.0, END)


def get_h():
    tkinter.messagebox.showinfo('提示', '输入待翻译的内容，语言自动识别\n'
                                      '选择翻译到哪种语言\n'
                                      '清空可以清空所有内容')


def tran():
    get_l()
    tstr = s.get(1.0, END)
    URL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    # Form_Data={'from':'en','to':'zh','query':en_str,'transtype':'hash'}
    Form_Data = {}
    Form_Data['from'] = 'auto'
    Form_Data['to'] = t
    Form_Data['q'] = tstr  # 要翻译数据
    Form_Data['transtype'] = 'hash'
    Form_Data['appid'] = 'your_id'  # 申请的APP ID
    Form_Data['salt'] = str(random.randint(32768, 65536))  # 随机数
    Key = "your_key"  # 平台分配的密钥
    m = Form_Data['appid'] + tstr + Form_Data['salt'] + Key
    m_MD5 = hashlib.md5(m.encode('utf8'))
    Form_Data['sign'] = m_MD5.hexdigest()
    if t == '':
        tkinter.messagebox.showerror('错误！', '你也不选个翻译的语言？？')
        return 'error'

    data = parse.urlencode(Form_Data).encode('utf-8')  # 使用urlencode方法转换标准格式
    response = request.urlopen(URL, data)  # 传递Request对象和转换完格式的数据
    html = response.read().decode('utf-8')  # 读取信息并解码
    translate_results = json.loads(html)  # 使用JSON
    translate_results = translate_results['trans_result'][0]['dst']  # 找到翻译结果
    r.delete(1.0, END)
    r.insert("insert", translate_results)
    return translate_results


Button(root, text='翻译', width=10, command=tran).grid(row=5, sticky=W)
Button(root, text='清空', width=10, command=del_t).grid(row=5)
Button(root, text='提示', width=10, command=get_h).grid(row=5, sticky=E)

mainloop()
