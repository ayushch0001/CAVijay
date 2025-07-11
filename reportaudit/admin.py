from django.contrib import admin
from .models import BackendReport ,Customer ,AuditType, MainReport ,Audit, Month,Collection,yearReportData ,Cluster
# Register your models here.
admin.site.register(BackendReport)
admin.site.register(Customer)
admin.site.register(AuditType)
admin.site.register(MainReport)
admin.site.register(Audit)
admin.site.register(Month)
admin.site.register(Collection)
admin.site.register(yearReportData)
admin.site.register(Cluster)