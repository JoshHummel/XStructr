import sys
from tkinter import *
from tkinter import ttk
from tkinter.constants import *
import os.path
import re
from physics import main_phys
from electronconfig import orbital_sim

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

class Options:
    def __init__(self, top=None):
        self.top = top
        
        self.mode = 0
        
        #Atomic Physics Options
        self.sdt = StringVar()
        self.slen = StringVar()
        self.cdt = StringVar()
        self.sc = StringVar()
        self.npart = StringVar()
        
        self.simstep = ttk.Entry(self.top)
        self.simstep.place(relx=0.433, rely=0.311, height=20, relwidth=0.14)
        self.simstep.configure(background="white", textvariable=self.sdt)
        self.simstep.configure(font="-family {Courier New} -size 10")
        self.simstep.configure(foreground="#000000")
        
        self.simstep_lbl = ttk.Label(self.top)
        self.simstep_lbl.place(relx=0.35, rely=0.311, height=21, width=54)
        self.simstep_lbl.configure(anchor='w')
        self.simstep_lbl.configure(background="#d9d9d9")
        self.simstep_lbl.configure(compound='left')
        self.simstep_lbl.configure(font="-family {Segoe UI} -size 9")
        self.simstep_lbl.configure(foreground="#000000")
        self.simstep_lbl.configure(text='''SDT: 10^''')
        
        self.simlen = ttk.Entry(self.top)
        self.simlen.place(relx=0.433, rely=0.244, height=20, relwidth=0.14)
        self.simlen.configure(background="white", textvariable=self.slen)
        self.simlen.configure(font="-family {Courier New} -size 10")
        self.simlen.configure(foreground="#000000")
        
        self.simlen_lbl = ttk.Label(self.top)
        self.simlen_lbl.place(relx=0.283, rely=0.244, height=21, width=94)
        self.simlen_lbl.configure(anchor='w')
        self.simlen_lbl.configure(background="#d9d9d9")
        self.simlen_lbl.configure(compound='left')
        self.simlen_lbl.configure(font="-family {Segoe UI} -size 9")
        self.simlen_lbl.configure(foreground="#000000")
        self.simlen_lbl.configure(text='''Sim Length: 10^''')\
            
        self.calcstep = ttk.Entry(self.top)
        self.calcstep.place(relx=0.433, rely=0.178, height=20, relwidth=0.14)
        self.calcstep.configure(background="white", textvariable=self.cdt)
        self.calcstep.configure(font="-family {Courier New} -size 10")
        self.calcstep.configure(foreground="#000000")

        self.calcstep_lbl = ttk.Label(self.top)
        self.calcstep_lbl.place(relx=0.35, rely=0.178, height=21, width=54)
        self.calcstep_lbl.configure(anchor='w')
        self.calcstep_lbl.configure(background="#d9d9d9")
        self.calcstep_lbl.configure(compound='left')
        self.calcstep_lbl.configure(font="-family {Segoe UI} -size 9")
        self.calcstep_lbl.configure(foreground="#000000")
        self.calcstep_lbl.configure(text='''CDT: 10^''')\
        
        self.scale = ttk.Entry(self.top)
        self.scale.place(relx=0.433, rely=0.378, height=20, relwidth=0.14)
        self.scale.configure(background="white", textvariable=self.sc)
        self.scale.configure(font="-family {Courier New} -size 10")
        self.scale.configure(foreground="#000000")

        self.scale_lbl = ttk.Label(self.top)
        self.scale_lbl.place(relx=0.3, rely=0.378, height=21, width=84)
        self.scale_lbl.configure(anchor='w')
        self.scale_lbl.configure(background="#d9d9d9")
        self.scale_lbl.configure(compound='left')
        self.scale_lbl.configure(font="-family {Segoe UI} -size 9")
        self.scale_lbl.configure(foreground="#000000")
        self.scale_lbl.configure(text='''Len Scale: 10^''')
        
        self.numpart = ttk.Entry(self.top)
        self.numpart.place(relx=0.433, rely=0.444, height=20, relwidth=0.14)
        self.numpart.configure(background="white", textvariable=self.npart)
        self.numpart.configure(font="-family {Courier New} -size 10")
        self.numpart.configure(foreground="#000000")
        
        self.nump_lbl = ttk.Label(self.top)
        self.nump_lbl.place(relx=0.35, rely=0.444, height=21, width=54)
        self.nump_lbl.configure(anchor='w')
        self.nump_lbl.configure(background="#d9d9d9")
        self.nump_lbl.configure(compound='left')
        self.nump_lbl.configure(font="-family {Segoe UI} -size 9")
        self.nump_lbl.configure(foreground="#000000")
        self.nump_lbl.configure(text='''# part. :''')

        self.settings_lbl = ttk.Label(self.top)
        self.settings_lbl.place(relx=0.283, rely=0.089, height=21, width=54)
        self.settings_lbl.configure(anchor='w')
        self.settings_lbl.configure(background="#d9d9d9")
        self.settings_lbl.configure(compound='left')
        self.settings_lbl.configure(font="-family {Segoe UI} -size 9")
        self.settings_lbl.configure(foreground="#000000")
        self.settings_lbl.configure(text='''Settings:''')
        
        #Orbital Model settings
        self.nval = StringVar()
        self.lval = StringVar()
        self.mlval = StringVar()
        
        self.n = ttk.Entry(self.top)
        #self.n.place(relx=0.433, rely=0.178, height=20, relwidth=0.14)
        self.n.configure(background="white", textvariable=self.nval)
        self.n.configure(font="-family {Courier New} -size 10")
        self.n.configure(foreground="#000000")
        
        self.n_lbl = ttk.Label(self.top)
        #self.n_lbl.place(relx=0.29, rely=0.178, height=21, width=85)
        self.n_lbl.configure(anchor='w')
        self.n_lbl.configure(background="#d9d9d9")
        self.n_lbl.configure(compound='left')
        self.n_lbl.configure(font="-family {Segoe UI} -size 9")
        self.n_lbl.configure(foreground="#000000")
        self.n_lbl.configure(text='''n quant. num.:''')
        
        self.l = ttk.Entry(self.top)
        #self.l.place(relx=0.433, rely=0.244, height=20, relwidth=0.14)
        self.l.configure(background="white", textvariable=self.lval)
        self.l.configure(font="-family {Courier New} -size 10")
        self.l.configure(foreground="#000000")
        
        self.l_lbl = ttk.Label(self.top)
        #self.l_lbl.place(relx=0.295, rely=0.244, height=21, width=85)
        self.l_lbl.configure(anchor='w')
        self.l_lbl.configure(background="#d9d9d9")
        self.l_lbl.configure(compound='left')
        self.l_lbl.configure(font="-family {Segoe UI} -size 9")
        self.l_lbl.configure(foreground="#000000")
        self.l_lbl.configure(text='''l quant. num.:''')
        
        self.ml = ttk.Entry(self.top)
        #self.ml.place(relx=0.433, rely=0.311, height=20, relwidth=0.14)
        self.ml.configure(background="white", textvariable=self.mlval)
        self.ml.configure(font="-family {Courier New} -size 10")
        self.ml.configure(foreground="#000000")
        
        self.ml_lbl = ttk.Label(self.top)
        #self.ml_lbl.place(relx=0.275, rely=0.311, height=21, width=90)
        self.ml_lbl.configure(anchor='w')
        self.ml_lbl.configure(background="#d9d9d9")
        self.ml_lbl.configure(compound='left')
        self.ml_lbl.configure(font="-family {Segoe UI} -size 9")
        self.ml_lbl.configure(foreground="#000000")
        self.ml_lbl.configure(text='''ml quant. num.:''')
        
        self.scale = ttk.Entry(self.top)
        #self.scale.place(relx=0.433, rely=0.378, height=20, relwidth=0.14)
        self.scale.configure(background="white", textvariable=self.sc)
        self.scale.configure(font="-family {Courier New} -size 10")
        self.scale.configure(foreground="#000000")
        
        self.scale_lbl = ttk.Label(self.top)
        #self.scale_lbl.place(relx=0.3, rely=0.378, height=21, width=84)
        self.scale_lbl.configure(anchor='w')
        self.scale_lbl.configure(background="#d9d9d9")
        self.scale_lbl.configure(compound='left')
        self.scale_lbl.configure(font="-family {Segoe UI} -size 9")
        self.scale_lbl.configure(foreground="#000000")
        self.scale_lbl.configure(text='''Len Scale: 10^''')
    
    def update_details(self, select):
        
        if len(select) == 1:
            if int(select[0]) == 0:
                self.mode = 0
        
                # Show Atomic Physics options
                self.numpart.place(relx=0.433, rely=0.444, height=20, relwidth=0.14)
                self.simstep.place(relx=0.433, rely=0.311, height=20, relwidth=0.14)
                self.simlen.place(relx=0.433, rely=0.244, height=20, relwidth=0.14)
                self.simlen_lbl.place(relx=0.283, rely=0.244, height=21, width=94)
                self.simstep_lbl.place(relx=0.35, rely=0.311, height=21, width=54)
                self.scale.place(relx=0.433, rely=0.378, height=20, relwidth=0.14)
                self.scale_lbl.place(relx=0.3, rely=0.378, height=21, width=84)
                self.nump_lbl.place(relx=0.35, rely=0.444, height=21, width=54)
                self.calcstep.place(relx=0.433, rely=0.178, height=20, relwidth=0.14)
                self.calcstep_lbl.place(relx=0.35, rely=0.178, height=21, width=54)
                
                # Hide Molecular Orbitals Options
                self.n.place(relx=0, rely=0, height=0, relwidth=0)
                self.n_lbl.place(relx=0, rely=0, height=0, relwidth=0)
                self.l.place(relx=0, rely=0, height=0, relwidth=0)
                self.l_lbl.place(relx=0, rely=0, height=0, relwidth=0)
                self.ml.place(relx=0, rely=0, height=0, relwidth=0)
                self.ml_lbl.place(relx=0, rely=0, height=0, relwidth=0)
                self.scale.place(relx=0, rely=0, height=0, relwidth=0)
                self.scale_lbl.place(relx=0, rely=0, height=0, relwidth=0)
                
            elif int(select[0]) == 1:
                self.mode = 1
                
                # Hide Atomic Physics options
                self.numpart.place(relx=0, rely=0, height=0, relwidth=0)
                self.simstep.place(relx=0, rely=0, height=0, relwidth=0)
                self.simlen.place(relx=0, rely=0, height=0, relwidth=0)
                self.simlen_lbl.place(relx=0, rely=0, height=0, width=0)
                self.simstep_lbl.place(relx=0, rely=0, height=0, width=0)
                self.scale.place(relx=0, rely=0, height=0, relwidth=0)
                self.scale_lbl.place(relx=0, rely=0, height=0, width=0)
                self.nump_lbl.place(relx=0, rely=0, height=0, width=0)
                self.calcstep.place(relx=0, rely=0, height=0, relwidth=0)
                self.calcstep_lbl.place(relx=0, rely=0, height=0, width=0)
                
                # Show Molecular Orbitals options
                self.n.place(relx=0.433, rely=0.178, height=20, relwidth=0.14)
                self.n_lbl.place(relx=0.29, rely=0.178, height=21, width=85)
                self.l.place(relx=0.433, rely=0.244, height=20, relwidth=0.14)
                self.l_lbl.place(relx=0.295, rely=0.244, height=21, width=85)
                self.ml.place(relx=0.433, rely=0.311, height=20, relwidth=0.14)
                self.ml_lbl.place(relx=0.275, rely=0.311, height=21, width=90)
                self.scale.place(relx=0.433, rely=0.378, height=20, relwidth=0.14)
                self.scale_lbl.place(relx=0.3, rely=0.378, height=21, width=84)
                
        
    def run_program(self):
        print("Running Program")
        if self.mode == 0:
            #run atomic physics module
            print("AP Selected")
        
            main_phys(int(self.sdt.get()), int(self.slen.get()), int(self.cdt.get()), int(self.sc.get()), int(self.npart.get()))
            
        elif self.mode == 1:
            #run molecular orbitals module
            print("MO Selected")
            if (int(self.nval.get()) >= 0 and int(self.nval.get()) <= 3 and int(self.lval.get()) >= 0 and int(self.lval.get()) <= int(self.nval.get()) - 1 and int(self.mlval.get()) >= -1*(int(self.nval.get()) - 1) and int(self.mlval.get()) <= (int(self.nval.get()) - 1)):
                orbital_sim(6, int(self.nval.get()), int(self.lval.get()), int(self.mlval.get()), 10**int(self.sc.get()))
            else:
                print("Invalid input variables.")

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x450+717+221")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("XStructr Config")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top

        self.menubar = Menu(top,font="ttkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        apo = Options(self.top)

        choices = ["Atomic Physics", "Orbital Models"]
        choicesvar = StringVar(value=choices)
        self.options = Listbox(self.top, listvariable=choicesvar)
        self.options.place(relx=0.033, rely=0.089, relheight=0.493
                , relwidth=0.2)
        self.options.configure(background="#e6fbff")
        self.options.configure(font="TkFixedFont")
        self.options.configure(foreground="#000000")
        self.options.bind("<<ListboxSelect>>", lambda e: apo.update_details(self.options.curselection()))
        self.run_button = ttk.Button(self.top)
        self.run_button.place(relx=0.6, rely=0.511, height=26, width=47)
        self.run_button.configure(text='''Run''', command=apo.run_program)
        self.top.bind('<Return>', lambda e: self.run_button.invoke())

        

def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5

if __name__ == "__main__":
    
    root = Tk()
    root.option_add('*tearOff', FALSE)
    
    window = Toplevel1(root)
    root.mainloop()