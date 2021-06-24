from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, FormView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from js.fullcalendar import fullcalendar

from .models import *

import datetime
import re
from datetime import datetime


# REST Framework
from rest_framework import viewsets
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from .form import *
from .tokens import *




# Create your views here.


def HomePage(request):
    return render(request, 'edl_management/home.html')



def AboutPage(request):
    return render(request, 'edl_management/about.html')








def ShowBookingPage(request):
    booking = Booking.objects.all() # Pull from database

    context = {'booking': booking}

    return render(request, 'edl_management/Into Page/detail_booking.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('edl_management/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('success')
    else:
        form = SignupForm()
    return render(request, 'edl_management/Into Page/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required
def Add_InfoPage(request):

    if request.method == 'POST':

        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()

            return redirect('edit-profile')



        return render(request, 'edl_management/Into Page/edit_profile.html', locals())




def RegisterPage(request):

    if request.method == 'POST':
        data = request.POST.copy()
        std_id = data.get('std_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        newuser = User()
        newuser.username = std_id
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.email = email
        newuser.set_password(password)
        newuser.save()
        return redirect('inner-page')

    return render(request, 'edl_management/Into Page/register.html',)





    # form = UserForm(instance=request.user)
    # profile_form = ProfileForm(instance=request.user.profile)

    # return render(request, 'edl_management/Into Page/edit_profile.html', locals())






def AccountPage(request):
    return render(request, 'edl_management/account.html')


def InnerPage(request):

    return render(request, 'edl_management/enter.html')



def ErrorPage(request):

    return render(request, 'edl_management/Into Page/error.html')

def SuccessPage(request):

    return render(request, 'edl_management/Into Page/complete.html')

def Send_Email(request):
    send_mail('Hello There this from "Central Research Laboratory: SMS ',
              'Oh Hello There',
              'bt.raoaengna01@gmail.com',
              ['bt.raoaengna01@gmail.com'],
              fail_silently=False,)

    return render(request, 'edl_management/Into Page/booking.html')


# ----------------------------------------------------------------------------------
#  Equipment Functions
# ----------------------------------------------------------------------------------


@login_required
def EquipmentCreate(request):
    if not request.user.is_superuser:
        return redirect('error')
    form = EquipmentForm()
    if request.method == 'POST':
        form = EquipmentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('device-list')
    return render(request, 'edl_management/Equipment/create_form.html', locals())


@login_required
def EquipmentUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('error')
    obj = Equipment.objects.get(id=pk)
    form = EquipmentForm(instance=obj)
    if request.method == 'POST':
        form = EquipmentForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('device-list')
    return render(request, 'edl_management/Equipment/create_form.html', locals())


@login_required
def EquipmentDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('error')
    obj = get_object_or_404(Equipment, pk=pk)
    obj.delete()
    return redirect('device-list')

def EquipmentDetailView(request, pk):
    dev = get_object_or_404(Equipment, id=pk)
    return render(request, 'edl_management/Equipment/equipment_detail.html', locals())

@login_required
def EquipmentList(request):
    devices = Equipment.objects.all()

    return render(request, 'edl_management/Equipment/equipment_list.html', locals())


@login_required
def re_functions(request, pk):
    if not request.user.is_superuser:
        return redirect('error')
    obj = Project.objects.get(id=pk)
    dev_pk = obj.book.id
    student_pk = obj.student.id
    student = BookEquipmentLetter.objects.get(id=student_pk)
    student.total_dev_due = student.total_dev_due-1
    student.save()

    dev = Equipment.objects.get(id=dev_pk)
    dev.available_copies = dev.available_copies+1
    dev.save()
    obj.delete()
    return redirect('inner-page')

@login_required
def Student_request_issue(request, pk):
    obj = Equipment.objects.get(id=pk)
    stu = BookEquipmentLetter.objects.get(user_number=request.user)
    s = get_object_or_404(BookEquipmentLetter, user_number=str(request.user))
    if s.total_books_due < 10:
        message = "equipment has been broke, You can collect equipment from laboratory"
        a = Project()
        a.student = s
        a.dev = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due = stu.total_books_due+1
        stu.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'edl_management/Equipment/result_form.html', locals())


# ----------------------------------------------------------------------------------
#  End Functions (Equipment)
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
#  Approval Functions
# ----------------------------------------------------------------------------------

@login_required
def ApprovalCreate(request):
    form = ProjectForm()
    petition_form = ApprovalForm()
    sender = request.user.profile
    user = request.user

    if request.method == 'POST':
        form = ProjectForm(data=request.POST, files=request.FILES)
        petition_form = ApprovalForm(data=request.POST, files=request.FILES)

        if form.is_valid() and petition_form.is_valid():
            pep = form.save(commit=False)
            pep.is_active = False
            apv = petition_form.save(False)
            apv.is_active = False

            pep.user = request.user.profile
            pep.save()

            pep.project_name = apv.project

            apv.save()

            current_email = request.user.email

            # user_form = form.save()
            # custom_form = profile_form.save(False)
            # custom_form.user = user_form
            # custom_form.save()


            # project.save()

            # apl = Profile.objects.filter(profile=request.user.profile)
            # apu = User.objects.filter(user=request.user)

            current_site = get_current_site(request)
            mail_subject = 'Approval form to reserve equipment'
            message = render_to_string('edl_management/approval.html', {
                'pep': pep,
                'apv': apv,
                'sender': sender,
                'user': user,
                'domain': current_site.domain,
                'apv_id': urlsafe_base64_encode(force_bytes(apv.pk)),
                'app_id': urlsafe_base64_encode(force_bytes(apv.pk)),
                'token': [accept_activation_token.make_token(apv), refuse_activation_token.make_token(apv)]

            })
            email = EmailMessage(
                mail_subject, message, to=["bt.raoaengna01@gmail.com", "bt.raoaengna02@gmail.com", "bt.raoaengna03@gmail.com",]
            )
            email.send()
            return redirect('home-page')


    return render(request, 'edl_management/Equipment/project_form.html', locals())


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

def accept(request, abid, token):
    try:
        apv_id = force_text(urlsafe_base64_decode(abid))
        apv = BookEquipmentLetter.objects.get(pk=apv_id)
        apv.is_active = False
        approval = ApprovalForm(request.POST)
        # approval.status.change_status('Approved')
    except(TypeError, ValueError, OverflowError, BookEquipmentLetter.DoesNotExist):
        apv = None

    if apv is not None and accept_activation_token.check_token(apv, token):
        apv.is_active = True
        apv.save()


        current_site = get_current_site(request)
        current_email = request.user.email
        mail_subject = 'Your Petition has been Approved.'
        message = render_to_string('edl_management/Email/Accept.html', {
            'apv': apv,
            'domain': current_site.domain,
        })

        email = EmailMessage(
            mail_subject, message, to=[current_email]
        )
        email.send()

        return HttpResponse('Now you send a approval for now.')
    else:
        return redirect('home-page')



def refuse(request, fbid, token):
    try:
        app_id = force_text(urlsafe_base64_decode(fbid))
        apv = BookEquipmentLetter.objects.get(pk=app_id)
        apv.is_active = False
        # approval = ApprovalForm(request.POST)
        # approval.related_id.change_status('Denied')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        apv = None

    if apv is not None and refuse_activation_token.check_token(apv, token):
        apv.is_active = True
        apv.save()

        current_site = get_current_site(request)
        current_email = request.user.email
        mail_subject = 'Your Petition has been Denied.'
        message = render_to_string('edl_management/Email/Denied.html', {
            'apv': apv,
            'domain': current_site.domain,
        })

        email = EmailMessage(
            mail_subject, message, to=[current_email]
        )
        email.send()

        return HttpResponse('Now you send a approval for now.')
    # else:
    #     return redirect('home-page')




@login_required
def ApprovalUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('error')

    obj = BookEquipmentLetter.objects.get(id=pk)
    form = ApprovalForm(instance=obj)
    if request.method == 'POST':
        form = ApprovalForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('inner-page')
    return render(request, 'edl_management/Equipment/create_form.html', locals())


@login_required
def ApprovalDelete(request, pk):
    obj = get_object_or_404(BookEquipmentLetter, pk=pk)
    obj.delete()
    return redirect('inner-page')

@login_required
def ApprovalList(request):
    students = BookEquipmentLetter.objects.all()
    return render(request, 'edl_management/Lab/user_list.html', locals())

@login_required
def ApprovalDetail(request, pk):
    student = get_object_or_404(BookEquipmentLetter, id=pk)
    # e = User.objects.filter(student=student)
    return render(request, 'edl_management/Lab/user_detail.html', locals())


# ----------------------------------------------------------------------------------
#  End Functions
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
#  Edit Profile
# ----------------------------------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserProfileInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileInfoSerializer


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):

    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_device(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['equipment_models', 'equipment_name', 'lender'])

        dev_list = Equipment.objects.filter(entry_query)

    return render(request, 'edl_management/enter.html', locals())

def search_student(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['user_number', 'user_first_name', 'user_email'])

        students = BookEquipmentLetter.objects.filter(entry_query)

    return render(request, 'edl_management/enter.html', locals())



@login_required
def ViewProfilePage(request):

    user_info = User.objects.get(id=request.user.id)

    user_profile = Profile.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('inner-page')
    else:
        form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form

        return render(request, 'edl_management/Into Page/profile.html', args)



    return render(request, 'edl_management/Into Page/profile.html', {'user':user_info, 'userprofilepic':user_profile,})

# ----------------------------------------------------------------------------------
#  End Functions
# ----------------------------------------------------------------------------------







# ----------------------------------------------------------------------------------
#  Laboratory Functions
# ----------------------------------------------------------------------------------


@login_required
def Laboratory_Create(request):
    if not request.user.is_superuser:
        return redirect('error')
    form = LaboratoryForm()
    if request.method == 'POST':
        form = LaboratoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-lab')
    return render(request, 'edl_management/Equipment/create_form.html', locals())


@login_required
def Laboratory_Update(request, pk):

    obj = Lab.objects.get(id=pk)
    form = LaboratoryForm(instance=obj)
    if request.method == 'POST':
        form = LaboratoryForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('all-lab')
    return render(request, 'edl_management/Equipment/create_form.html', locals())

@login_required
def All_Laboratory(request):
    lab = Lab.objects.all()
    return render(request, 'edl_management/Lab/All_lab.html', locals())

@login_required
def Laboratory_detail(request, pk):
    laboratory = get_object_or_404(Lab, id=pk)
    return render(request, 'edl_management/Lab/lab_detail.html', locals())

@login_required
def Laboratory_Delete(request, pk):

    obj = get_object_or_404(Lab, pk=pk)
    obj.delete()
    return redirect('all-lab')

# ----------------------------------------------------------------------------------
#  End Functions
# ----------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------
#  Reserve Functions (Optional)
# ----------------------------------------------------------------------------------


@login_required
def Lab_ReserveCreate(request):
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            lab = form.cleaned_data['lab']
            form.save()
            return redirect('inner-page')

    return render(request, 'edl_management/Lab/reserve_create.html', locals())

@login_required
def Lab_ReserveUpdate(request, pk):

    obj = Booking.objects.get(id=pk)
    form = BookingForm(instance=obj)
    if request.method == 'POST':
        form = BookingForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('inner-page')
    return render(request, 'edl_management/Equipment/create_form.html', locals())


@login_required
def Lab_ReserveDelete(request, pk):

    obj = get_object_or_404(Booking, pk=pk)
    obj.delete()
    return redirect('inner-page')

@login_required
def Lab_ReserveList(request):
    students = Booking.objects.all()
    return render(request, 'edl_management/Lab/lab_list.html', locals())

@login_required
def Lab_ReserveDetail(request, pk):
    reserve = get_object_or_404(Booking, id=pk)
    e = User.objects.filter(reserve=reserve)
    return render(request, 'edl_management/Lab/lab_detail.html', locals())


# @login_required
# def ProjectCreate(request):
#     form = ProjectForm()
#     # applicant = Profile.objects.get()
#
#     if request.method == 'POST':
#         form = ProjectForm(data=request.POST, files=request.FILES)
#
#         if form.is_valid():
#
#             # form.user = request.user.profile
#
#             project = form.save(commit=False)
#             project.user = request.user.profile
#             project.save()
#             form.save()
#
#             return redirect('br-create')
#     return render(request, 'edl_management/Equipment/project_form.html', locals())


@login_required
def ProjectUpdate(request, pk):
    obj = Project.objects.get(id=pk)
    form = ProjectForm(instance=obj)
    if request.method == 'POST':
        form = ProjectForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('inner-page')
    return render(request, 'edl_management/Equipment/create_form.html', locals())

@login_required
def ProjectDelete(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    obj.delete()
    return redirect('inner-page')

@login_required
def ProjectDetail(request, pk):
    project = get_object_or_404(Project, id=pk)
    return render(request, 'edl_management/Lab/project_detail.html', locals())


@login_required
def ProjectList(request):
    projects = Project.objects.filter(user=request.user.profile)

    return render(request, 'edl_management/Into Page/project_list.html', locals())



# ----------------------------------------------------------------------------------
#  End Functions
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
#  Calendar Functions
# ----------------------------------------------------------------------------------


def CalendarPage(request):

    all_events = BookEquipmentLetter.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'edl_management/Lab/calendar.html', context)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = BookEquipmentLetter(equipment=str(title), start_reservation=start, end_reservation=end)
    event.save()
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = BookEquipmentLetter.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = BookEquipmentLetter.objects.get(id=id)
    event.delete()


# ----------------------------------------------------------------------------------
#  End Functions
# ----------------------------------------------------------------------------------



