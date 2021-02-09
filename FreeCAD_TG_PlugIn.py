"""This Mcro is to provide upload facility from FreeCAD to www.truegeometry.com using API Key.
Please get your API Key by updating your profile at www.truegeometry.com"""

import requests as rs #Install this library before running this code
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

###Designe of GUI
window = Tk()
window.title("TrueGeometry")
window.geometry("600x450")

def submit():

    ###Exporting to Object File
    file_name = App.ActiveDocument.Name
    path_file = os.getcwd() + "/" + file_name + ".obj" #Path and Name of File to be exported
    __objs__ = [] #Empty List to appending document details and all object names


    for obj in FreeCAD.ActiveDocument.Objects: #Loop for appending all the object names as string to a list
        if obj.ViewObject.isVisible():
            __objs__.append(FreeCAD.getDocument(file_name).getObject(obj.Name)) #List with appended document details and all object names

    import Mesh
    Mesh.export(__objs__, path_file)#File Exported to object file (.obj)
    del __objs__

    ### Commands for Uploading to TrueGeometry.com
    API_Key = API_Key_Gui.get() #Permanent API Key
    url = ("http://www.truegeometry.com") #Website's URL
    r = rs.get("http://www.truegeometry.com/getUpldToken?APIKey=" + API_Key) #Temporary API Key Recieved
    Temp_APIKEY = r.json()['apiKeyToken'] #Temporary API Key
    to_Upload = {'media': open(path_file, 'rb')} #path of recently exported file
    GeometryClass = GeometryClass_Gui.get() #Getting Geometry Class
    Tags = Tags_Gui.get() #Getting Tags
    Upload_file = rs.post(url + "/upldAPI?APIKey=" + API_Key + "&APIKeyToken=" + Temp_APIKEY + "&tags=" + Tags + "&GeometryClass=" + GeometryClass, files = to_Upload)
    #File Upload command through HTTP Post using Requests Library.

    if Upload_file.ok: #Message to User Upload Successfull or Unsuccessful
        messagebox.showinfo("Info", "Upload Completed Successfully!")
        window.destroy()
    else:
        messagebox.showinfo("error", "Something Went Wrong, Please Try Again!")
        window.destroy()
    os.remove(path_file) #Removing the Created Object File from users Computer


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
GeometryClassChoose['values'] = (' Buildings',  
                          ' Mega Structures', 
                          ' Vehicles', 
                          ' Ships', 
                          ' Characters', 
                          ' Aircraft', 
                          ' Furniture', 
                          ' Electronics', 
                          ' Animals', 
                          ' Plants', 
                          ' Weapons', 
                          ' Sports'
                          ' Food',
                          ' Anatomy',
                          ' Topology',
                          ' Outer Space',
                          ' Others') 

GeometryClassChoose.grid(column = 1, row = 2)
GeometryClassChoose.current()


###Enter Tags
Tags_Gui = tk.StringVar() #Variable declaration to get Tags input
Tag_Lable = tk.Label(window, text = "Enter Tags").grid(row = 3, padx = 10, pady = 25)
Tags_Entry = tk.Entry(window, textvariable = Tags_Gui).grid(row = 3, column = 1)


###Submit Button
Submit_Button = tk.Button(window, text = "Submit", command = submit).grid(row = 5, column = 1)


window.mainloop()


