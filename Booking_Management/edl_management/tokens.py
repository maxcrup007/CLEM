from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()


class TokenGenerator_accept(PasswordResetTokenGenerator):
    def _make_hash_value(self, apv, timestamp):
        return (
            six.text_type(apv.pk) + six.text_type(timestamp) +
            six.text_type(apv.is_active)
        )

accept_activation_token = TokenGenerator_accept()




class TokenGenerator_refuse(PasswordResetTokenGenerator):
    def _make_hash_value(self, apv, timestamp):
        return (
            six.text_type(apv.pk) + six.text_type(timestamp) +
            six.text_type(apv.is_active)
        )

refuse_activation_token = TokenGenerator_refuse()