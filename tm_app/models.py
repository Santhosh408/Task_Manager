from django.db.models import CharField, Model, TextField, ForeignKey, CASCADE
from django.contrib.auth.models import User

class Task(Model):
    PRIORITY_CHOICES = [
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low')
    ]
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    ]
    title = CharField(max_length=255)
    description = TextField()
    priority = CharField(max_length=10,choices=PRIORITY_CHOICES)
    status = CharField(max_length=15,choices=STATUS_CHOICES)
    username = ForeignKey(User,on_delete=CASCADE,related_name='tasks')
    # username = CharField(max_length=100)

    def __str__(self):
        return self.title