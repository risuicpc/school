from django import forms
from .models import *


class GradeCreateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields =('g_name',)
        

    def clean_g_name(self):
        g_name = self.cleaned_data['g_name']
        if g_name > 12 or g_name < 1:
            raise forms.ValidationError("Grade was between 1 and 12.")

        return g_name


class RoomCreateForm(forms.ModelForm):
    grade   = Grade.objects.all().order_by('g_name')
    grades = forms.ModelMultipleChoiceField(queryset=grade, label='Grade', widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Room
        fields ='__all__'

    def clean_r_name(self):
        r_name = self.cleaned_data['r_name']
        
        if r_name.lower() < 'a' or r_name.lower() > 'z':
            raise forms.ValidationError("Room was between a to z or A to Z.")

        return r_name



class RoomChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        super(RoomChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Room
        fields ='__all__'


    def clean(self):
        cleaned_data = super().clean()
        r_name = self.cleaned_data['r_name']
        grade  = self.cleaned_data['grade']

        obj = Room.objects.filter(r_name=r_name, grade=grade).exclude(id=self.id)

        if obj:
            msg = "Room with this grade was already exists."
            self.add_error('r_name', msg)

        if r_name.lower() < 'a' or r_name.lower() > 'z':
            msg = "Room was between a to z or A to Z."
            self.add_error('r_name', msg)
        


class SubjectRegisterForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields ='__all__'

    def clean_grade(self):
        s_name = self.cleaned_data['s_name']
        grade = self.cleaned_data['grade']
        obj = Subject.objects.filter(s_name=s_name, grade=grade)
        if obj:
            raise forms.ValidationError("Subject with this grade was already exists.")

        return grade

class StudentRoomRegisterForm(forms.ModelForm):
    room = Room.objects.all().order_by('grade', 'r_name')
    r = forms.ModelChoiceField(queryset=room, required=False, empty_label='(Nothing)', label='Room',
            help_text='This field required for studeny only',
        )
    class Meta:
        model = StudentRoom
        fields =('r',)

    def clean_r(self):
        r = self.cleaned_data.get("r")
        if r is None:
            raise forms.ValidationError("This field is required.")
    
class SemisterCreationForm(forms.ModelForm):
    class Meta:
        model = Semister
        fields ='__all__'


class TeachCreationForm(forms.ModelForm):
    teacher   = User.objects.filter(role__r_name='teacher')
    teacherID = forms.ModelChoiceField(queryset=teacher, label='Teacher')
    class Meta:
        model = Teach
        exclude = ['semisterID']

        widgets = {
            'subjectID': forms.CheckboxSelectMultiple(), 
            'roomID': forms.CheckboxSelectMultiple(), 
        }    

    def clean(self):
        cleaned_data = super().clean()
        roomID = self.cleaned_data.get("roomID")
        subjectID = self.cleaned_data.get("subjectID")


        if roomID and subjectID:
            s_grade = set(g.grade for g in subjectID)
            r_grade = set(g.grade for g in roomID)

            for s in s_grade:
                if s not in r_grade:
                    msg = "Grade " + str(s) + " Subject was selected. So Grade " + str(s) + " Room is required."
                    self.add_error('roomID', msg)
                    break

            for r in r_grade:
                if r not in s_grade:
                    msg = "Grade " + str(r) + " Room was selected. So Grade " + str(r) + " Subject is required."
                    self.add_error('subjectID', msg)
                    break

    def save(self, commit=True):
        teach = super().save(commit=False)
        semister = Semister.objects.get(id=1).semister
        teach.semisterID=semister
        if commit:
            teach.save()
        return teach
        