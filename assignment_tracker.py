import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Vyas@123",
        database="assignment_tracker"
    )

class AssignmentTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Assignment Tracker")
        self.root.geometry("800x600")  # Set the initial size of the window
        self.root.minsize(800, 600)    # Set the minimum size of the window
        self.root.configure(bg="pale turquoise")  # Set background color
        
        self.file_path = None
        
        self.create_widgets()
        
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
        
    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Title", bg="pale turquoise")
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.desc_label = tk.Label(self.root, text="Description", bg="pale turquoise")
        self.desc_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.due_label = tk.Label(self.root, text="Due Date (YYYY-MM-DD)", bg="pale turquoise")
        self.due_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.due_entry = tk.Entry(self.root)
        self.due_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        self.status_label = tk.Label(self.root, text="Status", bg="pale turquoise")
        self.status_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.status_entry = tk.Entry(self.root)
        self.status_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        self.file_button = tk.Button(self.root, text="Upload File", command=self.upload_file, bg="lightgray")
        self.file_button.grid(row=4, column=0, padx=10, pady=5)
        
        self.add_button = tk.Button(self.root, text="Add Assignment", command=self.add_assignment, bg="lightgreen")
        self.add_button.grid(row=5, column=0, padx=10, pady=5)
        
        self.update_button = tk.Button(self.root, text="Update Assignment", command=self.update_assignment, bg="lightblue")
        self.update_button.grid(row=5, column=1, padx=10, pady=5)
        
        self.delete_button = tk.Button(self.root, text="Delete Assignment", command=self.delete_assignment, bg="lightcoral")
        self.delete_button.grid(row=6, column=0, padx=10, pady=5)
        
        self.view_button = tk.Button(self.root, text="View Assignments", command=self.view_assignments, bg="lightyellow")
        self.view_button.grid(row=6, column=1, padx=10, pady=5)
        
        self.save_button = tk.Button(self.root, text="Save to File", command=self.save_to_file, bg="lightpink")
        self.save_button.grid(row=7, column=0, padx=10, pady=5)
        
        self.load_button = tk.Button(self.root, text="Load from File", command=self.load_from_file, bg="lightcyan")
        self.load_button.grid(row=7, column=1, padx=10, pady=5)
        
        self.assignments_listbox = tk.Listbox(self.root)
        self.assignments_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        
    def upload_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("Success", "File uploaded successfully!")
        
    def add_assignment(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        due_date = self.due_entry.get()
        status = self.status_entry.get()
        
        query = "INSERT INTO assignments (title, description, due_date, status, file_path) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (title, description, due_date, status, self.file_path))
        self.conn.commit()
        self.clear_entries()
        messagebox.showinfo("Success", "Assignment added successfully!")
        
    def update_assignment(self):
        selected_assignment = self.assignments_listbox.get(tk.ACTIVE)
        assignment_id = selected_assignment.split()[0]
        title = self.title_entry.get()
        description = self.desc_entry.get()
        due_date = self.due_entry.get()
        status = self.status_entry.get()
        
        query = "UPDATE assignments SET title=%s, description=%s, due_date=%s, status=%s, file_path=%s WHERE id=%s"
        self.cursor.execute(query, (title, description, due_date, status, self.file_path, assignment_id))
        self.conn.commit()
        self.clear_entries()
        messagebox.showinfo("Success", "Assignment updated successfully!")
        
    def delete_assignment(self):
        selected_assignment = self.assignments_listbox.get(tk.ACTIVE)
        assignment_id = selected_assignment.split()[0]
        
        query = "DELETE FROM assignments WHERE id=%s"
        self.cursor.execute(query, (assignment_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Assignment deleted successfully!")
        self.view_assignments()
        
    def view_assignments(self):
        self.assignments_listbox.delete(0, tk.END)
        query = "SELECT * FROM assignments"
        self.cursor.execute(query)
        assignments = self.cursor.fetchall()
        
        for assignment in assignments:
            self.assignments_listbox.insert(tk.END, f"{assignment[0]} - {assignment[1]} (Due: {assignment[3]}) - {assignment[4]}")
        
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.file_path = None
        
    def save_to_file(self):
        with open("assignments.txt", "w") as file:
            query = "SELECT * FROM assignments"
            self.cursor.execute(query)
            assignments = self.cursor.fetchall()
            for assignment in assignments:
                file.write(f"{assignment[0]},{assignment[1]},{assignment[2]},{assignment[3]},{assignment[4]},{assignment[5]}\n")
        messagebox.showinfo("Success", "Assignments saved to file!")
        
    def load_from_file(self):
        with open("assignments.txt", "r") as file:
            for line in file:
                id, title, description, due_date, status, file_path = line.strip().split(',')
                query = "INSERT INTO assignments (id, title, description, due_date, status, file_path) VALUES (%s, %s, %s, %s, %s, %s)"
                self.cursor.execute(query, (id, title, description, due_date, status, file_path))
            self.conn.commit()
        messagebox.showinfo("Success", "Assignments loaded from file!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentTrackerApp(root)
    root.mainloop()
