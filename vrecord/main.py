import os
import json
import shutil
import traceback

import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import scrolledtext
from tkinter.simpledialog import askstring
from tkinter.font import Font

def get_homepath(_dir=None):
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
font = Font(family='Consolas',size=10)

def load_file_tree(
        local_dir,
        tree,
        local_node  = None,
        ignore      = ["__pycache__","__init__.py"],
        exignore    = [],
        mapdir_name = {},
        sorter      = {}
    ):
    ignore.extend(exignore)
    next_nodes = []
    for idx,i in enumerate(os.listdir(local_dir)):
        if i in ignore: continue
        abs_path = '/'.join([local_dir,i]).replace('\\','/')
        next_node = local_node if local_node else ""
        if os.path.isdir(abs_path):
            name = mapdir_name.get(i) if mapdir_name.get(i) is not None else i
            idx = sorter.get(i) if i in sorter else 100000
            node = tree.insert(next_node,idx,text=name,values=abs_path)
            next_nodes.append((abs_path,node))
        elif os.path.isfile(abs_path):
            tree.insert(next_node,idx,text=i,values=abs_path)
    for abs_path, node in next_nodes:
        load_file_tree(
            abs_path, tree, node,
            ignore      = ignore,
            mapdir_name = mapdir_name,
            sorter      = sorter
        )

def tree_on_select(tree):
    items = tree.selection()
    if len(items) != 1: return
    filepath = ''.join(tree.item(items[0],"values"))
    if os.path.isfile(filepath):
        # size = os.path.getsize(filepath)
        pass
    elif os.path.isdir(filepath):
        for item in tree.get_children():
            cfilepath = ''.join(tree.item(item,"values"))
            if filepath == cfilepath:
                projectname = tree.item(item, 'text')
                change_project(projectname)

class SimpleDialog:
    def __init__(self, master,
                 text='', buttons=[], default=None, cancel=None,
                 title=None, class_=None):
        self.root = tkinter.Toplevel(master, class_=class_) if class_ else tkinter.Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)
        self.message = tkinter.Message(self.root, text=text, aspect=400)
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

PROJECT = '.vrecord'
PROJECTDEFAULTNAME = '默认项目'
PROJECTHOME = get_homepath(PROJECT)
PROJECTDEFAULT = os.path.join(PROJECTHOME, PROJECTDEFAULTNAME)
PROJECTSTRUCT = ['操作', '识别', '启动', '合并']
PROJECTCURR = PROJECTDEFAULTNAME
PROJECTDEFAULTCONFIG = 'c4ca4238a0b923820dcc509a6f75849b'
PROJECTCONFIGNAME = 'vconfig.cfg'
PROJECTCONFIGFILE = os.path.join(PROJECTHOME, PROJECTCONFIGNAME)

def init_project():
    if not os.path.isdir(PROJECTHOME): 
        os.mkdir(PROJECTHOME)
    if not os.path.isdir(PROJECTDEFAULT):
        for i in PROJECTSTRUCT:
            d = os.path.join(PROJECTDEFAULT, i)
            if not os.path.isdir(d):
                os.makedirs(d)
    change_project(PROJECTDEFAULTNAME)
    reload_file_tree()

def clear_tree(*a):
    for item in tree.get_children():
        tree.delete(item)

def reload_file_tree():
    clear_tree()
    exignore = [PROJECTCONFIGNAME]
    load_file_tree(PROJECTHOME, tree, exignore=exignore, sorter={'默认项目':0})

def change_project(projectname):
    global PROJECTCURR
    oprojectname = PROJECTCURR
    PROJECTCURR  = projectname
    rlab1['text'] = '当前项目[{}]'.format(projectname)
    if oprojectname not in notebooks:
        fr = Frame(rightfr)
        nb = ttk.Notebook(fr)
        fr.pack(expand=True,fill="both")
        nb.pack(expand=True,fill="both")
        notebooks[oprojectname] = {'fr': fr, 'nb': nb, 'init':False}
    notebooks[oprojectname]['fr'].forget()
    if projectname not in notebooks:
        fr = Frame(rightfr)
        nb = ttk.Notebook(fr)
        fr.pack(expand=True,fill="both")
        nb.pack(expand=True,fill="both")
        notebooks[projectname] = {'fr': fr, 'nb': nb, 'init':False}
    else:
        notebooks[projectname]['fr'].pack(expand=True,fill="both")
    if notebooks[projectname]['init'] == False:
        notebooks[projectname]['init'] = True
        _config = CONFIG.get(projectname)
        if _config:
            for x,y in _config.items():
                d = y.copy()
                make_tab(nb, d.pop('name'), **d)
        else:
            _config = CONFIG.get(PROJECTDEFAULTCONFIG)
            for x,y in _config.items():
                d = y.copy()
                make_tab(nb, d.pop('name'), **d)
            CONFIG[projectname] = _config.copy()


def create_project(*a):
    projectname = askstring('项目名称','请输入项目名称，尽量不要使用特殊字符。')
    if not projectname: return 
    try:
        for i in PROJECTSTRUCT:
            d = os.path.join(PROJECTHOME, projectname, i)
            if not os.path.isdir(d):
                os.makedirs(d)
        change_project(projectname)
        reload_file_tree()
    except:
        einfo = '创建项目失败.'
        tkinter.messagebox.showinfo(einfo,traceback.format_exc())

def change_or_choice_project(*a):
    v = os.listdir(PROJECTHOME)
    if PROJECTCONFIGNAME in v: v.remove(PROJECTCONFIGNAME)
    if PROJECTDEFAULTNAME in v:v.remove(PROJECTDEFAULTNAME)
    v = [PROJECTDEFAULTNAME] + v
    g = SimpleDialog(root, buttons=v, default=0, cancel=-1)
    g = g.go()
    if g != -1:
        projectname = v[g]
        change_project(projectname)

def delete_project(*a):
    v = os.listdir(PROJECTHOME)
    if PROJECTCONFIGNAME in v: v.remove(PROJECTCONFIGNAME)
    if PROJECTDEFAULTNAME in v:v.remove(PROJECTDEFAULTNAME)
    if len(v) == 0:
        einfo = '无法删除默认项目.'
        tkinter.messagebox.showinfo(einfo, einfo)
        return
    g = SimpleDialog(root, buttons=v, default=0, cancel=-1)
    g = g.go()
    if g != -1:
        projectname = v[g]
        d = os.path.join(PROJECTHOME, projectname)
        shutil.rmtree(d)
        change_project(PROJECTDEFAULTNAME)
        reload_file_tree()
        try: CONFIG.pop(projectname)
        except: pass

def save_project(*a):
    with open(PROJECTCONFIGFILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(CONFIG, indent=4))

fr      = Frame(root)
topfr   = Frame(fr)
leftfr  = Frame(fr)
rightfr = Frame(fr)
fr.pack(expand=True,fill='both')
topfr  .pack(side='top',fill='x')
leftfr .pack(side='left',expand=True,fill='both')
rightfr.pack(side='left',expand=True,fill='both')
rlab1 = Label(topfr,text='当前项目[{}]'.format(PROJECTDEFAULTNAME))
rlab1.pack(side='left')
tbtn1 = Button(topfr,text='创建',width=4, command=create_project)
tbtn1.pack(side='right')
tbtn2 = Button(topfr,text='删除',width=4, command=delete_project)
tbtn2.pack(side='right')
tbtn3 = Button(topfr,text='选择',width=4, command=change_or_choice_project)
tbtn3.pack(side='right')
tbtn3 = Button(topfr,text='保存',width=4, command=save_project)
tbtn3.pack(side='right')

# 树状图frame
tree = Treeview(leftfr, show="tree")
tree.pack(side='left',fill="both")
tree.column("#0",minwidth=0,width=100, stretch='no')

# notebook页frame
# 不同的项目需要不同的 notebook
notebooks = {}

def create_pack_code_style(codetxt):
    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        d = ColorDelegator()
        Percolator(codetxt).insertfilter(d)
    except:
        import traceback
        traceback.print_exc()

def create_txt_fr():
    tempfr = Frame()
    codetxt = Text(tempfr)
    codetxt.pack(expand=True,fill='both')
    create_pack_code_style(codetxt)
    return tempfr

def create_lab_fr(text):
    tempfr = Frame()
    labtxt = Label(tempfr, text=text)
    labtxt.pack(expand=True,fill='both')
    return tempfr

def create_tab(notebook, frame, name, **kw):
    v = set(notebook.tabs())
    notebook.add(frame, text=name)
    tab_id = (set(notebook.tabs())^v).pop() 

def make_tab(notebook, name, **kw):
    if kw.get('type') == 'txt':
        create_tab(notebook, create_txt_fr(), name, **kw)
    elif kw.get('type') == 'lab':
        create_tab(notebook, create_lab_fr(text=kw.get('text')), name, **kw)
    else:
        print('none type setting.')




def bind_ctl_key(func, key=None, shift=False):
    key = key.upper() if shift else key
    root.bind("<Control-{}>".format(key),lambda e:func())






# 需要用一个 json 来保存相应的配置信息
CONFIG = {
    PROJECTDEFAULTNAME: { # 默认空间的配置
        0:{
            'name':'帮助',
            'type':'lab',
            'text':'asdfasdf',
        },
        1:{
            'name':'代码',
            'type':'txt',
            'text':'asdfasdf',
        }
    },
}

CONFIG[PROJECTDEFAULTCONFIG] = { # 没有配置时使用的配置
    0:{
        'name':'帮助',
        'type':'lab',
        'text':'感觉还是稍微有点奇怪的默认处理方式',
    },
    1:{
        'name':'代码',
        'type':'txt',
        'text':'asdfasdf',
    }
}


if __name__ == '__main__':
    init_project()
    root.geometry('400x500+100+100')
    root.bind('<Escape>',lambda e:root.quit())
    tree.bind("<<TreeviewSelect>>", lambda e:tree_on_select(tree))
    root.mainloop()







