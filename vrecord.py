
##import tkinter
##import pyHook
##import win32gui
##
##
##def edit_window():
##    # window 并不是唯一的，而是通过呼出创建，通过关闭
##    # 或者获取到某些按键事件之后就毁灭。
##    pass
##
##def some(editkey='F1',startkey='F2',pausekey='F3',stopkey='F4'):
##    pass
##
###v = win32gui.FindWindow('vedit','')


import pyHook
import pythoncom
import win32api
import tkinter
import threading

hookmanager = pyHook.HookManager()

class key_mouse_manager():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.withdraw() # 需要一个被隐藏的主界面，一切额外窗口循环需要该窗口存在才能
        self.edit_window = None
        self.edit_toggle = True
    
    def on_key_down(self,event):

        if event.Key in ['F1','F2','F3','F4']:
            if event.Key == 'F1': self.func_F1()
            if event.Key == 'F2': self.func_F2()
            if event.Key == 'F3': self.func_F3()
            if event.Key == 'F4': self.func_F4()
            return False

        if event.Key in ['Lwin',
                         'Rwin',
                         'Lcontrol',
                         'Rcontrol',
                         'Lmenu',
                         'Rmenu']:
            # 目前测试似乎存在组合键异常的问题，暂时去除问题
            return False

        if event.Key == 'Escape':
            # Esc 退出程序
            hookmanager.UnhookKeyboard()
            hookmanager.UnhookMouse()
            win32api.PostQuitMessage()
            self.root.destroy()
            return False


        if self.keyIsPressed:
            return True
        self.keyIsPressed = True
        return True

    def on_key_up(self,event):
        self.keyIsPressed = False
        return False


    def func_F1(self):
        print('F1')
        # 这里主要处理的创建脚本管理的窗口
        if self.edit_window is None:
            self.edit_window = tkinter.Toplevel()
            # 该窗口用于配置录制的脚本方式已经配置执行方式
            # 各种功能配置功能需要在这里实现
            self.edit_window.mainloop()
        elif self.edit_window is not None:
            if self.edit_toggle == True:
                self.edit_window.withdraw() # 这里用隐藏窗口会更加省资源一点。
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
        print("MessageName:",   msg)
        print("Time:",          tim)
        print("Position:",      pos)
        return True


if __name__ == '__main__':
    mykbmanager = key_mouse_manager()
    hookmanager.KeyDown  = mykbmanager.on_key_down
    hookmanager.KeyUp    = mykbmanager.on_key_up
    hookmanager.MouseAll = mykbmanager.on_mouse_event
    hookmanager.HookKeyboard()
    hookmanager.HookMouse()
    pythoncom.PumpMessages()


