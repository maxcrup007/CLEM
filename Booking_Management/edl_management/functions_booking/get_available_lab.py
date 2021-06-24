from .models import *
from .availability import *


def get_available_labs(category, check_in, check_out):
    lab_list = Lab.objects.filter(category=category)

    available_labs = []

    for lab in lab_list:
        if check_availability(lab, check_in, check_out):
            available_labs.append(lab)

    if len(available_labs) > 0:
        return available_labs
    else:
        return None
