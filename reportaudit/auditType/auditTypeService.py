# create Service
# edit Service
# view Service
# view By cusotmer Service

from reportaudit.models import AuditType


def create_audit_type(name, description):
    return AuditType.objects.create(name=name, description=description)

def edit_audit_type(audit_type_id, name, description):
    audit_type = AuditType.objects.get(id=audit_type_id)
    audit_type.name = name
    audit_type.description = description
    audit_type.save()
    return audit_type

def view_audit_type(audit_type_id):
    return AuditType.objects.get(id=audit_type_id)



    
