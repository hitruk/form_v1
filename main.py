import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
import re
from config import load_config

class Model:
    params = load_config()
    
    def __init__(self):#, value):
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

        #self._value = value

    # @property
    # def value(self):
    #    self._value = value
 
    # @value.setter
    # def value(self, value):
    #    if type(value) in [str]:
    #        self._value = value
    #    else:
    #        raise TypeError(f'Invalid data type {type(value)}')

    def _open_conn(self):
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()
        return self.cur # обязательно сделать return 
        

    def _close_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def version_query(self):
        sql = ''' select version() '''
        try:
            #self.cur = self._open_conn()
            
            #self.conn = psycopg2.connect(**self.params)
            #self.cur = self.conn.cursor()
            self.cur.execute(sql)
            res = self.cur.fetchone()
            print(res)
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self._close_conn()

    def add_query(self, text):
        sql = ''' INSERT INTO user_name(name) VALUES(%s) '''
        try:
            self.cur = self._open_conn()
            self.cur.execute(sql, (text,))
            self.conn.commit()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self._close_conn()

    def delete_query(self, text):
        sql = ''' DELETE FROM user_name WHERE name= %s '''
        try:
            self.cur = self._open_conn()
            self.cur.execute(sql, (text,))
            self.conn.commit()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.conn.close()

    def select_query(self):
        sql = ''' SELECT name FROM user_name '''

        try:
            self.cur = self._open_conn()
            self.cur.execute(sql)
            res = self.cur.fetchall()
            self.cur.close()
            return res
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.conn.close()

class Frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self['borderwidth'] = 1
        self['relief'] = SOLID
        self['height'] = 100
        self.pack(padx=2, pady=2, fill=BOTH)#, expand=True)

        # contant
        options = {'padx':2, 'pady':2} # , 'anchor':W}
        self.label_title = ttk.Label(self, text='Введите имя')
        self.label_title.grid(**options, column=0, row=0, sticky=W)

        # ENTRY
        self.entry_type = tk.StringVar()
        vcmd = (self.register(self.validate), '%P')
        self.entry = ttk.Entry(self, textvariable=self.entry_type)
        self.entry.config(validate='key', validatecommand=vcmd)
        self.entry.grid(**options, column=0, row=1)
        
        # ADD
        self.add = ttk.Button(self, text='add', command=self.click_add)
        # self.add.pack(**options)
        self.add.grid(column=1, row=1, padx=2, pady=2)

        # UPDATE
        self.update = ttk.Button(self, text='update')
        self.update.grid(column=2, row=1, padx=2, pady=2)

        self.label_result = ttk.Label(self, text='Result:')
        self.label_result.grid(**options, column=0, row=2, sticky=W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def click_add(self):
        if self.controller:
            try:
                value = str(self.entry.get())
                # временное решение!!!
                if value == '':
                    return 
                self.controller.add_value(value)
                self.entry.delete(0, END)
            except ValueError as error:
                print(f'Invalid value: {value} Type value: {type(value)}')


    # /* Validate Blok
    def validate(self, value):
        '''
        Validate item entry
        '''
        if re.search(r'[^A-Za-z]', value):
            return False
        return True
    # */

class FrameOne(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self['borderwidth'] = 1
        self['relief'] = SOLID
        self['height'] = 200
        self.pack(padx=2, pady=2, fill=BOTH, expand=True)

        # contant
        options = {}
 
        # LABEL
        self.label_d = ttk.Label(self, text='Выбрать значение для удаления')
        self.label_d.pack(padx=2, pady=2, anchor=W)
       
        # DELETE
        self.delete = ttk.Button(self, text='delete', command=self.click_delete)
        self.delete.pack(padx=2, pady=2, anchor=W)

        # LISTBOX
        self.listbox = tk.Listbox(
                self, 
                # listvariable=self.list_items, 
                height=3,
                selectmode=tk.SINGLE
        )
        self.listbox.pack(expand=True, fill=BOTH, side=LEFT, padx=2, pady=1)

        # SCROLLBAR
        self.scrollbar = ttk.Scrollbar(
                self.listbox, 
                orient=VERTICAL, 
                command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        # controller
        self.controller = None
    
    def load_list(self, list_data):
        var = tk.Variable(value=list_data)
        self.listbox['listvariable'] = var

    def set_controller(self, controller):
        self.controller = controller

    def click_delete(self):
        if self.controller:
            try:
                # получить все элементы из списка listbox
                print(f'all elements: {self.listbox.get(0, END)}')
                # получить значение выбранного элемента
                print(f'index element: {self.listbox.curselection()}')
                # получить значение по индексу
                index_element = self.listbox.curselection()
                if len(index_element) == 1:
                    print(f'element: {self.listbox.get(index_element)}')
                    value = self.listbox.get(index_element)[0]
                    self.controller.delete_value(value)
                else:
                    return
                if index_element == '':
                    return
            except ValueError as error:
                print(f'Invalid value: {value} Type value: {type(value)}')

    def click_update(self):
        pass

class Controller:
    def __init__(self, model, view, view_one):
        self.model = model
        self.view = view
        self.view_one = view_one

        # загрузить список в listbox
        self.view_one.load_list(model.select_query())
        
    def add_value(self, value):
        self.model.add_query(value)
        self.view_one.load_list(self.model.select_query())

    def delete_value(self, value):
        self.model.delete_query(value)
        self.view_one.load_list(self.model.select_query())

    def update_value(self, value):
        #self.model.update_query(value)
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('hello world!')
        self.geometry('500x300')

        model = Model()
        view = Frame(self)
        view_one = FrameOne(self)

        controller = Controller(model, view, view_one)

        view.set_controller(controller)
        view_one.set_controller(controller)

if __name__ == '__main__':
    app = App()
    app.mainloop()
