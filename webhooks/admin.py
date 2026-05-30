from django.contrib import admin
from . import models


class EnvVarInline(admin.TabularInline):
    model = models.EnvVar
    extra = 1


class WebhookAdmin(admin.ModelAdmin):
    inlines = [EnvVarInline]


admin.site.register(models.Webhook, WebhookAdmin)
