import datetime
from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import *
from aiogram import types
from loader import dp, bot


@sync_to_async
def get_user(user_id):
    try:
        user, created = User.objects.get_or_create(
            user_id=user_id
            )
        user.save()
        return user
    except Exception as exx:
        print(exx)
        return None
    

@sync_to_async
def get_users():
    try:
        return User.objects.all()
    except Exception as exx:
        print(exx)
        return None
    
    
@sync_to_async
def get_channels():
    try:
        channels = Channel.objects.all()
        return channels
    except:
        return None


@sync_to_async
def get_week_winners():
    try:
        return WeekWinner.objects.all()
    except:
        return None


@sync_to_async
def add_week_winners(winners):
    try:
        wins = WeekWinner.objects.all()
        for w in wins:
            w.delete()
        for user in winners:
            winner = WeekWinner.objects.create(
                user=user
            )    
            winner.save()
        return WeekWinner.objects.all()
    except:
        return None


