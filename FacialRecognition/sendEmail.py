import smtplib

def send_mail(recv_email,pswd):
    sender_email='AchyuthKowshik@pesu.pes.edu'
    sender_pswd='#####'

    msg=f"Your password to login to the Attendance GUI is {pswd}.\nDO NOT SHARE THIS WITH ANY ONE."

    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email,sender_pswd)
        smtp.sendmail(sender_email,recv_email,msg)
        