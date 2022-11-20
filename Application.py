import math
from oddart import choice, randint, random, sample, seed
from tkinter import *
from tkinter import ttk
import sys
import subprocess

from PIL import Image, ImageTk

from oddart import Picture

class ArtGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Odd Art")
        
        # https://github.com/rdbende/Sun-Valley-ttk-theme
        self.root.call("source", "sun-valley.tcl")
        self.root.call("set_theme", "dark")

        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        # All of these previous lines of code are essentially setting up the frame and window, and how they dynamically resize
        self.root.rowconfigure(0, weight=1)

        self.createLabels()
        self.createInputWidgets()

    # Creates GUI Labels
    def createLabels(self):
        self.artLabel = ttk.Label(self.frame, text="Odd Art", font="helvetica 14 bold")
        self.artLabel.grid(column=0, row=0, sticky=N)
        
        self.squareSidesLabel = ttk.Label(self.frame, text="Number of Squares on Each Side", font="helvetica 10 bold")
        self.squareSidesLabel.grid(column=0, row=1, sticky= N)
        
        self.spacingTitle = ttk.Label(self.frame, text="Enter Factor of Spacing", font="helvetica 10 bold")
        self.spacingTitle.grid(column=0, row=4, sticky= N)

    # Creates Input Widgets and Canvas
    def createInputWidgets(self):
        
        # Degree of art squares
        # 1 means 1x1 grid, 3 means 3x3 grid, etc. 
        self.squareDegree = StringVar()

        self.squareDegreeScale = ttk.Scale(self.frame, orient=HORIZONTAL, length=200, from_=1, to=100, value=10, command=lambda s: self.squareDegree.set(math.floor(float(s))))
        self.squareDegreeScale.set(10)
        self.squareDegreeScale.grid(column=0, row=2, padx=20, sticky=N)

        self.squareSidesLabel = ttk.Label(self.frame, textvariable=self.squareDegree)
        self.squareSidesLabel.grid(column=0, row=3, sticky=N)

        self.squareSpacing = StringVar()
        
        self.spacingScale = ttk.Scale(self.frame, orient= HORIZONTAL, length = 200, from_=0.1, to=15, value=10, command=lambda t: self.squareSpacing.set(round(float(t), 2)))
        self.spacingScale.set(10)
        self.spacingScale.grid(column = 0, row=5, padx=20, sticky=N)

        # Creating a label to write out the value of the scale variable (self.degree)
        self.spacingValueText = ttk.Label(self.frame, textvariable=self.squareSpacing)
        self.spacingValueText.grid(column = 0, row= 6, sticky=N)

        self.progressText = StringVar()
        self.progressText.set("Create Artwork")
        
        self.filePath = StringVar()
        self.filePath.set("default")

        self.generateArtButton = ttk.Button(self.frame, textvariable= self.progressText, command=lambda: self.create_art(), style="Accent.TButton")
        self.generateArtButton.grid(row=10, column=0, ipady=10, ipadx=20, sticky=S)
        
        self.openArtButton = ttk.Button(self.frame, text="Open Image", command=lambda: self.open_image((self.filePath.get()).rstrip() + ".png"))
        self.openArtButton.grid(row=11, column=0, ipady=10, ipadx=20, sticky=S)

        # Creating an entry
        self.filePathText = ttk.Label(self.frame, text="Enter a file name to download your file as a png.", font="helvetica 10 bold")
        self.filePathText.grid(column=0, row = 7, sticky= N)

        

        self.filePathEntry = ttk.Entry(self.frame, textvariable=self.filePath, width = 25)
        self.filePathEntry.grid(column = 0, row = 8, sticky= N)

        # Creating checkButton for light theme
        self.theme = StringVar(value="dark")
        self.lightThemeCheck = ttk.Checkbutton(self.frame, text="Light Theme", command=self.changeTheme, variable=self.theme, onvalue="light", offvalue= "dark")
        self.lightThemeCheck.grid(column=0, row=15, sticky=(W, S))

        # Canvas
        self.cv = Canvas(self.frame, width=720, height=720, highlightbackground="gray21")
        self.cv.grid(row=0, column=1, rowspan=16, padx= (25, 0))

    def changeTheme(self):
        if (self.theme.get() == "light"):
            self.root.call("set_theme", "light")
        else:
            self.root.call("set_theme", "dark")

    def create_art(self):
        self.generateArtButton.state(['disabled'])
        self.progressText.set("Creating Artwork...")
        self.frame.update()

        Picture(int(self.squareDegree.get()), float(self.squareSpacing.get()), (self.filePath.get()).rstrip())
        
        photoimage = ImageTk.PhotoImage(file=(self.filePath.get()).rstrip() + ".png")
        self.root.photoimage = photoimage
        self.cv.create_image((2, 2), image=photoimage, anchor=NW)
        self.generateArtButton.state(['!disabled'])
        self.progressText.set("Create Artwork")
        self.frame.update()
    
    # https://stackoverflow.com/questions/35304492/python-open-multiple-images-in-default-image-viewer
    def open_image(self, path):
        imageViewerFromCommandLine = {'linux':'xdg-open',
                                    'win32':'explorer',
                                    'darwin':'open'}[sys.platform]
        subprocess.Popen([imageViewerFromCommandLine, path])
        

if __name__ == '__main__':
    root = Tk()
    ArtGenerator(root)

    root.mainloop()
