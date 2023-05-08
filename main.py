from tkinter import*
from tkinter import messagebox
import random
import os
import re

class Basic_Compiler:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x560")
        self.root.title("Basic Compiler")
        title = Label(self.root, text="Basic Compiler", font=('Arial', 30, 'bold'), pady=2, bd=12, bg="#8A8A8A", fg="Black", relief=GROOVE)
        title.pack(fill=X)

        Input_Frame = LabelFrame(self.root, text="Input Tab", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        Input_Frame.place(x=0, y=78, width=625, height=480)
        
        self.Input_Code=Text(Input_Frame, height=12, width=50,font=('times new roman', 16, 'bold'), bd=5, relief=GROOVE)
        self.Input_Code.grid(row=0, column=1, padx=20, pady=10)

        Output_Frame = Frame(self.root, bd=10, relief=GROOVE)
        Output_Frame.place(x=625, y=78, width=625, height=480)

        Output_LB = Label(Output_Frame, text="Output", font='arial 15 bold', bd=7,bg="grey", relief=GROOVE)
        Output_LB.pack(fill=X)
        
        scroll_y = Scrollbar(Output_Frame, orient=VERTICAL)
        self.Output_Run = Text(Output_Frame, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.Output_Run.yview)
        self.Output_Run.pack(fill=BOTH, expand=1)
        
        self.clear = False
        self.detect = False
        self.Qct=0
        
        SubInput_Frame = LabelFrame(Input_Frame, text="Options", font=('arial', 14, 'bold'), bd=10, fg="Black", bg="grey")
        SubInput_Frame.place(x=0, y=325, relwidth=1, height=120)
        
        Run_Button = Button(SubInput_Frame, command=self.Permit_Response, text="Run", bg="#13B10F", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        Run_Button.grid(row=1, column=1, padx=5, pady=10)
        
        Clear_BTN = Button(SubInput_Frame, command=self.Clear_Data, text="Clear", bg="red", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        Clear_BTN.grid(row=1, column=2, padx=5, pady=10)
        
        Reset_BTN = Button(SubInput_Frame, command=self.ResetWindow, text="Reset", bg="red", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        Reset_BTN.grid(row=1, column=3, padx=5, pady=10)
        
        self.Output_Run.delete('1.0', END)
        self.Output_Run.insert(END, "\t \t     No Inputs Recieved...")
        self.Output_Run.insert(END, f"\n=====================================================================")
        
        self.symbols = ["(", ")", "{", "}",",",";"]
        self.operators = ["+", "-","/","%", "*","&&","||","<",">","=","!"]
        self.datatype = ["int", "float", "string", "double", "bool", "char"]
        self.functions = ["for", "while", "if", "do", "return", "break", "continue", "end"]
        
    
    def Filter_Breaks(self,Input):
        return ''.join(Input.splitlines())

    def Permit_Response(self):
        self.Input = self.Input_Code.get("1.0", "end-1c")
        self.Input = self.Filter_Breaks(self.Input)
        if self.Input == "":
            self.Output_Run.insert(END, f"\n")
            self.Output_Run.insert(END, f"\n No Input")
        else:
            if not self.clear:
                self.Output_Run.delete("1.0", END)
                self.Output_Run.insert(END, f"\t \t Input Detected...")
                self.Output_Run.insert(END, f"\n =====================================================================")
                self.clear = True 
            self.Get_Variables()  
            
    
    def Get_Variables(self):
        input_lines = self.Input.split(";")
        for line in input_lines:
            line = line.strip()
            if line:
                tokens = line.split()
                if len(tokens) >= 3 and tokens[0] in self.datatype:
                    var = tokens[1]
                    operator = tokens[2]
                    value = " ".join(tokens[3:])
                    symbol = ";"
                    print(f"Data Type: {tokens[0]}, Variable: {var}, Operator: {operator}, Value: {value}, Symbol: {symbol}")
                    self.Output_Run.insert(END, f"\n Data Type: {tokens[0]}, Variable: {var}, Operator: {operator}, Value: {value}, Symbol: {symbol}")
        self.Parser() 
                
    def Parser(self):
        input_lines = self.Input.split(";")
        for line in input_lines:
            line = line.strip()
            if line:
                tokens = line.split()
                if len(tokens) >= 3 and tokens[0] in self.datatype:
                    var = tokens[1]
                    operator = tokens[2]
                    value = " ".join(tokens[3:])
                    symbol = ";"
                    # print(f"Data Type: {tokens[0]}, Variable: {var}, Operator: {operator}, Value: {value}, Symbol: {symbol}")
                elif len(tokens) >= 3 and tokens[0] in self.functions:
                    if tokens[0] == "for":
                        if len(tokens) == 9 and tokens[2] == ";" and tokens[4] == ";" and tokens[6] == ")":
                            init_statement = " ".join(tokens[2:4])
                            condition = " ".join(tokens[4:6])
                            final_expression = " ".join(tokens[6:8])
                            print(f"For loop: Init Statement: {init_statement}, Condition: {condition}, Final Expression: {final_expression}")
                        else:
                            print("Invalid for loop syntax")
                    elif tokens[0] == "while":
                        if len(tokens) == 4:
                            condition = " ".join(tokens[2:4])
                            print(f"While loop: Condition: {condition}")
                        else:
                            print("Invalid while loop syntax")
                    elif tokens[0] == "if":
                        if len(tokens) >= 3 and tokens[-1] == "{":
                            condition = " ".join(tokens[1:-2])
                            print(f"If statement: Condition: {condition}")
                        else:
                            print("Invalid if statement syntax")
                    elif tokens[0] == "do":
                        if len(tokens) >= 3 and tokens[-2] == "while" and tokens[-1] == "(":
                            condition = " ".join(tokens[1:-3])
                            print(f"Do-while loop: Condition: {condition}")
                        else:
                            print("Invalid do-while loop syntax")
                    elif tokens[0] == "return":
                        if len(tokens) == 2:
                            print(f"Return statement: Value: {tokens[1]}")
                        else:
                            print("Invalid return statement syntax")
                    elif tokens[0] in ["break", "continue", "end"]:
                        if len(tokens) == 1:
                            print(f"{tokens[0]} statement")
                        else:
                            print(f"Invalid {tokens[0]} statement syntax")
                elif len(tokens) >= 3 and tokens[1] in self.operators and tokens[-1] == ";":
                    var = tokens[0]
                    operator = tokens[1]
                    value = " ".join(tokens[2:-1])
                    symbol = ";"
                    print(f"Assignment: Variable: {var}, Operator: {operator}, Value: {value}, Symbol: {symbol}")
                elif len(tokens) == 1 and tokens[0][-1] == ";":
                    var = tokens[0][:-1]
                    symbol = ";"
                    print(f"Declaration: Variable: {var}, Symbol: {symbol}")
                else:
                    print("Invalid syntax")
    
    def Compile(self):
       pass
        
   
    def Clear_Data(self):
        self.Output_Run.delete('1.0', END)
        self.Qct = 0
        

    def ResetWindow(self):
        root.destroy()
        os.system('main.py')


root = Tk()
obj = Basic_Compiler(root)
root.mainloop()