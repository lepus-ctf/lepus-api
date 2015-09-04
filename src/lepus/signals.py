# encoding=utf-8
import requests
import json
from django.core.signals import request_finished
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from django.conf import settings
from lepus.models import Answer, Notice, Category, Question, File

def send_realtime_event(data):
    if settings.PUSH_EVENT_URL:
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(settings.PUSH_EVENT_URL, data=json.dumps(data), headers=headers)

@receiver(post_save, sender=Answer)
def on_answer_sent(sender, **kwargs):
    if kwargs["created"]:
        answer = kwargs["instance"]

        if answer.is_correct:
            # For Users
            data = {
                "type":"answer",
                "user":answer.user.id,
                "team":answer.team.id,
                "question":answer.flag.question_id
            }
            send_realtime_event(data)

        # For Admin
        data = {
            "type":"answer",
            "user":answer.user.id,
            "team":answer.team.id,
            "answer":answer.answer,
            "flag":answer.flag.id if answer.flag else None,
            "is_correct":answer.is_correct,
            "is_admin":True
        }
        send_realtime_event(data)

def on_changed(sender, **kwargs):
    instance = kwargs["instance"]

    if hasattr(instance, "is_public") and not instance.is_public:
        return

    data = {
        "type": "update",
        "id": instance.id
    }
    if isinstance(instance, Category):
        data["model"] = "category"
    if isinstance(instance, Question):
        data["model"] = "question"
    if isinstance(instance, File):
        data["model"] = "file"
    if isinstance(instance, Notice):
        data["model"] = "notice"

    send_realtime_event(data)

post_save.connect(on_changed, sender=Category)
post_save.connect(on_changed, sender=Question)
post_save.connect(on_changed, sender=File)
post_save.connect(on_changed, sender=Notice)
