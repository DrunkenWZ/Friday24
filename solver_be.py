from PyQt6 import QtCore, QtGui, QtWidgets
from solver import Solver
from chempy import balance_stoichiometry
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from chemlib import Compound
import sqlite3
import sys
from databases import create_database, save_task_to_history


con = sqlite3.connect("users.db")
cur = con.cursor()


class Uncorrect_value(Exception):
    pass

class Unknow_error(Exception):
    pass


class Solv(QWidget, Solver): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonGet.clicked.connect(self.on_combobox_changed)
        self.pushButtonExit.clicked.connect(self.close_form)
        self.setWindowTitle("Решатель")

    def on_combobox_changed(self):
        selected_value = self.comboBox.currentText()
        self.call_function(selected_value)
      


    def call_function(self, value):
     
        if value == "Уравнять Реакцию":
            self.solve_example()
        elif value == "Вычислить молякулярную массу вещества":
            self.moll_mass()
        elif value == "массовая доля n-ого элемента в веществе":
            self.moll_mass_in()
   
        

    def solve_example(self):
        try:
            output_final = []
            input_value = self.input_value_browser.toPlainText()
            input_value = input_value.split(" ")
            reagent = []
            product = []
            reagent_ready = []
            product_ready = []

           
            for i in range(len(input_value)):
                if input_value[i] != "=":
                    reagent.append(input_value[i])
                else:
                    break
            
            
            product = set(input_value) - set(reagent)
            product = list(product)

            for i in range(len(reagent)):
                if str(reagent[i]) != "+":
                    reagent_ready.append(reagent[i])
            
            for i in range(len(product)):
                if str(product[i]) != "=":
                    product_ready.append(product[i])

           
            output_value = balance_stoichiometry(reagent_ready, product_ready)
            reagent_ready = output_value[0]
            product_ready = output_value[1]

            left_final = []
            right_final = []

          
            for key, value in reagent_ready.items():
                if value == 1: 
                    left_final.append(f"{key}")
                else:
                    left_final.append(f"{value}{key}")

            for key, value in product_ready.items():
                if value == 1:  
                    right_final.append(f"{key}")
                else:
                    right_final.append(f"{value}{key}")

        
            right_final = list(dict.fromkeys(right_final))

            output_final.append(' + '.join(left_final))
            output_final.append("=")
            output_final.append(' + '.join(right_final))
            
            self.output_value_browser.setText(' '.join(output_final)) 


            user_id = 1 
            type_of_task = "Уравнять Реакцию"
            input_text = self.input_value_browser.toPlainText()
            save_task_to_history(user_id, type_of_task, input_text)
        except Exception as e:
            self.output_value_browser.setText(f"Ошибка: {e}")


    def moll_mass(self):
        try:
            input_value = self.input_value_browser.toPlainText()
            input_value = Compound(input_value)
            self.output_value_browser.setText('%.0f' % input_value.molar_mass())
        except Exception as e:
            self.output_value_browser.setText(f"Ошибка: {e}")

    
    def moll_mass_in(self):
        try:
            input_text = self.input_value_browser.toPlainText().split(",")
            print(input_text)
            item = Compound(input_text[0])
            element = input_text[1]
            print(item, element)  
            element.lstrip()
            self.output_value_browser.setText('%.0f' % item.percentage_by_mass(element))
            

        except Exception as e:
            self.output_value_browser.setText(f"Ошибка: {e}")


    def close_form(self):
        from main_menu_logig import MainM
        self.main = MainM()
        self.main.show()
        self.close()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
