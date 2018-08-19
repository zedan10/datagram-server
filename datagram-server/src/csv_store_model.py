import datetime
from mongoengine import Document, StringField, DateTimeField

class CSVStoreModel(Document):
    business_name = StringField(required=True)
    file_path = StringField(required=True)
    date_uploaded = DateTimeField(default=datetime.datetime.utcnow)
    file_summary = StringField(required=True)