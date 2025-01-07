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

def db_create_meeting(start_date,end_date,title,person_ids):
    #fac checkuri pentru date incorecte inainte
    result = cur.execute("""INSERT INTO meetings (start_date,end_date,title) VALUES
                (%s,%s,%s)
                RETURNING id; 
                """, (start_date,end_date,title))
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
            m.id AS meeting_id, m.start_date, m.end_date, m.title,
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
                "title":row[3],
                "attendees": []
            }
        if row[4]:  
            meetings[meeting_id]["attendees"].append({
                "id": row[4],
                "name": row[5],
                "age": row[6]
            })    
    return meetings

def db_get_meeting_by_id(id):
    cur.execute("""
        SELECT 
            m.id AS meeting_id, m.start_date, m.end_date, m.title,
            p.id AS person_id, p.name AS person_name, p.age
        FROM 
            meetings m
        LEFT JOIN 
            meetings_persons mp ON m.id = mp.meeting_id
        LEFT JOIN 
            persons p ON mp.person_id = p.id
        WHERE 
            m.id = %s ;
    """, (id,))
    
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
                "title":row[3],
                "attendees": []
            }
        if row[4]:  
            meetings[meeting_id]["attendees"].append({
                "id": row[4],
                "name": row[5],
                "age": row[6]
            })    
    return meetings

def db_insert_meetings(data):
    for meeting in data:
        uid = meeting["id"]
        start_date = meeting['start_date']
        end_date = meeting['end_date']
        title = meeting['title']
        result = cur.execute("""INSERT INTO meetings (start_date,end_date,title) VALUES
                    (%s,%s,%s); 
                    """, (start_date,end_date,title))
        if result != None:
            return f"An error occurred while importing meeting with uid = {uid}!"
    conn.commit()
    return "Import succesfull"


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
    
    def open_export():
        root.destroy()
        export_window()

    def open_import():
        root.destroy()
        import_window()

    root = tk.Tk()
    root.geometry("300x230")
    root.title("Meeting Scheduler")

    tk.Button(root, text="Add a Person", command=open_add_person, width=20).pack(pady=10)
    tk.Button(root, text="Create a Meeting", command=open_create_meeting, width=20).pack(pady=10)
    tk.Button(root, text="Print Meetings in Interval", command=open_print_meetings, width=20).pack(pady=10)
    tk.Button(root, text="Export", command=open_export, width=20).pack(pady=10)
    tk.Button(root, text="Import", command=open_import, width=20).pack(pady=10)
    
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
        title = title_entry.get()
        selected_persons = [person[0] for idx, person in enumerate(persons_in_db) if person_vars[idx].get()]
        
        if not start_date or not end_date or not title or not selected_persons:
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
        

        
        result = db_create_meeting(start_date, end_date, title, selected_persons)
        messagebox.showinfo("Result", result)
        

    create_meeting = tk.Tk()
    create_meeting.title("Create a Meeting")
    
    tk.Label(create_meeting, text="Start Date (YYYY-MM-DD HH:MM):").grid(row=0, column=0, padx=10, pady=5)
    start_date_entry = tk.Entry(create_meeting)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(create_meeting, text="End Date (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
    end_date_entry = tk.Entry(create_meeting)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(create_meeting, text="Title:").grid(row=2, column=0, padx=10, pady=5)
    title_entry = tk.Entry(create_meeting)
    title_entry.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(create_meeting, text="Select Attendees:").grid(row=3, column=0, columnspan=2, pady=5)

    frame = tk.Frame(create_meeting)
    frame.grid(row=4, column=0, columnspan=2)
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
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)
    back_button = tk.Button(create_meeting, text="Back", command=back_to_main)
    back_button.grid(row=6, column=0, columnspan=2, pady=10)
    
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
                tk.Label(scrollable_frame, text=f"Title: {meeting['title']}").pack(anchor="w")
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

def import_from_ics(file_name):
    file_name+=".ics"
    try:
        meetings = []
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        meeting = {}
        for line in lines:
            line = line.strip()
            if line.startswith("BEGIN:VEVENT"):
                meeting = {}
            elif line.startswith("UID:"):
                meeting["id"] = line.split(":")[1]
            elif line.startswith("DTSTART:"):
                meeting["start_date"] = datetime.strptime(line.split(":")[1], "%Y%m%dT%H%M%S")
            elif line.startswith("DTEND:"):
                meeting["end_date"] = datetime.strptime(line.split(":")[1], "%Y%m%dT%H%M%S")
            elif line.startswith("SUMMARY:"):
                meeting["title"] = line.split(":")[1]
            elif line.startswith("ATTENDEE:"):
                if "attendees" not in meeting:
                    meeting["attendees"] = []
                meeting["attendees"].append(line.split(":")[1])
            elif line.startswith("END:VEVENT"):
                meetings.append(meeting)
        
        return meetings
    except Exception as e:
        return e

from pathlib import Path

def import_window():
    def back_to_main():
        import_widget.destroy()
        main_menu()

    def import_meeting():
        filename = filename_entry.get()
        if not filename:
            messagebox.showerror("Error", "No filename provided!")
            return
        my_file = Path("./"+filename+".ics")
        if not my_file.is_file():
            messagebox.showerror("Error", "File doesn`t exist!")
            return
        import_data = import_from_ics(filename)
        if not isinstance(import_data,list):
            messagebox.showerror("Error", import_data)
        # check pt datetime
        try:
            format = "%Y-%m-%d %H:%M"
            for meeting in import_data:
                id = meeting['id']
                start_date = meeting['start_date']
                end_date = meeting['end_date']
                time_diff = ( end_date - start_date).total_seconds() 
                if time_diff < 0:
                    messagebox.showerror("Error", f"Meeting with UID {id} has DTEND before DTSTART!")
                    return
                today = datetime.now()
                time_diff = (end_date - start_date).total_seconds() 
                if time_diff > 28800: #8*60*60 - 8 ore in sec
                    messagebox.showerror("Error", "A meeting cannot exceed 8 hours!")
                    return
        except ValueError:
            messagebox.showerror("Error", "Date format not respected!")
            return

        except ValueError:
            messagebox.showerror("Error", "Date format not respected!")
            return

        result = db_insert_meetings(import_data)
        messagebox.showinfo("Result", result)

    import_widget = tk.Tk()
    import_widget.title("Import")

    tk.Label(import_widget, text="Filename:").grid(row=0, column=0, padx=10, pady=5)
    filename_entry = tk.Entry(import_widget)
    filename_entry.grid(row=0, column=1, padx=10, pady=5)

    import_button = tk.Button(import_widget, text="Import", command=import_meeting)
    import_button.grid(row=1, column=0, columnspan=2, pady=10)

    back_button = tk.Button(import_widget, text="Back", command=back_to_main)
    back_button.grid(row=2, column=0, columnspan=2, pady=10)

    import_widget.mainloop()

def export_to_ics(meetings, file_name):
    file_name += ".ics"
    try:
        with open(file_name, "w") as f:
            f.write("BEGIN:VCALENDAR\n")
            f.write("VERSION:2.0\n")
            
            for meeting in meetings.values():
                f.write("BEGIN:VEVENT\n")
                f.write(f"UID:meeting_{meeting['meeting_id']}\n")
                f.write(f"DTSTART:{meeting['start_date'].strftime('%Y%m%dT%H%M%S')}\n")
                f.write(f"DTEND:{meeting['end_date'].strftime('%Y%m%dT%H%M%S')}\n")
                f.write(f"SUMMARY:{meeting['title']}\n")
                for attendee in meeting["attendees"]:
                    f.write(f"ATTENDEE:{attendee['name']}\n")
                f.write("END:VEVENT\n")
            
            f.write("END:VCALENDAR\n")
        return "Export successful!"
    except Exception as e:
        return f"Error during export: {e}"

def export_by_id_window():
    def back_to_export():
        export_by_id_widget.destroy()
        export_window()

    def export_meeting():
        meeting_id = meeting_id_entry.get()
        filename = filename_entry.get()
        if not meeting_id or not filename:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        try:
            meeting_id = int(meeting_id)
        except ValueError:
            messagebox.showerror("Error", "ID must be a number!")
            return
        meetings = db_get_meeting_by_id(meeting_id)
        if not meetings:
            messagebox.showerror("Error", f"Meeting with id {meeting_id} doesn`t exist!")
            return
        result = export_to_ics(meetings,filename)
        messagebox.showinfo("Result", result)
  
    export_by_id_widget = tk.Tk()
    export_by_id_widget.title("Export by id")

    tk.Label(export_by_id_widget, text="Meeting ID:").grid(row=0, column=0, padx=10, pady=5)
    meeting_id_entry = tk.Entry(export_by_id_widget)
    meeting_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(export_by_id_widget, text="File Name:").grid(row=1, column=0, padx=10, pady=5)
    filename_entry = tk.Entry(export_by_id_widget)
    filename_entry.grid(row=1, column=1, padx=10, pady=5)

    export_button = tk.Button(export_by_id_widget, text="Export", command=export_meeting)
    export_button.grid(row=2, column=0, columnspan=2, pady=10)

    back_button = tk.Button(export_by_id_widget, text="Back", command=back_to_export)
    back_button.grid(row=3, column=0, columnspan=2, pady=10)

    export_by_id_widget.mainloop()

def export_by_interval_window():
    def back_to_export():
        export_by_interval_widget.destroy()
        export_window()

    def export_meetings():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        filename = filename_entry.get()
        if not start_date or not end_date or not filename:
            messagebox.showerror("Error", "All fields must be filled!")
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
            return
        result = export_to_ics(meetings,filename)
        messagebox.showinfo("Result", result)
  
    export_by_interval_widget = tk.Tk()
    export_by_interval_widget.title("Export by interval")

    tk.Label(export_by_interval_widget, text="Start Date (YYYY-MM-DD HH:MM):").grid(row=0, column=0, padx=10, pady=5)
    start_date_entry = tk.Entry(export_by_interval_widget)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(export_by_interval_widget, text="End Date (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
    end_date_entry = tk.Entry(export_by_interval_widget)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(export_by_interval_widget, text="File Name:").grid(row=2, column=0, padx=10, pady=5)
    filename_entry = tk.Entry(export_by_interval_widget)
    filename_entry.grid(row=2, column=1, padx=10, pady=5)

    export_button = tk.Button(export_by_interval_widget, text="Export", command=export_meetings)
    export_button.grid(row=3, column=0, columnspan=2, pady=10)

    back_button = tk.Button(export_by_interval_widget, text="Back", command=back_to_export)
    back_button.grid(row=4, column=0, columnspan=2, pady=10)

    export_by_interval_widget.mainloop()

def export_window():
    def back_to_main():
        export_widget.destroy()
        main_menu()

    def open_export_by_id():
        export_widget.destroy()
        export_by_id_window()
    
    def open_export_by_interval():
        export_widget.destroy()
        export_by_interval_window()  
    
    export_widget = tk.Tk()
    export_widget.geometry("280x180")
    export_widget.title("Export")
    tk.Button(export_widget, text="Export by id", command=open_export_by_id, width=20).pack(pady=10)
    tk.Button(export_widget, text="Export by interval", command=open_export_by_interval, width=20).pack(pady=10)
    tk.Button(export_widget, text="Back", command=back_to_main, width=20).pack(pady=10)
    
    export_widget.mainloop()

main_menu()

#print(db_insert_meetings(import_from_ics("da")))

conn.commit()
cur.close()
conn.close()
