import Tkinter 
from Tkinter import *
import tkFileDialog
import sys,os
import gprConvert
class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.text_area.write(str,False)
def getRootDrive():
    path = sys.executable
    while os.path.split(path)[1]:
        path = os.path.split(path)[0]
    #return path
    return "C:/"
def selectFile(e,root):
    fileText=tkFileDialog.askdirectory(parent=root, initialdir=getRootDrive())
    e.delete(0,END)
    e.insert(0,fileText)
def convert(v,w,e,o,root):
    setDialog(v,"Converting")
    w0 = w.get()
    d0 = e.get()
    gprConvert.do(w0,d0)
    v.set("Done")
def setDialog(v,text):
    v.set(text)
root =Tk()
root.title('GPR Converter')
v=StringVar()
v.set("Set wavelength, select a directory, then press convert to create a CSV from the GPRs")
dialog=Label (textvariable=v)##
dialog.pack(side=TOP,padx=10,pady=10)
w=Entry(root, width=20)
w.pack(side=LEFT,padx=10,pady=10)
w.delete(0,END)
w.insert(0,"Wavelength")
e=Entry(root, width=50)##
e.pack(side=LEFT,padx=10,pady=10)
e.delete(0,END)
e.insert(0,"Select a directory")
o=1
Button(root, text='Browse',command=lambda: selectFile(e,root)).pack(side= LEFT)
Button(root, text='Convert',command=lambda: convert(v,w,e,o,root)).pack(side= LEFT)
root.mainloop()


##from Tkinter import *
##import tkFileDialog
##class Example(Frame):
##    def __init__(self, parent):
##        Frame.__init__(self, parent, background="white")   
##        self.parent = parent
##        self.initUI()
##    
##    def initUI(self):
##        self.parent.title("GPRConvert")
##        self.pack(fill=BOTH, expand=1)
##        self.fileEntry.place(x=0,y=10)
##        quitButton = Button(self, text="Select File",
##                            command=self.selectFile)
##        quitButton.place(x=50,y=100)
##
##    def selectFile(x):
##        print x
##        fileEntry.set("ABC")
##        pass
##def main():
##  
##    root = Tk()
##    root.geometry("250x150+300+300")
##    app = Example(root)
##    fileEntry = Entry(self)
##    root.mainloop()  
##
##
##if __name__ == '__main__':
##    main()  
