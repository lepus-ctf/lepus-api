# Lepus RESTful CTF Score Server

LepusはRESTfulなCTFスコアサーバーです。

[![Build Status](https://travis-ci.org/lepus-ctf/lepus-api.svg?branch=feat%2Freadme)](https://travis-ci.org/lepus-ctf/lepus-api)

## Requirement

* Python 3.4
* see `package.pip`

## Quick Start

* `git clone https://github.com/lepus-ctf/lepus-api.git`
* `cd lepus-api`
* `pip install -r package.pip`
* `cd src`
* `python manage.py migrate` to create database.
* `python manage.py createsuperuser` to create superuser.
* `python manage.py runserver` to running webserver.
* Open `http://localhost:8000/api/` for testing.

## Push Notification

WebSocketによるリアルタイムのプッシュ通知は [lepus-api-push](https://github.com/lepus-ctf/lepus-api-push) と組み合わせて提供されています。

## Copyright and license
Code and documentation copyright [Lepus CTF](http://lepus-ctf.org/).
Code released under MIT License [(See LICENSE)](https://github.com/lepus-ctf/lepus-api/blob/master/LICENSE)
Docs released under [Creative Commons License 4.0 BY](http://creativecommons.org/licenses/by/4.0/legalcode.ja).
