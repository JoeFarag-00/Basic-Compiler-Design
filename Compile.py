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
 
                        # if tokens[0] == 'float' or tokens[0] == 'double':
                        #     try:
                        #         value = float(tokens[3])
                        #     except ValueError:
                        #         print(f"\nError: Incorrect float value: '{tokens[3]}'")
                        #         self.Output_Run.insert(END, f"\nError: Incorrect float value: '{tokens[3]}'")
                        #         self.BadDec = True
                       
                        if tokens[0] == 'int':
                            try:
                                value = int(value)
                            except ValueError:
                                if self.Declared_Vars[value]["datatype"] != "int":
                                    print(f"\nError:value incompatible: '{value}'")
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
                                pass
                                # print(f"Declaration Errors Found")
                                # self.Output_Run.insert(END, f"\nDeclaration Errors Found")
                except:
                    # self.Output_Run.insert(END, f"\n Error: Declaration {var}")
                    pass
               

        
        # print("Memory: ",self.Declared_Vars)
        self.Check_Variables()
        self.Get_ResWords()
        self.Parse()
         
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

                
    def Get_ResWords(self):
        while_stack = []
        input_lines = self.Input.split(";")
        for line_num, line in enumerate(input_lines):
            line = line.strip()
            if line:
                tokens = line.split()
                if tokens[0] == "while":
                    if len(tokens) < 5 or tokens[1] != "(" or tokens[-2] != ")":
                        self.Output_Run.insert(END, f"\nError: While loop condition missing parentheses at line {line_num+1}")
                    else:
                        try:
                            var1 = int(tokens[2]) if tokens[2].isdigit() else self.Declared_Vars[tokens[2]]["value"]
                        except (KeyError, ValueError):
                            self.Output_Run.insert(END, f"\nError: While loop condition contains undeclared variable or invalid literal: {tokens[2]}")
                            continue

                        op = tokens[3]
                        if op not in self.comparison_signs:
                            self.Output_Run.insert(END, f"\nError: While loop condition contains invalid operator: {op}")
                            continue

                        try:
                            var2 = int(tokens[4]) if tokens[4].isdigit() else self.Declared_Vars[tokens[4]]["value"]
                        except (KeyError, ValueError):
                            self.Output_Run.insert(END, f"\nError: While loop condition contains undeclared variable or invalid literal: {tokens[4]}")
                            continue

                        if op == "<":
                            if var1 >= var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")
                        elif op == ">":
                            if var1 <= var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")
                        elif op == "<=":
                            if var1 > var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")
                        elif op == ">=":
                            if var1 < var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")
                        elif op == "==":
                            if var1 != var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")
                        elif op == "!=":
                            if var1 == var2:
                                self.Output_Run.insert(END, f"\nError: While loop condition is always false at line {line_num+1}")

                        while_stack.append(line_num)

                    if while_stack:
                        # If there are any unclosed while loops, report an error
                        for while_start in while_stack:
                            self.Output_Run.insert(END, f"\nError: Unclosed while loop starting at line {while_start+1}")
                    else:
                        pass
                        self.Output_Run.insert(END, f"\nAll while loops are closed")

    def Parse(self):
       input_lines = self.Input.split(";")
       for line in input_lines:
            line = line.strip()
            if line:
                # strip
                tokens = line.split()
                if tokens[0] in self.datatype: # initialize
                    if tokens[0] == 'int' or tokens[0] == 'float' or tokens[0]=='double':
                        varname=''
                        concatenated_slicedtokens=''
                        slicedtokens = tokens[3:]
                        # 
                        opernads = slicedtokens
                        for i in range(len(opernads)):
                            if  opernads[i] in self.Declared_Vars and not opernads[i].isdigit():
                                varname=opernads[i]
                                opernads[i]= self.Declared_Vars[varname]['value']
                            concatenated_slicedtokens+=str(opernads[i])
                        print(f'\n Updated Variable "{tokens[1]}" {self.Declared_Vars[tokens[1]]}')
                        self.Declared_Vars[tokens[1]]['value']=(eval(concatenated_slicedtokens))
                        # self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[1]}" {self.Declared_Vars[tokens[1]]}')


                elif tokens[0] in self.Declared_Vars: # update

                    if self.Declared_Vars[tokens[0]]['datatype'] == 'int' or self.Declared_Vars[tokens[0]]['datatype'] == 'float' or self.Declared_Vars[tokens[0]]['datatype'] == 'double': 
                        varname=''
                        concatenated_slicedtokens=''
                        slicedtokens = tokens[2:]
                        opernads=slicedtokens
                        for i in range(len(opernads)):
                            # if opernads[i].isdigit():
                            #     opernads[i] = self.Declared_Vars[tokens[0]]['value']
                            if  opernads[i] in self.Declared_Vars:
                                varname=opernads[i]
                                opernads[i]= self.Declared_Vars[varname]['value']
                            concatenated_slicedtokens+=str(opernads[i])
                        print(concatenated_slicedtokens)
                        self.Declared_Vars[tokens[0]]['value']=(eval(concatenated_slicedtokens))
                        print(f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                        self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')

                    elif self.Declared_Vars[tokens[0]]['datatype'] == 'bool':
                        
                        if tokens[2] =='false' or tokens[2] == 'true':
                            self.Declared_Vars[tokens[0]]['value']=tokens[2]
                            print(f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                            self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                        
                        elif tokens[2] in self.Declared_Vars and self.Declared_Vars[tokens[2]]['datatype'] == 'bool':
                            self.Declared_Vars[tokens[0]]['value'] = self.Declared_Vars[tokens[2]]['value'] 
                            print(f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                            self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')

                    elif self.Declared_Vars[tokens[0]]['datatype'] == 'char':
                        char = re.match(r"^'(?P<value>.*)'$", tokens[2])
                        if char and len(char.group('value')) <= 2:
                            tokens[2] = char.group('value')
                        self.Declared_Vars[tokens[0]]['value']=tokens[2]
                        print(f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                        self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                    
                    elif self.Declared_Vars[tokens[0]]['datatype'] == 'string':
                        string = re.match(r"^'(?P<value>.*)'$", tokens[2])
                        if string:
                            tokens[2] = char.group('value')
                            self.Declared_Vars[tokens[0]]['value']=tokens[2]
                            print(f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                            self.Output_Run.insert(END,f'\nUpdated Variable "{tokens[0]}" {self.Declared_Vars[tokens[0]]}')
                # else:
                            
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