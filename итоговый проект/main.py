import tkinter as tk
from tkinter import ttk
import sqlite3

# Создание класса MainApp, который представляет главное окно приложения
class MainApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()  # Инициализация главного окна
        self.db = Database()  # Инициализация объекта базы данных
        self.view_records()  # Отображение записей из базы данных

    # Инициализация главного окна
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)  # Создание панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)  # Размещение панели инструментов в верхней части окна

        # Загрузка изображений для кнопок
        self.img_add = tk.PhotoImage(file="C:\\Users\\Complife\\Desktop\\итоговый проект\\image\\add.png")
        btn_add = tk.Button(toolbar, text="Добавить", bg="#d7d7d7",
                            bd=0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)  # Размещение кнопки "Добавить" на панели инструментов

        self.img_upd = tk.PhotoImage(file="C:\\Users\\Complife\\Desktop\\итоговый проект\\image\\change.png")
        btn_upd = tk.Button(toolbar, bg="#d7d7d7",
                            bd=0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)  # Размещение кнопки "Изменить" на панели инструментов

        self.img_search = tk.PhotoImage(file="C:\\Users\\Complife\\Desktop\\итоговый проект\\image\\search.png")
        btn_search = tk.Button(toolbar, bg="#d7d7d7",
                               bd=0, image=self.img_search,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)  # Размещение кнопки "Поиск" на панели инструментов

        self.img_refresh = tk.PhotoImage(file="C:\\Users\\Complife\\Desktop\\итоговый проект\\image\\refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#d7d7d7",
                                bd=0, image=self.img_refresh,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)  # Размещение кнопки "Обновить" на панели инструментов

        # Создание виджета Treeview для отображения записей
        self.tree = ttk.Treeview(root,
                                 columns=("id", "name", "phone", "email", "earn"),
                                 height=45,
                                 show="headings")

        # Настройка столбцов и заголовков столбцов
        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("name", width=200, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("earn", width=150, anchor=tk.CENTER)

        self.tree.heading("id", text="id")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Электронная-Почта")
        self.tree.heading("earn", text="Зароботная плата")

        self.tree.pack(side=tk.LEFT)  # Размещение виджета Treeview в окне

        # Создание полосы прокрутки для Treeview
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод для отображения записей из базы данных в виджете Treeview
    def view_records(self):
        self.db.cur.execute("SELECT * FROM users")  # Выбор всех записей из таблицы users
        records = self.db.cur.fetchall()  # Получение всех записей
        self.update_treeview(records)  # Обновление виджета Treeview

    # Метод для обновления виджета Treeview с новыми данными
    def update_treeview(self, records):
        self.tree.delete(*self.tree.get_children())  # Очистка всех строк в Treeview
        for record in records:
            self.tree.insert("", "end", values=record)  # Вставка записи в виджет Treeview

    # Метод для открытия дочернего окна добавления записи
    def open_child(self):
        ChildWindow(self, self.db)

    # Метод для открытия дочернего окна изменения записи
    def open_update_child(self):
        selected_item = self.tree.selection()  # Получение выбранной записи
        if selected_item:
            id = self.tree.item(selected_item)['values'][0]  # Получение ID выбранной записи
            UpdateWindow(self, self.db, id)

    # Метод для открытия дочернего окна поиска
    def open_search(self):
        SearchWindow(self, self.db)

class ChildWindow(tk.Toplevel):      #класс создания окна для добавления сотрудника
    def __init__(self, main_app, db):
        super().__init__(main_app)
        self.main_app = main_app
        self.db = db
        self.title("Добавление контакта")
        self.geometry("400x200")
        self.resizable(False, False)

        label_name = tk.Label(self, text="ФИО")    #метки и поля ввода для ФИО телевона электронной почты и зарплаты сотрудника
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text="E-mail")
        label_email.place(x=50, y=110)
        label_earn = tk.Label(self, text="ЗП")
        label_earn.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_earn = tk.Entry(self)
        self.entry_earn.place(x=200, y=140)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy) #кнопка закрыть окно
        btn_cancel.place(x=200, y=170)

        btn_add = tk.Button(self, text="Добавить", command=self.add_record) #кнопка инициализирующая функцию добавить
        btn_add.place(x=265, y=170)

    def add_record(self):           #метод добавления новой записи
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get() 
        earn = self.entry_earn.get()
        self.db.insert_data(name, phone, email, earn)
        self.main_app.view_records()
        self.destroy()

class UpdateWindow(ChildWindow):      #класс для изменения контакта
    def __init__(self, main_app, db, id):
        super().__init__(main_app, db)
        self.title("Изменение контакта")
        self.record_id = id
        self.default_data()

    def default_data(self):
        record = self.db.get_record(self.record_id)
        self.entry_name.insert(0, record[1])
        self.entry_phone.insert(0, record[2])
        self.entry_email.insert(0, record[3])
        self.entry_earn.insert(0, record[4])

    def add_record(self):              #аналогичный add_record только изменяет контакты
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        earn = self.entry_earn.get()
        self.db.update_record(self.record_id, name, phone, email, earn)
        self.main_app.view_records()
        self.destroy()

class SearchWindow(tk.Toplevel):    #класс окна для поиска контактов
    def __init__(self, main_app, db):
        super().__init__(main_app)
        self.main_app = main_app
        self.db = db
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        label_name = tk.Label(self, text="ФИО")   #метка ФИО
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)         #поле для ввода
        self.entry_name.place(x=130, y=30)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)    #кнопка закрыть 
        btn_cancel.place(x=150, y=70)

        btn_search = tk.Button(self, text="Найти", command=self.search_record)  #кнопка найти
        btn_search.place(x=225, y=70)

    def search_record(self):            #метод поиска записей
        name = self.entry_name.get()
        records = self.db.search_records(name)
        self.main_app.update_treeview(records)

class Database:             #класс базы данных
    def __init__(self):
        self.conn = sqlite3.connect("contacts.db")         #указываем файл для хранения базы данных
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, earn TEXT)') #создаем таблицу users
        self.conn.commit()

    def insert_data(self, name, phone, email, earn):
        self.cur.execute('INSERT INTO users (name, phone, email, earn) VALUES (?, ?, ?, ?);', (name, phone, email, earn))           #добовляет новую запись в таблицу
        self.conn.commit()
            
    def update_record(self, id, name, phone, email, earn):
        self.cur.execute('UPDATE users SET name = ?, phone = ?, email = ?, earn = ? WHERE id = ?', (name, phone, email, earn, id))  #обновляет существующую запись
        self.conn.commit()

    def search_records(self, name):                                                         #метод получения данных из базы данных
        self.cur.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
        return self.cur.fetchall()

    def search_records(self, name):                                                         #метод поиска данных
        self.cur.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
        return self.cur.fetchall()

if __name__ == "__main__":              #создается экземпляр базы данных db и главное приложение. Создается основное окно и запускается цикл обработки событий
    root = tk.Tk()
    db = Database()
    app = MainApp(root)
    root.title("Список сотрудников")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()