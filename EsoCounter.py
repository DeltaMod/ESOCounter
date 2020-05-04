# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:05:55 2020
@author: Vidar Flodgren
Github: https://github.com/DeltaMod
"""
from win32api import GetAsyncKeyState
import threading
import tkinter as tk
import os
import json
import sys
from time import gmtime, strftime, sleep
from bindglobal import BindGlobal


# Use Later - For including the ascii file in the installation
#        import sys

# if getattr(sys, 'frozen', False):
#     image = PhotoImage(file=os.path.join(sys._MEIPASS, "files/bg.png"))
# else:
#     image = PhotoImage(file="files/bg.png")
# And then bundle it with pyinstaller like this:

# pyinstaller --clean -y -n "output_name" --add-data="files\bg.png;files" script.py

# pyinstaller --onefile --noconsole -i"C:\Users\Vidar\Dropbox\Code Projects\ESOCounter\EsoCounterIcon.ico" "C:\Users\Vidar\Dropbox\Code Projects\ESOCounter\EsoCounter.py"




"""
######################### Initialisation Setup #########################
"""
CD = os.getcwd()+'\\Settings\\'
#Check if default parameters exist - and if not, create the .json files that the script will load from.
DEBUG = False
def RestoreDCS():              
       #We make a default colour scheme file - that can either be altered or restored from the script 
       json.dump({'root':'darkgrey',
                  'frame':'moccasin',
                  'border':'goldenrod',
                  'button':'snow',
                  'check':'grey',
                  'label':'grey',
                  'labelrelief':'flat',
                  'EnergyBorder':'cadetblue',
                  'EnergyFill':'snow',
                  'FontParam':('Courier New',14,'bold'),
                  'FontC':'White',
                  'SimMad':'Red',
                  'SimOK':'snow'}, 
                 open(CD+"CS.json", 'w' ))
def RestoreCCS(): 
       #We create the basic custom colour profile, incase people wish to use it.
       json.dump({'root':'darkgrey',
                  'frame':'moccasin',
                  'border':'goldenrod',
                  'button':'snow',
                  'check':'grey',
                  'label':'grey',
                  'labelrelief':'flat',
                  'EnergyBorder':'cadetblue',
                  'EnergyFill':'snow',
                  'FontParam':('Courier New',14,'bold'),
                  'FontC':'White',
                  'SimMad':'Red',
                  'SimOK':'snow'}, 
                 open(CD+"CustomCS.json", 'w' ))

def RestoreInit():
       json.dump({'UseCustom':False},
                  open(CD+"Init.json", 'w' ))      
def RestoreAscii():
       SimAscii = """                                               ------                                               
                                              -======-                                              
                                              -======-                                              
                                              -======-                                              
                                         :==- -======- -==:                                         
                                         ===- -======- -===                                         
                                        -===- -======- -===-                                        
                           -:::         :===- -======- -===:         :::-                           
                          :====:-      -====- -======- -====       -:====:                          
                          =======-     :====- -======- -====-     -=======                          
              -           :=======-    :====- -======- -====:    -=======:           -              
            -:==:-        :========:  -=====- -======- -=====-  :========:        -:==:-            
          -:=======:-     :=========: :=====- -======- -=====: :=========:     -:=======:-          
         :============:-  -=========: ======- -======- -====== :=========-  -:============:         
         -===============:--::======--======- -======- -======--======::--:===============-         
          -=================:---:==: :======- -======- -======: :==:---:=================-          
           -===================:-----=======- -======- -=======-----:===================-           
            -:====================: :=======- -======- -=======: :====================:-            
              :===================: ========- -======- -=======: :===================:              
            -- :==================--========- -======- -========--==================: --            
           :==  :================= :========- -======- -========: =================:  ==:           
         -===-   :===============: =========- -======- -========= :===============:   -===-         
        :===-     :============::--:========- -======- -========:--::============:     -===:        
       -====       :========:--      -:=====- -======- -=====:-      --:========:       ====-       
       :====-       :===::-             -::=- -======- -=::-             -::===:       -====:       
       -====:        ---                      -======-                      ---        :====-       
        :=====-                           --:==========:--                           -=====:        
         :======:-                    --:==================:--                    -:======:         
          -:=======:--            --:==========================:--            --:=======:-          
            -:=========:::::::::====================================:::::::::=========:-            
              -::==================================================================::-              
                 --:============================================================:--                 
                      -::==================================================::-                      
                           ---:::==================================:::---                           
                                     ==========================                                     """
       with open(CD+"Ascii4.json", "w") as text_file:
              text_file.write(SimAscii)
       
if os.path.exists(CD) == False:
       os.mkdir(CD)       
       #We make an initialisation file that can be changed manually after first creation
       RestoreInit()
       RestoreDCS()
       RestoreCCS()

if 'Init.json' not in os.listdir(CD):
       RestoreInit()

if 'CS.json' not in os.listdir(CD):
       RestoreDCS()

if 'CustomCS.json' not in os.listdir(CD):
       RestoreCCS()
       
if 'Ascii4.json' not in os.listdir(CD):
       RestoreAscii()
       
if DEBUG == True:
       RestoreCCS()
       RestoreDCS()
       RestoreInit()



def key_down(key):
       state = GetAsyncKeyState(key)
       if (state != 0) and (state != 1):
            return True
       else:
            return False

    
"""
######################### Extra Functions #########################

"""
def floor(n):
    res = int(n)
    return res if res == n or n >= 0 else res-1

def GetTime(rawtime):
    seconds  = floor(rawtime)
    decimals = rawtime - seconds
    SecTime = strftime("%H:%M:%S", gmtime(seconds))
    RealTime = SecTime+str('%.3f'% decimals)[1:]
    RealTime = RealTime[6:]
    return(RealTime,rawtime)

"""
######################### GUI Generation #########################
"""


class ESOGUI(object):
       LABEL_TEXT = [  "ESOGUI!",
                    "Can't count to 10?",
                    "This GUI literally only counts down from 10",
                    "You want me to add the other abilities too?",
                    "No, I probably won't"]

       def __init__(self, master):   
              self.Ini              = json.load( open(CD+"Init.json" ))        
              self.master           = master 
              self.surpress_verbose = False 
              master.title('ESOGUI v0.1')
              #Setup Window Parameters
              self.XDIM = int(1600/4)
              self.YDIM = int(900/4)
              BDW = 2
              root.geometry('{}x{}'.format(2*self.XDIM,self.YDIM))
              
              #Load Colorscheme and Ascii
              if self.Ini['UseCustom']==True:
                     self.CS = json.load( open(CD+"CustomCS.json" ) )
              else:
                     self.CS = json.load( open(CD+"CS.json" ) )
              root.config(bg=self.CS['root'])
              with open(CD+'Ascii4.json', 'r') as f:
                     self.Ascii4 = f.read()

              self.BGWin = tk.Frame(root, bg=self.CS['root'],highlightbackground=self.CS['border'], highlightthickness=BDW,
                                   width=self.XDIM, height=self.YDIM, padx=10, pady=10, relief='flat')
              self.BGWin.pack(anchor='nw',expand=True,fill='both')
              
              self.ESOW = tk.Frame(self.BGWin, bg=self.CS['root'],padx=10, pady=10, relief='flat')
              self.ESOW.pack(side='top',anchor='nw',expand=True,fill='both')
              
              self.AF = {}
              for i in range(0,4):
                     self.AF[str(i+1)] = tk.Frame(self.ESOW,bg=self.CS['root'],padx=5, pady=5, relief='flat')
                     self.AF[str(i+1)].pack(anchor='nw',expand=True,side='left',fill='both')
                     
              
              #Create the countdown timers as [0 seconds since last cast], and set them to be [ready to cast]
              self.ACD   = {} #String variable for countdown timer
              self.ASec  = {} #Double var for the seconds left of the countdown
              self.ARDY  = {} #Bool to determine if Simaris will be mad when you press an ability
              self.AProc = {} #String var to remember the correct name of the after function in order to turn it off
              
              self.CDRes = 100 #Resolution of the countdown, in ms
              
              for i in range(0,4):
                     self.ACD[str(i+1)] = tk.StringVar() 
                     self.ACD[str(i+1)].set(GetTime(0)[0])
                     
                     self.ASec[str(i+1)] = tk.DoubleVar() 
                     self.ASec[str(i+1)].set(0)
                     
                     self.ARDY[str(i+1)] = tk.BooleanVar(root)
                     self.ARDY[str(i+1)].set(True)
                     
                     self.AProc[str(i+1)] = tk.StringVar(root)
                     self.AProc[str(i+1)].set(None)
              
              self.ATText = {}
              self.ATAscii = {}
              for i in range(0,4):
                     self.ATText[str(i+1)]  = tk.Label(self.AF[str(i+1)],textvariable = self.ACD[str(i+1)],bg=self.CS['root'],font=self.CS['FontParam'],fg=self.CS['FontC']) 
                     self.ATText[str(i+1)].pack(side='bottom',expand=True,fill='both')
                     
                     self.ATAscii[str(i+1)]  = tk.Label(self.AF[str(i+1)],bg=self.CS['root'],font=("Courier New",1,"bold"),justify='left',text = self.Ascii4,fg=self.CS['SimOK']) 
                     self.ATAscii[str(i+1)].pack(side='top',expand=True,fill='both')
                     
              
              self.EBF = tk.Frame(self.BGWin,bg=self.CS['EnergyFill'],highlightbackground=self.CS['EnergyBorder'], highlightthickness=BDW+2,padx=5, pady=5, relief='raised')
              self.EBF.pack(anchor='sw',expand=True,side='bottom',fill='both')
              def UserInput(t,ability):
                     self.LastInput = ability
                     if self.ARDY[ability].get() == False:
                            try:
                                root.after_cancel(self.AProc[ability].get())
                                self.ARDY[ability].set(False)
                                self.ACD[ability].set(GetTime(t))
                                self.ASec[ability].set(t)
                                self.ATAscii[ability].config(fg=self.CS['SimMad'])
                                self.ATText[ability].config(fg=self.CS['SimMad'])
                                ATimer()
                            except None:
                                   print('something is funky')
                     elif self.ARDY[ability].get() == True:
                            self.ARDY[ability].set(False)
                            self.ACD[ability].set(GetTime(t))
                            self.ASec[ability].set(t)
                            
                            self.ATAscii[ability].config(fg=self.CS['SimMad'])
                            self.ATText[ability].config(fg=self.CS['SimMad'])
                            
                            ATimer()
                            
              def ATimer():     
                     #elif self.ARDY[ability].get()==False:
                     #      root.after_cancel(_callback_id.get())
                     #Continue from this: https://stackoverflow.com/questions/57816486/how-to-stop-this-after-function-in-python-tkinter
                     ability = self.LastInput
                     
                     if self.ASec[ability].get() > 0.0001:
                            
                            self.ASec[ability].set(self.ASec[ability].get() - self.CDRes/1000) 
                            self.ACD[ability].set(GetTime(self.ASec[ability].get())[0])
                            self.AProc[ability].set(root.after(self.CDRes, ATimer))
                                                    
                     elif self.ASec[ability].get()<=0.0001:
                            
                            self.ACD[ability].set(GetTime(0)[0])
                            self.ASec[ability].set(0)
                            self.ARDY[ability].set(True)
                            self.ATAscii[ability].config(fg=self.CS['SimOK'])
                            self.ATText[ability].config(fg=self.CS['SimOK'])
                            root.after_cancel(self.AProc[ability].get()) 
              def key(event):
                     if event == '4':
                            UserInput(10,event) #seconds, key, 
              
              def CheckState():
                     Key4 = key_down(0x34)
                     if Key4 is True:
                            key('4')
                            sleep(0.1)
                            print('It is pressed, mkay')
                                   
              
                     root.after(100, CheckState)
              root.after(100, CheckState)
                            
              
       def Window_Exit_Event(self):
              #if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
              root.destroy()
              sys.exit()



root = tk.Tk()

EGUI = ESOGUI(root)
root.protocol("WM_DELETE_WINDOW", EGUI.Window_Exit_Event)
root.attributes('-alpha', 0.8)
#root.overrideredirect(1)
root.mainloop()


                     