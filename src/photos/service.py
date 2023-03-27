import datetime
import random

import pytz
from users.models import *


def get_random_user():
    count_users = CustomUser.objects.all().count()
    random_user_id = random.randint(1, count_users)
    random_user = CustomUser.objects.get(pk=random_user_id)
    return random_user


def get_random_user_model(user_id):
    random_user = RandomUser.objects.filter(user_id=user_id)
    if len(random_user) == 0:
        return None
    else:
        return random_user[0]


def update_or_create_random_user_model(user, random_user):
    time_expired = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    model, created = RandomUser.objects.update_or_create(user=user,
                                                         defaults={'user': user, 'random_user': random_user,
                                                                   'time_expired': time_expired})
    return model


def is_button_disabled(time_expired, hours):
    date_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    difference_time = date_now - time_expired
    hours_compare = datetime.timedelta(hours=hours)
    if difference_time > hours_compare:
        return False
    else:
        return True


def check_user_and_rangom_user(user_id):
    if user_id is None:
        return False
    user = CustomUser.objects.get(pk=user_id)
    random_user = get_random_user_model(user.pk)
    if random_user is None:
        return False
    return (user, random_user)
