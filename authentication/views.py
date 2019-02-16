from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView,
)
from django.contrib.auth import authenticate, login
from django.db.models import Q

from .forms import *
from .models import User, Role
from staff.forms import StudentRoomRegisterForm, SemisterCreationForm
from staff.models import StudentRoom, Room, Grade, Semister


value, _role_, _sex_ = [], 'all', 'a'
choices = {
    'sex' : {
        'All' : {'selected': True,'query_string':'?sex_exact=a'},
        'Male' : {'selected': False,'query_string':'?sex_exact=m' }, 
        'Female' : {'selected': False,'query_string':'?sex_exact=f'}
    },
    'role' : {
        'all' : {'selected': True,'query_string':'?role_exact=all'},
        'admin' : {'selected': False,'query_string':'?role_exact=admin'},
        'teacher' : {'selected': False,'query_string':'?role_exact=teacher'},
        'student' : {'selected': False,'query_string':'?role_exact=student'},
        'parent' : {'selected': False,'query_string':'?role_exact=parent'}
    }
    
}


def intionalize():
    global value, choices,_role_ , _sex_
    value, _role_, _sex_ = [], 'all', 'a'
    choices = {
        'sex' : {
            'All' : {'selected': True,'query_string':'?sex_exact=a'},
            'Male' : {'selected': False,'query_string':'?sex_exact=m' }, 
            'Female' : {'selected': False,'query_string':'?sex_exact=f'}
        },
        'role' : {
            'all' : {'selected': True,'query_string':'?role_exact=all'},
            'admin' : {'selected': False,'query_string':'?role_exact=admin'},
            'teacher' : {'selected': False,'query_string':'?role_exact=teacher'},
            'student' : {'selected': False,'query_string':'?role_exact=student'},
            'parent' : {'selected': False,'query_string':'?role_exact=parent'}
        }
        
    }

def list_filter(data):
    global value, choices,_role_ , _sex_
    key = list(data.keys())
    value = list(data.values())
    if '?' in value[0]:
        value = value[0].split('?')
        l, r = value[1].split('=')
        key.append(l)
        value[1] = r
    for i, j in zip(key, value):
        one_two = False
        if i == 'role_exact':
            for k in choices['role']:
                if k == j:
                    choices['role'][k]['selected'] =True
                else:
                    choices['role'][k]['selected'] =False
                
                if len(value) == 2:
                    _s = value[0]
                    if len(value[1]) == 1:
                        _s = value[1]
                    if _s != 'a':
                        choices['role'][k]['query_string'] = '?role_exact='+k+'?sex_exact='+_s
                    else:
                        choices['role'][k]['query_string'] = '?role_exact='+k
                elif value[0]:
                    one_two = True

            if one_two:
                if value[0] == 'all':
                    for k in choices['sex']:
                        choices['sex'][k]['query_string'] = '?sex_exact='+k[0].lower()
                else:
                    for k in choices['sex']:
                        choices['sex'][k]['query_string'] = '?sex_exact='+k[0].lower()+'?role_exact='+value[0]

        elif i == 'sex_exact':
            for k in choices['sex']:
                if k[0].lower() == j:
                    choices['sex'][k]['selected'] =True
                else:
                    choices['sex'][k]['selected'] =False
                
                if len(value) == 2:
                    _s = value[0]
                    if len(value[1]) > 1:
                        _s = value[1]
                    if _s != 'all':
                        choices['sex'][k]['query_string'] = '?sex_exact='+k[0].lower()+'?role_exact='+_s
                    else:
                        choices['sex'][k]['query_string'] = '?sex_exact='+k[0].lower()
                elif value[0]:
                    one_two = True
            if one_two:
                if value[0] == 'a':
                    for k in choices['sex']:
                        choices['sex'][k]['query_string'] = '?sex_exact='+k[0].lower()
                else:
                    for k in choices['role']:
                        choices['role'][k]['query_string'] = '?role_exact='+k+'?sex_exact='+value[0]
    
    for i in value:
        if len(i) == 1:
            _sex_ = i
        elif len(i) > 1:
            _role_ = i


def header_validetor(data):
    header = []
    for field in data:
        if field.lower() in ['name', 'f name', 'first name']:
            header.append('f_name')
        elif field.lower() in ['father name', 'm name', 'middel name']:
            header.append('m_name')
        elif field.lower() in ['grand father name', 'l name', 'last name']:
            header.append('l_name')
        elif field.lower() in ['u name', 'user name']:
            header.append('u_name')
        elif field.lower() in ['email', 'e-mail']:
            header.append('email')
        elif field.lower() in ['phone', 'phone number']:
            header.append('phone')
        elif field.lower() in ['sex', 'gender', 'Sex']:
            header.append('sex')
        elif field.lower() in ['role']:
            header.append('role')
        elif field.lower() in ['role1', 'role 1']:
            header.append('role1')
        elif field.lower() in ['role2', 'role 2']:
            header.append('role2')
        elif field.lower() in ['role3', 'role 3']:
            header.append('role3')
        elif field.lower() in ['grade']:
            header.append('grade')
        elif field.lower() in ['room']:
            header.append('room')

    if len(set(header)) < 8:
        return [len(header), field]
    else:
        return header

#####################################################################################
##                                                                                 ##
##                              LOGIN PAGE                                         ##
##                                                                                 ##
#####################################################################################

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'authentication/registration/login.html', {'form' : form})

#####################################################################################
##                                                                                 ##
##                              HOME PAGE                                          ##
##                                                                                 ##
#####################################################################################
    
    
@login_required
def index(request):
    context = {}
    
    if request.user.is_staff:
        return redirect('admin:index')
    else:
        return render(request, 'authentication/index.html', context)



#####################################################################################
##                                                                                 ##
##                              REGISTRETION PAGE                                  ##
##                                                                                 ##
#####################################################################################

@login_required
# print(User.has_admin())
# @user_passes_test
def user_create(request):
    exel = UserCreationExel()
    form = UserCreationForm()
    s_room = StudentRoomRegisterForm()
    
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            student = Role.objects.filter(r_name='student')
            if student and student[0] in form.cleaned_data['role']:
                s_room = StudentRoomRegisterForm(request.POST)
                if s_room.is_valid():
                    form.save()
                    form.save_m2m()
                    user = get_object_or_404(User, u_name=request.POST['u_name'])
                    room = get_object_or_404(Room, id=request.POST['r'])
                    s_room = StudentRoom(s=user, r=room)
                    s_room.save()
                    messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The user "<a href="/user/' + str(user.id) + '/edit/">' + request.POST["u_name"] + '</a>" was added successfully.')
                    return redirect('list')
                else:
                    messages.error(request, '<img src="/static/assets/img/icon-no.svg"> The user was not added successfully. Please correct the error below.')
            else:
                form.save()
                form.save_m2m()
                user = get_object_or_404(User, u_name=request.POST['u_name'])
                messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The user "<a href="/user/' + str(user.id) + '/edit/">' + request.POST["u_name"] + '</a>" was added successfully.')
                if request.POST['save'] == 'save':
                    return redirect('list')
                else:
                    form = UserCreationForm()
                    s_room = StudentRoomRegisterForm()
        else:
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> The user was not added successfully. Please correct the error below.')
    context = {
        'form' : form,
        'exel' : exel,
        's_room': s_room
    }
    return render(request, 'authentication/registration/register.html', context)
    

#####################################################################################
##                                                                                 ##
##                              REGISTRETION FROM EXEL PAGE                        ##
##                                                                                 ##
#####################################################################################

@login_required
def user_exel(request):
    CHOICES = {'male': 'm', 'female': 'f'}
    exel = UserCreationExel(request.POST, request.FILES)
    if exel.is_valid():
        data = request.FILES['exelfile']
        userdata = dict()
        invalid = False
        chake = True
        index = 2
        pas = []
        fail = []
        
        for chunk in data:
            if chake:
                header = str(chunk)[2:len(str(chunk))-3].split(',')
                chake = False
                header = header_validetor(header)
            elif len(header) > 7:
                body = str(chunk)[2:len(str(chunk))-3].split(',')
                user =  dict(zip(header, body))
                role = []
                for key in user:
                    if key == 'sex' and user[key]:
                        user[key] = CHOICES[user[key].lower()]
                    elif key[:4] == 'role':
                        try:
                            role.append(Role.objects.get(r_name=user[key].lower()).id)
                        except Role.DoesNotExist:
                            pass
                user['role'] = role 
                form = UserCreationForm(user)
                if form.is_valid():
                    student = Role.objects.filter(r_name='student')
                    if student and student[0] in form.cleaned_data['role']:
                        if user['grade'] and user['room']:
                            room = Room.objects.filter(r_name=user['room'].lower(), grade__g_name=user['grade'])
                            if room:
                                form.save()
                                form.save_m2m()
                                student = User.objects.filter(u_name=form.cleaned_data['u_name'])
                                s_room = StudentRoom(s=student[0], r=room[0])
                                s_room.save()
                                pas.append(index)
                            else:
                                fail.append(index)
                        else:
                            fail.append(index)
                    else:
                        form.save()
                        form.save_m2m()
                        pas.append(index)
                else:
                    fail.append(index)
                index = index + 1
            else:
                invalid = True
                break
        if not invalid:
            if len(pas) == 0:
                messages.error(request, '<img src="/static/assets/img/icon-no.svg"> All User on the file was not uploaded successfully, B/s some User with that User name already exists, and/or Some User has not full info on the exel sheet.')
                form = UserCreationForm()
                exel = UserCreationExel()
                return render(request, 'authentication/registration/register.html', {'form' : form, 'exel' : exel,})
            elif len(fail) == 0:
                messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> All User on the file was uploaded and added successfully.')
            elif len(pas) > len(fail):
                messages.info(request, '<img src="/static/assets/img/icon-yes.svg"> '+ str(len(pas)) +' User was uploaded and added successfully and <img src="/static/assets/img/icon-no.svg"> '+ str(len(fail)) +' User at row number ' + str(fail) + ' was not uploaded successfully. please checke exel sheet.')
            else:
                messages.warning(request, '<img src="/static/assets/img/icon-yes.svg"> '+ str(len(pas)) +' User was uploaded and added successfully and <img src="/static/assets/img/icon-no.svg"> '+ str(len(fail)) +' User at row number ' + str(fail) + ' was not uploaded successfully. please checke exel sheet.')
            return redirect('list')
        else:
            form = UserCreationForm()
            exel = UserCreationExel()
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> Invalid field name "' + header[1] + '" on the colum ' + str(header[0]) + '. Please correct the header on the exel like :- F Name, M Name, L Name, U Name, Email, Phone, Gender, Role1, Role2.')

    else:
        form = UserCreationForm()
        messages.error(request, '<img src="/static/assets/img/icon-no.svg"> The file was not uploaded successfully. Please correct the error below.')
    context = {
        'form' : form,
        'exel' : exel,
    }    
    return render(request, 'authentication/registration/register.html', context)


#####################################################################################
##                                                                                 ##
##                              VIEW ALL USER PAGE                                 ##
##                                                                                 ##
#####################################################################################

@login_required
def user_list(request):
    global _role_, _sex_
    if request.GET:
        list_filter(request.GET)
    else:
        intionalize()
    
    if _role_ == 'all' and _sex_ == 'a':
        queryset = User.objects.filter(is_admin=False).order_by('f_name', 'm_name', 'l_name')
    elif _role_ == 'all':
        queryset = User.objects.filter(sex=_sex_, is_admin=False).order_by('f_name', 'm_name', 'l_name')
    elif _sex_ == 'a':
        queryset = User.objects.filter(role__r_name=_role_, is_admin=False).order_by('f_name', 'm_name', 'l_name')
    else:
        queryset = User.objects.filter(sex=_sex_, role__r_name=_role_, is_admin=False).order_by('f_name', 'm_name', 'l_name')

    context = {
        'object_list' : queryset,
        'choices' : choices
    }
    return render(request, 'authentication/user_list.html', context)


#####################################################################################
##                                                                                 ##
##                              UPDATE USER PAGE                                   ##
##                                                                                 ##
#####################################################################################

@login_required
def user_update(request, id):
    user = get_object_or_404(User, id=id)
    form = UserChangeForm(instance=user)
    room = None
    try:
        room =StudentRoom.objects.get(s_id=id)
        s_room = StudentRoomRegisterForm(instance=room)
    except StudentRoom.DoesNotExist:
        s_room = StudentRoomRegisterForm()

    
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, id=id)
        if form.is_valid():
            student = Role.objects.filter(r_name='student')
            if student and student[0] in form.cleaned_data['role']:
                s_room = StudentRoomRegisterForm(request.POST, instance=room)
                if s_room.is_valid():
                    form.save()
                    if room:
                        room.delete()
                    room = get_object_or_404(Room, id=request.POST['r'])
                    s_room = StudentRoom(s=user, r=room)
                    s_room.save()
                    messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The user "<a href="/user/' + str(id) + '/edit/">' + request.POST["u_name"] + '</a>" was changed successfully.')
                    return redirect('list')
                else:
                    messages.error(request, '<img src="/static/assets/img/icon-no.svg"> The user was not added successfully. Please correct the error below.')
            else:
                try:
                    room = StudentRoom.objects.get(s_id=id)
                    room.delete()
                except StudentRoom.DoesNotExist:
                    pass
                form.save()
                messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The user "<a href="/user/' + str(id) + '/edit/">' + request.POST["u_name"] + '</a>" was changed successfully.')
                return redirect('list')
        else:
            messages.error(request, '<img src="/static/assets/img/icon-no.svg"> The user was not added successfully. Please correct the error below.')

    context = {
        'form': form,
        'user': user,
        'rooms': room,
        's_room': s_room,
        'relationship': len(user.role.all())
    }

    return render(request, 'authentication/user_edit.html', context)

#####################################################################################
##                                                                                 ##
##                              DELETE USER PAGE                                   ##
##                                                                                 ##
#####################################################################################

@login_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    u_name = user.u_name
    user.delete()
    messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> The user "' + u_name + '" was deleted successfully.')
    return redirect('list')

#####################################################################################
##                                                                                 ##
##                              VIEW PROFILE PAGE                                  ##
##                                                                                 ##
#####################################################################################    

@login_required
def user_profile(request):
    context = { } 
    return render(request, 'authentication/user_profile.html', context)

#####################################################################################
##                                                                                 ##
##                              EDIT PROFILE PAGE                                  ##
##                                                                                 ##
#####################################################################################

def user_profile_edit(request):
    profile = ProfileEditForm(instance=request.user)
    if request.user.admin:
        obj = Semister.objects.all()
        if obj:
            semister = SemisterCreationForm(instance=obj[0])
        else:
            semister = SemisterCreationForm()
    p_or_s = True
    if request.method == 'POST':
        if request.POST['save'] == 'profile':
            profile = ProfileEditForm(request.POST, request.FILES, instance=request.user)
            if profile.is_valid():
                profile.save()
                messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Your address was updated successfully.')
            else:
                messages.success(request, '<img src="/static/assets/img/icon-no.svg"> Your address was not updated successfully.')
     
        elif request.POST['save'] == 'semister':
            if obj:
                semister = SemisterCreationForm(request.POST, instance=obj[0])
            else:
                semister = SemisterCreationForm(request.POST)
            if semister.is_valid():
                semister.save()
                messages.success(request, '<img src="/static/assets/img/icon-yes.svg"> Semister was updated successfully.')
            p_or_s = False
    context = {
        'profile': profile,
        'p_or_s': p_or_s,
    } 
    if request.user.admin:
        context['semister'] = semister

    return render(request, 'authentication/edit_profile.html', context)

