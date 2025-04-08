import tkinter as tk
from tkinter import messagebox, ttk


class Student:
    def __init__(self, name, student_id, grades):
        self.name = name
        self.student_id = student_id
        self.grades = grades

    def get_average(self):
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return f"{self.name} (ID: {self.student_id}) - Avg: {self.get_average():.2f}"


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("600x600")
        self.root.configure(bg="#2e2e2e")  # Dark background
        self.students = []

        header = tk.Label(root, text="👨‍💻 Student Management App", font=("Arial", 18, "bold"), bg="#2e2e2e", fg="white")
        header.pack(pady=10)

        form_frame = tk.Frame(root, bg="#2e2e2e")  # Dark frame
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Name:", bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.name_entry = tk.Entry(form_frame, width=30, bg="#424242", fg="white", insertbackground="white")
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="ID (4 digits):", bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.id_entry = tk.Entry(form_frame, width=30, bg="#424242", fg="white", insertbackground="white")
        self.id_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Grades (0–100):", bg="#2e2e2e", fg="white").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.grades_entry = tk.Entry(form_frame, width=30, bg="#424242", fg="white", insertbackground="white")
        self.grades_entry.grid(row=2, column=1, padx=5, pady=2)

        button_frame = tk.Frame(root, bg="#2e2e2e")  # Dark button frame
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Student", command=self.add_student, width=15, bg="gray", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Student", command=self.update_student, width=15, bg="gray", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Remove by ID", command=self.remove_student, width=15, bg="gray", fg="white").grid(row=0, column=2, padx=5)

        search_frame = tk.Frame(root, bg="#2e2e2e")  # Dark search frame
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Name or ID:", bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e")
        self.search_entry = tk.Entry(search_frame, width=25, bg="#424242", fg="white", insertbackground="white")
        self.search_entry.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_student, bg="gray", fg="white").grid(row=0, column=2, padx=5)

        sort_frame = tk.Frame(root, bg="#2e2e2e")  # Dark sort frame
        sort_frame.pack(pady=10)

        tk.Label(sort_frame, text="Sort By:", bg="#2e2e2e", fg="white").grid(row=0, column=0)
        self.sort_option = ttk.Combobox(sort_frame, values=["Name (A-Z)", "Average Grade (High-Low)"], state="readonly", width=25)
        self.sort_option.grid(row=0, column=1, padx=5)
        self.sort_option.set("Name (A-Z)")
        tk.Button(sort_frame, text="List Students", command=self.list_students, bg="gray", fg="white").grid(row=0, column=2, padx=5)

        self.output_box = tk.Text(root, height=15, width=70, bg="#424242", fg="white")  # Dark output box
        self.output_box.pack(pady=15)

    def add_student(self):
        try:
            name = self.name_entry.get().strip()
            student_id_str = self.id_entry.get().strip()
            grades_str = self.grades_entry.get().strip()

            if not name or not all(c.isalpha() or c.isspace() for c in name):
                messagebox.showerror("Error", "Name must contain only letters and spaces.")
                return

            if not (student_id_str.isdigit() and len(student_id_str) == 4):
                messagebox.showerror("Error", "ID must be a 4-digit number.")
                return

            student_id = int(student_id_str)

            if any(s.student_id == student_id for s in self.students):
                messagebox.showerror("Error", f"Student with ID {student_id} already exists.")
                return

            grades = [int(g) for g in grades_str.split()]
            if not grades:
                messagebox.showerror("Error", "Please enter at least one grade.")
                return
            if not all(0 <= g <= 100 for g in grades):
                messagebox.showerror("Error", "Grades must be between 0 and 100.")
                return

            student = Student(name, student_id, grades)
            self.students.append(student)
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_entries()
            self.list_students()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only for ID and grades.")

    def list_students(self):
        self.output_box.delete("1.0", tk.END)
        if not self.students:
            self.output_box.insert(tk.END, "No students to display.")
            return

        sort_by = self.sort_option.get()
        if sort_by == "Name (A-Z)":
            sorted_students = sorted(self.students, key=lambda s: s.name.lower())
        elif sort_by == "Average Grade (High-Low)":
            sorted_students = sorted(self.students, key=lambda s: s.get_average(), reverse=True)
        else:
            sorted_students = self.students

        for s in sorted_students:
            self.output_box.insert(tk.END, str(s) + "\n")

    def remove_student(self):
        try:
            student_id = int(self.id_entry.get())
            for i, s in enumerate(self.students):
                if s.student_id == student_id:
                    del self.students[i]
                    messagebox.showinfo("Removed", f"Removed student with ID {student_id}")
                    self.clear_entries()
                    self.list_students()
                    return
            messagebox.showwarning("Not Found", "Student ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid ID.")

    def search_student(self):
        query = self.search_entry.get().strip()
        self.output_box.delete("1.0", tk.END)

        if not query:
            self.output_box.insert(tk.END, "Please enter a name or ID to search.")
            return

        found = False
        for s in self.students:
            if query.lower() in s.name.lower() or query == str(s.student_id):
                self.output_box.insert(tk.END, str(s) + "\n")
                found = True

        if not found:
            self.output_box.insert(tk.END, f"No student found for: {query}")

    def update_student(self):
        try:
            student_id_str = self.id_entry.get().strip()
            if not (student_id_str.isdigit() and len(student_id_str) == 4):
                messagebox.showerror("Error", "ID must be a 4-digit number.")
                return
            student_id = int(student_id_str)

            name = self.name_entry.get().strip()
            grades_str = self.grades_entry.get().strip()
            grades = [int(g) for g in grades_str.split()]
            if not name:
                messagebox.showerror("Error", "Please enter a valid name.")
                return
            if not grades or not all(0 <= g <= 100 for g in grades):
                messagebox.showerror("Error", "Grades must be between 0 and 100.")
                return

            for student in self.students:
                if student.student_id == student_id:
                    student.name = name
                    student.grades = grades
                    messagebox.showinfo("Success", f"Updated student with ID {student_id}")
                    self.clear_entries()
                    self.list_students()
                    return

            messagebox.showwarning("Not Found", "Student ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only for ID and grades.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.grades_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
