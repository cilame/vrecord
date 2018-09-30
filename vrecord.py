import pyHook
import pythoncom
import win32api
import tkinter






def create_window():
    root = tkinter.Tk()
    vvvv = tkinter.IntVar(value=1)
    ffff = tkinter.Checkbutton(root,text='是否使用模板顺序（选择后，跳过未翻译将无效）',variable=vvvv)
    ffff.pack()
    return root


class key_mouse_manager():

    def __init__(self):
        self.root = create_window()
        self.edit_window = None
        self.edit_toggle = True
    
    def on_key_down(self,event):
        if event.Key in ['F1','F2','F3','F4']:
            if event.Key == 'F1': self.func_F1()
            if event.Key == 'F2': self.func_F2()
            if event.Key == 'F3': self.func_F3()
            if event.Key == 'F4': self.func_F4()
            return False
        elif event.Key in ['Lwin',
                         'Rwin',
                         'Lcontrol',
                         'Rcontrol',
                         'Lmenu',
                         'Rmenu']: # 目前测试似乎存在组合键异常的问题，暂时去除
            return False
        elif event.Key == 'Escape':
            hookmanager.UnhookKeyboard()
            hookmanager.UnhookMouse()
            win32api.PostQuitMessage()
            self.root.destroy()
            return False
        else:
            return True


    def func_F1(self):
        print('F1')
        if self.edit_window is None:
            self.edit_window = self.root
            self.edit_window.mainloop()
        elif self.edit_window is not None:
            if self.edit_toggle == True:
                self.edit_window.withdraw()
                self.edit_toggle = False
            else:
                self.edit_window.deiconify() # 显示隐藏窗口。withdraw 和 deiconify 为配对的函数。
                self.edit_toggle = True

    def func_F2(self):
        print('F2')
        # 这里主要处理的开始录制的行为，有窗口存在则会主动关闭窗口
        if self.edit_window is not None:
            self.edit_window.withdraw()
            self.edit_toggle = False

    def func_F3(self):
        print('F3')
        # 预计要扩展测试执行的功能

    def func_F4(self):
        print('F4')
        # 暂时为保留扩展


    # 鼠标相关的内容在这里实现
    def on_mouse_event(self,event):
        msg = event.MessageName
        tim = event.Time
        pos = event.Position
        #print("MessageName:",   msg)
        #print("Time:",          tim)
        print("Position:",      pos)
        return True


if __name__ == '__main__':
    mykbmanager = key_mouse_manager()
    hookmanager = pyHook.HookManager()
    hookmanager.KeyDown  = mykbmanager.on_key_down
    hookmanager.MouseAll = mykbmanager.on_mouse_event
    hookmanager.HookKeyboard()
    hookmanager.HookMouse()
    pythoncom.PumpMessages()


