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

    def load_data(self):
        self.doctors = load_doctors_data()
        self.patients, self.grouped_patients = load_patients_data()
        self.discharged_patients = load_discharged_patients_data()

        doctor_by_name = {doctor.full_name(): doctor for doctor in self.doctors}
        update_patients_list_in_doctor(doctor_by_name, self.patients)

    def show_main_menu(self):
        self.clear_frame()

        tk.Label(self.current_frame, text=f"Welcome, {self.admin.get_username()}", font=("Helvetica", 18, "bold")).pack(pady=15)

        btn_style = {"font": ("Helvetica", 12), "width": 35, "pady": 10}

        tk.Button(self.current_frame, text="1. Doctor Management", **btn_style,command=self.open_doctor_management).pack(pady=8)
        tk.Button(self.current_frame, text="2. Patient Management", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="3. View Discharged Patients", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="4. Assign Doctor to Patient", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="5. Reallocate Doctor to Patient", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="6. View Management Reports", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="7. Update Admin Details", **btn_style).pack(pady=8)
        tk.Button(self.current_frame, text="8. Quit", bg="#f44336", fg="white",font=("Helvetica", 12, "bold"), width=35, pady=10).pack(pady=30)

    # Doctor Management Starts Here
    def open_doctor_management(self):
        doc_win = tk.Toplevel(self.root)
        doc_win.title("Doctor Management")
        doc_win.geometry("900x600")

        tk.Label(doc_win, text="Doctor Management", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview for doctors
        columns = ("ID", "Full Name", "Speciality")
        self.doctor_tree = ttk.Treeview(doc_win, columns=columns, show="headings", height=15)
        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Full Name", text="Full Name")
        self.doctor_tree.heading("Speciality", text="Speciality")
        self.doctor_tree.column("ID", width=50, anchor="center")
        self.doctor_tree.column("Full Name", width=300)
        self.doctor_tree.column("Speciality", width=250)
        self.doctor_tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(doc_win)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Register Doctor", width=20).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Update Doctor", width=20).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Doctor", width=20).pack(side="left", padx=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()