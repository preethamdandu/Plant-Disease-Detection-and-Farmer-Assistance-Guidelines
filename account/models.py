from django.db import models

class farmer(models.Model):
    fname=models.CharField(max_length=100,default="None")
    lname=models.CharField(max_length=100,default="None")
    pno=models.CharField(max_length=13,default="None")
    village= models.CharField(max_length=20,default="None")
    district= models.CharField(max_length=20,default="None")
    state= models.CharField(max_length=20,default="None")
    uname= models.CharField(max_length=15,default="None")
    pwd= models.CharField(max_length=30,default="None")

class volunteer(models.Model):
    fname=models.CharField(max_length=100,default="None")
    lname=models.CharField(max_length=100,default="None")
    pno=models.CharField(max_length=13,default="None")
    village= models.CharField(max_length=20,default="None")
    district= models.CharField(max_length=20,default="None")
    state= models.CharField(max_length=20,default="None")
    uname= models.CharField(max_length=15,default="None")
    pwd= models.CharField(max_length=30,default="None")
    des=models.TextField()

class vol_comment(models.Model):
    com = models.TextField()
    vol = models.ForeignKey(volunteer, on_delete=models.CASCADE)

class far_comment(models.Model):
    com = models.TextField()
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)

class question(models.Model):
    ques=models.TextField()
    comsv=models.ManyToManyField(vol_comment)
    comsf=models.ManyToManyField(far_comment)
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    uploaded_by = models.ForeignKey(volunteer, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender_farmer = models.ForeignKey(farmer, on_delete=models.CASCADE, null=True, blank=True)
    sender_volunteer = models.ForeignKey(volunteer, on_delete=models.CASCADE, null=True, blank=True)
    receiver_farmer = models.ForeignKey(farmer, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    receiver_volunteer = models.ForeignKey(volunteer, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('question', 'New Question'),
        ('answer', 'New Answer'),
        ('message', 'New Message'),
        ('resource', 'New Resource'),
    ]
    
    recipient_farmer = models.ForeignKey(farmer, on_delete=models.CASCADE, null=True, blank=True)
    recipient_volunteer = models.ForeignKey(volunteer, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    related_question = models.ForeignKey(question, on_delete=models.CASCADE, null=True, blank=True)
    related_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    related_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']


"""class question(models.Model):
    ques=models.TextField()
    date=models.DateField()
    coms=models.ManyToManyField(comment)
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)

class comment(models.Model):
    com = models.TextField()
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)
    vol = models.ForeignKey(volunteer, on_delete=models.CASCADE)"""
