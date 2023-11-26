import tkinter as tk
import tkinter.font as tkFont

try:
    from pynput import mouse
except:
    import os
    os.system("pip install pynput")
    from pynput import mouse

import bot

pi = tk.PhotoImage

root = tk.Tk()
root.geometry("420x720")
root.configure(bg='#F2F2F2')
root.resizable(False, False)

###############################################################
# -----Display parameters-----

size_x, size_y = (420, 720)

# gothic_italic_font = tkFont.Font(family="맑은 고딕", size=18, slant="italic")
gothic_bold_font = tkFont.Font(family="맑은 고딕", size=18, weight="bold")
gothic_regular_font = tkFont.Font(family="맑은 고딕", size=11)

white = '#FFFFFF'
black = '#373737'
grey = '#737376'
bot_color ='#FFFFFF'

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
        self.text_slices = self.get_text_slices()
        print(self.text_slices)
        self.bubble_width, self.bubble_height = self.calc_bubble_dimensions()
        self.x, self.y = self.calc_bubble_position()
        # # print(self.bubble_width, self.bubble_height, self.x, self.y)


    # Method
    def get_text_slices(self):
        # Length of "AAAAAAAAAAAAAAAAAAAA"
        linebreak = gothic_regular_font.measure("A" * 30)
        text_length = len(self.text)
        text_slices = []

        # for i in range(0, text_length - 1, linebreak):
        #     text_slices.append(self.text[i:i + linebreak if i + linebreak <= text_length - 1 else text_length - 1])

        current_slice_index = 0
        last_space_index = 0
        for i in range(0, text_length):
            if self.text[i] == " ":
                last_space_index = i

            if gothic_regular_font.measure(self.text[current_slice_index:i]) > linebreak:
                if current_slice_index < last_space_index:
                    text_slices.append(self.text[current_slice_index:last_space_index])
                    current_slice_index = last_space_index + 1
                else:
                    text_slices.append(self.text[current_slice_index:i])
                    current_slice_index = i

            if i == text_length - 1:
                text_slices.append(self.text[current_slice_index:i+1])
        return text_slices

    def calc_bubble_dimensions(self):

        text_width = max([gothic_regular_font.measure(this_slice) for this_slice in self.text_slices])
        text_height = gothic_regular_font.metrics("linespace") \
                      * (len(self.text_slices) + sum([s.count('\n') for s in self.text_slices]))
        vertical_pad, horizontal_pad = 10, 18
        bubble_width = text_width + horizontal_pad*2
        bubble_height = text_height + vertical_pad*2

        return (bubble_width, bubble_height)

    def calc_bubble_position(self):
        base_x = 62 if self.is_bot else size_x - self.bubble_width - 20
        base_y = size_y - (entry_height + 20 + self.bubble_height)
        return (base_x, base_y)


    def render_bubble(self):

        fg = black if self.is_bot else white
        bg = bot_color if self.is_bot else black

        if not self.is_bot:
            bubble_frame = tk.Frame(root,
                                    width=self.bubble_width,
                                    height=self.bubble_height,
                                    bg=bg)
            bubble_frame.place(x=self.x, y=self.y)

            bubble_text = "\n".join(self.text_slices)
            # # print(bubble_text)

            bubble_label = tk.Label(bubble_frame,
                                    text=bubble_text,
                                    fg=fg,
                                    bg=bg,
                                    font=gothic_regular_font,
                                    anchor="w",
                                    justify="left")
            bubble_label.place(x=14, y=5)  # manual magic number

            return bubble_frame
        else:
            # Is bot
            icon_x_offset = -42

            bubble_frame = tk.Frame(root,
                                    width=self.bubble_width - icon_x_offset,
                                    height=self.bubble_height,
                                    bg=bg)
            bubble_frame.place(x=self.x + icon_x_offset, y=self.y)

            bubble_text = "\n".join(self.text_slices)
            # # print(bubble_text)

            bubble_label = tk.Label(bubble_frame,
                                    text=bubble_text,
                                    fg=fg,
                                    bg=bg,
                                    font=gothic_regular_font,
                                    anchor="w",
                                    justify="left")
            bubble_label.place(x=14-icon_x_offset, y=5)  # manual magic number

            avatar_profile_image = pi(file='images/avatar icon1.png')
            avatar_profile = tk.Label(bubble_frame, image=avatar_profile_image, borderwidth=0, highlightthickness=0, bg=black)
            avatar_profile.place(x=0, y=0)
            avatar_profile.image = avatar_profile_image

            return bubble_frame

class chat:
    def __init__(self):
        self.bubbles = []
        self.bubble_frames = []
        self.scroll_y = 0

    def add_bubble(self, new_bubble):
        self.bubbles.insert(0, new_bubble)

        prev_y = 0
        y_gap = 16
        for i, bubble in enumerate(self.bubbles):
            bubble.y = size_y - (entry_height + 20 + bubble.bubble_height) if i == 0 \
                else prev_y - bubble.bubble_height - (y_gap if i != 0 else 0)

            prev_y = bubble.y

    def render_chat(self):
        for frame in self.bubble_frames:
            frame.destroy()
        for bubble in self.bubbles:
            this_frame = bubble.render_bubble()
            self.bubble_frames.append(this_frame)

    def scroll(self, dy):
        speed = 10

        # Don't scroll if there are no bubbles
        if len(self.bubbles) == 0:
            return

        # Get list of y position values for each bubble to prevent scrolling past upper/lower border
        y_list = [bubble.y for bubble in self.bubbles]
        # min_index = y_list.index(min(y_list))
        max_index = y_list.index(max(y_list))

        # Check if text bubbles span out of screen
        scrollable = True if max(y_list) > size_y - entry_height - 20 - self.bubbles[max_index].bubble_height or min(y_list) <= 100 else False

        if not scrollable:
            return

        # Condition 1 : Upper border
        if (min(y_list) > 100) and (dy > 0):
            return

        # Condition 2 : Lower border
        if max(y_list) < size_y - entry_height - 20 - self.bubbles[max_index].bubble_height and dy < 0:
            return

        for bubble in self.bubbles:
            bubble.y += dy * speed

        ##########################################################
        # Scroll past border correction
        #
        y_list = [bubble.y for bubble in self.bubbles]
        # min_index = y_list.index(min(y_list))
        max_index = y_list.index(max(y_list))

        # Condition 1 : Upper border
        y_offset1 = 100 - min(y_list)
        y_offset2 = max(y_list) - (size_y - entry_height - 20 - self.bubbles[max_index].bubble_height)
        if y_offset1 < 0:
            for bubble in self.bubbles:
                bubble.y += y_offset1

        # Condition 2 : Lower border

        if y_offset2 < 0:
            for bubble in self.bubbles:
                bubble.y -= y_offset2
        ##########################################################

main_chat = chat()


# hint the text
def on_entry_click(event):
    """Function to handle the click event on the entry widget."""
    if entry.get() == '메세지를 입력하세요':
        entry.delete(0, tk.END)
        entry.config(fg=black)  # Change text color to black when user starts typing
        entry.insert(0, '')

def on_focusout(event):
    """Function to handle focus out event on the entry widget."""
    if entry.get() == '':
        entry.insert(0, '메세지를 입력하세요')
        entry.config(fg=grey)  # Change text color to grey as a hint

def on_return(event):
    send_text()

gpt_message = ""
def send_text():
    global gpt_message
    text = entry.get()

    if text == '':
        return

    entry.delete(0, tk.END)
    new_text_bubble = text_bubble(text, False)
    main_chat.add_bubble(new_text_bubble)
    main_chat.render_chat()

    response = bot.send_text(text)
    if response == "Inquire GPT-4":
        add_loading_indicator()
        gpt_message = text
        root.after(50, send_gpt_message)
    else:
        main_chat.add_bubble(text_bubble(response, True))
    main_chat.render_chat()

def add_loading_indicator():
    main_chat.add_bubble(text_bubble("Requesting response...", True))
    main_chat.render_chat()

def send_gpt_message():
    main_chat.add_bubble(text_bubble(bot.send_text_gpt(gpt_message), True))

top_label = tk.Label(root, text="    💬  Dr.G 도우미 상담",
                     font=gothic_bold_font,
                     bg=black,
                     fg=white,
                     anchor="w",
                     justify='left'
)

top_label.place(x=0, y=0, width=size_x, height=size_y/10)

# Create an entry widget
entry = tk.Entry(root, fg=grey, bg=white, borderwidth=0, highlightthickness=0, font=gothic_regular_font)  # Set default text color to grey
entry.insert(0, '메세지를 입력하세요')  # Default or hint text
entry.bind('<FocusIn>', on_entry_click)  # Bind click event
entry.bind('<FocusOut>', on_focusout)  # Bind focus out event
entry.bind('<Return>', on_return)
entry.place(x=entry_pad, y=size_y*0.9, width=size_x - entry_pad - size_x * 0.1, height=entry_height)

entry_padding_label = tk.Label(bg=white)
entry_padding_label.place(x=0, y=size_y*0.9, width=entry_pad, height=entry_height)

#  Create send button
send_button_image = pi(file='images/send icon white.png')

send_button = tk.Button(root, image=send_button_image, bg=white, relief='flat', borderwidth=0, highlightthickness=0, command=send_text)
send_button.place(x=size_x * 0.9, y=size_y * 0.9, width=size_x * 0.1, height=entry_height)

###############################################################
# ----- Mouse input handling----
# scroll_y = 0
def on_scroll(x, y, dx, dy):
    # scroll_y += dy
    # print(dy)
    main_chat.scroll(dy)

# Create and start the listener
listener = mouse.Listener(on_scroll=on_scroll)
listener.start()

###############################################################
# ----- Custom Update Function -----

# avatar_profile_image = pi(file='images/avatar icon1.png')
# avatar_profile = tk.Label(root, image=avatar_profile_image, borderwidth=0, highlightthickness=0, bg=black)
# avatar_profile.place(x=0, y=0)


def update():
    main_chat.render_chat()
    # print("update call")
    top_label.lift()
    entry.lift()
    send_button.lift()
    entry_padding_label.lift()

    root.after(50, update)


update()
root.mainloop()


