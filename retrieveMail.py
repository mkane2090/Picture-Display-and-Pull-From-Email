# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.

import email, imaplib, os
from datetime import datetime

def updateAttachments():
    print(f'Checking for new mail: {datetime.now()}')
    # Directory to place photos pulled from email
    detach_dir = './Images'

    # Email address and app single signon password for the receiving email
    userName = ''   # Enter your email address into this string
    passwd = ''     # You must generate an app single signon password for your email and store it here

    # Signin to the gmail using the above username and password
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)

    # Check that signon was successful
    if typ != 'OK':
        print('Not able to sign in!')
        raise
    
    imapSession.select('Inbox')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
        print('Error searching Inbox.')
        raise
        
    # Iterating over all emails
    for msgId in data[0].split():
        #print(msgId)
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()

            if bool(fileName):
                # Add message id so that repeating image names do not overwrite each other
                fileName = str(msgId) + fileName
                filePath = os.path.join(detach_dir, fileName)# 'attachments', fileName)
                if not os.path.isfile(filePath):
                    print(f'Saving new file {filePath}')
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
    #except :
    #    print('Not able to download all attachments.')