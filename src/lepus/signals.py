# encoding=utf-8
import requests
import json
from django.core.signals import request_finished
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from lepus.models import Answer

def send_realtime_event(data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post("http://localhost:8001/events/", data=json.dumps(data), headers=headers)
    print(data)

@receiver(post_save, sender=Answer)
def on_answer_sent(sender, **kwargs):
    if kwargs["created"]:
        answer = kwargs["instance"]
        data = {
            "type":"answer",
            "user":answer.user.id,
            "team":answer.team.id,
            "answer":answer.answer,
            "flag":answer.flag.id if answer.flag else None,
            "is_correct":answer.is_correct
        }
        send_realtime_event(data)
