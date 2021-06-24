from booking.models import *


def book_lab(request, lab, check_in, check_out):
    booking = Booking.objects.create(
        user = request.user,
        lab = lab,
        check_in = check_in,
        check_out = check_out,
    )
    booking.save()