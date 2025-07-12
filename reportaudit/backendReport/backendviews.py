#create 
#edit - by id but it will show name of employee also and also its data also 
#delete - by id
#list - all data filter hoke dikehega cusotmer wise and moths wise also (agar possible hoga to whi pe edit krenge apan)

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from reportaudit.models import BackendReport ,Customer ,AuditType


class backendView:
    @csrf_exempt
    def createBackendreport(request):
        if request.method == "POST":
            cashOrBank = request.POST.get("cashOrBank")
            receiptOrPayment = request.POST.get("receiptOrPayment")
            formula = request.POST.get("formula")
            values = request.POST.getlist("values[]")  
            auditId = request.POST.get("auditType")
            auditType = AuditType.objects.get(id=auditId)
            title = request.POST.get("title")
            data = {}

            for value in values:
                temp = {value: "0"}
                data.update(temp)  # Merging the temp dictionary into data
                
            BackendReport.objects.create(auditType=auditType,dict = data,title=title,cashOrBank = cashOrBank,receiptOrPayment =receiptOrPayment,formula = formula)
            
            print(values)
            return redirect('createBackend')
        auditTypes = AuditType.objects.all()
        return render(request, "templates/module/backreportform.html",{ 'auditTypes':auditTypes})
    
    
    def allToAddValue(request):
        if request.methods == "POST":
            
            return render(request, "templates/module/backreportform.html")
        #  customer se audittype ka id le lenge usse fir back end report ka data le lenge months wise 
        # usko row me bhejenge 
        #  jaab vo post hoga to moths id utha lenge haar row ka uss row se 
        all 
        