from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import *



class SignupForm(UserCreationForm):

    STATUS_CHOICES = (('นักวิจัย', 'นักวิจัย'),
                     ('นิสิต', 'นิสิต'),
                     ('อาจารย์', 'อาจารย์'),
                     ('อื่นๆ', 'อื่นๆ'),
                     )


    first_name = forms.CharField(
        max_length=30, required=True, help_text='=ชื่อ.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='นามสกุล.')
    email = forms.EmailField(max_length=200, required=False)
    # profile_category = forms.ChoiceField(choices=STATUS_CHOICES, )
    # contact = forms.CharField(max_length=20, required=False)
    # tel = forms.CharField(max_length=10, required=False, help_text='=เบอร์โทร')
    # faculty = forms.CharField(max_length=50, required=False, help_text='=คณะ')
    # branch = forms.CharField(max_length=50, required=False, help_text='=สาขา')
    # photo_profile = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    # (, 'profile_category', 'contact', 'tel', 'faculty', 'branch', 'photo_profile')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # user.profile.status = self.cleaned_data['status']
        # user.profile.contact = self.cleaned_data['contact']
        # user.profile.tel = self.cleaned_data['tel']
        # user.profile.faculty = self.cleaned_data['faculty']
        # user.profile.branch = self.cleaned_data['branch']
        # user.profile.photo_profile = self.cleaned_data['photo_profile']

        if commit:
            user.save()

        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# ('contact', 'photo_profile', 'tel', 'faculty', 'branch', 'photo_profile',)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('status', 'information', 'contact', 'tel', 'faculty', 'branch', 'photo_profile')


# ['check_in', 'check_out']
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        check_in = forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            ))

        check_out = forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            ))


class EquipmentForm(forms.ModelForm):

    # confirm = forms.ChoiceField(choices=OPTION, widget=forms.RadioSelect, help_text='โดยข')

    class Meta:
        model = Equipment
        fields = '__all__'


class ProjectForm(forms.ModelForm):

    class Meta:
            model = Project
            exclude = ('user',)







class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'


class ApprovalForm(forms.ModelForm):

    OPTION = (('Accept', 'Accept'),
              ('Deny', 'Deny'),
              )

    OPTION2 = (('Yes', 'Yes'),
              ('No', 'No'),
              )

    APPROVAL_CHOICES = [
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    ]

    start_reservation = forms.DateField(widget=DateInput)
    end_reservation = forms.DateField(widget=DateInput)
    official_working = forms.ChoiceField(choices=OPTION2, widget=forms.RadioSelect, help_text='')
    confirm = forms.ChoiceField(choices=OPTION, widget=forms.RadioSelect, help_text='โดยข้าพเจ้าได้อ่านระเบียบการใช้ห้องปฏิบัติการวิจัยกลางคณะวิทยาศาสตร์การแพทย์ มหาวิทยาลัยพะเยา และยินยอมปฏิบัติตามกฎระเบียบดังกล่าวทุกประการ ในระหว่างปฏิบัติงาน หากห้องปฏิบัติการ เครื่องมือ อุปกรณ์ เกิดการชำรุดหรือเสียหาย ข้าพเจ้ายินดีรับผิดชอบชดใช้ค่าเสียหายที่เกิดขึ้น')




    class Meta:
        model = BookEquipmentLetter
        exclude = ('status', 'reason', 'applicant', 'project')

    def save(self, commit=True):

        apv = super(ApprovalForm, self).save(commit=False)

        apv.start_reservation = self.cleaned_data['start_reservation']
        apv.end_reservation = self.cleaned_data['end_reservation']
        apv.equipment = self.cleaned_data['equipment']


        if commit:
            apv.save()

        return apv


class Approval(forms.Form):
    APPROVAL_CHOICES = [
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    ]
    status = forms.CharField(label='Approval:', widget=forms.RadioSelect(choices=APPROVAL_CHOICES))
    reason = forms.CharField(max_length=100)
    related_id = None







