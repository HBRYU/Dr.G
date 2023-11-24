import tkinter as tk
import tkinter.font as tkFont

# pi = tk.PhotoImage
#
# root = tk.Tk()
# root.geometry("300x200")
#
# # Frame for pack
# pack_frame = tk.Frame(root)
# pack_frame.pack(side="top", fill="both", expand=True)
#
# button1 = tk.Button(pack_frame, text="Packed Button", width=20)
# button1.pack(pady=10)
#
# # Frame for grid
# grid_frame = tk.Frame(root)
# grid_frame.pack(side="top", fill="both", expand=True)
#
# entry = tk.Entry(grid_frame, width=20)
# entry.grid(row=0, column=0, padx=10, pady=10)
#
# button2 = tk.Button(grid_frame, text="Grid Button")
# button2.grid(row=0, column=1, padx=10)
#
# root.mainloop()
#
# # this is a comment

pi = tk.PhotoImage

root = tk.Tk()
root.geometry("420x720")
root.resizable(False, False)

gothic_italic_font = tkFont.Font(family="맑은 고딕", size=20, slant="italic")

size_x, size_y = (420, 720)


class text_bubble:
    def __init__(self, text):
        self.text = text
        self.position = self.get_new_position()

    def get_new_position(self):
        return (0, 0)


top_label = tk.Label(root, text="Dr.G 도우미 상담",
                     font=gothic_italic_font,
                     bg="grey",
                     fg="white"
)

top_label.place(x=0, y=0, width=size_x, height=size_y/10)

# number of spaces for padding entry text
space_pad = 2

#hint the text
def on_entry_click(event):
    """Function to handle the click event on the entry widget."""
    if entry.get() == '  메세지를 입력하세요':
        entry.delete(0, tk.END)
        entry.config(fg='black')  # Change text color to black when user starts typing

def on_focusout(event):
    """Function to handle focus out event on the entry widget."""
    if entry.get() == '  ':
        entry.insert(0, '  메세지를 입력하세요')
        entry.config(fg='grey')  # Change text color to grey as a hint


# Create an entry widget
entry = tk.Entry(root, fg='grey',bg='white')  # Set default text color to grey
entry.insert(0, '  메세지를 입력하세요')  # Default or hint text
entry.bind('<FocusIn>', on_entry_click)  # Bind click event
entry.bind('<FocusOut>', on_focusout)  # Bind focus out event
entry.place(x=0, y=size_y*0.9, width=size_x, height=size_y*0.1)


root.mainloop()


