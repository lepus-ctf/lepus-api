from django.contrib import admin
from django.contrib import admin
from lepus.models import Category, Question, Team, User, Flag, Answer, Notice, File, \
    UserConnection, Config, AttackPoint

class NoticeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "body", "is_public")
    list_editable = ("title", "body", "is_public")

admin.site.register(Notice, NoticeAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_score_time")

admin.site.register(Team, TeamAdmin)

class UserConnectionInline(admin.TabularInline):
    model = UserConnection
    extra = 0
    readonly_fields = ("id", "ip", "updated_at")
    fields = ("id", "ip", "updated_at")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "username", "is_staff", "is_superuser")
    list_filter = ("team", "is_staff", "is_superuser")
    inlines = [UserConnectionInline, ]

admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ordering")
    list_editable = ("name", "ordering")

admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "title", "ordering", "is_public")
    list_filter = ("category", "is_public")
    list_editable = ("ordering",)

admin.site.register(Question, QuestionAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ("question", "file", "is_public")
    list_filter = ("question", "is_public")

admin.site.register(File, FileAdmin)

class FlagAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "flag", "point")
    list_filter = ("question",)

admin.site.register(Flag, FlagAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "question", "answer", "flag", "created_at")
    list_filter = ("team", "user", "question",)

admin.site.register(Answer, AnswerAdmin)


class AttackPointAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "question", "point", "token", "created_at")
    list_filter = ("team", "user", "question",)

admin.site.register(AttackPoint, AttackPointAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "value",)

admin.site.register(Config, ConfigAdmin)
