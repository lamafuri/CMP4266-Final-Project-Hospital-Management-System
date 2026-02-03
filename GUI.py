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

        # Hardcoded admin 
        self.admin = Admin.load_admin_data()
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

        tk.Button(self.current_frame, text="1. Doctor Management", **btn_style,command=self.open_doctor_management).pack(pady=5)
        tk.Button(self.current_frame, text="2. Patient Management", **btn_style , command=self.open_patient_management).pack(pady=5)
        tk.Button(self.current_frame, text="3. View Discharged Patients", **btn_style , command=self.view_discharged_patients).pack(pady=5)
        tk.Button(self.current_frame, text="4. Assign Doctor to Patient", **btn_style , command=self.open_assign_doctor).pack(pady=5)
        tk.Button(self.current_frame, text="5. Reallocate Doctor to Patient", **btn_style ,command=self.open_reallocate_doctor).pack(pady=5)
        tk.Button(self.current_frame, text="6. View Management Reports", **btn_style , command=self.open_management_reports).pack(pady=8)
        tk.Button(self.current_frame, text="7. Update Admin Details", **btn_style ,command=self.open_update_admin).pack(pady=5)
        tk.Button(self.current_frame, text="8. View Patient Grouped by Family", **btn_style ,command=self.view_pateints_grouped_by_family).pack(pady=5)
        tk.Button(self.current_frame, text="9. Quit", bg="#f44336", fg="white",font=("Helvetica", 12, "bold"), command=self.quit_application, width=35, pady=10).pack(pady=10)

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
        
    # Patient Management Start Here
    def open_patient_management(self):
        pat_win = tk.Toplevel(self.root)
        pat_win.title("Patient Management")
        pat_win.geometry("900x600")

        tk.Label(pat_win, text="Patient Management", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview for patients (used in View & Discharge)
        columns = ("ID", "Full Name", "Doctor", "Age", "Mobile", "Postcode")
        self.patient_tree = ttk.Treeview(pat_win, columns=columns, show="headings", height=15)
        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col,anchor="center")
        
        self.patient_tree.column("ID", width=50)
        self.patient_tree.column("Full Name", width=220)
        self.patient_tree.column("Doctor", width=180)
        self.patient_tree.column("Age", width=60)
        self.patient_tree.column("Mobile", width=120)
        self.patient_tree.column("Postcode", width=100)
        
        self.patient_tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.refresh_patient_tree()

        # Buttons
        btn_frame = tk.Frame(pat_win)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Admit New Patient", width=20, command=self.admit_patient).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Discharge Selected",width=20, command=self.perform_discharge,bg="#f44336", fg="white").pack(side="left" ,padx=10)

    def refresh_patient_tree(self):
        """Clear and repopulate patient treeview"""
        self.patient_tree.delete(*self.patient_tree.get_children())
        for idx, pat in enumerate(self.patients, 1):
            self.patient_tree.insert("", "end",values=(idx, pat.full_name(), pat.get_doctor(), pat.age,pat.mobile, pat.postcode))


    def admit_patient(self):
        adm_win = tk.Toplevel(self.root , padx=30 , pady=20)
        adm_win.title("Admit New Patient")
        adm_win.geometry("450x380")

        adm_win.columnconfigure(0, weight=1, pad=15)
        adm_win.columnconfigure(1, weight=3, pad=15)
        adm_win.rowconfigure(list(range(8)) , weight=1 , pad=8)

        tk.Label(adm_win, text="First Name:").grid(row=0, column=0, sticky='e')
        fn_entry = tk.Entry(adm_win)
        fn_entry.grid(row=0, column=1, sticky='ew')

        tk.Label(adm_win, text="Surname:").grid(row=1, column=0, sticky='e')
        sn_entry = tk.Entry(adm_win)
        sn_entry.grid(row=1, column=1, sticky='ew')

        tk.Label(adm_win, text="Age:").grid(row=2, column=0, sticky='e')
        age_entry = tk.Entry(adm_win)
        age_entry.grid(row=2, column=1, sticky='ew')

        tk.Label(adm_win, text="Mobile:").grid(row=3, column=0, sticky='e')
        mob_entry = tk.Entry(adm_win)
        mob_entry.grid(row=3, column=1, sticky='ew')

        tk.Label(adm_win, text="Postcode:").grid(row=4, column=0, sticky='e')
        pc_entry = tk.Entry(adm_win)
        pc_entry.grid(row=4, column=1, sticky='ew')

        def save():
            try:
                first_name = fn_entry.get().strip()
                surname    = sn_entry.get().strip()
                age        = int(age_entry.get().strip())
                mobile     = mob_entry.get().strip()
                postcode   = pc_entry.get().strip()

                if not all([first_name, surname, mobile, postcode]):
                    raise ValueError("Please fill all fields correctly.")
                if age <=0:
                    raise ValueError("Age must be positive.")

                new_pat = Patient(first_name, surname, age, mobile, postcode)
                self.patients.append(new_pat)
                self.grouped_patients.setdefault(surname, []).append(new_pat)
                update_file(self.patients, 'patient.txt')
                self.refresh_patient_tree()          # update main tree if visible
                adm_win.destroy()
                messagebox.showinfo("Success", "Patient admitted successfully.")
            except ValueError as e:
                messagebox.showerror("Input Error", e)

        tk.Button(adm_win, text="Admit", command=save,bg="#4CAF50", fg='white').grid(row=6, column=0, columnspan=2, sticky='ew', pady=10)

    def perform_discharge(self):
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a patient to discharge.")
            return
        
        index = int(self.patient_tree.item(selected[0] , 'values')[0]) - 1
        pat = self.patients[index]

        if messagebox.askyesno("Confirm Discharge", f"Discharge {pat.full_name()}?"):
            # Remove from doctor's list if assigned
            doc_name = pat.get_doctor()
            if doc_name != 'None':
                for doc in self.doctors:
                    if doc.full_name() == doc_name:
                        doc.remove_patient(pat)
                        break

            discharged = self.patients.pop(index)
            self.discharged_patients.append(discharged)
            update_file(self.patients, 'patient.txt')
            update_file(self.discharged_patients, 'discharged_patient.txt')
            
            # Refresh both trees if they exist
            self.refresh_patient_tree()       
            messagebox.showinfo("Success", "Patient discharged successfully.")

    # View Discharged Patients
    def view_discharged_patients(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("Discharged Patients")
        view_win.geometry("1000x600")

        columns = ("ID", "Full Name", "Doctor", "Age", "Mobile", "Postcode")
        tree = ttk.Treeview(view_win, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        for i, pat in enumerate(self.discharged_patients, 1):
            tree.insert("", "end", values=(i, pat.full_name(), pat.get_doctor(), pat.age, pat.mobile, pat.postcode))
        tree.pack(pady=10, padx=20, fill="both", expand=True)

    # Assign Doctor
    def open_assign_doctor(self):
        ass_win = tk.Toplevel(self.root)
        ass_win.title("Assign Doctor to Patient")
        ass_win.geometry("1200x600")

        # Patients without doctor
        tk.Label(ass_win, text="Unassigned Patients",font=("Helvetica", 18, "bold")).grid(row=0, column=0, padx=20 , pady=18)
        pat_columns = ("ID", "Full Name")
        self.unassigned_tree = ttk.Treeview(ass_win, columns=pat_columns, show="headings", height=20)
        self.unassigned_tree.heading("ID",text="ID")
        self.unassigned_tree.heading("Full Name",text="Full Name")
        self.unassigned_tree.column("ID",width=100 , anchor='center')
        self.unassigned_tree.column("Full Name",width=250)
        self.refresh_unassigned_tree()
        self.unassigned_tree.grid(row=1, column=0, padx=20)

        # Doctors
        tk.Label(ass_win, text="Doctors" ,font=("Helvetica", 18, "bold")).grid(row=0, column=1, padx=20 , pady=18)
        doc_columns = ("ID", "Full Name", "Speciality")
        self.doc_tree_ass = ttk.Treeview(ass_win, columns=doc_columns, show="headings", height=20)
        self.doc_tree_ass.column("ID" , width=100 , anchor='center')
        self.doc_tree_ass.column("Full Name" , width=250)
        self.doc_tree_ass.column("Speciality" , width=250)
        for col in doc_columns:
            self.doc_tree_ass.heading(col, text=col)
        self.refresh_doc_tree_ass()
        self.doc_tree_ass.grid(row=1, column=1, padx=20)

        tk.Button(ass_win, text="Assign Selected", command=self.perform_assign , bg="#4CAF50" ,fg='white').grid(row=2, column=0, columnspan=2, pady=20)

    def refresh_unassigned_tree(self):
        self.unassigned_tree.delete(*self.unassigned_tree.get_children())
        unassigned = [p for p in self.patients if p.get_doctor() == 'None']
        for i, pat in enumerate(unassigned, 1):
            self.unassigned_tree.insert("", "end", values=(i, pat.full_name()))

    def refresh_doc_tree_ass(self):
        self.doc_tree_ass.delete(*self.doc_tree_ass.get_children())
        for i, doc in enumerate(self.doctors, 1):
            self.doc_tree_ass.insert("", "end", values=(i, doc.full_name(), doc.get_speciality()))

    def perform_assign(self):
        pat_sel = self.unassigned_tree.selection()
        doc_sel = self.doc_tree_ass.selection()
        if not pat_sel:
            messagebox.showwarning("Selection Error", "Select a patient by clicking it.")
            return
        if not doc_sel:
            messagebox.showwarning("Selection Error", "Select a doctor by clicking it.")
            return

        pat_index = int(self.unassigned_tree.item(pat_sel[0] , 'values')[0]) - 1
        unassigned = [p for p in self.patients if p.get_doctor() == 'None']
        pat = unassigned[pat_index]
        doc_index = int(self.doc_tree_ass.item(doc_sel[0], 'values')[0]) - 1
        doc = self.doctors[doc_index]
        pat.link(doc.full_name())
        doc.add_patient(pat)
        update_file(self.patients, 'patient.txt')
        self.refresh_unassigned_tree()
        messagebox.showinfo("Success", "Doctor assigned.")

    # Reallocate Doctor (similar to assign but for assigned patients)
    def open_reallocate_doctor(self):
        rea_win = tk.Toplevel(self.root)
        rea_win.title("Reallocate Doctor to Patient")
        rea_win.geometry("1200x600")

        # Assigned patients
        tk.Label(rea_win, text="Assigned Patients",font=("Helvetica", 18, "bold")).grid(row=0, column=0, padx=20 , pady=18)
        pat_columns = ("ID", "Full Name", "Current Doctor")
        self.assigned_tree = ttk.Treeview(rea_win, columns=pat_columns, show="headings", height=20)
        self.assigned_tree.column("ID",width=70 , anchor="center")
        self.assigned_tree.column("Full Name",width=200)
        self.assigned_tree.column("Current Doctor",width=200)
        for col in pat_columns:
            self.assigned_tree.heading(col, text=col)
        self.refresh_assigned_tree()
        self.assigned_tree.grid(row=1, column=0, padx=20)

        # Doctors
        tk.Label(rea_win, text="Doctors",font=("Helvetica", 18, "bold")).grid(row=0, column=1, padx=20 , pady=18)
        doc_columns = ("ID", "Full Name", "Speciality")
        self.doc_tree_rea = ttk.Treeview(rea_win, columns=doc_columns, show="headings", height=20)
        self.doc_tree_rea.column("ID",width=50 , anchor="center")
        self.doc_tree_rea.column("Full Name",width=200)
        self.doc_tree_rea.column("Speciality",width=200)
        for col in doc_columns:
            self.doc_tree_rea.heading(col, text=col)
        self.refresh_doc_tree_rea()
        self.doc_tree_rea.grid(row=1, column=1, padx=20)

        tk.Button(rea_win, text="Reallocate Selected", command=self.perform_reallocate ,bg="#4CAF50" ,fg='white').grid(row=2, column=0, columnspan=2, pady=20)

    def refresh_assigned_tree(self):
        self.assigned_tree.delete(*self.assigned_tree.get_children())
        assigned = [p for p in self.patients if p.get_doctor() != 'None']
        for i, pat in enumerate(assigned, 1):
            self.assigned_tree.insert("", "end", values=(i, pat.full_name(), pat.get_doctor()))

    def refresh_doc_tree_rea(self):
        self.doc_tree_rea.delete(*self.doc_tree_rea.get_children())
        for i, doc in enumerate(self.doctors, 1):
            self.doc_tree_rea.insert("", "end", values=(i, doc.full_name(), doc.get_speciality()))

    def perform_reallocate(self):
        pat_sel = self.assigned_tree.selection()
        doc_sel = self.doc_tree_rea.selection()
        if not pat_sel:
            messagebox.showwarning("Selection Error", "Select a patient by clicking on it.")
            return
        if not doc_sel:
            messagebox.showwarning("Selection Error", "Select a new doctor by clicking on it.")
            return
        pat_index = int(self.assigned_tree.item(pat_sel[0] , 'values')[0]) - 1
        assigned = [p for p in self.patients if p.get_doctor() != 'None']
        pat = assigned[pat_index]
        old_doc_name = pat.get_doctor()
        doc_index = int(self.doc_tree_rea.item(doc_sel[0])['values'][0]) - 1
        new_doc = self.doctors[doc_index]
        if old_doc_name == new_doc.full_name():
            messagebox.showwarning("Error", "Same doctor selected.")
            return
        # Remove from old doctor
        for doc in self.doctors:
            if doc.full_name() == old_doc_name:
                doc.remove_patient(pat)
                break
        # Assign to new
        pat.link(new_doc.full_name())
        new_doc.add_patient(pat)
        update_file(self.patients, 'patient.txt')
        self.refresh_assigned_tree()
        messagebox.showinfo("Success", "Doctor reallocated.")

    # Management Reports
    def open_management_reports(self):
        rep_win = tk.Toplevel(self.root)
        rep_win.title("Management Reports")
        rep_win.geometry("600x500")

        tk.Label(rep_win, text="Management Reports", font=("Helvetica", 16, "bold")).pack(pady=10)

        btn_style = {"font": ("Helvetica", 12), "width": 40, "pady": 10}

        tk.Button(rep_win, text="1. Total Number of Doctors", **btn_style,command=lambda: messagebox.showinfo("Report", f"Total Doctors: {len(self.doctors)}")).pack(pady=8)

        tk.Button(rep_win, text="2. Total Patients per Doctor", **btn_style,command=self.show_patients_per_doctor).pack(pady=8)

        tk.Button(rep_win, text="3. Total Appointments per Doctor", **btn_style,command=lambda: messagebox.showinfo("Report", "Appointments not implemented yet.")).pack(pady=8)

        tk.Button(rep_win, text="4. Patients by Illness Type", **btn_style,command=lambda: messagebox.showinfo("Report", "Illness types not implemented yet.")).pack(pady=8)

    def show_patients_per_doctor(self):
        text = "Patients per Doctor:\n\n"
        for doc in self.doctors:
            text += f"{doc.full_name()}: {len(doc.get_patients())} patients\n"
        messagebox.showinfo("Report", text)
    
    # Update Admin Details
    def open_update_admin(self):
        upd_win = tk.Toplevel(self.root)
        upd_win.title("Update Admin Details")
        upd_win.geometry("450x400")

        tk.Label(upd_win, text="Username:").pack(pady=5)
        un_entry = tk.Entry(upd_win, width=35)
        un_entry.insert(0, self.admin.get_username())
        un_entry.pack()

        tk.Label(upd_win, text="Password:").pack(pady=5)
        pw_entry = tk.Entry(upd_win, show="*", width=35)
        pw_entry.pack()

        tk.Label(upd_win, text="Confirm Password:").pack(pady=5)
        cpw_entry = tk.Entry(upd_win, show="*", width=35)
        cpw_entry.pack()

        tk.Label(upd_win, text="Address:").pack(pady=5)
        addr_entry = tk.Entry(upd_win, width=35)
        addr_entry.insert(0, self.admin.get_address())
        addr_entry.pack()

        def save():
            new_un = un_entry.get().strip()
            new_pw = pw_entry.get().strip()
            conf_pw = cpw_entry.get().strip()
            new_addr = addr_entry.get().strip()

            if new_un:
                self.admin.set_username(new_un)
            if new_pw:
                if new_pw != conf_pw:
                    messagebox.showerror("Error", "Passwords do not match.")
                    return
                self.admin.set_password(new_pw)
            if new_addr:
                self.admin.set_address(new_addr)
            self.admin.update_admin_file()
            upd_win.destroy()
            messagebox.showinfo("Success", "Admin details updated.")

        tk.Button(upd_win, text="Update", command=save).pack(pady=20)

    def view_pateints_grouped_by_family(self):
        fam_win = tk.Toplevel(self.root)
        fam_win.title("Patients Grouped by Family")
        fam_win.geometry("1000x600")
        tk.Label(fam_win,text="Patients Grouped by Family (Surname)",font=("Helvetica", 16, "bold"),pady=10).pack()

        # ── Add scrollable container ──
        canvas = tk.Canvas(fam_win)
        scrollbar = ttk.Scrollbar(fam_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        sorted_surnames = sorted(self.grouped_patients.keys())
        columns = ('ID','Full Name','Age','Doctor','Mobile','Postcode')

        for surname in sorted_surnames:
            family = self.grouped_patients[surname]
            if not family:
                continue
            tk.Label(scrollable_frame,text=f"Family: {surname.upper()} ({len(family)} member{'s' if len(family)>1 else ''})",font=("Helvetica", 12, "bold"),anchor="w",padx=20).pack(fill="x", pady=(15, 5))
            self.family_tree = ttk.Treeview(scrollable_frame , columns=columns , show='headings' , height=len(family))
            for col in columns:
                self.family_tree.heading(col , text=col)
                self.family_tree.column(col ,anchor="center")
            
            self.family_tree.column('ID' , width=50)
            self.family_tree.column('Full Name' , width=150)
            self.family_tree.column('Age' , width=50)
            self.family_tree.column('Doctor' , width=150)
            self.family_tree.column('Mobile' , width=150)
            self.family_tree.column('Postcode' , width=150)
            
            self.load_family_tree(family)
            self.family_tree.pack(pady=20, padx=20, fill="x")   # changed to fill="x" so it doesn't force expand vertically
    def load_family_tree(self , family):
        for idx , pat in enumerate(family , 1):
            self.family_tree.insert("","end",values=(idx , pat.full_name() ,pat.age ,pat.get_doctor() , pat.mobile , pat.postcode))
    # Quit
    def quit_application(self):
        """Properly close the application"""
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?"):
            self.root.quit()          # Stops the mainloop
            self.root.destroy()       # Destroys the window and frees resources
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()