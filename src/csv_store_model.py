import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datagram_user_model import Datagram_User

class CSVStoreModel(Document):
    business_id = ReferenceField(Datagram_User)
    business_name = StringField(required=True)
    file_path = StringField(required=True)
    date_uploaded = DateTimeField(default=datetime.datetime.utcnow)
    file_summary = StringField(required=True)