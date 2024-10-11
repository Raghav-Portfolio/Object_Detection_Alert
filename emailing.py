import smtplib
import imghdr
from email.message import EmailMessage

#Enter sender's email_ID:
sender = ''
#Enter your app password:
password = '' 
#Enter receiver's email_ID:
receiver = ''


def send_email(image_path):
    print('send_email has started')
    email_message = EmailMessage() # this object behaves like a dictionary
    email_message['Subject'] = 'A new customer has entered'
    email_message.set_content('Hey, we just got a new customer')
    
    with open(image_path, 'rb') as file:
        content = file.read() 
    
    email_message.add_attachment(content, maintype = 'image', subtype = imghdr.what(None, content))
    
    gmail = smtplib.SMTP('smtp.gmail.com', port = 587) 
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password=password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()    
    print('send_email has ended')
if __name__ == '__main__':
    send_email(image_path='images/19.png')