import tkinter as tk
import tkinter.font as tkFont

pi = tk.PhotoImage

root = tk.Tk()
root.geometry("420x720")
root.resizable(False, False)

###############################################################
# -----Display parameters-----

size_x, size_y = (420, 720)

gothic_italic_font = tkFont.Font(family="맑은 고딕", size=18, slant="italic")
gothic_regular_font = tkFont.Font(family="맑은 고딕", size=15)

# number of pixels for padding entry text
entry_pad = 10

entry_height = size_y*0.1

###############################################################



class text_bubble:
    # Constructor
    def __init__(self, text, is_bot):
        # Attributes
        self.text = text
        self.is_bot = is_bot
        self.bubble_width, self.bubble_height = self.calc_bubble_dimensions()
        self.x, self.y = self.calc_bubble_position()
        print(self.bubble_width, self.bubble_height)

    # Method
    def calc_bubble_dimensions(self):
        text_width = gothic_regular_font.measure(self.text)
        text_height = gothic_regular_font.metrics("linespace")
        vertical_pad, horizontal_pad = 16, 18
        bubble_width = text_width + horizontal_pad*2
        bubble_height = text_height + vertical_pad*2

        return (bubble_width, bubble_height)

    def calc_bubble_position(self):
        base_x = 62 if self.is_bot else size_x - self.bubble_width - 20
        base_y = entry_height + 31 + self.bubble_height
        return (base_x, base_y)

    def render_bubble(self):
        bubble_label = tk.Label(text=self.text, width=self.bubble_width, height=self.bubble_height,
                                fg="black" if self.is_bot else "white",
                                bg="white" if self.is_bot else "black",
                                font=gothic_regular_font)
        bubble_label.place(x=self.x, y=self.y)

#hint the text
def on_entry_click(event):
    """Function to handle the click event on the entry widget."""
    if entry.get() == '메세지를 입력하세요':
        entry.delete(0, tk.END)
        entry.config(fg='black')  # Change text color to black when user starts typing
        entry.insert(0, '')

def on_focusout(event):
    """Function to handle focus out event on the entry widget."""
    if entry.get() == '':
        entry.insert(0, '메세지를 입력하세요')
        entry.config(fg='grey')  # Change text color to grey as a hint

def send_text():
    text = entry.get()
    new_text_bubble = text_bubble(text, False)

    new_text_bubble.render_bubble()



top_label = tk.Label(root, text="Dr.G 도우미 상담",
                     font=gothic_italic_font,
                     bg="grey",
                     fg="white"
)

top_label.place(x=0, y=0, width=size_x, height=size_y/10)

# Create an entry widget
entry = tk.Entry(root, fg='grey', bg='white', borderwidth=0, highlightthickness=0)  # Set default text color to grey
entry.insert(0, '메세지를 입력하세요')  # Default or hint text
entry.bind('<FocusIn>', on_entry_click)  # Bind click event
entry.bind('<FocusOut>', on_focusout)  # Bind focus out event
entry.place(x=entry_pad, y=size_y*0.9, width=size_x - entry_pad, height=entry_height)

entry_padding_label = tk.Label(bg='white')
entry_padding_label.place(x=0, y=size_y*0.9, width=entry_pad, height=entry_height)

#  Create send button
send_button_image = pi(file='images/send icon white.png')

send_button = tk.Button(root, image=send_button_image, bg='white', relief='flat', borderwidth=0, highlightthickness=0, command=send_text)
send_button.place(x=size_x * 0.9, y=size_y * 0.9, width=size_x * 0.1, height=entry_height)


root.mainloop()


