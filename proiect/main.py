import datetime
import psycopg2
import time
conn = psycopg2.connect(host="localhost",dbname="postgres",user="postgres",password="1762",port=5432)

cur = conn.cursor()

def create_person(name,age,gender):
    result = cur.execute("""INSERT INTO persons (name,age,gender) VALUES
                (%s,%s,%s);
                """,(name,age,gender))
    if result == None:
        return "Person created succesfully."
    return "An error occurred while creating the person."
    
def create_meeting(start_date,end_date,person_ids):
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
    return "Meeting created succesfully"
    
def meetings_in_interval(start_date, end_date):
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
        print("No meetings in this interval!")
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
    
    for meeting in meetings.values():
        print(f"Meeting ID: {meeting['meeting_id']}, Start Date: {meeting['start_date']}, End Date: {meeting['end_date']}")
        print("Attendees:")
        for attendee in meeting["attendees"]:
            print(f"  ID: {attendee['id']}, Name: {attendee['name']}, Age: {attendee['age']}")
        print()
    
    #return meetings


print(create_person("didi2",30,"b"))

tobj = time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S",tobj)
end_time =  time.strftime("%Y-%m-%d %H:%M:%S",tobj)
print(create_meeting(start_time,end_time,[1,2]))

meetings_in_interval("2023-01-01 12:12:12",end_time)


#conn.commit()
cur.close()
conn.close()