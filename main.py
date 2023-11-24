import tkinter as tk

pi = tk.PhotoImage

root = tk.Tk()
root.geometry("300x200")

# Frame for pack
pack_frame = tk.Frame(root)
pack_frame.pack(side="top", fill="both", expand=True)

button1 = tk.Button(pack_frame, text="Packed Button", width=20)
button1.pack(pady=10)

# Frame for grid
grid_frame = tk.Frame(root)
grid_frame.pack(side="top", fill="both", expand=True)

entry = tk.Entry(grid_frame, width=20)
entry.grid(row=0, column=0, padx=10, pady=10)

button2 = tk.Button(grid_frame, text="Grid Button")
button2.grid(row=0, column=1, padx=10)

root.mainloop()
