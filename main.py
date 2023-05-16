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
        
        self.Empty = False
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
        self.res_words = ["for", "while", "if", "do", "return", "break", "continue", "end", "switch", "default", "case"]
        self.spliter = [";","}"]
        
        
    
    def Filter_Breaks(self,Input):
        return ''.join(Input.splitlines())

    def Permit_Response(self):
        self.Input = self.Input_Code.get("1.0", "end-1c")
        self.Input = self.Filter_Breaks(self.Input)
        if self.Input == "":
            self.Output_Run.insert(END, f"\n")
            self.Output_Run.insert(END, f"\n No Input")
        else:
            if not self.Empty:
                self.Output_Run.delete("1.0", END)
                self.Output_Run.insert(END, f"\t \t Input Detected...")
                self.Output_Run.insert(END, f"\n =====================================================================")
                self.Empty = True 
            self.Output_Run.insert(END, f"\n")
            self.Get_Declarations()  
            
    
    def Get_Declarations(self):
        self.Declared_Vars = {}
        self.BadDec = False
        symbol = ""
        input_lines = self.Input.split(";")
        for line in input_lines:
            line = line.strip()
            if line:
                tokens = line.split()
                try:
                    if len(tokens) >= 3 and tokens[0] in self.datatype:
                        self.DecPos = 0
                        var = tokens[1]
                        matchVar = re.match(r'^(?![0-9]).*',var)
                        if not matchVar or var.isdigit():
                            print(f"\nError: Incorrect Name: '{var}'")
                            self.Output_Run.insert(END, f"\nError: Incorrect Variable Name: '{var}'")
                            self.BadDec = True

                        operator = tokens[2]
                        if operator != "=":
                            print(f"\nError: Incorrect operator: '{operator}'")
                            self.Output_Run.insert(END, f"\nError: Incorrect operator: '{operator}'")
                            self.BadDec = True
                            
                        value = tokens[3]
                                                
                        if tokens[0] == 'bool':
                                if value != "true" and value != "false":
                                    print(f"\nError: Incorrect bool value: '{value}'")
                                    self.Output_Run.insert(END, f"\nError: Incorrect bool value: '{value}'")
                                    self.BadDec = True
                                
                        if tokens[0] == 'string':
                            string = re.match(r"[\"'](?P<value>[\w\s]+)[\"']", value)
                            if not string:
                                print(f"\nError: Incorrect string value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect string value: '{value}'")
                                self.BadDec = True
                            else:
                                value = string.group('value')
                        
                        if tokens[0] == 'char':
                            char = re.match(r"^'(?P<value>.*)'$", value)
                            if char and len(char.group('value')) <= 2:
                                value = char.group('value')
                            else:
                                print(f"\nError: Incorrect Char value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect Char value: '{value}'")
                                self.BadDec = True
 
                        if tokens[0] == 'float' or tokens[0] == 'double':
                            try:
                                value = float(value)
                            except ValueError:
                                print(f"\nError: Incorrect float value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect float value: '{value}'")
                                self.BadDec = True
                       
                        if tokens[0] == 'int':
                            try:
                                value = int(value)
                            except ValueError:
                                print(f"\nError: Incorrect int value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect int value: '{value}'")
                                self.BadDec = True
                        else:
                            if float(value) != int(value):
                                print(f"\nError: Incorrect int value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect int value: '{value}'")
                                self.BadDec = True
                      
                        self.DecPos+=1
                        #Handle ; here
                except:
                    # self.Output_Run.insert(END, f"\n Error: Declaration {var}")
                    pass
                        
                if var in self.Declared_Vars:
                    print(f"Error: Duplicate declaration of variable {var}. Value: {value}")
                    self.Output_Run.insert(END, f"\nError: Duplicate declaration of variable '{var}' Value: '{value}'")
                else:
                    if not self.BadDec:
                        print(f"Data Type: {tokens[0]}, Variable: {var}, Operator: '{operator}', Value: {value}, Symbol: {symbol}")
                        self.Output_Run.insert(END, f"\nData Type: {tokens[0]}, Variable: {var}, Operator: '{operator}', Value: {value}, Symbol: {symbol}")
                        self.Declared_Vars[var] = {"datatype": tokens[0], "value": value, "pos": self.DecPos}
                    else:
                        print(f"Declaration Errors Found")
                        self.Output_Run.insert(END, f"\nDeclaration Errors Found")
              
              
        print("Memory: ",self.Declared_Vars)
        self.Get_ResWords()

                
    def Get_ResWords(self):
        input_lines = self.Input.split(";")
        for line in input_lines:
            if line:
                tokens = line.split()
                if tokens[0] in self.res_words:
                    if tokens[0] in ["break", "continue", "end"]:
                        print(f"Reserved Word: {tokens[0]}")
                        self.Output_Run.insert(END, f"\n Reserved Word: {tokens[0]}")
                    else:
                        argument = " ".join(tokens[1:])
                        print(f"Reserved Word: {tokens[0]}, Argument: {argument}")
                        self.Output_Run.insert(END, f"\n Reserved Word: {tokens[0]}, Argument: {argument}")
   

    def Compile(self):
       pass
        
   
    def Clear_Data(self):
        self.Output_Run.delete('1.0', END)
        # self.Output_Run.insert(END, f"\n ")
        self.Qct = 0
        self.BadDec = False
        

    def ResetWindow(self):
        root.destroy()
        # os.startfile('Basic Compiler\main.py')


root = Tk()
obj = Basic_Compiler(root)
root.mainloop()
