# -*- coding: utf-8 -*-

from django.db.utils import IntegrityError


def verify_email(email: str) -> bool:
    """verify the validation of email address"""
    if not (isinstance(email, str) and '@' in email):
        return False
    email_prefix, email_suffix = email.split('@')
    if not all([len(email_prefix) >= 5,
                len(email_suffix) >= 5,
                email_suffix.endswith('.com') or email_suffix.endswith('.cn')]):
        return False
    return True


def un_from_email(email: str) -> str:
    """Get default username from email address"""
    if verify_email(email):
        return email.split('@')[0]
    else:
        return ''


def db_insert(instance):
    try:
        instance.save()
        return True
    except IntegrityError:
        return False


class ObjectDict(dict):
    """A dict can get value via key|attribute"""

    def __init__(self, data, **kwargs):
        if isinstance(data, dict):
            for k, v in data.items():
                kwargs[k] = ObjectDict(v) if isinstance(v, dict) else v
        super().__init__(**kwargs)
        self.__dict__ = self
