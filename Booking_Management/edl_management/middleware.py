import datetime
from datetime import timedelta
from .models import BookEquipmentLetter


class LetterMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            fecha_actual = datetime.date.today()
            letter = BookEquipmentLetter.objects.filter()
            for letters in letter:
                reserve_now = letter.start_