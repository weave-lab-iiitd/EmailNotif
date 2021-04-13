import os
import pickle
import base64
import pyfirmata
import time
#Gmail API utils

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type
from bs4 import BeautifulSoup


"""
    PIN POSITIONS:
    (1) 7 == FALL
    (2) 8 == FLIP
    (3) 9 == BEND
    (4) 10 == DRAG
    (5) 11 == ROTATE

"""


"""
Arduino PyFirmata Code
Main Function initialises the Arduino board
"""
def main():
    
    board = pyfirmata.Arduino('COM5')
    it = pyfirmata.util.Iterator(board)
    it.start()
    SERVO_MOTOR = 9
    END = 180


    servo_pin1 = board.get_pin('d:7:s')  # FALL
    servo_pin2 = board.get_pin('d:8:s')  # FLIP
    servo_pin3 = board.get_pin('d:9:s')  # BEND
    servo_pin4 = board.get_pin('d:10:s') # DRAG
    servo_pin5 = board.get_pin('d:11:s') # ROTATE
    #servo_pin.write(0)
    #time.sleep(2)
    board.servo_config(SERVO_MOTOR, 544,2400,0)
    #servo_pin.write(90)

    """
    for i in range(0, END):
        servo_pin.write(i)
        time.sleep(.015)
        #time.sleep(.5)

    for j in range(END, 0, -1):
        servo_pin.write(j)
        time.sleep(.015)
        #time.sleep(.5)
    """

    """
    while True:
        board.digital[9].write(1)
        time.sleep(3)
        board.digital[13].write(0)
        time.sleep(3)
    """
    # Request all access (permission to read/send/receive emails, manage the inbox, and more)
    SCOPES = ['https://mail.google.com/']
    our_email = 'notiwall@2021.gmail.com'
    gmail_authenticate()


    # =============== FALL MOTION, IMP MESSAGE ======================
    imp_mssg = search_messages(service, 'from:aryan15134@iiitd.ac.in OR from:saini.aaaryan@gmail.com')
    imp_txt = service.users().messages().get(userId='me', id=imp_mssg[0]['id']).execute()
    imp_payload = imp_txt['payload']
    imp_headers = imp_payload['headers']
    for d in imp_headers:
        if d['name'] == 'Subject':
            imp_subject = d['value']
            print("Important Mail Subject: ", imp_subject)
        if d['name'] == 'From':
            imp_sender = d['value']
            print("Important Mail Sender: ", imp_sender)
            #print(sender)
    imp_parts = imp_payload.get('parts')[0]
    print("FALL MOVEMENT")
    print("============================================================")
    servo_pin1.write(0)
    # ================ FALL MOTION, IMP MESSAGE =======================

    # ================ FLIP MOTION, CANCELED EVENT ====================
    cancel_mssg = search_messages(service, 'subject: Canceled event')
    cancel_txt = service.users().messages().get(userId='me', id=cancel_mssg[0]['id']).execute()
    cancel_payload = cancel_txt['payload']
    cancel_headers = cancel_payload['headers']
    for d in cancel_headers:
        if d['name'] == 'Subject':
            cancel_subject = d['value']
            print("Canceled Event Subject: ", cancel_subject)
        if d['name'] == 'From':
            cancel_sender = d['value']
            #print("Important Mail Sender: ", imp_sender)
            print("Sender is : ", cancel_sender)
    cancel_parts = cancel_payload.get('parts')[0]
    print("FLIP MOVEMENT")
    print("============================================================")
    servo_pin2.write(180)
    # ================ FLIP MOTION, CANCELED EVENT ==================== 

    # ================= ROTATE MOTION, UPCOMING MEETING TIME ==========
    meeting_mssg = search_messages(service, 'subject: Invitation')
    meeting_txt = service.users().messages().get(userId='me', id=meeting_mssg[0]['id']).execute()
    meeting_payload = meeting_txt['payload']
    meeting_headers = meeting_payload['headers']
    for d in meeting_headers:
        if d['name'] == 'Subject':
            meeting_subject = d['value']
            print("Meeting Subject: ", meeting_subject)
        if d['name'] == 'From':
            meeting_sender = d['value']
            #print("Important Mail Sender: ", imp_sender)
            print("Meeting Invitation Sender is : ", meeting_sender)
    meeting_parts = cancel_payload.get('parts')[0]
    print("ROTATION MOVEMENT")
    meeting_subject = meeting_subject.split()
    for i in range(0, len(meeting_subject)):
        if('pm' in meeting_subject[i]):
            meeting_index = i
            #print(t1)
            break
    meeting_time = (meeting_subject[meeting_index].split('pm'))[0]
    print(meeting_time)
    #print(meeting_time.split(':'))
    meeting_time = meeting_time.split(":")
    meeting_hours = int(meeting_time[0])
    meeting_min = int(meeting_time[1])
    print("Hours: ", meeting_hours, " Min: ", meeting_min)
    print("============================================================")
    #servo_pin5.write(180)


    # ================= ROTATE MOTION, UPCOMING MEETING TIME ==========


    #mssgs = search_messages(service, 'from:calendar-notification@google.com OR from:aryan15134@iiitd.ac.in OR from:saini.aaaryan@gmail.com OR from:paras15154@iiitd.ac.in')
    

    # ============= BEND MOTION, LABEL MESSAGE ========================
    
    label_msg = search_messages(service, 'label:Label1')
    if label_msg is not None:
        print("label_msg[0] is: ", label_msg[0])
        label_txt = service.users().messages().get(userId='me', id=label_msg[0]['id']).execute()
        label_payload = label_txt['payload']
        label_headers = label_payload['headers']
        for p in label_headers:
            if p['name'] == 'Subject':
                label_subject = p['value']
                print("Subject of labelled email is: ", label_subject)
            if p['name'] == 'From':
                label_sender = p['value']
                print("Sender of labelled email is: ", label_sender)
        print("BEND Movement");
        print("============================================================")
        servo_pin3.write(180)
    # =============== BEND MOTION, LABEL MESSAGE =======================

    """
    txt = service.users().messages().get(userId='me', id=mssgs[0]['id']).execute()
    payload = txt['payload']
    headers = payload['headers']
    for d in headers:
        if d['name'] == 'Subject':
            subject = d['value']
            print("Subject: ", subject)
        if d['name'] == 'From':
            sender = d['value']
            print("Sender: ", sender)
            #print(sender)
    parts = payload.get('parts')[0]
 
    if 'Canceled' in subject:
        # FLIP Movement
        print("Meeting has been Canceled")
        servo_pin2.write(180)

     # FALL Movement
    if 'paras15154@iiitd.ac.in' in sender :
        print("Received email from sender ", sender)
        print("FALL MOVEMENT")
        servo_pin1.write(0)

    if 'Notification' in subject:
        # ROTATE movement
        print("Received Meeting Reminder for 5 min")
        for i in range(0,30):
            servo_pin5.write(17)
            time.sleep(0.0467)
            servo_pin.write(20)
            time.sleep(10)

    if 'Invitation' in subject:
        print("Received Meeting Invitation")
        subject = subject.split()
        #print(subject)
        for i in range(0, len(subject)):
            if('pm' in subject[i]):
                t1 = i
                #print(t1)
                break
        meeting_time = (subject[t1].split('pm'))[0]
        print(meeting_time)

    """




def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(destination, obj, body, attachments=[]):
    if not attachments: # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
        message.attach(MIMEText(body))
    for filename in attachments:
        add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
    userId="me",
    body=build_message(destination, obj, body, attachments)
    ).execute()

    # test send email
#send_message(service, "paras15154@iiitd.ac.in", "This is a subject", 
#            "This is the body of the email", ["test.txt"])

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


"""

#mssgs = search_messages(service, 'from:calendar-notification@google.com OR from:aryan15134@iiitd.ac.in OR from:saini.aaaryan@gmail.com OR from:paras15154@iiitd.ac.in')

# the below is for rotation
#mssgs = search_messages(service, 'from:calendar-notification@google.com')

#print(mssgs)
#print("type: ", mssgs)
count = 0
#print(len(mssgs))
print("mssg[0] is: ", end=" ")
print(mssgs[0])
txt = service.users().messages().get(userId='me', id=mssgs[0]['id']).execute()
payload = txt['payload']
#print("payload: ", end=" ")
#print(payload)
headers = payload['headers']
#print(headers)
for d in headers:
    if d['name'] == 'Subject':
        subject = d['value']
        print("Subject: ", subject)
    if d['name'] == 'From':
        sender = d['value']
        print("Sender: ", sender)
        #print(sender)
parts = payload.get('parts')[0]
#print("Parts: ", parts['body'])
#data = parts['body']['data']
#data = data.replace("-","+").replace("_","/")
#decoded_data = base64.b64decode(data)
#print("Decoded data is: ", decoded_data)

#soup = BeautifulSoup(decoded_data , "lxml")
#body = soup.body()
#print(body)

if 'Canceled' in subject:
    # FLIP Movement
    print("Meeting has been Canceled")
    servo_pin.write(180)

if 'aryan15134@iiitd.ac.in' in sender :
    print("Received email from sender ", sender)
    # FALL Movement
    servo_pin.write(180)

if 'Notification' in subject:
    # ROTATE movement
    print("Received Meeting Reminder for 5 min")
    for i in range(0,30):
        servo_pin.write(17)
        time.sleep(0.0467)
        servo_pin.write(20)
        time.sleep(10)
"""


"""
for msg in mssgs:
    txt = service.users().messages().get(userId='me', id=msg['id']).execute()
    #print("count: " + str(count))
    count += 1
    # Use try-except to avoid any Errors
    try:
        # Get value of 'payload' from dictionary 'txt'
        payload = txt['payload']
        headers = payload['headers']
        #print(headers)

        # Look for Subject and Sender Email in the headers
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
                #print(subject)
            if d['name'] == 'From':
                sender = d['value']

        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)

        # Now, the data obtained is in lxml. So, we will parse 
        # it with BeautifulSoup library
        soup = BeautifulSoup(decoded_data , "lxml")
        body = soup.body()

        # Printing the subject, sender's email and message
        print("Subject: ", subject)
        print("From: ", sender)
        print("\n")
    except:
        pass
"""

if __name__ == '__main__':
    main()
