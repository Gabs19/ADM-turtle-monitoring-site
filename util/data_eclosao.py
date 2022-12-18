import datetime
import email.message
import time
import smtplib
import schedule
from service import service
from email.message import EmailMessage


def readingDates():

    reports = service.db.child('data-eclosao').get()
    report = reports.val().values()

    for date in report:
        print('inicio')
        data_current = datetime.datetime.now()
        print('func')
        print(data_current)

        data = date['data'].split('GMT-0300')[0].split(' ')
        del data[0]
        del data[4]

        new_date = ' '.join(data)
        data_format = datetime.datetime.strptime(new_date, "%b %d %Y %H:%M:%S")
        next_day = data_format - datetime.timedelta(days=1)

        if data_current.date() == next_day.date():
            send_email()


schedule.every().day.at("00:00").do(readingDates)

def send_email():

    corpo_email = """
        <p>Olá, </p>
        <p>Amanhã será a data marcada para eclosão do ninho</p>
    """

    msg = email.message.Message()
    msg['Subject'] = 'Alerta Eclosão'
    msg['From'] = 'apptartarugasninhos@gmail.com'
    msg['To'] = 'gabriellima.glgs@gmail.com'
    password = 'xequrcgqjplkteqk'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    #login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)