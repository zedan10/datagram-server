from mongoengine import Document, StringField, BinaryField, DateTimeField
import datetime

class Datagram_User(Document):
    business_email = StringField(required=True, unique=True)
    business_password = BinaryField(required=True)
    business_name = StringField(required=True)
    number = StringField(required=True)
    dg_token = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_accessed = DateTimeField(default=datetime.datetime.utcnow)