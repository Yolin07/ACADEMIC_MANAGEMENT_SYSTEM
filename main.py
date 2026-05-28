import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class AcademicManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Management System v8 - Persistent Edition")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f5f6fa')

        self.db_file = "academic_data_v8.json"
        self.auth_file = "teacher_auth.json"
        
        self.current_teacher = None
        self.current_folder = None 
        self.current_level = None 

        self.load_initial_data()
        self.main_container = tk.Frame(self.root, bg='#f5f6fa')
        self.main_container.pack(fill="both", expand=True)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_welcome_screen()

    def load_initial_data(self):
        try:
            with open(self.auth_file, 'r') as f:
                self.accounts = json.load(f)
            if not isinstance(self.accounts, dict):
                self.accounts = {}
        except Exception:
            self.accounts = {}
        
        try:
            with open(self.db_file, 'r') as f:
                self.database = json.load(f)
            if not isinstance(self.database, dict):
                self.database = {}
        except Exception:
            self.database = {}

    def save_all_data(self):
        try:
            with open(self.auth_file, 'w') as f:
                json.dump(self.accounts, f, indent=4)
            with open(self.db_file, 'w') as f:
                json.dump(self.database, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data to files:\n{e}")

    def manual_save(self):
        self.save_all_data()
        messagebox.showinfo("System", "Database updated and saved successfully!")

    def exit_system(self):
        if self.current_teacher:
            self.save_all_data()
        self.show_goodbye_screen()

    def clear_view(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def on_closing(self):
        if self.current_teacher:
            self.save_all_data()
        self.root.destroy()

    def show_welcome_screen(self):
        if self.current_teacher:
            self.save_all_data()
            self.current_teacher = None
        self.clear_view()
        
        frame = tk.Frame(self.main_container, bg='#f5f6fa')
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="WELCOME TO THE", font=("Segoe UI", 16), bg='#f5f6fa', fg='#7f8c8d').pack()
        tk.Label(frame, text="ACADEMIC RECORD MANAGEMENT SYSTEM", font=("Segoe UI", 28, "bold"), bg='#f5f6fa', fg='#2c3e50').pack(pady=(0, 40))
        
        btns_top = tk.Frame(frame, bg='#f5f6fa')
        btns_top.pack()
        
        tk.Button(btns_top, text="LOGIN", command=lambda: self.show_auth_form("LOGIN"), bg='#1877f2', fg='white', font=("Segoe UI", 12, "bold"), width=15, height=2, bd=0).pack(side="left", padx=10)
        tk.Button(btns_top, text="REGISTER", command=lambda: self.show_auth_form("REGISTER"), bg='#2ecc71', fg='white', font=("Segoe UI", 12, "bold"), width=15, height=2, bd=0).pack(side="left", padx=10)
        
        tk.Button(frame, text="EXIT SYSTEM", command=self.exit_system, bg='#e74c3c', fg='white', font=("Segoe UI", 12, "bold"), width=32, height=2, bd=0).pack(pady=20)

    def show_goodbye_screen(self):
        self.clear_view()
        frame = tk.Frame(self.main_container, bg='#f5f6fa')
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="THANK YOU FOR USING THIS", font=("Segoe UI", 16), bg='#f5f6fa', fg='#7f8c8d').pack()
        tk.Label(frame, text="ACADEMIC MANAGEMENT SYSTEM", font=("Segoe UI", 28, "bold"), bg='#f5f6fa', fg='#2c3e50').pack(pady=(10, 20))
        tk.Label(frame, text="I hope that it can help you in terms of grading.", font=("Segoe UI", 18, "italic"), bg='#f5f6fa', fg='#34495e').pack(pady=(0, 40))
        
        tk.Button(frame, text="CLOSE APPLICATION", command=self.root.destroy, bg='#e74c3c', fg='white', font=("Segoe UI", 12, "bold"), width=25, height=2, bd=0).pack()

    def show_auth_form(self, mode):
        self.clear_view()
        f = tk.Frame(self.main_container, bg='white', padx=40, pady=40, bd=1, relief="solid")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(f, text=mode, font=("Segoe UI", 24, "bold"), bg='white').pack(pady=(0, 20))
        tk.Label(f, text="Username", bg='white').pack(anchor="w")
        
        self.u_in = tk.Entry(f, font=("Arial", 14), width=30)
        self.u_in.pack(pady=5)
        
        tk.Label(f, text="Password", bg='white').pack(anchor="w", pady=(10, 0))
        self.p_in = tk.Entry(f, font=("Arial", 14), width=30, show="*")
        self.p_in.pack(pady=5)
        
        if mode == "REGISTER":
            privacy_frame = tk.LabelFrame(f, text="Data Privacy & Anti-Scam Protection", bg='white', font=("Segoe UI", 9, "bold"), padx=10, pady=10)
            privacy_frame.pack(pady=15, fill="x")
            
            privacy_text = (
                "DATA PRIVACY NOTICE: To protect against online scams, this system operates "
                "100% locally. No data is shared over the internet. Your account credentials "
                "and student logs are stored securely on this hard drive and can only be "
                "unlocked by entering your registered password."
            )
            tk.Label(privacy_frame, text=privacy_text, bg='white', font=("Segoe UI", 9), wraplength=300, justify="left", fg="#2c3e50").pack()
            
            self.privacy_var = tk.BooleanVar(value=False)
            tk.Checkbutton(privacy_frame, text="I accept the Data Privacy Terms.", variable=self.privacy_var, bg='white', font=("Segoe UI", 9, "bold"), fg="#1877f2").pack(anchor="w", pady=(5, 0))
        
        cmd = self.process_login if mode == "LOGIN" else self.process_reg
        tk.Button(f, text="CONTINUE", command=cmd, bg='#1877f2', fg='white', font=("Segoe UI", 11, "bold"), width=25, pady=10, bd=0).pack(pady=20)
        tk.Button(f, text="Go Back", command=self.show_welcome_screen, bg='white', relief="flat").pack()

    def process_login(self):
        u, p = self.u_in.get().strip(), self.p_in.get().strip()
        if u in self.accounts and self.accounts[u] == p: 
            self.current_teacher = u
            if u not in self.database: 
                self.database[u] = {}
            self.show_folders()
        else: 
            messagebox.showerror("Access Denied", "Invalid credentials. Please double-check your username and password.")

    def process_reg(self):
        u, p = self.u_in.get().strip(), self.p_in.get().strip()
        
        if not self.privacy_var.get():
            messagebox.showerror("Security Block", "You must read and accept the Data Privacy Terms to safeguard your workspace.")
            return

        if u and p: 
            self.accounts[u] = p
            if u not in self.database: 
                self.database[u] = {}
            self.save_all_data()
            messagebox.showinfo("Security", "Account successfully registered and secured!")
            self.show_auth_form("LOGIN")
        else:
            messagebox.showerror("Error", "Username and Password fields cannot be empty.")
    
    def show_folders(self):
        self.clear_view()
        nav = tk.Frame(self.main_container, bg='#2c3e50', pady=10)
        nav.pack(fill="x")
        
        tk.Button(nav, text="Logout", command=self.show_welcome_screen, bg="#e74c3c", fg="white", bd=0, padx=10).pack(side="left", padx=20)
        tk.Button(nav, text="💾 SAVE ALL DATA", command=self.manual_save, bg="#f1c40f", fg="black", font=("Arial", 9, "bold"), bd=0, padx=10).pack(side="left", padx=10)
        tk.Button(nav, text="🚪 EXIT", command=self.exit_system, bg="#95a5a6", fg="white", font=("Arial", 9, "bold"), bd=0, padx=10).pack(side="right", padx=20)
        
        tk.Label(self.main_container, text=f"Teacher Workspace: {self.current_teacher}", font=("Segoe UI", 12)).pack(pady=(10, 0))
        tk.Label(self.main_container, text="CLASS FOLDERS", font=("Segoe UI", 22, "bold")).pack(pady=10)
        
        entry_f = tk.LabelFrame(self.main_container, text="Create New Class", bg='white', padx=10, pady=10)
        entry_f.pack()
        
        self.nf_name = tk.Entry(entry_f)
        self.nf_name.grid(row=0, column=0, padx=5)
        
        self.nf_lvl = tk.StringVar(value="COLLEGE")
        ttk.Combobox(entry_f, textvariable=self.nf_lvl, values=["ELEMENTARY", "HIGH SCHOOL", "SENIOR HIGH", "COLLEGE"], state="readonly").grid(row=0, column=1, padx=5)
        tk.Button(entry_f, text="ADD CLASS", command=self.add_folder, bg="#2ecc71", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5)

        self.f_grid = tk.Frame(self.main_container)
        self.f_grid.pack(pady=20)
        self.render_folders()

    def add_folder(self):
        n, l = self.nf_name.get().strip().upper(), self.nf_lvl.get()
        if n:
            periods = ["1ST SEMESTER", "2ND SEMESTER"] if l in ["COLLEGE", "SENIOR HIGH"] else ["FULL YEAR"]
            if n not in self.database[self.current_teacher]:
                self.database[self.current_teacher][n] = {"level": l, "periods": {p: {} for p in periods}}
            self.save_all_data() 
            self.render_folders()
            self.nf_name.delete(0, 'end')

    def render_folders(self):
        for w in self.f_grid.winfo_children(): 
            w.destroy()
        folders = self.database.get(self.current_teacher, {})
        r, c = 0, 0
        for n, info in folders.items():
            fb = tk.Frame(self.f_grid, bg='white', bd=1, relief="solid", padx=10, pady=10)
            fb.grid(row=r, column=c, padx=10, pady=10)
            
            tk.Button(fb, text=f"📂\n{n}\n{info['level']}", width=15, height=5, command=lambda x=n, y=info['level']: self.open_f(x, y), bg="#ecf0f1", relief="flat").pack()
            tk.Button(fb, text="Delete", fg="white", bg="#e74c3c", command=lambda x=n: self.del_f(x), bd=0).pack(pady=5, fill="x")
            
            c += 1
            if c > 4: 
                c = 0
                r += 1

    def del_f(self, f):
        if messagebox.askyesno("Confirm", f"Delete {f}? All records inside will be lost."):
            del self.database[self.current_teacher][f]
            self.save_all_data()
            self.render_folders()

    def open_f(self, f, l): 
        self.current_folder = f
        self.current_level = l
        self.show_data_panel()

    def show_data_panel(self):
        self.clear_view()
        header = tk.Frame(self.main_container, bg='#1877f2', pady=10)
        header.pack(fill="x")
        
        tk.Button(header, text="⬅ Back", command=self.show_folders, bg="white").pack(side="left", padx=20)
        tk.Label(header, text=f"FOLDER: {self.current_folder} | LEVEL: {self.current_level}", fg="white", font=("Arial", 12, "bold")).pack(side="left")

        sel_frame = tk.Frame(self.main_container, pady=10)
        sel_frame.pack()
        
        periods = list(self.database[self.current_teacher][self.current_folder]["periods"].keys())
        self.active_p = tk.StringVar(value=periods[0])
        
        tk.Label(sel_frame, text="Select Semester:").pack(side="left", padx=5)
        p_drop = ttk.Combobox(sel_frame, textvariable=self.active_p, values=periods, state="readonly", width=25)
        p_drop.pack(side="left", padx=10)
        p_drop.bind("<<ComboboxSelected>>", lambda e: self.refresh_entry_ui())

        self.entry_area = tk.Frame(self.main_container, bg='white', padx=20, pady=20, bd=1, relief="ridge")
        self.entry_area.pack(fill="x", padx=40)
        
        self.table_area = tk.Frame(self.main_container, bg='white')
        self.table_area.pack(fill="both", expand=True, padx=40, pady=(20, 40)) 
        
        self.refresh_entry_ui()

    def refresh_entry_ui(self):
        for w in self.entry_area.winfo_children(): 
            w.destroy()
        id_lbl = "Student No." if self.current_level == "COLLEGE" else "LRN"
        
        if self.current_level == "COLLEGE": 
            p_vals = ["PRELIM", "MIDTERM", "FINAL"]
        elif self.current_level == "SENIOR HIGH": 
            p_vals = ["MIDTERM", "FINAL"]
        else: 
            p_vals = ["1ST QTR", "2ND QTR", "3RD QTR", "4TH QTR"]

        self.fields = {}
        labels = [id_lbl, "Student Name", "Subject"]
        for i, l in enumerate(labels):
            tk.Label(self.entry_area, text=l+":", bg='white').grid(row=0, column=i*2)
            ent = tk.Entry(self.entry_area, width=15)
            ent.grid(row=0, column=i*2+1, padx=5)
            self.fields[l] = ent
        
        tk.Label(self.entry_area, text="Grading Period:", bg='white').grid(row=0, column=6)
        self.period_choice = tk.StringVar(value=p_vals[0])
        ttk.Combobox(self.entry_area, textvariable=self.period_choice, values=p_vals, state="readonly", width=12).grid(row=0, column=7, padx=5)
        
        tk.Label(self.entry_area, text="Grade:", bg='white').grid(row=0, column=8)
        self.g_in = tk.Entry(self.entry_area, width=8)
        self.g_in.grid(row=0, column=9, padx=5)

        tk.Button(self.entry_area, text="SAVE ENTRY", command=self.save_record, bg='#1877f2', fg='white', font=("Arial", 9, "bold")).grid(row=0, column=10, padx=15)
        self.render_table()

    def save_record(self):
        p_sem = self.active_p.get()
        id_key = "Student No." if self.current_level == "COLLEGE" else "LRN"
        sid = self.fields[id_key].get().strip()
        name = self.fields["Student Name"].get().strip().upper()
        subj = self.fields["Subject"].get().strip().upper()
        period = self.period_choice.get()
        
        if not sid or not name or not subj:
            messagebox.showerror("Error", "Please fill up all fields.")
            return

        try:
            grade = float(self.g_in.get())
            path = self.database[self.current_teacher][self.current_folder]["periods"][p_sem]
            if sid not in path: 
                path[sid] = {"name": name, "grades": {}}
            
            column_name = f"[{period}] {subj}"
            path[sid]["grades"][column_name] = grade
            
            self.save_all_data() 
            self.render_table()
            self.fields["Subject"].delete(0, 'end')
            self.g_in.delete(0, 'end')
        except ValueError: 
            messagebox.showerror("Error", "Invalid grade input. Please insert a numeric value.")

    def render_table(self):
        for w in self.table_area.winfo_children(): 
            w.destroy()
            
        p_sem = self.active_p.get()
        data = self.database[self.current_teacher][self.current_folder]["periods"][p_sem]
        id_key = "Student No." if self.current_level == "COLLEGE" else "LRN"
        
        all_cols = set()
        for sid in data:
            for gc in data[sid]["grades"].keys(): 
                all_cols.add(gc)
        
        sorted_cols = sorted(list(all_cols))
        headers = [id_key, "NAME"] + sorted_cols + ["GWA"]

        table_frame = tk.Frame(self.table_area)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=headers, show="headings")
        
        for h in headers:
            tree.heading(h, text=h)
            if h == "NAME":
                tree.column(h, width=150, minwidth=120, anchor="w", stretch=True)
            elif h in [id_key]:
                tree.column(h, width=90, minwidth=80, anchor="center", stretch=True)
            elif h == "GWA":
                tree.column(h, width=70, minwidth=60, anchor="center", stretch=True)
            else:
                # Ito para sa mga subjects, siksik lang sila para laging kita ang dulo
                tree.column(h, width=100, minwidth=90, anchor="center", stretch=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        for sid, info in data.items():
            row = [sid, info["name"]]
            g_vals = []
            for c in sorted_cols:
                val = info["grades"].get(c, "-")
                row.append(val)
                if isinstance(val, (int, float)): 
                    g_vals.append(val)
            
            gwa = round(sum(g_vals)/len(g_vals), 2) if g_vals else 0
            row.append(gwa)
            tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    AcademicManagementSystem(root)
    root.mainloop()