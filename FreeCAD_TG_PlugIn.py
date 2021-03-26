"""This Macro is to provide upload facility from FreeCAD to www.truegeometry.com using API Key.
Please get your API Key by updating your profile at www.truegeometry.com"""

import platform
import sys

###Library check
try:
    import requests as rs
except ImportError:
    import subprocess
    if platform.system() == 'Windows':
        subprocess.check_call(['python', '-m', 'pip', 'install', 'requests'])
    else:
        subprocess.check_call(['python3', '-m', 'pip', 'install', 'requests'])
finally:
    import requests as rs

from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tempfile
import os
from tkinter.ttk import Progressbar

###Designe of GUI

window = Tk()
window.title("TrueGeometry Upload")
window.geometry("600x480")

def submit():

    def Progress_Bar_th():
        import time
        while(1):                
            Progress_Bar['value'] = 20
            window.update_idletasks()
            time.sleep(1)

            Progress_Bar['value'] = 40
            window.update_idletasks()
            time.sleep(1)

            Progress_Bar['value'] = 60
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 80
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 100
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 80
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 60
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 40
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 20
            window.update_idletasks()
            time.sleep(1)
            
            Progress_Bar['value'] = 0
            window.update_idletasks()
            time.sleep(1)
            

    
    def Upload_th():

        P1 = Thread(target = Progress_Bar_th, daemon = True).start()#starting the Progress Bar Thread

        ###Exporting to Object File
        file_name = App.ActiveDocument.Name
        Format = Format_Gui.get()
        path_file = tempfile.gettempdir()

        if Format == "FreeCAD Standard(.FCStd)": #For Uploading as a FreeCAD Standard Format (.FCStd)
            path_file = path_file + "/" + file_name + ".FCStd"
            App.getDocument(file_name).saveCopy(path_file)
        
        else:
            path_file = path_file + "/" + file_name + ".obj" #Path and Name of File to be exported 
            __objs__ = [] #Empty List to appending document details and all object names
            for obj in FreeCAD.ActiveDocument.Objects: #Loop for appending all the object names as string to a list
                if obj.ViewObject.isVisible():
                    __objs__.append(FreeCAD.getDocument(file_name).getObject(obj.Name)) #List with appended document details and all object names
            import Mesh
            Mesh.export(__objs__, path_file)#File Exported to object file (.obj)
            del __objs__

        ###Commands for Uploading to TrueGeometry.com
        API_Key = API_Key_Gui.get() #Permanent API Key
        url = ("http://www.truegeometry.com") #Website's URL
        r = rs.get("http://www.truegeometry.com/getUpldToken?APIKey=" + API_Key) #Temporary API Key Recieved
        Temp_APIKEY = r.json()['apiKeyToken'] #Temporary API Key
        to_Upload = {'media': open(path_file, 'rb')} #path of recently exported file
        GeometryClass = GeometryClass_Gui.get() #Getting Geometry Class
        Tags = Tags_Gui.get() #Getting Tags
        Upload_file = rs.post(url + "/upldAPI?APIKey=" + API_Key + "&APIKeyToken=" + Temp_APIKEY + "&tags=" + Tags + "&GeometryClass=" + GeometryClass, files = to_Upload)
        #File Upload command through HTTP Post using Requests Library.
        
        if Upload_file.text == 'success' : #Message to User Upload Successfull or Unsuccessful
            messagebox.showinfo("TrueGeometry", "Upload Completed Successfully!")
            window.destroy()         

        else:
            messagebox.showinfo("TrueGeometry", "Something Went Wrong, Please Try Again!")
            window.destroy()

        os.remove(path_file) #Removing the Created Object File from users Computer    
        P2.exit()        
    
    P2 = Thread(target = Upload_th, daemon = True).start()  
    
    

###Information for user 
Text_Label = tk.Label(window, text = "Get your Permanent API Key from Profile Page by \n Updagting your Profile @ www.truegeometry.com").grid(row = 0, column = 1, padx = 10, pady = 25)


### API Key Field
API_Key_Gui = tk.StringVar() #Variable declaration to get API Key input
API_Key_Label = tk.Label(window, text = "Enter API Key").grid(row = 1, padx = 10, pady = 25) 
API_Key_Entry = tk.Entry(window, textvariable = API_Key_Gui).grid(row = 1, column = 1)


### Select Geommetry Class Drop Down Menu 
ttk.Label(window, text = "Select Geometry Class").grid(row = 2, column = 0, padx = 10, pady = 25)
GeometryClass_Gui = tk.StringVar()
GeometryClassChoose = ttk.Combobox(window, width = 27, textvariable = GeometryClass_Gui)
GeometryClassChoose['values'] = ('Buildings',  
                          'Mega Structures', 
                          'Vehicles', 
                          'Ships', 
                          'Characters', 
                          'Aircraft', 
                          'Furniture', 
                          'Electronics', 
                          'Animals', 
                          'Plants', 
                          'Weapons', 
                          'Sports'
                          'Food',
                          'Anatomy',
                          'Topology',
                          'Outer Space',
                          'Others') 

GeometryClassChoose.grid(column = 1, row = 2)
GeometryClassChoose.current()


###Enter Tags
Tags_Gui = tk.StringVar() #Variable declaration to get Tags input
Tag_Lable = tk.Label(window, text = "Enter Tags").grid(row = 3, padx = 10, pady = 25)
Tags_Entry = tk.Entry(window, textvariable = Tags_Gui).grid(row = 3, column = 1)


###Enter File Format .FCStd or .Obj
ttk.Label(window, text = "Select File Format").grid(row = 4, column = 0, padx = 10, pady = 25)
Format_Gui = tk.StringVar()
FormatChosen = ttk.Combobox(window, width = 27, textvariable = Format_Gui)
FormatChosen['values'] = ('FreeCAD Standard(.FCStd)',  
                          'Object File(.obj)') 

FormatChosen.grid(column = 1, row = 4)
FormatChosen.current()


###Progress Bar
Progress_Level = tk.Label(window, text = "Upload Progress").grid(row = 5, pady = 25)
Progress_Bar = Progressbar(window, length = 100, mode = "indeterminate")
Progress_Bar["value"] = 0
Progress_Bar.grid(column = 1, row = 5)


###Submit Button
Submit_Button = tk.Button(window, text = "Submit", command = submit).grid(row = 6, column = 1)


window.mainloop()


