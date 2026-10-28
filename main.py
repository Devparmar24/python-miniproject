import tkinter as tk
import student_ui
import instructor_ui

BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"

def main_menu():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.configure(bg=BG_COLOR)
    tk.Label(root, text="Welcome to the Automated Report System", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="#f1c40f").pack(pady=40)
    tk.Label(root, text="Please select your role to continue:", font=("Helvetica", 14), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    tk.Button(root, text="I am a Student", bg="#3498db", fg=FG_COLOR, font=("Helvetica", 14, "bold"), width=20, pady=10, 
              command=lambda: student_ui.load_student_dashboard(root, main_menu)).pack(pady=20)
              
    tk.Button(root, text="I am an Instructor", bg="#9b59b6", fg=FG_COLOR, font=("Helvetica", 14, "bold"), width=20, pady=10, 
              command=lambda: instructor_ui.load_instructor_dashboard(root, main_menu)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Student Report & Email System")
    root.geometry("700x550")
    main_menu()
    root.mainloop()