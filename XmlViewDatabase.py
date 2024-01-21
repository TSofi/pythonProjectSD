import tkinter as tk
from tkinter import font, ttk, messagebox

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PatientDatabse import *
from PatientProfile import *
from analyse import *


class CreatePatientApp:
    def __init__(self, master, db):
        """
        Constructor Create Patient App view window (displays after running)
                Arguments:
                    - master -- Tkinter window instance
                    - db -- sqlite3 (database) instance

        Returns view window with filedes to assign values to table (db)
        """
        self.master = master
        self.master.title("Patients")
        self.master.geometry("600x550")
        self.master.configure(bg="Skyblue")
        self.master.resizable(False, False)
        self.db = db

        # Title
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        title_label = tk.Label(master, text="Patient Database", font=title_font, background="Skyblue",
                               foreground="White")
        title_label.grid(row=0, column=0, columnspan=3, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Lables for Rows
        labels = ["Doctors ID:", "Full name:", "Pesel:", "Age:", "Sex:", "Disease:", "Medication:"]

        # Loops to adjust labels in window/root
        # Columns
        for i in range(3):
            self.master.columnconfigure(i, weight=1)
        # Rows
        for i in range(len(labels) + 1):
            self.master.rowconfigure(i, weight=1)
        # Putting labels into rows
        for i, label_text in enumerate(labels):
            tk.Label(master, text=label_text, background="Skyblue").grid(row=i + 1, column=0, padx=10, pady=2,
                                                                         sticky=tk.E)

        # Entry boxes
        entry_width = 40
        self.entry_doctors_id = tk.Entry(master, width=entry_width)
        self.entry_full_name = tk.Entry(master, width=entry_width)
        self.entry_pesel = tk.Entry(master, width=entry_width)
        self.entry_age = tk.Entry(master, width=entry_width)
        self.entry_disease = tk.Entry(master, width=entry_width)
        self.entry_medication = tk.Entry(master, width=entry_width)

        # Combobox - sex optional
        self.sex_options = ["Male", "Female", "Other"]
        self.sex_st = tk.StringVar()
        self.sex_combobox = ttk.Combobox(master, textvariable=self.sex_st, values=self.sex_options, state="readonly",
                                         width=38)

        # Create menu bar
        menu = tk.Menu(master)
        master.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', compound='left', underline=0)
        file_menu.add_command(label='Exit', compound='left', underline=0, command=master.quit)
        statistics_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Statistics', menu=statistics_menu)
        statistics_menu.add_command(label='Yearly Submitted Patients', command=self.open_yearly_statistics_window)
        statistics_menu.add_command(label='Statistic Patients Sex', command=self.open_statistic_patients_sex_window)

        # Placing Entry boxes and combobox(sex) in rows
        for i, entry_widget in enumerate(
                [self.entry_doctors_id, self.entry_full_name, self.entry_pesel, self.entry_age, self.sex_combobox,
                 self.entry_disease, self.entry_medication]):
            entry_widget.grid(row=i + 1, column=1, padx=10, pady=2)

        # Creating button to insert values to database
        insert_button = tk.Button(master, text="Insert Data", command=self.check_inserted_data)
        insert_button.grid(row=(len(labels) + 1), column=1, padx=5, pady=10)

    def open_yearly_statistics_window(self):

        """
        Opens the yearly_statistics_window widget and displays vertical bar graph with yearly submitted patients
        """

        data = self.db.get_all_data()
        yearly_stats = calculate_yearly_regist_stats(data)

        yearly_window = tk.Toplevel(self.master)
        yearly_window.title("Yearly Submitted Patients")
        yearly_window.geometry('500x500')
        fig, axis = plt.subplots(figsize=(4, 6))
        years = list(yearly_stats.keys())
        counts = list(yearly_stats.values())
        axis.bar(years, counts)
        axis.set_xlabel('Year')
        axis.set_ylabel('Number of patients')
        axis.set_title('Yearly Submitted Patients')

        canvas = FigureCanvasTkAgg(fig, master=yearly_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def open_statistic_patients_sex_window(self):

        data = self.db.get_all_data()
        gender_stats = calculate_gender_distribution(data)

        sex_window = tk.Toplevel(self.master)
        sex_window.title("Gender Distribution")
        sex_window.geometry('500x500')
        fig, axis = plt.subplots(figsize=(10,10))
        genders = list(gender_stats.keys())
        counts = list(gender_stats.values())

        axis.bar(genders, counts)
        axis.set_xlabel('Gender')
        axis.set_ylabel('Count')
        axis.set_title('Gender Distribution')

        canvas = FigureCanvasTkAgg(fig, master=sex_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand =1)

    def check_inserted_data(self):
        """
        Inserts the data into the database, function inherits function insert_data_database from class PatientDatabase
                and values specified in Entry
        """
        # Assigning values using .get() from window's entries
        full_name = self.entry_full_name.get()
        pesel = self.entry_pesel.get()
        age = self.entry_age.get()
        sex = self.sex_st.get()
        disease = self.entry_disease.get()
        medication = self.entry_medication.get()
        doctors_id = self.entry_doctors_id.get()

        # Checking if all necessary fields are filed
        if not all((full_name, pesel, age, sex)):
            messagebox.showinfo("Error", "Full Name, PESEL, Age and Sex must be field")
            return

        # Checking PESEL as it is primary key (most important value)
        if len(pesel) != 11:
            messagebox.showerror("Error", "Invalid Pesel")

        # If everything checks inserting values using insert_data_database function class PatientDatabase
        else:
            patient = PatientProfile(full_name, pesel, age, sex, disease, medication, doctors_id)
            self.db.insert_data_database(patient)


if __name__ == "__main__":
    db = PatientDatabase(r"C:\Studia\patientDatabase.db")
    db.create_table()

    window = tk.Tk()
    app = CreatePatientApp(window, db)
    window.mainloop()
