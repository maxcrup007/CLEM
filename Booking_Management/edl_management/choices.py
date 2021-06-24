# from django.utils.translation import gettext_lazy as _
#
# from djchoices import DjangoChoices, ChoiceItem
#
#
# class Action(DjangoChoices):
#     create = ChoiceItem('วิจัย', ('วิจัย'))
#     update = ChoiceItem('การเรียนการสอน/IS', ('การเรียนการสอน/IS'))
#     delete = ChoiceItem('อื่นๆ', ('อื่นๆ'))
#
#
# class Status(DjangoChoices):
#     approved = ChoiceItem('approved', ('Approved'))
#     rejected = ChoiceItem('rejected', ('Rejected'))
#     none = ChoiceItem('', ('No action taken'))
#
#
# class Applicant_status(DjangoChoices):
#     researcher = ChoiceItem('นักวิจัย', 'นักวิจัย')
#     professor = ChoiceItem('อาจารย์', 'อาจารย์')
#     student = ChoiceItem('นิสิต', 'นิสิต')
#     none = ChoiceItem('', 'อื่นๆ')      