import tkinter as tk
from tkinter import messagebox
from database import Database


class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин - Авторизация")
        self.root.geometry("500x500")
        self.root.configure(bg="#F0F4F8")

        self.db = Database()

        self.current_user = None

        self.show_login_window()



    def show_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.login_frame = tk.Frame(self.root, bg="#FFFFFF", relief="groove", borderwidth=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=450)

        title_label = tk.Label(self.login_frame,text="Вход в систему",
                               font=("Calibri", 18, "bold"), bg="#FFFFFF",
                               fg="#333333")

        title_label.pack(pady=20)

        label_username = tk.Label(self.login_frame,text="Логин (username)",
                               font=("Calibri", 12), bg="#FFFFFF")
        label_username.pack(pady=20, anchor="w")

        self.entry_username = tk.Entry(self.login_frame, font=("Calibri", 12),width=25)
        self.entry_username.pack(padx=20, pady=5)

        button_login = tk.Button(
            self.login_frame, text="Войти", font=("Calibri", 12, "bold"), bg="#4CAF50",fg="white",
            activebackground="#45A049", command = self.login)
        button_login.pack(pady=20)
        self.entry_username.bind('<Return>', lambda event: self.login())

        button_guest = tk.Button(self.login_frame, text="Просмотр каталога (Гость)", font=("Calibri", 10), bg="#2196F3",
                                 fg="white", activebackground="#1976D2", command=self.show_catalog_window)
        button_guest.pack(pady=5)

    def login(self):
        username_input = self.entry_username.get().strip()

        if not username_input:
            messagebox.showwarning("Атэеншн!", "Пожалуйста, введите логин или юзернейм")
            return
        sql_query = ("""
        SELECT familiy,imya, otchectvo, login, rol FROM users
        WHERE login = %s
        """)

        params = (username_input,)

        user_data = self.db.fetch_one(sql_query, params)


        if user_data:
            self.current_user = user_data
            messagebox.showinfo("Урааа!", f"Добро пожаловать, {self.current_user['imya']}!")

            #self.show_main_window()
            self.show_catalog_window()
            print("Переход в главное окно...")
        else:
            messagebox.showerror("Ошибка входа", "неверный логин или аккаунт неактивен \nПроверьте правильность данных")
            self.entry_username.delete(0, tk.END)
            self.entry_username.focus()

    def logout(self):
        self.current_user = None
        self.show_login_window()

    def show_catalog_window (self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Каталог товаров")
        self.root.geometry("850x600")

        sql_query = (""" SELECT kategoria, podkategoria, img, tavar, proisvotctvo, opisanie, coctav, zena FROM products
        """)
        products_data = self.db.fetch_all(sql_query)
        header_frame = tk.Frame(self.root, bg="#FFFFFF", relief="solid", bd=1)
        header_frame.pack(fill="x", pady=10, padx=10)
        if self.current_user:
            user_info = f"👤 {self.current_user['login']} |имя  {self.current_user['imya']} "
        else:
            user_info = "👤 Вы вошли как гость. Для покупок нужна авторизация."
        tk.Label(header_frame, text=user_info, font=("Calibri", 12, "bold"), bg="#FFFFFF", fg="#333").pack(side="left",
                                                                                                           padx=10,
                                                                                                           pady=10)
        btn_logout = tk.Button(header_frame, text="Выйти / Авторизоваться", bg="#f44336", fg="white",
                               command=self.logout)
        btn_logout.pack(side="right", padx=10)
        catalog_frame = tk.Frame(self.root, bg="#D2F6E7")
        catalog_frame.pack(fill="both", expand=True, padx=10, pady=10)
        if not products_data:
            tk.Label(catalog_frame, text="Каталог пуст или таблица 'products' не найдена", font=("Calibri", 14),
                     bg="#F0F4F8").pack(pady=50)
            return
        max_columns = 3
        for index, product in enumerate(products_data):
            row = index // max_columns
            column = index % max_columns
            card = tk.Frame(catalog_frame, bd=1, relief="solid", bg="white")
            card.grid(row=row, column=column, padx=10, pady=10,
                  sticky="nsew")
            title_text = product.get("tavar", "Неизвестный товар")
            desc_text = product.get("opisanie", "")
            price_text = f"{product.get('zena', 0)} ₽"
            tk.Label(card, text=title_text, font=("Arial", 12, "bold"), bg="white", wraplength=200).pack(pady=(10, 5))
            tk.Label(card, text=desc_text, font=("Arial", 10), bg="white", fg="#666", wraplength=200).pack(pady=5)
            tk.Label(card, text=price_text, font=("Arial", 13, "bold"), bg="white", fg="#2c3e50").pack(pady=(5, 15))

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopApp(root)
    root.mainloop()
