import psycopg2
from firebase_admin import credentials, firestore, initialize_app
import smtplib, ssl
from email.mime.text import MIMEText
from google.cloud import firestore

cred = credentials.Certificate('cred.json')
initialize_app(cred)

db = firestore.client()
user_ref = db.collection('students')
posts_ref = db.collection('posts')

def post_email(data, context):
    post_data = data['value']['fields']
    if 'title' in post_data and 'content' in post_data:
        users = [user.to_dict().get('email') for user in user_ref.stream()]
        msg = MIMEText(f"A new post '{post_data['title']['stringValue']}' has been created.\n\n{post_data['content']['stringValue']}")
        msg['Subject'] = 'New post created'
        msg['From'] = 'theashesinetwork@gmail.com'
        msg['To'] = ", ".join(users)
        ssl_context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=ssl_context) as smtp:
            
            smtp.send_message(msg)
