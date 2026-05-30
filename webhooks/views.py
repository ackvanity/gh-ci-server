from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
    HttpResponseNotFound,
    HttpRequest,
)
from django.views.decorators.http import require_POST
import hmac
import hashlib
from . import models
import os
import subprocess
import uuid


@require_POST
def webhook(request: HttpRequest, id: uuid.UUID):
    sig = request.headers.get("X-Hub-Signature-256")

    try:
        webhook = models.Webhook.objects.get(id=id)
    except models.Webhook.DoesNotExist:
        return HttpResponseNotFound(f"No webhook registered at UUID {id}")

    if sig is None:
        return HttpResponseForbidden("No signature given")

    mac = hmac.new(
        webhook.secret.encode("utf-8"), msg=request.body, digestmod=hashlib.sha256
    )
    if not hmac.compare_digest("sha256=" + mac.hexdigest(), sig):
        return HttpResponseForbidden(f"Invalid signature")

    event = request.headers.get("X-GitHub-Event")

    if event == "push":
        try:
            if webhook.script != "":
                script_env = os.environ.copy()
                script_env["GIT_PATH"] = webhook.path

                vars = models.EnvVar.objects.filter(webhook=webhook)

                for var in vars:
                    script_env[var.name] = var.value

                subprocess.run(
                    ["bash", webhook.script],
                    env=script_env,
                    shell=True,
                    cwd=webhook.path,
                )
            return HttpResponse("Deploy triggered")
        except Exception as e:
            return HttpResponseServerError("Deployment Failed")

    return HttpResponse("Ignored event")
