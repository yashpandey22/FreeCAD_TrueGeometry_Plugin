###Code to import downloaded file from www.truegeometry.com to FreeCAD
import requests as rs
import tempfile
import os
import Mesh
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar


###Design of GUI
window = Tk()
window.title("TrueGeometry Download")
window.geometry("600x450")


def submit():    

    ###File Download Code
    API_Key = API_Key_Gui.get()
    API_FileName = API_FileName_Gui.get()
    r = rs.get("http://www.truegeometry.com/api/get3DAsm?modelName=" + API_FileName + "&APIKey=" + API_Key)

    response_get = r.text
    response_get = response_get[response_get.find(":") + 2 : response_get.find("}")]
    count = response_get.count(':')
    path = tempfile.gettempdir()
    


    ###Creating a New File in FreeCAD
    App.newDocument("Unnamed")
    App.setActiveDocument("Unnamed")
    App.ActiveDocument=App.getDocument("Unnamed")
    Gui.ActiveDocument=Gui.getDocument("Unnamed")
    Gui.activeDocument().activeView().viewDefaultOrientation()

    ###Looping through all the parts in a 3D model and importing to FreeCAD
    for i in range(count):
        progress = int(i) * 7
        Progress_Bar['value'] = progress
        window.update_idletasks() 
        part_name = response_get[response_get.find("\"") + 1 : response_get.find(":") - 1]
        a = response_get = response_get[response_get.find(":") + 2 : ]
        a = response_get[: response_get.find("\"")]
        response_get = response_get[response_get.find(",") : ]    
        part = rs.get("http://www.truegeometry.com" + a + "&APIKey=" + API_Key)
        filename_downloaded = path + "/" + part_name + ".obj"
        open(filename_downloaded, 'wb').write(part.content)
        Mesh.insert(filename_downloaded, "Unnamed")
        Gui.SendMsgToActiveView("ViewFit")

    messagebox.showinfo("TrueGeometry Download", "Download Completed Successfully!")
    window.destroy()


###Information for user 
Text_Label = tk.Label(window, text = "Get your Permanent API Key from Profile Page by \n Updagting your Profile @ www.truegeometry.com").grid(row = 0, column = 1, padx = 10, pady = 25)


### API Key Field
API_Key_Gui = tk.StringVar() #Variable declaration to get API Key input
API_Key_Label = tk.Label(window, text = "Enter API Key").grid(row = 1, padx = 10, pady = 25) 
API_Key_Entry = tk.Entry(window, textvariable = API_Key_Gui).grid(row = 1, column = 1)


###Enter Tags
API_FileName_Gui = tk.StringVar() #Variable declaration to get File Name
API_FileName_Lable = tk.Label(window, text = "Enter File Name").grid(row = 2, padx = 10, pady = 25)
API_FileName_Entry = tk.Entry(window, textvariable = API_FileName_Gui).grid(row = 2, column = 1)


###Progress Bar
Progress_Level = tk.Label(window, text = "Download Progress").grid(row = 3, pady = 25)
Progress_Bar = Progressbar(window, length = 100, mode = "determinate")
Progress_Bar["value"] = 0
Progress_Bar.grid(column = 1, row = 3)

###Submit Button
Submit_Button = tk.Button(window, text = "Submit", command = submit).grid(row = 4, column = 1, pady = 25)

window.mainloop()