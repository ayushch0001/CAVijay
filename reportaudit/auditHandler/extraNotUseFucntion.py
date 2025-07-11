import json
import logging
from venv import logger
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from reportaudit.auditHandler.auditServices import setAudit
from reportaudit.forms import AuditForm
from reportaudit.models import BackendReport ,Customer ,AuditType ,Audit, Month

  
  
  
  
  
  
  
@csrf_exempt
def viewBackReportcomplete_re(request):
        if request.method == 'POST':
            audityear = request.POST.get('year')
            # customer = request.POST.get('customerId')
            customer = Customer.objects.all().first()
            # Validate the audit record
            audit = Audit.objects.filter(year=audityear,customer = customer ).first()
            if not audit:
                return JsonResponse({'error': 'Audit record not found'}, status=404)

            months = Month.objects.filter(collectionId=audit.collection.id)
            report_data = []

            for month in months:
                records = BackendReport.objects.filter(month=month)

                month_data = {
                    "month": month.id,
                    "Office Ex": 0,
                    "Mislileneous Ex": {"A": 0, "B": 0, "C": 0, "D": 0},
                    "Stationary Ex": {"Pencil": 0, "Pen": 0}
                }

                for record in records:
                    if record.title == "Office Ex":
                        month_data["Office Ex"] = record.dict.get("value", 0)  # Assuming Office Ex stores single value
                    elif record.title == "Mislileneous Ex":
                        month_data["Mislileneous Ex"].update(record.dict)
                    elif record.title == "Stationary Ex":
                        month_data["Stationary Ex"].update(record.dict)

                report_data.append(month_data)

            return JsonResponse({"reports": report_data})  # Return formatted JSON response

        return JsonResponse({'error': 'Invalid request method'}, status=400)

        
        
        
        
    
        
    #update json data 
@csrf_exempt
def update_json_data(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)  # Parse JSON data
                print("Received Updated Data:", data)
                
                # yaha pe data base me save karane ka code llikhna hai 

              
                return JsonResponse({"status": "success", "message": "Report updated successfully!"})
            
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
    # by anil 
    
        @csrf_exempt
    # def viewBackReportcomplete(request):
    #     if request.method == 'POST':
    #         audityear = request.POST.get('year')
    #         customer = Customer.objects.all().first()
    #         print(customer)
    #         print(audityear,"jjj")
    #         # Validate the audit record
    #         audit = Audit.objects.filter(year=audityear,customer = customer).first()
    #         if not audit:
    #             return JsonResponse({'error': 'Audit record not found'}, status=404)

    #         months = Month.objects.filter(collectionId=audit.collection.id)
    #         Coll = []

    #         for month in months:
    #             Brs = BackendReport.objects.filter(month=month)
    #             Coll.extend(Brs)  # Flattening the list instead of appending QuerySets

    #         json_data = serializers.serialize('json', Coll)
    #         print(json_data, "json_data");
    #         # return HttpResponse(json_data, content_type='application/json')
    #         return JsonResponse({"reports": json_data}) 

    #     return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt  # Temporarily disable CSRF (Not recommended for production)
def update_Backreport(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)  # Get JSON from request
                # global fruit_data  # Modify global dictionary (Use DB in production)
                # fruit_data.update(data)  # Update all values at once
                print(data)
                return JsonResponse({"message": "Data updated successfully!"}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    
    
    
def report_new(request):
        return render(request, 'templates\\audit\\report.html')
    
def report_new2(request):
        return render(request, 'templates\\audit\\report2.html')