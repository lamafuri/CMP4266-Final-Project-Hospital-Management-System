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
        self.refresh_doctor_tree()
        # Buttons
        btn_frame = tk.Frame(doc_win)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Register Doctor", width=20 , command=self.register_doctor).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Update Doctor", width=20 , command=self.update_doctor).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Doctor", width=20 , command=self.delete_doctor).pack(side="left", padx=10)
    def refresh_doctor_tree(self):
        """Refresh the whole table tree"""
        all_doctor_tree_rows_id = self.doctor_tree.get_children()
        self.doctor_tree.delete(*all_doctor_tree_rows_id)
        for indx ,doc in enumerate(self.doctors , 1):
            self.doctor_tree.insert("" , "end", values=(indx , doc.full_name() , doc.get_speciality()))

    def register_doctor(self):
        reg_form = tk.Toplevel(self.root , padx=35 ,pady=15)
        reg_form.title("Register New Doctor")
        reg_form.geometry("450x350")

        reg_form.columnconfigure(0 , weight=1 , pad=15)
        reg_form.columnconfigure(1 , weight=3 , pad=15)

        reg_form.rowconfigure(list(range(10)) , weight=1 , pad=10)

        tk.Label(reg_form , text="First Name:").grid(row=0 , column=0 , sticky='e')
        fn_entry = tk.Entry(reg_form)
        fn_entry.grid(row=0 , column=1 , sticky='ew')
        tk.Label(reg_form , text="Surname:").grid(row=1 , column=0 , sticky='e')
        sur_entry = tk.Entry(reg_form)
        sur_entry.grid(row=1 , column=1 , sticky='ew')
        tk.Label(reg_form , text="Speciality:").grid(row=2 , column=0 , sticky='e')
        spec_entry = tk.Entry(reg_form)
        spec_entry.grid(row=2 , column=1 , sticky='ew')

        def save():
            first_name = fn_entry.get().strip()
            surname = sur_entry.get().strip()
            speciality = spec_entry.get().strip()

            if not all([first_name , surname , speciality]):
                messagebox.showerror("Error","All the input fields need to be filled")
                return
            for doc in self.doctors:
                if first_name == doc.get_first_name() and surname == doc.get_surname():
                    messagebox.showerror("Error" , "Doctor already exists with the given name")
                    return
            new_doctor = Doctor(first_name , surname , speciality)
            self.doctors.append(new_doctor)
            update_file(self.doctors , 'doctor.txt')
            self.refresh_doctor_tree()
            reg_form.destroy()
            messagebox.showinfo("Success","Doctor registered successfully")

        tk.Button(reg_form , text="Register",command=save , bg="#4CAF50" ,fg='white').grid(row=4 , column=0 , columnspan=2 , sticky='ew')

    def update_doctor(self):
        selected = self.doctor_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a doctor to update.")
            return
        index = int(self.doctor_tree.item(selected[0] ,'values')[0]) - 1
        doc = self.doctors[index]
        
        update_form = tk.Toplevel(self.root , padx=35 ,pady=15)
        update_form.title("Update Doctor")
        update_form.geometry("450x350")

        update_form.columnconfigure(0 , weight=1 , pad=15)
        update_form.columnconfigure(1 , weight=3 , pad=15)

        update_form.rowconfigure(list(range(10)) , weight=1 , pad=10)

        tk.Label(update_form , text="First Name:").grid(row=0 , column=0 , sticky='e')
        fn_entry = tk.Entry(update_form)
        fn_entry.insert(0 , doc.get_first_name())
        fn_entry.grid(row=0 , column=1 , sticky='ew')
        tk.Label(update_form , text="Surname:").grid(row=1 , column=0 , sticky='e')
        sur_entry = tk.Entry(update_form)
        sur_entry.insert(0 , doc.get_surname())
        sur_entry.grid(row=1 , column=1 , sticky='ew')
        tk.Label(update_form , text="Speciality:").grid(row=2 , column=0 , sticky='e')
        spec_entry = tk.Entry(update_form)
        spec_entry.insert(0 , doc.get_speciality())
        spec_entry.grid(row=2 , column=1 , sticky='ew')

        def save():
            new_fn = fn_entry.get().strip()
            new_sur = sur_entry.get().strip()
            new_spec = spec_entry.get().strip()
            if not all([new_fn , new_sur , new_spec]):
                messagebox.showerror("Error","All the input fields need to be filled")
                return
            for doc in self.doctors:
                if new_fn == doc.get_first_name() and new_sur == doc.get_surname():
                    messagebox.showerror("Error" , "Doctor already exists with the given name")
                    return
            doc.set_first_name(new_fn)
            doc.set_surname(new_sur)
            doc.set_speciality(new_spec)
            update_file(self.doctors, 'doctor.txt')
            self.refresh_doctor_tree()
            update_form.destroy()
            messagebox.showinfo("Success", "Doctor updated.")

        tk.Button(update_form , text="Update",command=save , bg="#4CAF50" ,fg='white').grid(row=4 , column=0 , columnspan=2 , sticky='ew')

    def delete_doctor(self):
        selected = self.doctor_tree.selection()
        if not selected:
            messagebox.showerror("Error","Select a doctor to delete")
            return
        selection_id = selected[0]
        index = int(self.doctor_tree.item(selection_id ,'values')[0]) - 1
        doc = self.doctors[index]
        if doc.get_patients():  # Check if the selected doctor has patients
            messagebox.showerror("Error", "Cannot delete doctor with assigned patients.")
            return
        if messagebox.askyesno("Confirm",f"Delete {doc.full_name()}?"):
            self.doctors.pop(index)
            update_file(self.doctors , 'doctor.txt')
            self.refresh_doctor_tree()
            messagebox.showinfo("Success", "Doctor deleted.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()