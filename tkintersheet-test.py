from tkinter import *

root = Tk()

height = 5
width = 5
for i in range(height):
    for j in range(width):
        b = Entry(root, text="Test")
        b.grid(row=i, column=j)

def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        if info['row'] == str(row) and info['column'] == str(column):
            return children
    return None

button = Button()

print(find_in_grid(root, i+1, j))
mainloop()