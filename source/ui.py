import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from constants import (
    COLLEGE_PASSING_GWA,
    K12_PASSING_GWA,
    STATUS_INCOMPLETE,
    STATUS_PASSED,
    STATUS_REMEDIAL,
)
from database import Database
from privacy_terms import DATA_PRIVACY_TERMS


class AcademicApplicationManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SECURE GRADE MANAGEMENT SYSTEM (SQL EDITION)")
        self.root.geometry("650x550")
        self.root.configure(bg="#f5f6fa")

        # Intercept the window close (X) button to use our confirm exit
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        self.db = Database()
        self.current_teacher_user = None
        self.current_teacher_id = None

        self.show_login_screen()

    # -----------------------------------------------------------------------
    # EXIT HANDLER — shared confirm dialog
    # -----------------------------------------------------------------------
    def confirm_exit(self):
        """Ask for confirmation before closing the application."""
        if messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit the\nSecure Grade Management System?"
        ):
            self.root.destroy()

    # -----------------------------------------------------------------------
    # HELPER: Show Data Privacy Terms in a Modal Window
    # -----------------------------------------------------------------------
    def show_privacy_terms_modal(self, parent=None):
        """Opens a read-only modal window displaying the full Data Privacy Terms."""
        win = tk.Toplevel(self.root)
        win.title("📋 Data Privacy Policy & Terms of Use")
        win.geometry("720x580")
        win.configure(bg="#f0f4f8")
        win.resizable(True, True)
        win.grab_set()  # Make modal

        if parent:
            win.transient(self.root)

        # Header
        hdr = tk.Frame(win, bg="#1877f2", pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔒  DATA PRIVACY POLICY & TERMS OF USE",
                 font=("Segoe UI", 13, "bold"), fg="white", bg="#1877f2").pack()
        tk.Label(hdr, text="Republic Act No. 10173 — Data Privacy Act of 2012",
                 font=("Segoe UI", 9), fg="#cce0ff", bg="#1877f2").pack()

        # Scrollable text area
        text_frame = tk.Frame(win, bg="#f0f4f8", padx=15, pady=10)
        text_frame.pack(fill="both", expand=True)

        text_box = scrolledtext.ScrolledText(
            text_frame,
            font=("Courier New", 9),
            bg="#ffffff",
            fg="#2c3e50",
            relief="solid",
            bd=1,
            wrap="word",
            state="normal",
            padx=12,
            pady=12
        )
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", DATA_PRIVACY_TERMS)
        text_box.configure(state="disabled")  # Read-only

        # Close button
        btn_frame = tk.Frame(win, bg="#f0f4f8", pady=10)
        btn_frame.pack(fill="x")
        tk.Button(
            btn_frame,
            text="✔  I Understand — Close",
            command=win.destroy,
            bg="#1877f2",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=6
        ).pack()

    # -----------------------------------------------------------------------
    # FORGOT PASSWORD FLOW
    # -----------------------------------------------------------------------
    def show_forgot_password_screen(self):
        """Step 1: Ask for username to begin recovery."""
        self.clear_screen()
        self.root.geometry("650x550")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=35, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🔑 FORGOT PASSWORD", font=("Segoe UI", 15, "bold"),
                 bg="white", fg="#e67e22").pack(pady=(0, 5))
        tk.Label(frame, text="Enter your username to begin account recovery.",
                 font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(pady=(0, 18))

        tk.Label(frame, text="Registered Username:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        u_entry = tk.Entry(frame, width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        u_entry.pack(pady=8)

        error_lbl = tk.Label(frame, text="", bg="white", fg="#e74c3c", font=("Segoe UI", 9))
        error_lbl.pack()

        def proceed_to_security_question():
            username = u_entry.get().strip()
            if not username:
                error_lbl.config(text="Please enter your username.")
                return
            question = self.db.get_recovery_question(username)
            if not question:
                error_lbl.config(text="Username not found in the system.")
                return
            self.show_security_question_screen(username, question)

        tk.Button(frame, text="FIND MY ACCOUNT", command=proceed_to_security_question,
                  bg="#e67e22", fg="white", width=28, font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2").pack(pady=18)

        tk.Button(frame, text="← Back to Login", command=self.show_login_screen,
                  fg="#7f8c8d", bg="white", borderwidth=0, cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack()

        # EXIT button
        tk.Button(frame, text="✖  EXIT APPLICATION", command=self.confirm_exit,
                  bg="#c0392b", fg="white", width=28, font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2").pack(pady=(8, 0))

    def show_security_question_screen(self, username, question):
        """Step 2: Display the security question and validate the answer."""
        self.clear_screen()
        self.root.geometry("650x550")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=35, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🛡️ SECURITY VERIFICATION", font=("Segoe UI", 15, "bold"),
                 bg="white", fg="#8e44ad").pack(pady=(0, 5))
        tk.Label(frame, text=f"Verifying identity for: {username}",
                 font=("Segoe UI", 9, "italic"), bg="white", fg="#7f8c8d").pack(pady=(0, 18))

        # Security question display box
        q_frame = tk.Frame(frame, bg="#f8f9fa", bd=1, relief="solid", padx=15, pady=10)
        q_frame.pack(fill="x", pady=(0, 14))
        tk.Label(q_frame, text="Your Security Question:", font=("Segoe UI", 9, "bold"),
                 bg="#f8f9fa", fg="#555").pack(anchor="w")
        tk.Label(q_frame, text=f"  ❓  {question}", font=("Segoe UI", 11),
                 bg="#f8f9fa", fg="#2c3e50", wraplength=340, justify="left").pack(anchor="w", pady=(4, 0))

        tk.Label(frame, text="Your Answer:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        a_entry = tk.Entry(frame, width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        a_entry.pack(pady=8)

        error_lbl = tk.Label(frame, text="", bg="white", fg="#e74c3c", font=("Segoe UI", 9))
        error_lbl.pack()

        def verify_and_proceed():
            answer = a_entry.get().strip()
            if not answer:
                error_lbl.config(text="Please enter your security answer.")
                return
            if self.db.verify_recovery(username, answer):
                self.show_reset_password_screen(username)
            else:
                error_lbl.config(text="Incorrect answer. Please try again.")
                a_entry.delete(0, "end")

        tk.Button(frame, text="VERIFY IDENTITY", command=verify_and_proceed,
                  bg="#8e44ad", fg="white", width=28, font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2").pack(pady=18)

        tk.Button(frame, text="← Back to Login", command=self.show_login_screen,
                  fg="#7f8c8d", bg="white", borderwidth=0, cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack()

    def show_reset_password_screen(self, username):
        """Step 3: Allow user to set a new password."""
        self.clear_screen()
        self.root.geometry("650x550")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=35, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🔓 RESET YOUR PASSWORD", font=("Segoe UI", 15, "bold"),
                 bg="white", fg="#27ae60").pack(pady=(0, 5))
        tk.Label(frame, text=f"Setting new password for: {username}",
                 font=("Segoe UI", 9, "italic"), bg="white", fg="#7f8c8d").pack(pady=(0, 18))

        tk.Label(frame, text="New Password (min 6 characters):", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        np_entry = tk.Entry(frame, show="*", width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        np_entry.pack(pady=8)

        tk.Label(frame, text="Confirm New Password:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        cp_entry = tk.Entry(frame, show="*", width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        cp_entry.pack(pady=8)

        # Password strength indicator
        strength_lbl = tk.Label(frame, text="", bg="white", font=("Segoe UI", 9))
        strength_lbl.pack()

        def check_strength(event=None):
            p = np_entry.get()
            if len(p) == 0:
                strength_lbl.config(text="", fg="#7f8c8d")
            elif len(p) < 6:
                strength_lbl.config(text="⚠ Too short", fg="#e74c3c")
            elif len(p) < 10:
                strength_lbl.config(text="● Moderate strength", fg="#e67e22")
            else:
                strength_lbl.config(text="✔ Strong password", fg="#27ae60")

        np_entry.bind("<KeyRelease>", check_strength)

        error_lbl = tk.Label(frame, text="", bg="white", fg="#e74c3c", font=("Segoe UI", 9))
        error_lbl.pack()

        def reset_and_save():
            new_p = np_entry.get().strip()
            confirm_p = cp_entry.get().strip()
            if len(new_p) < 6:
                error_lbl.config(text="Password must be at least 6 characters.")
                return
            if new_p != confirm_p:
                error_lbl.config(text="Passwords do not match.")
                cp_entry.delete(0, "end")
                return
            self.db.reset_password(username, new_p)
            messagebox.showinfo("✔ Password Reset Successful",
                                "Your password has been updated successfully.\nPlease log in with your new password.")
            self.show_login_screen()

        tk.Button(frame, text="SAVE NEW PASSWORD", command=reset_and_save,
                  bg="#27ae60", fg="white", width=28, font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2").pack(pady=18)

        tk.Button(frame, text="← Back to Login", command=self.show_login_screen,
                  fg="#7f8c8d", bg="white", borderwidth=0, cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack()

    # -----------------------------------------------------------------------
    # LOGIN SCREEN
    # -----------------------------------------------------------------------
    def show_login_screen(self):
        self.clear_screen()
        self.root.geometry("650x550")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=40, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🔒 CONTROL PANEL LOGIN", font=("Segoe UI", 16, "bold"),
                 bg="white", fg="#1877f2").pack(pady=15)

        tk.Label(frame, text="Administrative Username:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        u_entry = tk.Entry(frame, width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        u_entry.pack(pady=8)

        tk.Label(frame, text="Account Password:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        p_entry = tk.Entry(frame, show="*", width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        p_entry.pack(pady=8)

        # Show/Hide password toggle
        login_show_pw = tk.BooleanVar(value=False)

        def toggle_login_password():
            p_entry.config(show="" if login_show_pw.get() else "*")

        tk.Checkbutton(frame, text="Show password", variable=login_show_pw,
                       command=toggle_login_password, bg="white", activebackground="white",
                       font=("Segoe UI", 9), cursor="hand2").pack(anchor="w")

        # Forgot Password link — right-aligned under password field
        fp_frame = tk.Frame(frame, bg="white")
        fp_frame.pack(fill="x")
        tk.Button(fp_frame, text="Forgot Password?", command=self.show_forgot_password_screen,
                  fg="#e67e22", bg="white", borderwidth=0, cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack(side="right")

        def login_process():
            u = u_entry.get().strip()
            p = p_entry.get().strip()
            if self.db.authenticate(u, p):
                self.current_teacher_user = u
                self.current_teacher_id = self.db.get_teacher_id(u)
                self.show_dashboard()
            else:
                messagebox.showerror("Access Denied", "Invalid administrative credentials.")

        tk.Button(frame, text="SECURE SIGN IN", command=login_process, bg="#1877f2", fg="white",
                  width=28, font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2").pack(pady=15)
        tk.Button(frame, text="Create New Administrator Profile", command=self.show_register_screen,
                  fg="#1877f2", bg="white", borderwidth=0, cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack()

        # ── EXIT button on Login Screen ──────────────────────────────────────
        tk.Button(frame, text="✖  EXIT APPLICATION", command=self.confirm_exit,
                  bg="#c0392b", fg="white", width=28, font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2").pack(pady=(12, 0))
        # ─────────────────────────────────────────────────────────────────────

    # -----------------------------------------------------------------------
    # REGISTER SCREEN (with Data Privacy Terms checkbox)
    # -----------------------------------------------------------------------
    def show_register_screen(self):
        self.clear_screen()
        self.root.geometry("650x600")

        frame = tk.Frame(self.root, bg="white", padx=40, pady=30, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🛡️ REGISTER SECURE SQL ACCOUNT",
                 font=("Segoe UI", 13, "bold"), bg="white", fg="#2ecc71").pack(pady=(0, 15))

        tk.Label(frame, text="Create Username:", bg="white").pack(anchor="w")
        u_entry = tk.Entry(frame, width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        u_entry.pack(pady=5)

        tk.Label(frame, text="Secure Password (min 6 characters):", bg="white").pack(anchor="w")
        p_entry = tk.Entry(frame, show="*", width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        p_entry.pack(pady=5)

        # Show/Hide password toggle
        register_show_pw = tk.BooleanVar(value=False)

        def toggle_register_password():
            p_entry.config(show="" if register_show_pw.get() else "*")

        tk.Checkbutton(frame, text="Show password", variable=register_show_pw,
                       command=toggle_register_password, bg="white", activebackground="white",
                       font=("Segoe UI", 9), cursor="hand2").pack(anchor="w")

        tk.Label(frame, text="Security Recovery Question:", bg="white").pack(anchor="w")
        questions = ["What was your childhood nickname?", "What was the name of your first elementary school?"]
        q_cb = ttk.Combobox(frame, values=questions, state="readonly", width=30, font=("Segoe UI", 10))
        q_cb.set(questions[0])
        q_cb.pack(pady=5)

        tk.Label(frame, text="Your Security Secret Answer:", bg="white").pack(anchor="w")
        a_entry = tk.Entry(frame, width=32, font=("Segoe UI", 11), relief="solid", bd=1)
        a_entry.pack(pady=5)

        # ── Data Privacy Terms Checkbox Row ──────────────────────────────────
        privacy_frame = tk.Frame(frame, bg="white")
        privacy_frame.pack(fill="x", pady=(12, 4))

        privacy_agreed = tk.BooleanVar(value=False)

        privacy_cb = tk.Checkbutton(
            privacy_frame,
            text="I have read and agree to the",
            variable=privacy_agreed,
            bg="white",
            font=("Segoe UI", 9),
            activebackground="white",
            cursor="hand2"
        )
        privacy_cb.pack(side="left")

        terms_link = tk.Label(
            privacy_frame,
            text="Data Privacy Terms",
            fg="#1877f2",
            bg="white",
            font=("Segoe UI", 9, "underline"),
            cursor="hand2"
        )
        terms_link.pack(side="left")
        terms_link.bind("<Button-1>", lambda e: self.show_privacy_terms_modal(parent=frame))

        tk.Label(privacy_frame, text="*", fg="#e74c3c", bg="white",
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        # ─────────────────────────────────────────────────────────────────────

        def register_process():
            u = u_entry.get().strip()
            p = p_entry.get().strip()
            q = q_cb.get()
            a = a_entry.get().strip()

            if not u or not p or not a:
                messagebox.showerror("Error", "All security fields must be filled.")
                return
            if len(p) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if not privacy_agreed.get():
                messagebox.showwarning(
                    "Privacy Agreement Required",
                    "You must read and agree to the Data Privacy Terms before creating an account.\n\n"
                    "Click the 'Data Privacy Terms' link to review the policy."
                )
                return

            if self.db.register(u, p, q, a):
                messagebox.showinfo("Success", "Account successfully registered into SQL Server.")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "Username already taken.")

        tk.Button(frame, text="INITIALIZE ACCOUNT", command=register_process,
                  bg="#2ecc71", fg="white", width=28, font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2").pack(pady=15)
        tk.Button(frame, text="← Return to Login Core", command=self.show_login_screen,
                  fg="#7f8c8d", bg="white", borderwidth=0, cursor="hand2").pack()

        # ── EXIT button on Register Screen ───────────────────────────────────
        tk.Button(frame, text="✖  EXIT APPLICATION", command=self.confirm_exit,
                  bg="#c0392b", fg="white", width=28, font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2").pack(pady=(8, 0))
        # ─────────────────────────────────────────────────────────────────────

    # -----------------------------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------------------------
    def show_dashboard(self):
        self.clear_screen()
        self.root.geometry("900x600")

        nav = tk.Frame(self.root, bg="#2c3e50", pady=12)
        nav.pack(fill="x")
        tk.Label(nav, text=f"🔒 SECURED PROFILE: {self.current_teacher_user.upper()}",
                 fg="#2ecc71", bg="#2c3e50", font=("Segoe UI", 11, "bold")).pack(side="left", padx=20)

        # ── EXIT button in Dashboard navbar ──────────────────────────────────
        tk.Button(nav, text="✖ EXIT", command=self.confirm_exit,
                  bg="#c0392b", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", cursor="hand2").pack(side="right", padx=10)
        # ─────────────────────────────────────────────────────────────────────

        tk.Button(nav, text="SECURE LOGOUT", command=self.logout, bg="#e74c3c", fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat").pack(side="right", padx=10)

        tk.Label(self.root, text="ARCHIVED CLASS DIRECTORIES",
                 font=("Segoe UI", 16, "bold"), fg="#2c3e50", pady=15).pack()

        form = tk.LabelFrame(self.root, text=" Directory Deployment Framework ",
                             font=("Segoe UI", 9), padx=15, pady=10)
        form.pack(pady=10)

        tk.Label(form, text="Folder Class Name:").pack(side="left", padx=5)
        f_entry = tk.Entry(form, font=("Segoe UI", 11), width=18, relief="solid")
        f_entry.pack(side="left", padx=5)

        levels = ["ELEMENTARY", "HIGH SCHOOL", "SENIOR HIGH", "COLLEGE"]
        level_cb = ttk.Combobox(form, values=levels, state="readonly", width=15, font=("Segoe UI", 10))
        level_cb.set("COLLEGE")
        level_cb.pack(side="left", padx=5)

        grid_frame = tk.Frame(self.root)
        grid_frame.pack(fill="both", expand=True, padx=40, pady=10)

        def render_folders():
            for w in grid_frame.winfo_children():
                w.destroy()
            folders = self.db.get_folders(self.current_teacher_id)
            if not folders:
                tk.Label(grid_frame, text="🔒 Database core index is empty.",
                         fg="#7f8c8d", font=("Segoe UI", 11, "italic")).pack(pady=30)
                return

            for i, (name, info) in enumerate(folders.items()):
                card = tk.Frame(grid_frame, bg="white", bd=1, relief="solid", padx=15, pady=15)
                card.grid(row=i // 4, column=i % 4, padx=15, pady=15)

                tk.Button(card, text=f"📁\n{name}\n[{info['level']}]",
                          command=lambda n=name, l=info['level']: self.open_folder(n, l),
                          bg="#f8f9fa", font=("Segoe UI", 11, "bold"), fg="#1877f2",
                          width=14, height=4, relief="flat", cursor="hand2").pack()

                def drop_folder(n=name):
                    if messagebox.askyesno("Database Purge", f"Delete folder '{n}'?"):
                        self.db.delete_folder(self.current_teacher_id, n)
                        render_folders()

                tk.Button(card, text="PURGE DIRECTORY", command=drop_folder,
                          bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                          relief="flat", width=16).pack(pady=(8, 0))

        def add_folder_process():
            n = f_entry.get().strip().upper()
            if n and self.db.add_folder(self.current_teacher_id, n, level_cb.get()):
                f_entry.delete(0, "end")
                render_folders()
            else:
                messagebox.showerror("Error", "Folder deployment failed.")

        tk.Button(form, text="DEPLOY DIRECTORY", command=add_folder_process,
                  bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), relief="flat").pack(side="left", padx=10)
        render_folders()

    # -----------------------------------------------------------------------
    # FOLDER / GRADE VIEW
    # -----------------------------------------------------------------------
    def open_folder(self, folder_name, level):
        self.clear_screen()
        self.root.geometry("1100x650")
        folder_id = self.db.get_folder_id(self.current_teacher_id, folder_name)

        hdr = tk.Frame(self.root, bg="#1877f2", pady=12)
        hdr.pack(fill="x")
        tk.Button(hdr, text="⬅️ Return to Dashboard", command=self.show_dashboard,
                  bg="white", fg="#1877f2", font=("Segoe UI", 9, "bold")).pack(side="left", padx=20)
        tk.Label(hdr, text=f"📂 CLASS: {folder_name} | SCOPE: {level}",
                 fg="white", bg="#1877f2", font=("Segoe UI", 13, "bold")).pack(side="left", padx=15)

        # ── EXIT button in folder header ──────────────────────────────────────
        tk.Button(hdr, text="✖ EXIT", command=self.confirm_exit,
                  bg="#c0392b", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", cursor="hand2").pack(side="right", padx=20)
        # ─────────────────────────────────────────────────────────────────────

        sem_row = tk.Frame(self.root, pady=10)
        sem_row.pack(fill="x", padx=25)

        tk.Label(sem_row, text="Active Database Segment Filter:",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        sems = ["1ST SEMESTER", "2ND SEMESTER"] if level in ("COLLEGE", "SENIOR HIGH") else ["FULL YEAR REPORT"]
        sem_cb = ttk.Combobox(sem_row, values=sems, state="readonly", width=22, font=("Segoe UI", 10))
        sem_cb.set(sems[0])
        sem_cb.pack(side="left", padx=10)

        form = tk.LabelFrame(self.root, text=" Secure Data Transaction Entry ",
                             font=("Segoe UI", 9), padx=10, pady=10)
        form.pack(fill="x", padx=25, pady=5)

        fields = ["Student Matrix ID", "Student Complete Name", "Subject Code", "Numeric Grade"]
        entries = {}
        for f in fields:
            tk.Label(form, text=f"{f}:").pack(side="left", padx=4)
            w = 8 if f == "Numeric Grade" else 14
            e = tk.Entry(form, width=w, font=("Segoe UI", 11), relief="solid")
            e.pack(side="left", padx=6)
            entries[f] = e

        p_vals = ["PRELIM", "MIDTERM", "FINAL"] if level == "COLLEGE" else ["1ST QTR", "2ND QTR", "3RD QTR", "4TH QTR"]
        p_cb = ttk.Combobox(form, values=p_vals, state="readonly", width=12, font=("Segoe UI", 10))
        p_cb.set(p_vals[0])
        p_cb.pack(side="left", padx=6)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=25, pady=15)

        def refresh_table_view():
            for w in table_frame.winfo_children():
                w.destroy()
            data = self.db.get_semester_records(folder_id, sem_cb.get())

            headers = ["Student ID Code", "Student Identity Profile", "📊 GWA", "📌 STATUS"]
            subjects_found = set()
            for s in data.values():
                subjects_found.update(s["grades"].keys())
            sorted_subjects = sorted(list(subjects_found))
            all_headers = headers + sorted_subjects

            tree = ttk.Treeview(table_frame, columns=all_headers, show="headings")
            tree.pack(fill="both", expand=True)

            style = ttk.Style()
            style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

            for h in all_headers:
                tree.heading(h, text=h)
                w_size = 100 if h in ["📊 GWA", "📌 STATUS"] else 140
                tree.column(h, width=w_size, anchor="center")

            for sid, info in data.items():
                grades_list = info.get("raw_list", [])
                if grades_list:
                    gwa_value = sum(grades_list) / len(grades_list)
                    gwa_text = f"{gwa_value:.2f}"
                    if level == "COLLEGE":
                        status_text = STATUS_PASSED if gwa_value <= COLLEGE_PASSING_GWA else STATUS_REMEDIAL
                    else:
                        status_text = STATUS_PASSED if gwa_value >= K12_PASSING_GWA else STATUS_REMEDIAL
                else:
                    gwa_text = "N/A"
                    status_text = STATUS_INCOMPLETE

                row = [sid, info["name"], gwa_text, status_text]
                for sub in sorted_subjects:
                    row.append(info["grades"].get(sub, "N/A"))
                tree.insert("", "end", values=row)

            def entry_deletion_event(e):
                sel = tree.selection()
                if not sel:
                    return
                target_id = tree.item(sel[0], "values")[0]
                target_name = tree.item(sel[0], "values")[1]
                if messagebox.askyesno("Data Drop Warning", f"Purge rows for: {target_name}?"):
                    self.db.delete_student(folder_id, sem_cb.get(), target_id)
                    refresh_table_view()
            tree.bind("<Delete>", entry_deletion_event)

        def save_grade_transaction():
            sid = entries["Student Matrix ID"].get().strip()
            name = entries["Student Complete Name"].get().strip().upper()
            sub = entries["Subject Code"].get().strip().upper()
            grade_raw = entries["Numeric Grade"].get().strip()

            if not sid or not name or not sub:
                messagebox.showerror("Error", "Student ID, Name and Subject Code must be filled.")
                return
            try:
                raw_grade = float(grade_raw)
            except ValueError:
                messagebox.showerror("Error", "Grade must be a number.")
                return

            if level == "COLLEGE":
                if not (1.0 <= raw_grade <= 5.0):
                    messagebox.showerror("Error", "College grades must be between 1.0 and 5.0.")
                    return
            else:
                if not (0 <= raw_grade <= 100):
                    messagebox.showerror("Error", "K-12 grades must be between 0 and 100.")
                    return

            self.db.save_grade(folder_id, sem_cb.get(), sid, name, sub, p_cb.get(), raw_grade)
            entries["Subject Code"].delete(0, "end")
            entries["Numeric Grade"].delete(0, "end")
            refresh_table_view()

        tk.Button(form, text="COMMIT DATA", command=save_grade_transaction,
                  bg="#1877f2", fg="white", font=("Segoe UI", 10, "bold"), relief="flat").pack(side="left", padx=10)
        sem_cb.bind("<<ComboboxSelected>>", lambda e: refresh_table_view())
        refresh_table_view()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_teacher_id = None
        self.current_teacher_user = None
        self.show_login_screen()

    def run(self):
        self.root.mainloop()

