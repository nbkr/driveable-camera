from Tkinter import *

root = Tk()



b1 = Button(root, text = 'Quit', command=root.quit)
b1.grid(row=0, column=0, sticky=W)


frame = Canvas(root, background='red', width=640, height=480)
frame.grid(row=1, column=0, columnspan=3)

b2 = Button(root, text = 'Forward')
b2.grid(row=2, column=1, sticky=W+E)

b3 = Button(root, text = 'Left')
b3.grid(row=3, column=0, sticky=W+E)

b4 = Button(root, text = 'Right')
b4.grid(row=3, column=2, sticky=W+E)

b5 = Button(root, text = 'Reverse')
b5.grid(row=4, column=1, sticky=W+E)


root.mainloop()
