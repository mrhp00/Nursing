from django.db import models


class Hospital(models.Model):
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)

    class Meta:
        db_table = 'hospital'


class Ward(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        db_table = 'ward'


class HospitalWard(models.Model):  # connecting table of Hospital and Ward
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # foreign key to Hospital ID
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)  # foreign key to Ward ID

    class Meta:
        db_table = 'hospital_ward'


class Permission(models.Model):  # all available permissions
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    crud = models.CharField(max_length=4)

    class Meta:
        db_table = 'permissions'


class Nurse(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=6)
    social_number = models.CharField(max_length=10)
    experience = models.IntegerField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    email = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)


    class Meta:
        db_table = 'nurse'


class Shift(models.Model):  # shifts of hospital like Dawn, Evening, Night
    title = models.CharField(max_length=10)
    hours = models.IntegerField()

    class Meta:
        db_table = 'shift'


class NurseShift(models.Model):  # connecting table of Nurse and Shift
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)  # foreign key to Shift ID
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)  # foreign key to Hospital ID
    date = models.DateField()

    class Meta:
        db_table = 'nurse_shift'


class NurseHistory(models.Model):
    ward = models.ForeignKey(HospitalWard, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    start = models.DateField(default=None)
    end = models.DateField(default=None, blank=True, null=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'nurse_history'


class HospitalShift(models.Model):
    ward = models.ForeignKey(HospitalWard, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    minimum_nurse = models.IntegerField(default=1)

    class Meta:
        db_table = 'hospital_shift'


class ShiftRequest(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    request_date = models.DateField()
    desire_date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shift_request'


class IsLoggedIn(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    login_date = models.DateField(default=None, blank=True, null=True)
    expire_date = models.DateField(default=None, blank=True, null=True)
