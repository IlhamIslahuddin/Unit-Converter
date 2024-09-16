import tkinter as tk

class UnitConverter(tk.Frame):
    def __init__(self,root):
        self.colour1 = '#cbdceb'
        self.colour2 = '#3c6f9f'
        self.colour3 = '#ffffff'
        
        self.conversions = {"Distance" : ['km → mi',
                            'mi → km',
                            'ft → cm',
                            'cm → ft',
                            'inches → cm',
                            'cm → inches',
                            'km → cm',
                            'cm → km'],
                            "Weight": ['kg → lbs',
                            'lbs → kg',
                            'kg → stone',
                            'stone → kg',
                            'oz → g',
                            'g → oz'],
                            'Temperature': ['°F → °C',
                            '°C → °F'],
                            'Time': ['hour → second',
                            'second → hour',
                            'days → minutes',
                            'minutes → days']}
        
        super().__init__(
            root,
        bg=self.colour1
        )
        
        self.main_frame = self
        self.main_frame.pack()
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2,weight=1)
        self.create_widgets()
        
    def create_widgets(self):
        self.title = tk.Label(self.main_frame,
                              bg=self.colour1,
                              fg=self.colour2,
                              font=('Arial',24,'bold underline'),
                              text="Unit Converter")
        
        self.title.grid(column=0,row=0,sticky=tk.EW,pady=(10,20))
        
        self.category = tk.StringVar(value=list(self.conversions.keys())[0])
        self.conversion = tk.StringVar()
                
        self.select_category = tk.OptionMenu(self.main_frame, self.category, *self.conversions.keys(), command=self.update_submenu)
        
        self.select_category.config(
            bg=self.colour3,
            fg=self.colour2,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Arial',14),
            border=0,
            highlightthickness=0,
            indicatoron=0,
        )
        self.select_category['menu'].config(
            bg=self.colour3,
            fg=self.colour2,
            activebackground=self.colour1,
            activeforeground=self.colour2,
            font=('Arial',14),
            activeborderwidth=0,
            border=1,
            relief=tk.FLAT
        )
        
        self.select_conversion = tk.OptionMenu(
            self.main_frame,
            self.conversion,
            *self.conversions[self.category.get()]
        )
        self.select_conversion.config(
            bg=self.colour3,
            fg=self.colour2,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Arial',14),
            border=0,
            highlightthickness=0,
            indicatoron=0,
        )
        self.select_conversion['menu'].config(
            bg=self.colour3,
            fg=self.colour2,
            activebackground=self.colour1,
            activeforeground=self.colour2,
            font=('Arial',14),
            activeborderwidth=0,
            border=1,
            relief=tk.FLAT
        )
        self.select_category.grid(column=0,row=1,sticky=tk.EW,padx=50,pady=10)
        self.select_conversion.grid(column=0,row=3,sticky=tk.EW,padx=50)
        
        self.formula = tk.Label(self.main_frame,text="Formula",bg=self.colour1)
        self.formula.grid(column=0,row=5)
        
        self.update_submenu(self.category.get())
        
        self.container_values = tk.Frame(self.main_frame,bg=self.colour2)
        self.container_values.columnconfigure(1,weight=1)
        self.container_values.grid(column=0,row=4,sticky=tk.NSEW,padx=50,pady=40)
        
        def validation(value):
            if not value or value == '-':
                return True
            try:
                value = float(value)
            except ValueError:
                return False
            
            return True
        
        value_validation_command = self.container_values.register(validation)
        
        self.value_to_convert = tk.Entry(
            self.container_values,
            bg=self.colour3,
            fg=self.colour2,
            selectbackground=self.colour1,
            selectforeground=self.colour2,
            font=('Arial',14),
            highlightthickness=0,
            border=0,
            justify=tk.CENTER,
            width=11,
            validate='key',
            validatecommand=(value_validation_command,'%P',)
        )
        self.value_to_convert.grid(column=0,row=0,sticky=tk.N,ipady=6)
        self.value_to_convert.bind('<KeyPress>', self.call_convert_value_delay)
        
        self.arrow = tk.Label(
            self.container_values,
            bg=self.colour1,
            fg=self.colour2,
            text="→",
            font=('Arial',19)
        )
        self.arrow.grid(column=1,row=0,ipady=1)
        self.converted_value = tk.StringVar()
        self.entry_converted_value = tk.Entry(
            self.container_values,
            bg=self.colour3,
            fg=self.colour2,
            disabledbackground=self.colour3,
            disabledforeground=self.colour2,
            font=('Arial',14),
            highlightthickness=0,
            border=0,
            justify=tk.CENTER,
            width=11,
            state=tk.DISABLED,
            cursor='arrow',
            textvariable=self.converted_value
        )
        self.entry_converted_value.grid(column=2,row=0,sticky=tk.N, ipady=6)
        
    def call_convert_value_delay(self,event):
        self.main_frame.after(100, self.convert_value)
                
    def convert_value(self):
        conversion = self.conversion.get()
        value = self.value_to_convert.get()

        if not value or value == "-":
            self.converted_value.set("")
            return
        
        value_to_convert_local = float(self.value_to_convert.get())
        
        def callback_trace_conversion(*args):
            self.convert_value()
            
        self.conversion.trace('w', callback_trace_conversion)
        
        match conversion:
            case 'km → mi':
                self.formula.configure(text=f"Formula: km / 1.609")
                self.converted_value.set(f"{value_to_convert_local/1.609344:.5f}")
            case 'mi → km':
                self.formula.configure(text=f"Formula: miles x 1.609")
                self.converted_value.set(f"{value_to_convert_local*1.609344:.5f}")
            case 'ft → cm':
                self.formula.configure(text=f"Formula: feet x 30.48")
                self.converted_value.set(f"{value_to_convert_local*30.48:.5f}")
            case 'cm → ft':
                self.formula.configure(text=f"Formula: cm / 30.48")
                self.converted_value.set(f"{value_to_convert_local/30.48:.5f}")
            case 'inches → cm':
                self.formula.configure(text=f"Formula: inches x 2.54")
                self.converted_value.set(f"{value_to_convert_local*2.54:.5f}")
            case 'cm → inches':
                self.formula.configure(text=f"Formula: cm / 2.54")
                self.converted_value.set(f"{value_to_convert_local/2.54:.5f}")
            case 'km → cm':
                self.formula.configure(text=f"Formula: km x 100,000")
                self.converted_value.set(f"{value_to_convert_local*100000:.5f}")
            case 'cm → km':
                self.formula.configure(text=f"Formula: cm / 100,000")
                self.converted_value.set(f"{value_to_convert_local/100000:.5f}")
            case 'kg → lbs':
                self.formula.configure(text=f"Formula: kg x 2.205")
                self.converted_value.set(f"{value_to_convert_local*2.2046:.5f}")
            case 'lbs → kg':
                self.formula.configure(text=f"Formula: lbs / 2.205")
                self.converted_value.set(f"{value_to_convert_local/2.2046:.5f}")
            case 'kg → stone':
                self.formula.configure(text=f"Formula: kg / 6.35")
                self.converted_value.set(f"{value_to_convert_local/6.35029:.5f}")
            case 'stone → kg':
                self.formula.configure(text=f"Formula: stone x 6.35")
                self.converted_value.set(f"{value_to_convert_local*6.35029:.5f}")
            case 'oz → g':
                self.formula.configure(text=f"Formula: ounces x 28.35")
                self.converted_value.set(f"{value_to_convert_local*28.3495:.5f}")
            case 'g → oz':
                self.formula.configure(text=f"Formula: grams / 28.35")
                self.converted_value.set(f"{value_to_convert_local/28.3495:.5f}")
            case '°F → °C':
                self.formula.configure(text=f"Formula: (°F-32) x (5/9)")
                self.converted_value.set(f"{(value_to_convert_local-32)*(5/9):.5f}")
            case '°C → °F':
                self.formula.configure(text=f"Formula: (°C x (9/5)) + 32")
                self.converted_value.set(f"{(value_to_convert_local*(9/5))+32:.5f}")
            case 'hour → second':
                self.formula.configure(text=f"Formula: hour x 3600")
                self.converted_value.set(f"{(value_to_convert_local*3600):.5f}")
            case 'second → hour':
                self.formula.configure(text=f"Formula: seconds / 3600")
                self.converted_value.set(f"{(value_to_convert_local/3600):.5f}")
            case 'days → minutes':
                self.formula.configure(text=f"Formula: days x 1440")
                self.converted_value.set(f"{(value_to_convert_local*1440):.5f}")
            case 'minutes → days':
                self.formula.configure(text=f"Formula: minutes / 1440")
                self.converted_value.set(f"{(value_to_convert_local/1440):.5f}")
                
    def update_submenu(self, category):
        self.select_category = self.select_conversion['menu']
        self.select_category.delete(0, 'end')
        
        for option in self.conversions[category]:
            self.select_category.add_command(label=option, command=tk._setit(self.conversion, option))
        
        self.conversion.set(self.conversions[category][0])

        
root = tk.Tk()
unit_converter_app = UnitConverter(root)
root.title("Unit Converter")
root.geometry("400x300")
root.resizable(width=False,height=False)
root.mainloop()
