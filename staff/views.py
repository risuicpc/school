from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from .forms import *
from .models import *

#####################################################################################
##                                                                                 ##
##                      Grade => Add, View, Update, Delete                         ##
##                                                                                 ##
#####################################################################################

class GradeListView(View):
    template_name = 'staff/grade_list.html'

    def get(self, request):
        grade = Grade.objects.all().order_by('g_name')
        return render(request, self.template_name, {'object_list': grade})

class GradeCreateView(View):
    form_class    = GradeCreateForm
    template_name = 'staff/grade_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            id = get_object_or_404(Grade, g_name=request.POST['g_name']).id
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Grade "<a href="/staff/grade/' + str(id) + '/edit/">' + request.POST["g_name"] + '</a>" was added successfully.')
            if request.POST['save'] == 'save':
                return redirect('staff:list')
            else:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Grade was not added successfully. Please correct the error below.')
            return render(request, self.template_name, {'form': form})
            

class GradeUpdateView(View):
    form_class    = GradeCreateForm
    template_name = 'staff/grade_edit.html'

    def get_object(self):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Grade, id=id)
        return obj

    def get(self, request, id):
        obj = self.get_object()
        subject, room, studentroom = [], [], []
        # subject = Subject.objects.filter(grade__grade_id=obj.id)
        room = Room.objects.filter(grade_id=obj.id)
        studentroom =StudentRoom.objects.filter(r__grade_id=obj)
        form = self.form_class(instance=obj)
        context = {
            'form': form,
            'obj' : obj,
            'subject': subject,
            'room': room,
            'rooms': len(room),
            'subjects': len(subject),
            'studentroom': studentroom,
            'students': len(studentroom)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        obj = self.get_object()
        # subject = Subject.objects.filter(grade_id=obj.id)
        room = Room.objects.filter(grade_id=obj.id)
        studentroom =StudentRoom.objects.filter(r__grade_id=obj)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Grade "<a href="/staff/grade/' + str(id) + '/edit/">' + request.POST["g_name"] + '</a>" was updated successfully.')
            return redirect('staff:list')
        else:
            context = {
                'obj' : obj,
                'room': room,
                'form': form,
                'rooms': len(room),
                'subject': subject,
                'subjects': len(subject),
                'studentroom': studentroom,
                'students': len(studentroom)
            }
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Grade was not updated successfully. Please correct the error below.')
            return render(request, self.template_name, context)

class GradeDeleteView(View):

    def post(self, request, id):
        obj = get_object_or_404(Grade, id=id)
        g_name = obj.g_name
        obj.delete()
        messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The grade "' + str(g_name) + '" was deleted successfully.')
        return redirect('staff:list')

#####################################################################################
##                                                                                 ##
##                      Room => Add, View, Update, Delete                          ##
##                                                                                 ##
#####################################################################################

class RoomListView(View):
    template_name = 'staff/room_list.html'

    def get(self, request):
        room = Room.objects.all().order_by('grade', 'r_name')
        grade = Grade.objects.all().order_by('g_name')
        return render(request, self.template_name, {'object_list': room, 'grade': grade})

class RoomCreateView(View):
    form_class    = RoomCreateForm
    template_name = 'staff/room_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
         
    def post(self, request):
        data = dict(request.POST)
        if 'r_name' in data.keys():
            data['r_name'] = data['r_name'][0]

        if 'grades' in data.keys():
            data['grade'] = data['grades'][0]

        form = self.form_class(data)
        if form.is_valid():
            for grade in form.cleaned_data['grades']:
                try:
                    room = Room.objects.get(r_name=form.cleaned_data['r_name'], grade=grade)
                except Room.DoesNotExist:
                    room = Room(r_name=form.cleaned_data['r_name'], grade=grade)
                    room.save()
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Room  was added successfully.')
            if request.POST['save'] == 'save':
                return redirect('staff:r-list')
            else:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})


        messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Room was not added successfully. Please correct the error below.')
        return render(request, self.template_name, {'form': form})
        

class RoomUpdateView(View):
    form_class    = RoomChangeForm
    template_name = 'staff/room_edit.html'

    def get_object(self):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Room, id=id)
        s_room =StudentRoom.objects.filter(r_id=id)
        return obj, s_room

    def get(self, request, id):
        object, student_room = self.get_object()
        form = self.form_class(instance=object)
        context = {
            'form': form,
            'object': object,
            'studentroom': student_room,
        }
        if student_room:
            context['user']= len(student_room)
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        object, student_room = self.get_object()
        form = self.form_class(request.POST, instance=object, id=id)
        if form.is_valid():
            form.save()
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Room "<a href="/staff/room/' + str(id) + '/edit/">' + request.POST["r_name"] + '</a>" was updated successfully.')
            return redirect('staff:r-list')
        else:
            context = {
                'form': form,
                'object' : object,
                'studentroom': student_room,
            }
            if student_room:
                context['user']= len(student_room)
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Room was not updated successfully. Please correct the error below.')
            return render(request, self.template_name, context)

class RoomDeleteView(View):

    def post(self, request, id):
        obj = get_object_or_404(Room, id=id)
        r_name = obj.r_name
        obj.delete()
        messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The Room "' + str(r_name) + '" was deleted successfully.')
        return redirect('staff:r-list')

#####################################################################################
##                                                                                 ##
##                      Subject => Add, View, Update, Delete                      ##
##                                                                                 ##
#####################################################################################

class SubjectListView(View):
    template_name = 'staff/subject_list.html'

    def get(self, request):
        subject = Subject.objects.all()
        return render(request, self.template_name, {'object_list': subject})

class SubjectCreateView(View):
    form_class    = SubjectRegisterForm
    template_name = 'staff/subject_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
         
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            id = get_object_or_404(Subject, s_name=request.POST['s_name'], grade=request.POST['grade']).id
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Subject "<a href="/staff/subject/' + str(id) + '/edit/">' + request.POST["s_name"] + '</a>" was added successfully.')
            if request.POST['save'] == 'save':
                return redirect('staff:s-list')
            else:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Subject was not added successfully. Please correct the error below.')
            return render(request, self.template_name, {'form': form})

class SubjectUpdateView(View):
    form_class    = SubjectRegisterForm
    template_name = 'staff/subject_edit.html'

    def get_object(self):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Subject, id=id)
        return obj

    def get(self, request, id):
        obj = self.get_object()
        form = self.form_class(instance=obj)
        context = {
            'form': form,
            'obj' : obj
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        obj = self.get_object()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Subject "<a href="/staff/subject/' + str(id) + '/edit/">' + request.POST["s_name"] + '</a>" was updated successfully.')
            return redirect('staff:s-list')
        else:
            context = {
                'form': form,
                'obj' : obj
            }
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Subject was not updated successfully. Please correct the error below.')
            return render(request, self.template_name, context)

class SubjectDeleteView(View):

    def post(self, request, id):
        obj = get_object_or_404(Subject, id=id)
        s_name = obj.s_name
        obj.delete()
        messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The subject "' + str(s_name) + '" was deleted successfully.')
        return redirect('staff:s-list')


#####################################################################################
##                                                                                 ##
##                      Teach => Add, View, Update, Delete                          ##
##                                                                                 ##
#####################################################################################



class TeachListView(View):
    template_name = 'staff/teach/teach_list.html'

    def get(self, request):
        semister = Semister.objects.get(id=1).semister
        teach = Teach.objects.filter(semisterID=semister)
        teacher = User.objects.filter(role__r_name='teacher')
        t = [u.teacherID for u in teach]
        context = {
            'object_list': teach, 
            'teacher': teacher,
            'teach': t
        }
        return render(request, self.template_name, context)


# class TeachCreateView(View):
#     form_class    = TeachCreationForm
#     template_name = 'staff/teach/teach_create.html'

#     def get_object(self):
#         s = Subject.objects.all().order_by('grade__g_name', 's_name')
#         r = Room.objects.all().order_by('grade__g_name', 'r_name')
#         g = Grade.objects.all().order_by('g_name')

#         return s, r, g

#     def get(self, request):
#         subject, room, grade = self.get_object()
#         form = self.form_class()
#         context = {
#             'form': form,
#             'subject': subject,
#             'room': room,
#             'grade': grade
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             form.save_m2m()
#             return redirect('staff:t-list')
#         else:
#             subject, room, grade = self.get_object()
#         context = {
#             'form': form,
#             'subject': subject,
#             'room': room,
#             'grade': grade
#         }
#         return render(request, self.template_name, context)


        
class TeachUpdateView(View):
    form_class    = TeachCreationForm
    template_name = 'staff/teach/teach_edit.html'

    def get_object(self):
        s = Subject.objects.all().order_by('grade__g_name', 's_name')
        r = Room.objects.all().order_by('grade__g_name', 'r_name')
        g = Grade.objects.all().order_by('g_name')

        return s, r, g

    def get(self, request, id):
        subject, room, grade = self.get_object()
        try:
            teach = Teach.objects.get(id=id)
        except Teach.DoesNotExist:
            semister = Semister.objects.get(id=1).semister
            teach = Teach(teacherID_id=id, semisterID=semister)
            teach.save()
        form = self.form_class(instance=teach)
        context = {
            'form': form,
            'subject': subject,
            'room': room,
            'subjects': len(teach.subjectID.all()),
            'rooms': len(teach.roomID.all()),
            'grade': grade,
            'object': teach,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        try:
            teach = Teach.objects.get(id=id)
        except Teach.DoesNotExist:
            teach = get_object_or_404(Teach, teacherID=id)
        form = self.form_class(request.POST, instance=teach)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Teacher "<a href="/staff/teach/' + str(teach.id) + '/edit/">' + str(teach) + '</a>" teachs subject and room was updated successfully.')
            return redirect('staff:t-list')
        else:
            subject, room, grade = self.get_object()
        context = {
            'form': form,
            'subject': subject,
            'room': room,
            'subjects': len(subject),
            'rooms': len(room),
            'grade': grade,
            'obj': teach
        }
        messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Teach was not updated successfully. Please correct the error below.')
        return render(request, self.template_name, context)

class TeachDeleteView(View):

    def post(self, request, id):
        obj = get_object_or_404(Teach, id=id)
        name = obj.teacherID
        obj.delete()
        messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The Teach "' + str(name) + '" was deleted successfully.')
        return redirect('staff:t-list')