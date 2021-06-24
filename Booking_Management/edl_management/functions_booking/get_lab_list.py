from booking.models import Lab
from django.urls import reverse


def get_lab_url_list():
    lab = Lab.objects.all()[0]

    lab_url_list = []

    lab_categories = dict(lab.LAB_CATEGORIES)

    for category in lab_categories:
        lab_category = lab_categories.get(category)
        lab_url = reverse('booking:LabDetailView', kwargs={'category': category})

        lab_url_list.append((lab_category, lab_url))

    return lab_url_list