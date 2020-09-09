import tkinter as tk

main_window = tk.Tk()
label = tk.Label(
    text='test',
    fg='white',
    bg='gray20',
    width=100,
    height=50
)
label.pack()
button = tk.Button(
    text='Button',
    width=20,
    height=5,
    bg='gray25',
    fg='white'
)
button.pack()

main_window.mainloop()
