import openai
import os
import tkinter as tk
from tkinter.font import Font
from tkinter import scrolledtext, Button, Label, Canvas

def drawGradient(canvas):
    # draws a vertical gradient filled rectangle on canvas
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.delete("gradient")

    # gradient colors for background
    (r1, g1, b1) = canvas.winfo_rgb(canvas.gradient_from)
    (r2, g2, b2) = canvas.winfo_rgb(canvas.gradient_to)  
    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")

def resizeWindow(event, canvas):
    # redraw gradient when the window is resized
    drawGradient(canvas)

def inputWindowGUI():
    root = tk.Tk()
    root.title("QuickPlot - Real Movie Summary")
    root.geometry('500x700')

    canvas = Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.gradient_from = '#000000'
    canvas.gradient_to = '#434343' 

    # gradient when window is resized
    root.bind('<Configure>', lambda event, canvas=canvas: resizeWindow(event, canvas))

    customFont = Font(family="Helvetica", size=14)
    buttonFont = Font(family="Broadway", size=12, weight="bold")

    Label(canvas, text="Enter the movie title:", bg='black', fg='white', font=customFont).pack(pady=5)

    # text widget for input
    inputText = scrolledtext.ScrolledText(canvas, wrap=tk.WORD, height=1, width=38, borderwidth=2, relief="solid", highlightbackground="blue")
    inputText.pack(padx=10, pady=5)

    # movie info button
    lookup_button = Button(canvas, text="What's this movie about?", command=lambda: lookupMovie(inputText, outputText, outputLabel), bg='#e4b759', font=buttonFont)
    lookup_button.pack(pady=10)

    # Label for output text area
    outputLabel = Label(canvas, text="Movie Information:", bg='dark grey', fg='white', font=customFont)
    outputLabel.pack(pady=(5, 0))
    outputLabel.pack_forget()  

    # Text widget for output
    outputText = scrolledtext.ScrolledText(canvas, wrap=tk.WORD, height=11, width=60, bg='light gray', borderwidth=2, relief="solid", highlightbackground="blue")
    outputText.pack(padx=10, pady=5)
    outputText.config(state=tk.DISABLED)
    outputText.pack_forget()

    def lookupMovie(inputText, outputText, outputLabel):
        """Handles the movie lookup."""
        movieTitle = inputText.get("1.0", "end-1c").strip()
        if movieTitle:
            try:
                prompt = f"Provide a summary, about three sentences, on the movie titled '{movieTitle}' and provide one piece of trivia about the movie. Combine this into one answer. If the movie actually exists."
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=110
                )
                movieInfo = response['choices'][0]['message']['content'].strip()

                # display movie information in outputText widget
                outputText.config(state=tk.NORMAL)
                outputText.delete("1.0", tk.END)
                outputText.insert(tk.END, movieInfo)
                outputText.config(state=tk.DISABLED)
                
                # show the output widgets if hidden
                outputLabel.pack(pady=(5, 0))
                outputText.pack(padx=10, pady=5)

            except Exception as e:
                outputText.config(state=tk.NORMAL)
                outputText.delete("1.0", tk.END)
                outputText.insert(tk.END, f"An error occurred: {e}")
                outputText.config(state=tk.DISABLED)
                outputLabel.pack(pady=(5, 0))
                outputText.pack(padx=10, pady=5)

    root.mainloop()

openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

inputWindowGUI()
