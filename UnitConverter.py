import tkinter as tk

class UnitConverter(tk.Frame):
    def __init__(self,root):
        self.colour1 = '#cbdceb'
        self.colour2 = '#7ea7ce'
        self.colour3 = '#8ea7be'
        
        self.conversions = ['km → mi',
                            'mi → km',
                            'kg → lbs',
                            'lbs → kg',
                            '°F → °C',
                            '°C → °F',
                            'hour → second',
                            'second → hour']
        
        super().__init__(
            root,
        bg=self.colour1
        )
        
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2,weight=1)
        self.create_widgets()
        
    def create_widgets(self):
        self.title = tk.Label(self.main_frame,
                              bg=self.colour1,
                              fg=self.colour2,
                              font=('Arial',22,'bold'),
                              text="Unit Converter")
        
        self.title.grid(column=0,row=0,sticky=tk.EW,pady=(10,20))
        
        self.conversion = tk.StringVar()
        self.conversion.set(self.conversions[0])
        
        def callback_trace_conversion(*args):
            self.convert_value()
            
        self.conversion.trace('w', callback_trace_conversion)
        
        self.select_conversion = tk.OptionMenu(
            self.main_frame,
            self.conversion,
            *self.conversions
        )
        self.select_conversion.config(
            bg=self.colour3,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Arial',14),
            border=0,
            highlightthickness=0,
            indicatoron=0,
        )
        self.select_conversion['menu'].config(
            bg=self.colour3,
            fg=self.colour1,
            activebackground=self.colour1,
            activeforeground=self.colour2,
            font=('Arial',14),
            activeborderwidth=0,
            border=1,
            relief=tk.FLAT
        )
        self.select_conversion.grid(column=0,row=1,sticky=tk.EW,padx=50)
        
        self.container_values = tk.Frame(self.main_frame,bg=self.colour2)
        self.container_values.columnconfigure(1,weight=1)
        self.container_values.grid(column=0,row=2,sticky=tk.NSEW,padx=50,pady=40)
        
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
            fg=self.colour1,
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
        self.value_to_convert.grid(column=0,row=0,sticky=tk.N,ipady=3)
        self.value_to_convert.bind('<KeyPress>', self.call_convert_value_delay)
        
        self.arrow = tk.Label(
            self.container_values,
            bg=self.colour2,
            text="→",
            font=('Arial',18)
        )
        self.arrow.grid(column=1,row=0)
        self.converted_value = tk.StringVar()
        self.entry_converted_value = tk.Entry(
            self.container_values,
            bg=self.colour3,
            fg=self.colour1,
            disabledbackground=self.colour3,
            disabledforeground=self.colour1,
            font=('Arial',14),
            highlightthickness=0,
            border=0,
            justify=tk.CENTER,
            width=11,
            state=tk.DISABLED,
            cursor='arrow',
            textvariable=self.converted_value
        )
        self.entry_converted_value.grid(column=2,row=0,sticky=tk.N, ipady=3)
        
    def call_convert_value_delay(self,event):
        self.main_frame.after(100, self.convert_value)
        
    def convert_value(self):
        conversion = self.conversion.get()

        if not self.value_to_convert.get() or self.value_to_convert.get() == "-":
            self.converted_value.set("")
            return
        
        value_to_convert_local = float(self.value_to_convert.get())
        
        match conversion:
            case 'km → mi':
                # append km to end of entry
                self.converted_value.set(f"{value_to_convert_local/1.609:.5f}")
            case 'mi → km':
                self.converted_value.set(f"{value_to_convert_local*1.609:.5f}")
            case 'kg → lbs':
                self.converted_value.set(f"{value_to_convert_local*2.205:.5f}")
            case 'lbs → kg':
                self.converted_value.set(f"{value_to_convert_local/2.205:.5f}")
            case '°F → °C':
                self.converted_value.set(f"{(value_to_convert_local-32)*(5/9):.5f}")
            case '°C → °F':
                self.converted_value.set(f"{(value_to_convert_local*(9/5))+32:.5f}")
            case 'hour → second':
                self.converted_value.set(f"{(value_to_convert_local*3600):.5f}")
            case 'second → hour':
                self.converted_value.set(f"{(value_to_convert_local/3600):.5f}")

        
        
        
root = tk.Tk()
unit_converter_app = UnitConverter(root)
root.title("Unit Converter")
root.geometry("400x250")
root.resizable(width=False,height=False)

root.mainloop()
