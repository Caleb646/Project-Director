from django.contrib import admin

from .models import Job, RFI, Response, Attachment, User_RFI, User_Job


admin.site.register(Job)
admin.site.register(RFI)
admin.site.register(Response)
admin.site.register(Attachment)
admin.site.register(User_RFI)
admin.site.register(User_Job)
