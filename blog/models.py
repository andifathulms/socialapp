from django.db import models
from django.utils import timezone
from django_editorjs import EditorJsField

from account.models import Account

class Blog(models.Model):
	title = models.CharField(max_length=60)
	body=EditorJsField(
        editorjs_config={
            "tools":{
                "Link":{
                    "config":{
                        "endpoint":
                            '/linkfetching/'
                        }
                },
                "Image":{
                    "config":{
                        "endpoints":{
                            "byFile":'/uploadi/',
                            "byUrl":'/uploadi/'
                        },
                       
                    }
                },
                "Attaches":{
                    "config":{
                        "endpoint":'/uploadf/'
                    }
                }
            }
        }
    )
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)