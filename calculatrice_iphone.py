import tkinter as tk
from tkinter import font

class CalculatriceiPhone:
    def __init__(self, master):
        self.master = master
        master.title("Calculatrice iPhone")
        master.configure(bg='black')
        
        # Style iPhone
        self.buttons_font = font.Font(family="Helvetica", size=20)
        self.display_font = font.Font(family="Helvetica", size=32)
        
        # Affichage
        self.display_var = tk.StringVar()
        self.display = tk.Label(master, textvariable=self.display_var, 
                              font=self.display_font, bg='black', fg='white',
                              anchor='e', padx=20)
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew')
        
        # Boutons
        buttons = [
            ('C', 1, 0, 'light gray'), ('±', 1, 1, 'light gray'), ('%', 1, 2, 'light gray'), ('÷', 1, 3, 'orange'),
            ('7', 2, 0, 'dark gray'), ('8', 2, 1, 'dark gray'), ('9', 2, 2, 'dark gray'), ('×', 2, 3, 'orange'),
            ('4', 3, 0, 'dark gray'), ('5', 3, 1, 'dark gray'), ('6', 3, 2, 'dark gray'), ('-', 3, 3, 'orange'),
            ('1', 4, 0, 'dark gray'), ('2', 4, 1, 'dark gray'), ('3', 4, 2, 'dark gray'), ('+', 4, 3, 'orange'),
            ('0', 5, 0, 'dark gray'), ('.', 5, 2, 'dark gray'), ('=', 5, 3, 'orange')
        ]
        
        for (text, row, col, color) in buttons:
            btn = tk.Button(master, text=text, font=self.buttons_font,
                          bg=color, fg='white', borderwidth=0,
                          command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
            if text == '0':
                btn.grid(columnspan=2, sticky='nsew')
        
        # Configuration des tailles
        for i in range(6):
            master.rowconfigure(i, weight=1)
        for i in range(4):
            master.columnconfigure(i, weight=1)
        
        self.reset_calcul()
    
    def reset_calcul(self):
        self.current = '0'
        self.operation = None
        self.previous = None
        self.update_display()
    
    def update_display(self):
        self.display_var.set(self.current)
    
    def on_button_click(self, text):
        if text in '0123456789':
            if self.current == '0':
                self.current = text
            else:
                self.current += text
        elif text == '.':
            if '.' not in self.current:
                self.current += '.'
        elif text == 'C':
            self.reset_calcul()
            return
        elif text in '+-×÷':
            if self.operation:
                self.calculate()
            self.previous = self.current
            self.operation = text
            self.current = '0'
        elif text == '=':
            if self.operation:
                self.calculate()
                self.operation = None
        
        self.update_display()
    
    def calculate(self):
        try:
            a = float(self.previous)
            b = float(self.current)
            if self.operation == '+':
                result = a + b
            elif self.operation == '-':
                result = a - b
            elif self.operation == '×':
                result = a * b
            elif self.operation == '÷':
                result = a / b
            
            self.current = str(result)
            self.previous = None
        except:
            self.current = 'Error'
        
        self.update_display()

root = tk.Tk()
app = CalculatriceiPhone(root)
root.mainloop()
