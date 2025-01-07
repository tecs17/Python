import datetime
from datetime import datetime
import psycopg2
import time
import tkinter as tk
from tkinter import messagebox,ttk


conn = psycopg2.connect(host="localhost",dbname="postgres",user="postgres",password="1762",port=5432)

cur = conn.cursor()

def db_create_person(name,age,gender):
    result = cur.execute("""INSERT INTO persons (name,age,gender) VALUES
                (%s,%s,%s);
                """,(name,age,gender))
    if result == None:
        conn.commit()
        return "Person created succesfully."
    return "An error occurred while creating the person."

def db_get_all_persons():
    result = cur.execute("""SELECT id,name,age FROM persons;""")
    rows = cur.fetchall()
    persons = []
    for row in rows:
        persons.append(row)
    return persons

def db_create_meeting(start_date,end_date,person_ids):
    #fac checkuri pentru date incorecte inainte
    result = cur.execute("""INSERT INTO meetings (start_date,end_date) VALUES
                (%s,%s)
                RETURNING id; 
                """, (start_date,end_date))
    if result != None:
        return "An error occurred while creating the meeting."
    
    inserted_meeting_id = cur.fetchone()[0]
    for person_id in person_ids:
        result = cur.execute(""" INSERT INTO meetings_persons(meeting_id,person_id) VALUES
                    (%s,%s);
                     """,(inserted_meeting_id,person_id))
        if result != None:
            return f"An error occurred while creating the meeting-person entry for person_id = {person_id}."
    conn.commit()
    return "Meeting created succesfully"
    
def db_meetings_in_interval(start_date, end_date):
    cur.execute("""
        SELECT 
            m.id AS meeting_id, m.start_date, m.end_date,
            p.id AS person_id, p.name AS person_name, p.age AS person_age
        FROM 
            meetings m
        LEFT JOIN 
            meetings_persons mp ON m.id = mp.meeting_id
        LEFT JOIN 
            persons p ON mp.person_id = p.id
        WHERE 
            m.start_date >= %s AND m.end_date <= %s
        ORDER BY 
            m.id;
    """, (start_date, end_date))
    
    rows = cur.fetchall()
    
    if len(rows) == 0:  
        return
    
    meetings = {}
    for row in rows:
        meeting_id = row[0]
        if meeting_id not in meetings:
            meetings[meeting_id] = {
                "meeting_id": row[0],
                "start_date": row[1],
                "end_date": row[2],
                "attendees": []
            }
        if row[3]:  
            meetings[meeting_id]["attendees"].append({
                "id": row[3],
                "name": row[4],
                "age": row[5]
            })    
    return meetings

def main_menu():
    def open_add_person():
        root.destroy()
        add_person_window()

    def open_create_meeting():
        root.destroy()
        create_meeting_window()

    def open_print_meetings():
        root.destroy()
        print_meetings_window()

    root = tk.Tk()
    root.geometry("300x140")
    root.title("Meeting Scheduler")

    tk.Button(root, text="Add a Person", command=open_add_person, width=20).pack(pady=10)
    tk.Button(root, text="Create a Meeting", command=open_create_meeting, width=20).pack(pady=10)
    tk.Button(root, text="Print Meetings in Interval", command=open_print_meetings, width=20).pack(pady=10)
    
    root.mainloop()

def add_person_window():
    def back_to_main():
        add_person.destroy()
        main_menu()

    def submit_person():
        name = name_entry.get()
        age = age_entry.get()
        gender = gender_var.get()
        
        if not name or not age or not gender:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return

        result = db_create_person(name, age, gender)
        messagebox.showinfo("Result", result)

    add_person = tk.Tk()
    add_person.geometry("280x180")
    add_person.title("Add a Person")
    
    tk.Label(add_person, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_person)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(add_person, text="Age:").grid(row=1, column=0, padx=10, pady=5)
    age_entry = tk.Entry(add_person)
    age_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(add_person, text="Gender:").grid(row=2, column=0, padx=10, pady=5)
    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(add_person, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_dropdown.grid(row=2, column=1, padx=10, pady=5)
    
    submit_button = tk.Button(add_person, text="Submit", command=submit_person)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)
    back_button = tk.Button(add_person, text="Back", command=back_to_main)
    back_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    add_person.mainloop()

def create_meeting_window():
    persons_in_db = db_get_all_persons()

    def back_to_main():
        create_meeting.destroy()
        main_menu()

    def submit_meeting():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        selected_persons = [person[0] for idx, person in enumerate(persons_in_db) if person_vars[idx].get()]
        
        if not start_date or not end_date or not selected_persons:
            messagebox.showerror("Error", "All fields must be filled and at least one person must be selected!")
            return
        
        format = "%Y-%m-%d %H:%M"
        try:
            temp_start_time_obj = datetime.strptime(start_date, format)
            temp_end_time_obj = datetime.strptime(end_date, format)
            today = datetime.now()
            if temp_start_time_obj < today and temp_end_time_obj < today:
                messagebox.showerror("Error", "Start Date and End Date must be in the future!")
                return
            time_diff = (temp_end_time_obj - temp_start_time_obj).total_seconds() 
            if time_diff < 0:
                messagebox.showerror("Error", "Start Date must be before End Date!")
                return
            if time_diff > 28800: #8*60*60 - 8 ore in sec
                messagebox.showerror("Error", "A meeting cannot exceed 8 hours!")
                return
        except ValueError:
            messagebox.showerror("Error", "Date format not respected!")
            return
        

        
        result = db_create_meeting(start_date, end_date, selected_persons)
        messagebox.showinfo("Result", result)
        

    create_meeting = tk.Tk()
    create_meeting.title("Create a Meeting")
    
    tk.Label(create_meeting, text="Start Date (YYYY-MM-DD HH:MM):").grid(row=0, column=0, padx=10, pady=5)
    start_date_entry = tk.Entry(create_meeting)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(create_meeting, text="End Date (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
    end_date_entry = tk.Entry(create_meeting)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(create_meeting, text="Select Attendees:").grid(row=2, column=0, columnspan=2, pady=5)

    frame = tk.Frame(create_meeting)
    frame.grid(row=3, column=0, columnspan=2)
    canvas = tk.Canvas(frame, width=300, height=200)
    scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    list_frame = tk.Frame(canvas)
    
    person_vars = []
    for person in persons_in_db:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(list_frame, text=f"{person[1]} (Age: {person[2]})", variable=var)
        chk.pack(anchor="w")
        person_vars.append(var)
        
    canvas.create_window((0, 0), window=list_frame, anchor="nw")
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    
    submit_button = tk.Button(create_meeting, text="Submit", command=submit_meeting)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)
    back_button = tk.Button(create_meeting, text="Back", command=back_to_main)
    back_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    create_meeting.mainloop()

def print_meetings_window():
    def back_to_main():
        print_meetings.destroy()
        main_menu()

    def fetch_meetings():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Both start and end dates must be filled!")
            return

        format = "%Y-%m-%d %H:%M"
        try:
            time_diff = ( datetime.strptime(end_date, format) - datetime.strptime(start_date, format)).total_seconds() 
            if time_diff < 0:
                messagebox.showerror("Error", "Start Date must be before End Date!")
                return
        except ValueError:
            messagebox.showerror("Error", "Date format not respected!")
            return

        meetings = db_meetings_in_interval(start_date, end_date)
        if not meetings:
            messagebox.showinfo("Result", "No meetings found in the specified interval.")
        else:
            print_meetings.destroy()  
            result_window = tk.Tk()
            result_window.title("Meetings")

            def back_to_print_meetings():
                result_window.destroy()
                print_meetings_window()

            frame = tk.Frame(result_window)
            frame.pack(fill="both", expand=True)
            canvas = tk.Canvas(frame)
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for meeting in meetings.values():
                tk.Label(scrollable_frame, text=f"Meeting ID: {meeting['meeting_id']}", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
                tk.Label(scrollable_frame, text=f"Start Date: {meeting['start_date']}").pack(anchor="w")
                tk.Label(scrollable_frame, text=f"End Date: {meeting['end_date']}").pack(anchor="w")
                tk.Label(scrollable_frame, text="Attendees:").pack(anchor="w")
                for attendee in meeting["attendees"]:
                    tk.Label(scrollable_frame, text=f"  - {attendee['name']} (Age: {attendee['age']})").pack(anchor="w")
                tk.Label(scrollable_frame, text="").pack()

            tk.Button(result_window, text="Back", command=back_to_print_meetings).pack(pady=10)

            result_window.mainloop()


    print_meetings = tk.Tk()
    print_meetings.title("Print Meetings in Interval")
    
    tk.Label(print_meetings, text="Start Date (YYYY-MM-DD HH:MM):").grid(row=0, column=0, padx=10, pady=5)
    start_date_entry = tk.Entry(print_meetings)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(print_meetings, text="End Date (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
    end_date_entry = tk.Entry(print_meetings)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5)
    
    fetch_button = tk.Button(print_meetings, text="Fetch Meetings", command=fetch_meetings)
    fetch_button.grid(row=2, column=0, columnspan=2, pady=10)
    back_button = tk.Button(print_meetings, text="Back", command=back_to_main)
    back_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    print_meetings.mainloop()


main_menu()

conn.commit()
cur.close()
conn.close()
