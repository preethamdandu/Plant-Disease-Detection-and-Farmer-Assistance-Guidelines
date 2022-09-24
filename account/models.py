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


"""class question(models.Model):
    ques=models.TextField()
    date=models.DateField()
    coms=models.ManyToManyField(comment)
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)

class comment(models.Model):
    com = models.TextField()
    far = models.ForeignKey(farmer, on_delete=models.CASCADE)
    vol = models.ForeignKey(volunteer, on_delete=models.CASCADE)"""
