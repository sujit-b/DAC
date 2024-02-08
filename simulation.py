import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psycopg2
from datetime import datetime
import time
from twilio.rest import Client
from datetime import datetime, timedelta
account_sid = 'ACc15cb0d6aa7c23d0f91b4d739d7f8a83'
auth_token = '12d229001d3170e85f661f80b940a21b'

client = Client(account_sid, auth_token)


situation_map = {
    0: ([], 0),
    1: ([1, 3], 3),
    2: ([5], 1),
    3: ([3], 1),
    4: ([2], 3),
    5: ([0, 2], 3),
    6: ([2], 2),
    7: ([0, 1, 2, 3, 4, 5], 4),
    8: ([4], 4),
}

Situation ={
    0:"No-Situation",
    1:"Signal Break",
    2:"Supply Low",
    3:"Maintainence Alarm",
    4:"Chemical Spill",
    5:"Gas Leak Detected",
    6:"Fire Alarm",
    7:"Intrusion Alert",
    8:"General Hazard",
    9:"Employee Brawl",
    10:"Pest and Animal Control"
}
actions={
0:"Normal",
1:"Tech Support Assistance Required",
2:"Check Inventory and Resupply",
3:"Perform Regular Maintainence",
4:"Clean up and alert fire dept. immediately",
5:"Check and fix leakage",
6:"Alert Fire Department Authority",
7:"Check Security and Alert Police",
8:"Ring Alarm and Evacuate",
9:"Call Security Guards",
10:"Call Pest Control and Animal Shelter"
}
Roles={
    0:"Security",
    1:"Manufacturing Engineer",
    2:"Fire Authority",
    3:"Supervisor",
    4:"Security",
    5:"Inventory Manager",
    6:"IT Specialist"
}

Priorities={
    0:"No Priority",
    1:"Low",
    2:"Medium",
    3:"High",
    4:"Very High"
}

employees={
"c0:e8:62:e6:cc:e4":(3, 51.45984385,-0.932728353,0,"+12134217536"),
"88:b4:a6:67:4a:6d":(3, 51.45995792,-0.932447075,2,"+12134217536"),
"98:ca:33:b5:26:b6":(3, 51.45985812,-0.932665255,3,"+12134217536"),
"88:66:a5:8f:bb:ad":(3, 51.45975269,-0.932427203,4,"+12134217536"),
"3c:28:6d:18:27:6d":(3, 51.46015383,-0.932735759,5,"+12134217536"),
"84:c7:ea:97:91:f2":(2, 51.45974519,-0.932598167,0,"+12134217536"),
"cc:25:ef:86:61:bf":(1, 51.45954663,-0.932693041,0,"+12134217536"),
"88:66:a5:8f:a7:85":(2, 51.45972256,-0.932463938,1,"+12134217536"),
"38:78:62:ec:78:16":(2, 51.45978596,-0.932545479,1,"+12134217536"),
"6c:96:cf:c3:45:4f":(1, 51.46019227,-0.932629096,2,"+12134217536"),
"88:66:a5:33:9f:c2":(1, 51.45989368,-0.932353664,2,"+12134217536"),
"40:4e:36:86:9c:12":(3, 51.45972704,-0.932683136,3,"+12134217536"),
"74:b5:87:5e:67:02":(3, 51.46010886,-0.932288045,3,"+12134217536"),
"80:58:f8:38:3c:47":(3, 51.4602041,-0.932695147 ,4,"+12134217536"),
"50:a6:7f:6f:9f:e1":(3, 51.46017548,-0.932647019,4,"+12134217536"),
"5c:f7:e6:e7:ff:62":(2, 51.46019626,-0.932331524,5,"+12134217536"),
"8c:8e:f2:b1:14:ee":(1, 51.46007976,-0.932290362,2,"+12134217536"),
"c0:e8:62:01:15:2e":(1, 51.45968135,-0.932639904,2,"+12134217536"),
"64:a2:f9:30:4f:8c":(3, 51.45983847,-0.932633624,1,"+12134217536")

}


def send_email(subject, body, to_email):
    from_email = "saisujitb333"  # email address
    password = ""  # email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # SMTP server details
    server.ehlo()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)



def get_closet_employee(role_list):
    compatible_employees=[]
    #distances = []
    for key in employees.keys():
        role=employees.get(key)[3]
        if role in role_list:
            compatible_employees.append(key)
        else:
            continue
    for employee in compatible_employees:
        distances=[]
        distances.append(distance(employees.get(employee)[1],employees.get(employee)[1],final_list[0],final_list[1]))
    compatible_employee=compatible_employees[distances.index(min(distances))]
    return(compatible_employee)

def get_contact(employee_key):
    return (employees.get(employee_key)[4])

def generate_work_order(situation):
    job_roles, priority = situation_map.get(situation, ([], 0))
    responsible_employee = get_closet_employee(job_roles)
    contact = get_contact(responsible_employee)
    text = "\nSituation:" + Situation.get(situation) + "\nAction Required:" + actions.get(situation) + "\nEmployee Role:" + Roles.get(job_roles[0]) + "\nContact number" + contact + "\nPriority:" + Priorities.get(priority)

    # Sending SMS via Twilio
    message = client.messages.create(
        from_='+18334321231',
        body=text,
        to=contact
    )
    print("SMS sent:", text)

    # Sending email via smtplib
    email_subject = f"Emergency Situation: {Situation.get(situation)}"
    email_body = f"Situation: {Situation.get(situation)}\nAction Required: {actions.get(situation)}\nEmployee Role: {Roles.get(job_roles[0])}\nContact number: {contact}\nPriority: {Priorities.get(priority)}"

    send_email(email_subject, email_body, "bayanabo@usc.edu")  # recipient's email address
    send_email(email_subject, email_body, "tianluny@usc.edu")
    send_email(email_subject, email_body, "dbagadia@usc.edu")
    send_email(email_subject, email_body, "luyingca@usc.edu")
    send_email(email_subject, email_body, "shuruipa@usc.edu")
    send_email(email_subject, email_body, "yongbiny@usc.edu")
    send_email(email_subject, email_body, "junweiz@usc.edu")
    send_email(email_subject, email_body, "guanyuz@usc.edu")
    send_email(email_subject, email_body, "feifanwe@usc.edu")
    print("Email sent:", email_body)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    
    host="127.0.0.1",
    database="kiana",
    user="postgres",
    password="GETIN@postgres1209"
)

#  cursor object to execute queries
cur = conn.cursor()

# Get the timestamp of the last query from a separate table or variable
last_query_timestamp = datetime(2023, 11, 21, 0, 0, 0)

#  query to select newly added rows since the last query, or all rows if first query
while True:
    if last_query_timestamp is None:
        query = "SELECT * FROM stimuli_devices"
    else:
        query = f"SELECT * FROM stimuli_devices WHERE time_stamp > '{last_query_timestamp}'"

# fetch the results
    cur.execute(query)
    results = cur.fetchall()


    for row in results:
        if row[4]!= 0:
            final_list=(float(row[2]),float(row[3]))
            generate_work_order(row[4])
        else:
            continue
# If this is the first query, store the current timestamp in a separate table or variable
    if last_query_timestamp is None:
        last_query_timestamp = datetime.utcnow() - timedelta(seconds=10)  # assuming a 10s window before script execution
    # storing last_query_timestamp in a separate table or variable for future queries
    last_query_timestamp = datetime.utcnow() - timedelta(seconds=10)
    time.sleep(5)
# Close the cursor and connection
cur.close()
conn.close()
