from tkinter import*
from tkinter import messagebox
import random
import os
import re
import sys

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
        self.operators = ["+", "-","/","*","++","--","+=","-=","="]
        self.comparison_signs = ["%","&&","||","<",">","<=",">=","!=","=="]
        self.datatype = ["int", "float", "string", "double", "bool", "char"]
        self.res_words = ["for", "while", "if", "do", "return", "break", "continue", "end", "switch", "default", "case"]
        self.spliter = [";","}"]
        self.DecPos = 0

    def Get_Declarations(self):
        self.Declared_Vars = {}
        self.BadDec = False
        symbol = ""
        input_lines = self.Input.split(";")
        for line in input_lines:
            line = line.strip()
            if line:
                tokens = line.split()
                self.DecPos+=1
                try:
                    if len(tokens) >= 3 and tokens[0] in self.datatype:
                        # try:
                        #     if tokens[0] in self.datatype and tokens[3].isalpha() and tokens[3] in self.Declared_Vars or tokens[0] in self.datatype and tokens[3].isdigit():
                        #             if tokens[1].isalpha() and tokens[2] == "=" and tokens[3].isdigit() or tokens[3] in self.Declared_Vars and tokens[4].isdigit() or tokens[4] in self.Declared_Vars:
                        #                 print(f"Data Type: {tokens[0]}, operator: {tokens[2]}, var1: '{tokens[3]}', var2: {tokens[4]}")
                        #                 self.Output_Run.insert(END, f"Data Type: {tokens[0]}, operator: {tokens[2]}, var1: '{tokens[3]}', var2: {tokens[4]}")
                        # except:
                        #     self.Output_Run.insert(END, f"TEMP")
                        #     pass
                        
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
                                value = float(tokens[3])
                            except ValueError:
                                print(f"\nError: Incorrect float value: '{tokens[3]}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect float value: '{tokens[3]}'")
                                self.BadDec = True
                       
                        if tokens[0] == 'int':
                            try:
                                value = int(value)
                            except ValueError:
                                print(f"\nError: Incorrect int value: '{value}'")
                                self.Output_Run.insert(END, f"\nError: Incorrect int value: '{value}'")
                                self.BadDec = True
                        # else:
                        #     if float(value) != int(value):
                        #         print(f"\nError: Incorrect int value: '{value}'")
                        #         self.Output_Run.insert(END, f"\nError: Incorrect int value: '{value}'")
                        #         self.BadDec = True
                                
                        #Handle ; here

                        if var in self.Declared_Vars:
                            print(f"Error: Duplicate declaration of variable {var}. Value: {value}")
                            self.Output_Run.insert(END, f"\nError: Duplicate declaration of variable '{var}' Value: '{value}'")
                        else:
                            if not self.BadDec:
                                print(f"Data Type: {tokens[0]}, Variable: {var}, Operator: '{operator}', Value: {value}")
                                self.Output_Run.insert(END, f"\nData Type: {tokens[0]}, Variable: {var}, Operator: '{operator}', Value: {value}")
                                self.Declared_Vars[var] = {"datatype": tokens[0], "value": value, "pos": self.DecPos}
                            else:
                                print(f"Declaration Errors Found")
                                self.Output_Run.insert(END, f"\nDeclaration Errors Found")
                except:
                    # self.Output_Run.insert(END, f"\n Error: Declaration {var}")
                    pass
               

        
        # print("Memory: ",self.Declared_Vars)
        self.Check_Variables()
        self.Get_ResWords()
         
    def Check_Variables(self):
        for line in self.Input.split(";"):
            line = line.strip()
            if line:
                first_word = line.split()[0]
                if first_word in self.res_words or first_word in self.datatype:
                    continue
                
                tokens = line.split()
                for i, token in enumerate(tokens):
                    if token in self.symbols or token in self.operators or token in self.datatype:
                        continue
                    
                    if token not in self.Declared_Vars and not token.isdigit():
                        print(f"\nError: Undeclared variable '{token}'")
                        self.Output_Run.insert(END, f"\nError: Undeclared variable '{token}'")
                    
                    elif token == "=":
                        if len(tokens) < 3 or tokens[0] in self.datatype:
                            print(f"\nError: Syntax error: '{line}'")
                            self.Output_Run.insert(END, f"\nError: Syntax error: '{line}'")
                    elif token in self.comparison_signs:
                        if len(tokens) < 3 or tokens[0] in self.datatype:
                            print(f"\nError: Syntax error: '{line}'")
                            self.Output_Run.insert(END, f"\nError: Syntax error: '{line}'")
                    elif token == "++" or token == "--":
                        if len(tokens) != 2 or tokens[0] in self.datatype:
                            print(f"\nError: Syntax error: '{line}'")
                            self.Output_Run.insert(END, f"\nError: Syntax error: '{line}'")
                    elif token == "+=" or token == "-=":
                        if len(tokens) < 3 or tokens[0] in self.datatype:
                            print(f"\nError: Syntax error: '{line}'")
                            self.Output_Run.insert(END, f"\nError: Syntax error: '{line}'")
                    elif token == ";":
                        if len(tokens) > 1:
                            print(f"\nError: Syntax error: '{line}'")
                            self.Output_Run.insert(END, f"\nError: Syntax error: '{line}'")
                    
                    elif token.isdigit():
                        if self.Declared_Vars[token]["datatype"] != "int":
                            print(f"\nError: Type error: '{token}' is not an integer")
                            self.Output_Run.insert(END, f"\nError: Type error: '{token}' is not an integer")
                    elif token.replace(".", "", 1).isdigit():
                        if self.Declared_Vars[token]["datatype"] != "float" and self.Declared_Vars[token]["datatype"] != "double":
                            print(f"\nError: Type error: '{token}' is not a floating point number")
                            self.Output_Run.insert(END, f"\nError: Type error: '{token}' is not a floating point number")
                    elif token == "true" or token == "false":
                        if self.Declared_Vars[token]["datatype"] != "bool":
                            print(f"\nError: Type error: '{token}' is not a boolean")
                            self.Output_Run.insert(END, f"\nError: Type error: '{token}' is not a boolean")
                    elif token in self.Declared_Vars:
                        if self.Declared_Vars[token]["datatype"] == "undefined":
                            print(f"\nError: Type error: '{token}' is not defined")
                            self.Output_Run.insert(END, f"\nError: Type error: '{token}' is not defined")
                    else:
                        print(f"\nError: Type error: '{token}' is not defined")
                        self.Output_Run.insert(END, f"\nError: Type error: '{token}' is not defined")
             
                    
                
    def Get_ResWords(self):
        input_lines = self.Input.split(";")
        while_index = -1
        while_stack = []

        switch_cases = {}
        switch_var = None
        switch_start = None
        switch_end = None
        default_found = False
        
        for i, line in enumerate(input_lines):
            if line:
                tokens = line.split()
                
                # if tokens[0] in self.res_words and token[0] != "while" and tokens[0] != "switch" and tokens[0] != "case" and tokens[0] != "default":
                #     if tokens[0] in ["break", "continue", "end"]:
                #         print(f"Reserved Word: {tokens[0]}")
                #         self.Output_Run.insert(END, f"\n Reserved Word: {tokens[0]}")
                #     else:
                #         argument = " ".join(tokens[1:])
                #         print(f"Reserved Word: {tokens[0]}, Argument: {argument}")
                #         self.Output_Run.insert(END, f"\n Reserved Word: {tokens[0]}, Argument: {argument}")
                        
                if tokens[0] == "while":
                    if len(tokens) < 4 or tokens[1] != "(" or tokens[-2] != ")":
                        print("Error: Invalid while loop syntax")
                        self.Output_Run.insert(END, "\nError: Invalid while loop syntax")
                        continue
                    valid_comparison = False
                    for sign in self.comparison_signs:
                        if sign in line:
                            valid_comparison = True
                            break
                    if not valid_comparison:
                        print("Error: Invalid comparison argument")
                        self.Output_Run.insert(END, "\nError: Invalid comparison argument")
                        continue
                    loop_code = " ".join(line.split("{")[1:])[:-1].strip()
                    tokens = loop_code.split()
                    for j in range(len(tokens)):
                        if tokens[j] in self.Declared_Vars:
                            if self.Declared_Vars[tokens[j]]["datatype"] == "bool":
                                if j < len(tokens) - 2 and tokens[j+1] not in self.comparison_signs:
                                    print(f"Error: Invalid bool expression")
                                    self.Output_Run.insert(END, "\nError: Invalid bool expression")
                            elif j < len(tokens) - 2 and tokens[j+1] in self.comparison_signs:
                                print(f"Error: Invalid comparison operation")
                                self.Output_Run.insert(END, "\nError: Invalid comparison operation")
                        elif tokens[j] not in self.symbols and tokens[j] not in self.res_words and tokens[j] not in self.Declared_Vars and not tokens[j].isdigit() and not re.match('^\'\w\'$', tokens[j]):
                            print(f"Error: Undeclared variable '{tokens[j]}'")                       
                            self.Output_Run.insert(END, f"\nError: Undeclared variable '{tokens[j]}'")
                    while_stack.append(i)
                    while_index = i
                elif while_index != -1:
                    if line.strip()[-1] == "}":
                        while_stack.pop()
                        if not while_stack:
                            loop_code = " ".join(input_lines[while_index:i+1]).split("{")[1:]
                            if len(loop_code) == 1:
                                loop_code = loop_code[0][:-1].strip()
                            else:                           
                                loop_code = "{".join(loop_code)[:-1].strip()
                            tokens = loop_code.split()
                            for j in range(len(tokens)):
                                if tokens[j] in self.Declared_Vars:
                                    if self.Declared_Vars[tokens[j]]["datatype"] == "bool":
                                        if j < len(tokens) - 2 and tokens[j+1] not in self.comparison_signs:
                                            print(f"Error: Invalid bool expression")
                                            self.Output_Run.insert(END, "\nError: Invalid bool expression")
                                    # elif j < len(tokens) - 2 and tokens[j+1] in self.comparison_signs:
                                    #     print(f"Error: Invalid comparison operation")
                                    #     self.Output_Run.insert(END, "\nError: Invalid comparison operation")
                                elif tokens[j] not in self.symbols and tokens[j] not in self.res_words and tokens[j] not in self.comparison_signs and tokens[j] not in self.operators and not tokens[j].isdigit() and not re.match('^\'\w\'$', tokens[j]):                               
                                    print(f"Error: Undeclared variable '{tokens[j]}'")
                                    self.Output_Run.insert(END, f"\nError: Undeclared variable '{tokens[j]}'")
                            print("Valid while loop")
                            self.Output_Run.insert(END, "\nValid while loop")
                        while_index = -1
                    elif line.strip()[-1] != "}":
                        continue
                    else:
                        print("Error: Invalid while loop syntax")
                        self.Output_Run.insert(END, "\nError: Invalid while loop syntax")
                        
                elif tokens[0] == "switch":
                    if len(tokens) < 2 or tokens[1] != "(" or tokens[-2] != ")":
                        print("Error: Invalid switch statement syntax")
                        self.Output_Run.insert(END, "\nError: Invalid switch statement syntax")
                        continue

                    switch_var = tokens[2]
                    if switch_var not in self.Declared_Vars:
                        print(f"Error: Undeclared variable '{switch_var}' in switch statement")
                        self.Output_Run.insert(END, f"\nError: Undeclared variable '{switch_var}' in switch statement")
                        continue

                    switch_start = i
                    switch_cases = {}
                    default_found = False

                elif tokens[0] == "case":
                    if switch_var is None:
                        print("Error: case statement used outside of switch statement")
                        self.Output_Run.insert(END, "\nError: case statement used outside of switch statement")
                        continue
                    if switch_end is not None:
                        print("Error: case statement used after switch statement has ended")
                        self.Output_Run.insert(END, "\nError: case statement used after switch statement has ended")
                        continue

                    if len(tokens) < 2 or not tokens[1].isdigit() or len(tokens) > 3 or (len(tokens) == 3 and tokens[2] != ":"):
                        print("Error: Invalid case statement syntax")
                        self.Output_Run.insert(END, "\nError: Invalid case statement syntax")
                        continue

                    case_value = int(tokens[1])
                    if case_value in switch_cases:
                        print(f"Error: Duplicate case value {case_value}")
                        self.Output_Run.insert(END, f"\nError: Duplicate case value {case_value}")
                        continue

                    switch_cases[case_value] = i

                elif tokens[0] == "default":
                    if switch_var is None:
                        print("Error: default statement used outside of switch statement")
                        self.Output_Run.insert(END, "\nError: default statement used outside of switch statement")
                        continue
                    if switch_end is not None:
                        print("Error: default statement used after switch statement has ended")
                        self.Output_Run.insert(END, "\nError: default statement used after switch statement has ended")
                        continue
                    if default_found:
                        print("Error: Duplicate default statement")
                        self.Output_Run.insert(END, "\nError: Duplicate default statement")
                        continue

                    default_found = True
                    switch_cases["default"] = i

                elif tokens[0] == "break":
                    if switch_var is None:
                        print("Error: break statement used outside of switch statement")
                        self.Output_Run.insert(END, "\nError: break statement used outside of switch statement")
                        continue
                    if switch_end is not None:
                        print("Error: break statement used after switch statement has ended")
                        self.Output_Run.insert(END, "\nError: break statement used after switch statement has ended")
                        continue
                    if not while_stack:
                        print("Error: break statement used outside of while loop")
                        self.Output_Run.insert(END, "\nError: break statement used outside of while loop")
                        continue

                    switch_end = while_stack.pop()

                elif tokens[0] == "while":
                    while_stack.append(i)

                else:
                    # Check if the statement is inside a switch statement without a case or default label
                    if switch_var is not None and switch_end is None:
                        print("Error: statement used inside switch statement without a case or default label")
                        self.Output_Run.insert(END, "\nError: statement used inside switch statement without a case or default label")
                        continue
                    
                    # Check if the variable is declared
                    if switch_var is not None and switch_var not in self.Declared_Vars:
                        print(f"Error: Undeclared variable '{switch_var}' in switch statement condition")
                        self.Output_Run.insert(END, f"\nError: Undeclared variable '{switch_var}' in switch statement condition")
                        continue

                    # Check if the variable is declared in the case statement
                    if switch_var is not None and len(tokens) > 1 and tokens[0] == "case":
                        case_value = tokens[1]
                        if not case_value.isdigit() or int(case_value) not in self.Declared_Vars:
                            print(f"Error: Undeclared variable '{case_value}' in case statement")
                            self.Output_Run.insert(END, f"\nError: Undeclared variable '{case_value}' in case statement")
                            continue

            # Check if the switch statement has a default label
            if switch_var is not None and switch_end is None:
                print("Error: switch statement without a default label")
                self.Output_Run.insert(END, "\nError: switch statement without a default label")
                 

    def Parse(self):
       pass
    
    def Compile(self):
       pass
    
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
            
    def Clear_Data(self):
        self.Output_Run.delete('1.0', END)
        # self.Output_Run.insert(END, f"\n ")
        self.Qct = 0
        self.BadDec = False

    def ResetWindow(self):
        root.destroy()
        # os.startfile('Basic Compiler\main.py')


    # input_lines = self.Input.split(";")
    # for line in input_lines:
    #     if line:
    #         tokens = line.split()
    #         if tokens[0] == "while":
    #             pass
   
   


root = Tk()
obj = Basic_Compiler(root)
root.mainloop()
