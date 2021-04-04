from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from sudoku_solver_project.testing_solver import *

color = '#00cfd5'
# #00cfd5
# #de8b43


top = Tk()
top.title("Solve any sudoku problem")
top.geometry('550x480')
# 600X650
top.configure(background=color)


def open():
    filename = filedialog.askopenfilename()
    # this function find the solution
    callMe(filename)


heading = Label(top, text="Solve any Sudoku Board", pady=20, font=('arial',20,'bold'))
heading.configure(background=color, foreground='#364156')
heading.pack()

img = ImageTk.PhotoImage(Image.open("Resources/nicon_small.jpg"))
label = Label(top, image = img)
label.pack()

upload = Button(top,text="Select a Sudoku Board", command=open,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)


top.mainloop()
