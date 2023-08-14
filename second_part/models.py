from mongoengine import Document
from mongoengine.fields import BooleanField, StringField, ListField, ReferenceField

class Contact(Document):
    fullname = StringField()
    email = StringField()
    status = BooleanField(default=False)
    