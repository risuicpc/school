from django.db import models
from authentication.models import User

class Grade(models.Model):
    g_name = models.IntegerField(unique=True, verbose_name='Grade')

    def __str__(self):
        return str(self.g_name)

class Room(models.Model):
    r_name = models.CharField(max_length=1, verbose_name='Room')
    grade  = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='Grade')

    def __str__(self):
        return '{} {}'.format(self.grade, self.r_name.upper())

    def fullname(self):
        return '{} {}'.format(self.grade, self.r_name.upper())

class Subject(models.Model):
    s_name = models.CharField(max_length=100, verbose_name='Subject')
    grade  = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='Grade')

    def __str__(self):
        return '{} {}'.format(self.grade, self.s_name)

    def fullname(self):
        return '{} {}'.format(self.grade, self.s_name)

class StudentRoom(models.Model):
    s = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__r_name': 'student'}, verbose_name='Student')
    r = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Room')

    def __str__(self):
        return '{} {}'.format(self.s, str(self.r).upper())

class Semister(models.Model):
    CHOICES  = (('1', 'First',), ('2', 'Second',))
    semister = models.CharField(max_length=1, choices=CHOICES, default='1')

    def __str__(self):
        return self.semister

class Teach(models.Model):
    teacherID  = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__r_name': 'teacher'}, verbose_name='Teacher')
    semisterID = models.IntegerField( verbose_name='Semister')
    subjectID  = models.ManyToManyField(Subject, verbose_name='Subject')
    roomID     = models.ManyToManyField(Room, verbose_name='Room')

    def __str__(self):
        return str(self.teacherID)

    class Meta:
        verbose_name_plural = 'teach'
        

