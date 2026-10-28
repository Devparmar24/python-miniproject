import tkinter as tk
from tkinter import ttk, messagebox
import data_manager
import mailer

BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
BTN_COLOR = "#9b59b6"
ENTRY_BG = "#3c3f41"

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def load_instructor_dashboard(root, go_back_callback):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Instructor Portal Login", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=30)

    tk.Label(root, text="Username:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12)).pack()
    user_entry = tk.Entry(root, bg=ENTRY_BG, fg=FG_COLOR, font=("Helvetica", 12), insertbackground=FG_COLOR)
    user_entry.pack(pady=5)

    tk.Label(root, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12)).pack()
    pass_entry = tk.Entry(root, bg=ENTRY_BG, fg=FG_COLOR, font=("Helvetica", 12), show="*", insertbackground=FG_COLOR)
    pass_entry.pack(pady=5)

    def attempt_login():
        if user_entry.get().strip().lower() == "renia dias" and pass_entry.get().strip().lower() == "djsc":
            show_instructor_panel(root, go_back_callback)
        else:
            messagebox.showerror("Access Denied", "Incorrect username or password.")

    tk.Button(root, text="Login", bg=BTN_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"), command=attempt_login, width=15).pack(pady=20)
    tk.Button(root, text="Back to Main Menu", bg="#e74c3c", fg=FG_COLOR, command=go_back_callback).pack(pady=10)


def show_instructor_panel(root, go_back_callback):
    clear_window(root)
    tk.Label(root, text="Instructor Dashboard - Student Status", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    # Style the Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#3c3f41", foreground="white", fieldbackground="#3c3f41", rowheight=30)
    style.map('Treeview', background=[('selected', BTN_COLOR)])

    columns = ('sapid', 'name', 'status')
    tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
    tree.heading('sapid', text='SAP ID')
    tree.heading('name', text='Student Name')
    tree.heading('status', text='Email Status')
    tree.pack(pady=10, padx=20, fill="x")

    def refresh_tree():
        for item in tree.get_children():
            tree.delete(item)
        for student in data_manager.get_all_students():
            name = f"{student['first_name']} {student['last_name']}"
            tree.insert('', tk.END, values=(student['sapid'], name, student['email_status'].capitalize()))

    refresh_tree()

    def on_student_select():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Selection", "Please select a student from the list.")
            return
        
        values = tree.item(selected, 'values')
        sapid = values[0]
        
        # Find student full data
        student_data = next((s for s in data_manager.get_all_students() if str(s['sapid']) == str(sapid)), None)
        if student_data:
            open_student_popup(student_data, refresh_tree)

    tk.Button(root, text="View Selected Student & Send Email", bg="#27ae60", fg=FG_COLOR, font=("Helvetica", 12, "bold"), command=on_student_select).pack(pady=10)
    tk.Button(root, text="Logout", bg="#e74c3c", fg=FG_COLOR, command=go_back_callback).pack(pady=10)

def open_student_popup(student, refresh_callback):
    popup = tk.Toplevel()
    popup.title(f"Details - {student['first_name']} {student['last_name']}")
    popup.geometry("400x350")
    popup.configure(bg=BG_COLOR)

    tk.Label(popup, text=f"SAP ID: {student['sapid']}", font=("Helvetica", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
    
    marks_text = f"Python: {student['python']} | Credits: 3\nEDC: {student['edc']} | Credits: 3\nDSD: {student['dsd']} | Credits: 3\nMaths 3: {student['maths_3']} | Credits: 3"
    tk.Label(popup, text=marks_text, font=("Helvetica", 12), bg=ENTRY_BG, fg=FG_COLOR, justify="left", padx=10, pady=10).pack(pady=10)

    def send_email_action():
        success, msg = mailer.send_report_card(student)
        if success:
            data_manager.update_email_status(student['sapid'])
            messagebox.showinfo("Success", msg)
            refresh_callback()
            popup.destroy()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(popup, text="Send Automated Email", bg="#3498db", fg=FG_COLOR, font=("Helvetica", 12, "bold"), command=send_email_action).pack(pady=20)