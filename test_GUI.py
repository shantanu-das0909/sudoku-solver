from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from sudoku_solver_project.testing_solver import *

color = '#12ffb9'
# #00cfd5
# #de8b43


top = Tk()
top.title("Solve any sudoku problem")
top.geometry('550x480')
# 600X650
top.configure(background=color)

filename = ""


def open():
    global filename
    filename = filedialog.askopenfilename()
    print("Image selected ......")
    print("Press 'Solve' button to solve the sudoku board ..... ")
    print()
    # this function find the solution
    # callMe(filename)


def solve():
    callMe(filename)


heading = Label(top, text="Solve any Sudoku Board", pady=20, font=('arial',20,'bold'))
heading.configure(background=color, foreground='#364156')
heading.pack()

img = ImageTk.PhotoImage(Image.open("Resources/nicon_small.jpg"))
label = Label(top, image = img)
label.pack()

upload = Button(top,text="Select a Sudoku Board", command=open,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM, pady=25)

upload1 = Button(top,text="Solve", command=solve,padx=10,pady=5)
upload1.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload1.pack(side=BOTTOM)

top.mainloop()
