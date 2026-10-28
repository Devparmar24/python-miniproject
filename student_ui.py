import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import data_manager

BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
BTN_COLOR = "#3498db"
ENTRY_BG = "#3c3f41"

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def load_student_dashboard(root, go_back_callback):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Student Portal Login", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=30)

    tk.Label(root, text="First Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12)).pack()
    fname_entry = tk.Entry(root, bg=ENTRY_BG, fg=FG_COLOR, font=("Helvetica", 12), insertbackground=FG_COLOR)
    fname_entry.pack(pady=5)

    tk.Label(root, text="Last Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12)).pack()
    lname_entry = tk.Entry(root, bg=ENTRY_BG, fg=FG_COLOR, font=("Helvetica", 12), insertbackground=FG_COLOR)
    lname_entry.pack(pady=5)

    tk.Label(root, text="SAP ID:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12)).pack()
    sapid_entry = tk.Entry(root, bg=ENTRY_BG, fg=FG_COLOR, font=("Helvetica", 12), insertbackground=FG_COLOR)
    sapid_entry.pack(pady=5)

    def attempt_login():
        student = data_manager.authenticate_student(sapid_entry.get(), fname_entry.get(), lname_entry.get())
        if student:
            show_report_card(root, student, go_back_callback)
        else:
            messagebox.showerror("Error", "Invalid Details. Please try again.")

    tk.Button(root, text="Login", bg=BTN_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"), command=attempt_login, width=15).pack(pady=20)
    tk.Button(root, text="Back to Main Menu", bg="#e74c3c", fg=FG_COLOR, command=go_back_callback).pack(pady=10)

def show_report_card(root, student, go_back_callback):
    clear_window(root)
    tk.Label(root, text=f"Report Card: {student['first_name'].capitalize()} {student['last_name'].capitalize()}", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
    
    frame = tk.Frame(root, bg=ENTRY_BG, padx=20, pady=20)
    frame.pack(pady=10)

    subjects = [('Python', student['python']), ('EDC', student['edc']), ('DSD', student['dsd']), ('Maths 3', student['maths_3'])]
    
    tk.Label(frame, text="Subject\t\tCredits\t\tScore", font=("Helvetica", 12, "bold"), bg=ENTRY_BG, fg=BTN_COLOR).pack(anchor="w")
    for sub, score in subjects:
        tk.Label(frame, text=f"{sub}\t\t3\t\t{score}", font=("Helvetica", 12), bg=ENTRY_BG, fg=FG_COLOR).pack(anchor="w", pady=5)
    
    total = sum(score for _, score in subjects)
    gpa = (total / 4) / 10
    tk.Label(frame, text=f"\nTotal Marks: {total}/400  |  Estimated GPA: {gpa:.2f}", font=("Helvetica", 12, "bold"), bg=ENTRY_BG, fg="#2ecc71").pack(pady=10)

    tk.Button(root, text="View Performance Graph", bg="#f39c12", fg=FG_COLOR, font=("Helvetica", 12, "bold"), command=lambda: open_graph(student)).pack(pady=20)
    tk.Button(root, text="Logout", bg="#e74c3c", fg=FG_COLOR, command=go_back_callback).pack()

def open_graph(student):
    graph_window = tk.Toplevel()
    graph_window.title("Performance Analytics")
    graph_window.geometry("800x500")

    avg_scores, max_scores, avg_total, max_total, avg_gpa, max_gpa = data_manager.get_class_stats()
    
    labels = ['Python', 'EDC', 'DSD', 'Maths 3', 'Avg Marks', 'GPA']
    student_data = [student['python'], student['edc'], student['dsd'], student['maths_3'], sum([student['python'], student['edc'], student['dsd'], student['maths_3']])/4, (sum([student['python'], student['edc'], student['dsd'], student['maths_3']])/4)/10]
    avg_data = [avg_scores['python'], avg_scores['edc'], avg_scores['dsd'], avg_scores['maths_3'], avg_total, avg_gpa]
    max_data = [max_scores['python'], max_scores['edc'], max_scores['dsd'], max_scores['maths_3'], max_total, max_gpa]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor('#2b2b2b')
    ax.set_facecolor('#3c3f41')
    
    ax.bar(x - width, student_data, width, label='You', color='#3498db')
    ax.bar(x, avg_data, width, label='Class Average', color='#f39c12')
    ax.bar(x + width, max_data, width, label='Highest Peer', color='#2ecc71')

    ax.set_ylabel('Scores / Value', color='white')
    ax.set_title('Performance Comparison', color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color='white')
    ax.tick_params(colors='white')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)