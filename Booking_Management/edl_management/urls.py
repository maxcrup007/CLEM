from django.urls import path
from .views import *
from Booking_Management.feed import LatestEntriesFeed
from django.conf.urls import include, url

# On App

urlpatterns = [

    path('', HomePage, name="home-page"),
    path('abouts/', AboutPage, name="about-page"),
    path('dashboard/', InnerPage, name="inner-page"),
    path('calendar/', CalendarPage, name="calendar-page"),
    path('register/', RegisterPage, name="register-page"),
    path('account/', AccountPage, name="account-page"),
    path('home/404/', ErrorPage, name='error'),
    path('home/success/', SuccessPage, name='success'),
    path('show_booking/', ShowBookingPage, name='show-booking'),
    path('profile_account/', ViewProfilePage, name='edit-profile'),
    path('signup/information/', Add_InfoPage, name='edit-profile-info'),
    path('feed/', LatestEntriesFeed(), name='feed'),
    path('return/<int:pk>', re_functions, name='ref'),


    # Approval & Borrower
    path('petition/list', ApprovalList, name='br-list'),
    path('petition/create/', ApprovalCreate, name='br-create'),
    path('petition/<int:pk>/update/', ApprovalUpdate, name='br-update'),
    path('petition/<int:pk>/delete/', ApprovalDelete, name='br-delete'),
    path('petition/<int:pk>/', ApprovalDetail, name='br-detail'),
    path('approval/', ApprovalCreate, name='approval_create'),

    # Laboratory
    path('laboratory/', All_Laboratory, name='all-lab'),
    path('laboratory/detail/<int:pk>', Laboratory_detail, name='all-lab-detail'),
    path('laboratory/create/', Laboratory_Create, name='all-lab-create'),
    path('laboratory/<int:pk>/update/', Laboratory_Update, name='all-lab-update'),
    path('laboratory/<int:pk>/delete/', Laboratory_Delete, name='all-lab-delete'),

    # Equipment
    path('equipment/create', EquipmentCreate, name='device-create'),
    path('equipment/<int:pk>/update/', EquipmentUpdate, name='device-update'),
    path('equipment/<int:pk>/delete/', EquipmentDelete, name='device-delete'),
    path('equipment/<int:pk>/request_issue/', Student_request_issue, name='device-issue'),
    path('equipment/', EquipmentList, name='device-list'),
    path('equipment/<int:pk>', EquipmentDetailView, name='device-detail'),

    # Project Forms
    # path('project/create', ProjectCreate, name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdate, name='project-update'),
    path('project/<int:pk>/delete/', ProjectDelete, name='project-delete'),
    path('project/detail/<int:pk>', ProjectDetail, name='project-detail'),
    path('project/', ProjectList, name='project-list'),

    # Reservation
    path('laboratory/reserve/<int:pk>/delete/', Lab_ReserveDelete, name='lab-delete'),
    path('laboratory/reserve/<int:pk>/update/', Lab_ReserveUpdate, name='lab-update'),
    path('laboratory/reserve/', Lab_ReserveCreate, name='lab-reserve'),
    path('laboratory/reserve/<int:pk>/', Lab_ReserveDetail, name='lab-detail'),

    url(r'^search_d/', search_device, name="search_d"),
    url(r'^search_s/', search_student, name="search_s"),

    url(r'^signup/$', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    url(r'^accept/(?P<abid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', accept, name='accept'),
    url(r'^refuse/(?P<fbid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', refuse, name='refuse'),

    # url('/calendar2', calendar, name='calendar'),
    url('^add_event$', add_event, name='add_event'),
    url('^update$', update, name='update'),
    url('^remove', remove, name='remove'),







]
