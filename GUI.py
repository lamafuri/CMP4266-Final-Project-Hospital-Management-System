import tkinter as tk
from tkinter import ttk, messagebox
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
from utility_functions import (
    load_doctors_data,
    load_patients_data,
    load_discharged_patients_data,
    update_file,
    update_patients_list_in_doctor
)

class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1000x650")

        # Hardcoded admin for simplicity, as in Main.py
        self.admin = Admin('admin', '123', 'B1 1AB')
        self.doctors = []
        self.patients = []
        self.grouped_patients = {}
        self.discharged_patients = []

        self.current_frame = None

        self.show_login_screen()
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, padx=20, pady=20)
        self.current_frame.pack(fill="both", expand=True)
    def show_login_screen(self):
        self.clear_frame()

        tk.Label(self.current_frame, text="Hospital Management System", font=("Helvetica", 22, "bold")).pack(pady=30)

        login_frame = tk.Frame(self.current_frame)
        login_frame.pack(pady=20)

        tk.Label(login_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="e")
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=10)

        tk.Label(login_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, sticky="e")
        self.password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12), width=25)
        self.password_entry.grid(row=1, column=1, pady=10)

        tk.Button(self.current_frame, text="Login", font=("Helvetica", 12, "bold"),
                bg="#4CAF50", fg="white", width=15,
                command=self.attempt_login).pack(pady=30)
    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            self.admin.login(username, password)  # Use modified login that takes params
            self.load_data()
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()