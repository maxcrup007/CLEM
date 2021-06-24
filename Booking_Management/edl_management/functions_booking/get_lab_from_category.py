from booking.models import Lab

def get_lab_category_student_format(category):
    '''
    A function that takes computer format lab_category and returns it in Student Format
    '''
    lab = Lab.objects.all()[0]
    lab_category = dict(lab.LAB_CATEGORIES).get(category, None)
    return lab_category
