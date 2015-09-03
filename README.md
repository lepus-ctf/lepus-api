# Lepus RESTful CTF Score Server

LepusはRESTfulなCTFスコアサーバーです。

## Requirement

* Python 3.4
* see `package.pip`

## Quick Start

* `git clone https://github.com/lepus-ctf/lepus-api.git`
* `cd lepus-api`
* `pip install -r package.pip`
* `cd src`
* `python migrate` to create database.
* `python createsuperuser` to create superuser.
* `python manage.py runserver` to running webserver.
* Open `http://localhost:8000/api/` for testing.

## Push Notification

WebSocketによるリアルタイムのプッシュ通知は [lepus-api-push](https://github.com/lepus-ctf/lepus-api-push) と組み合わせて提供されています。

## Copyright and license
Code and documentation copyright Lepus CTF.
Code released under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE).
Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).
