from reportaudit.models import BackendReport


def setAllBr(month, auditType):
    # get all backend reports of a particular month and audit type
    get_all_br = BackendReport.objects.filter(auditType=auditType)
    # for all we need to create the replica of this 
    for br in get_all_br:
        # create a new backend report with the same audit type and month
        new_br = BackendReport.objects.create(auditType=None, title=br.title, dict=br.dict, month=month)
        print(new_br)
        new_br.save()
    return True
    