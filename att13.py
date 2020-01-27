from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import psycopg2
import datetime

conn = psycopg2.connect(host="localhost",database="ivat_database", user="odoo", password="krishna321")

tod = datetime.datetime.now()
print("Execution Time : ", tod)
from datetime import datetime
import pytz
from pytz import timezone
format = "%Y-%m-%d %H:%M:%S"
# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
print(now_utc.strftime(format))
# Convert to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
print(now_asia.strftime(format))

from datetime import time

from datetime import date
today = date.today()

def main1():
    cls = conn.cursor()

    #cls.execute("select hr_attendance.check_in,hr_attendance.check_out, hr_attendance.employee_id,hr_employee.name_related from hr_attendance,hr_employee where check_in>='2019-12-27 06:28:31'")#where date = '2019-07-24'shift_in_c ='T' and

    cls.execute("select hr_attendance.check_in,hr_attendance.check_out,hr_employee.name_related from hr_attendance,hr_employee where check_in> timestamp 'today' and hr_attendance.employee_id=hr_employee.id")

    conn.commit()
    m = []
    for x in cls:
        user_tz = pytz.timezone('Asia/Kolkata')
        date_today = pytz.utc.localize(x[0]).astimezone(user_tz)
        print("This is Our date",date_today)
        date = date_today.date()
        day = date.strftime("%A")
        check_in = date_today.time()
        if x[1]:
            date_today1 = pytz.utc.localize(x[1]).astimezone(user_tz)
            check_out = date_today1.time()
            difference = str(date_today1-date_today)
            print("----------------------------------diifference",difference)

        else:
            check_out = None
            date_today1= None
            difference = None

        name = str(x[2])
        m.append(date)
        m.append(day)
        m.append(name)
        m.append(check_in)
        m.append(check_out)
        m.append(difference)
        print(m)
    i = 0
    a1 = []
    while i < len(m):
        a1.append('<tr>   <td>'    + str(m[i]) + ' '  + str(m[i + 1]) +     '</td>' + '<td>'    + str(m[i+2])+  '</td>' + '<td>'    +str(m[i+3])+ '</td>' + '<td>'  +str(m[i+4])+ '</td>'+ '<td>'  +str(m[i+5])+  '</td></tr>')

        i = i + 6

    msg = MIMEMultipart()
    html = """\
    <html>
    <head>
    <style>

         tr,th, td {
         padding: 10px;
         border: 1px solid #666;
        }

    </style>
    </head>
      <body>
           <table style="width:80%; margin:30px auto; border-collapse:collapse;">

           <tr>
            <th>    Login Report </td>
            <th>    Employee Name  </td>

            <th>    Check In      </td>
            <th>    Check Out   </td>
            <th> Total Worked Hours </td>
            </tr>
            """ + " ".join(map(str, a1)) + """
            </table>

      </body>
    </html>
    """
    fromaddr = 'rahul@ivat.com'
    server = smtplib.SMTP('smtp.gmail.com: 587')
    p = 'rahul99@@##'
    subject = "Employee Login Report "
    toaddr = "rahul@ivat.com",
    #toaddr = ["hr@ivat.com","travel@ivat.com","rahulrawatrkt@gmail.com"]
    msg = MIMEMultipart()
    # msg['cc'] = ccaddr
# msg['bcc'] = bccaddr
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    msg['Subject'] = subject
    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # send the message
    server.starttls()
    server.login(fromaddr, p)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("successfully sent early_email  to %s:" % (msg['To']))

def main():
    get_count = conn.cursor()
    get_count.execute("SELECT count(*) from hr_attendance")
    myresult = get_count.fetchone()
    count = myresult[0]
    #print(count)
    #print(type(count))
    if (count > 0):
        main1()
main()
