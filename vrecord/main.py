import os
import tkinter
import tkinter.ttk as ttk
from tkinter import scrolledtext

def get_homepath(_dir=None):
    # 放置配置文件的地址。
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    return home if _dir is None else os.path.join(home, _dir)

Frame    = tkinter.Frame
Treeview = ttk.Treeview
Label    = ttk.Label
Button   = ttk.Button
Text     = scrolledtext.ScrolledText
Combobox = ttk.Combobox
Entry    = ttk.Entry
Checkbutton = tkinter.Checkbutton

root = tkinter.Tk()

def load_file_tree(
        local_dir,
        tree,
        local_node  = None,
        ignore      = ["__pycache__"],
        mapdir_name = {},
    ):
    next_nodes = []
    for idx,i in enumerate(os.listdir(local_dir)):
        if i in ignore: continue
        abs_path = '/'.join([local_dir,i]).replace('\\','/')
        next_node = local_node if local_node else ""
        if os.path.isdir(abs_path):
            name = mapdir_name.get(i) if mapdir_name.get(i) is not None else i
            node = tree.insert(next_node,idx,text=name)
            next_nodes.append((abs_path,node))
        elif os.path.isfile(abs_path):
            tree.insert(next_node,idx,text=i,values=abs_path)
    for abs_path, node in next_nodes:
        load_file_tree(
            abs_path, tree, node,
            ignore      = ignore,
            mapdir_name = mapdir_name,
        )

def tree_on_select(tree, codetxt):
    items = tree.selection()
    if len(items) != 1: return
    filepath = ''.join(tree.item(items[0],"values"))
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        codetxt.delete(0.,"end")
        if size < 5*2**20:
            for idx,i in enumerate(open(filepath,encoding="utf-8").readlines()):
                codetxt.insert(tkinter.END,i)
        else:
            codetxt.insert(0.,"file is too large. (codefile size limit: 5M).")


fr      = Frame(root)
topfr   = Frame(fr)
leftfr  = Frame(fr)
rightfr = Frame(fr)
fr.pack(expand=True,fill='both')
topfr  .pack(side='top',fill='x')
leftfr .pack(side='left',expand=True,fill='both')
rightfr.pack(side='left',expand=True,fill='both')
tbtn1 = Button(topfr,text='创建项目',width=7)
tbtn1.pack(side='right')
tbtn2 = Button(topfr,text='删除项目',width=7)
tbtn2.pack(side='right')
tbtn3 = Button(topfr,text='选择项目',width=7)
tbtn3.pack(side='right')


tree = Treeview(leftfr, show="tree")
tree.pack(side='left',fill="both")
tree.column("#0",minwidth=0,width=110, stretch='no')# 整理长度

homepath_filedir = get_homepath('.vscrapy')# 暂时使用 C:\Users\Administrator\.vscrapy 作为测试
mapdir_name = {'v':'你好'}
load_file_tree(homepath_filedir, tree, mapdir_name=mapdir_name)

nb = ttk.Notebook(rightfr)
nb.pack(expand=True,fill="both")
def create_tab(frame, name):
    v = set(nb.tabs())
    nb.add(frame, text=name)
    tab_id = (set(nb.tabs())^v).pop() 
    # nb.select(tab_id)
tempfr = Frame()
codetxt = Text(tempfr)
codetxt.pack(expand=True,fill='both')
create_tab(tempfr, '123123')
tempfr = Frame()
create_tab(tempfr, '333333')


try:
    from idlelib.colorizer import ColorDelegator
    from idlelib.percolator import Percolator
    d = ColorDelegator()
    Percolator(codetxt).insertfilter(d)
except:
    import traceback
    traceback.print_exc()

# root.geometry('600x725+100+100')
root.bind('<Escape>',lambda e:root.quit())
tree.bind("<<TreeviewSelect>>", lambda e:tree_on_select(tree, codetxt))
root.mainloop()



from tkinter import (
    Toplevel,
    Message,
)

class SimpleDialog:
    def __init__(self, master,
                 text='', buttons=[], default=None, cancel=None,
                 title=None, class_=None):
        self.root = Toplevel(master, class_=class_) if class_ else Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)
        self.message = Message(self.root, text=text, aspect=400)
        self.message.pack(expand=1, fill='both')
        self.frame = Frame(self.root)
        self.frame.pack(fill='both')
        self.num = default
        self.cancel = cancel
        self.default = default
        self.root.bind('<Return>', self.return_event)
        for num in range(len(buttons)):
            s = buttons[num]
            b = Button(self.frame, text=s,
                       command=(lambda self=self, num=num: self.done(num)))
            b.pack(side='top', fill='both')
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self._set_transient(master)
    def _set_transient(self, master, relx=0.5, rely=0.3):
        widget = self.root
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
        widget.update_idletasks() # Actualize geometry information
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location
    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()
        return self.num
    def return_event(self, event):
        if self.default is None:
            self.root.bell()
        else:
            self.done(self.default)
    def wm_delete_window(self):
        if self.cancel is None:
            self.root.bell()
        else:
            self.done(self.cancel)
    def done(self, num):
        self.num = num
        self.root.quit()


# def some(top, list):
#     s = SimpleDialog(
#         top,
#         buttons = list,
#         default = 0,  # 回车时的默认选项
#         cancel  = 0,  # 关闭时的默认选项
#     )
#     v = s.go()
#     print(v)
# if __name__ == '__main__':
#     # recorder_gui().start()
#     top = tkinter.Tk()
#     btn = Button(top, text='asdf', command=lambda *a:some(top, ['123','333']))
#     btn.pack()
#     top.mainloop()