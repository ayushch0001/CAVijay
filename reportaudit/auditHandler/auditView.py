
from datetime import datetime
import json
import logging
from tokenize import String
from venv import logger
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import pdfkit
from reportaudit.auditHandler.auditServices import setAuditFR, setAuditFRSingleYear
from reportaudit.forms import AuditForm, ClusterForm
from reportaudit.models import BackendReport, Cluster ,Customer ,AuditType ,Audit, MainReport, Month, yearReportData
from reportaudit.auditHandler.formulas import  Fromula
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import tempfile

class auditView:
    
 
    @csrf_exempt
    def createAudit(request):
        error_message = None  # Initialize error message variable
        clusters = Cluster.objects.all()
        if request.method == 'POST': # type: ignore
            form = AuditForm(request.POST)
            nameC = request.POST.get("customer")
            # nameC = form.changed_data['customer']
            # nameC =  form.get_context("customer")
            print("getting1" ,nameC)
            if form.is_valid():
                print("getting2")
                # nameC = form.cleaned_data['customer']
                yearPresentCheck = form.cleaned_data['yearStart']
                cust = Customer.objects.get(id = nameC)
                print(cust)
                audits = Audit.objects.filter(customer=int(cust.pk))
                print(audits)
                if yearPresentCheck in audits:
                    error_message = "An audit for this year already exists for the selected customer."
                    return render(request, 'audit/auditForm.html', {'form': form, 'error_message': error_message,'clusters': clusters}) # type: ignore

                audit = form.save(commit=False)
                audit.customer = cust
                audit.save()
                setAuditFR(audit)
                return render(request,'audit/auditForm.html',{'form': form,'status': 'success','clusters': clusters}) # type: ignore
            
            else:
                error_message = "Please correct the errors in the form."
        
        else:
            form = AuditForm()

        return render(request, 'audit/auditForm.html', {'form': form, 'error_message': error_message,'clusters': clusters})


    def get_customers_by_cluster(request):
        cluster_id = request.GET.get('cluster_id')
        print(cluster_id)
        customers = Customer.objects.filter(cluster_id=cluster_id).values('id', 'nameOfOrganization')
        data = {
            'customers': [{'id': c['id'], 'name': c['nameOfOrganization']} for c in customers]
        }
        return JsonResponse(data)
        
    def audit_list_view(request):
        clusters = Cluster.objects.all()
        audits = []

        cluster_id = request.GET.get('cluster_id')
        customer_id = request.GET.get('customer_id')

        if cluster_id and customer_id:
            audits = Audit.objects.filter(customer__id=customer_id)

        context = {
            'clusters': clusters,
            'audits': audits,
        }
        return render(request, 'templates/audit/audit_list.html', context)

    

    @login_required
    def edit_audit(request, audit_id):
        print("ggghh",audit_id)
        audit = get_object_or_404(Audit, id=audit_id)
        clusters = Cluster.objects.all()
        if request.method == "POST":
            form = AuditForm(request.POST, instance=audit)
            if form.is_valid():
                form.save()
                return redirect('list_audits')  # Replace with your actual list view name
        else:
            form = AuditForm(instance=audit)
        return render(request, 'audit/auditForm.html', {'form': form,'clusters': clusters})
       

    @login_required
    def delete_audit(request, audit_id):
        audit = get_object_or_404(Audit, id=audit_id)
        print("f1")
        
        print("f2")
        audit.delete()
           # Replace with your actual list view name
        return redirect('list_audits')



    def report_view(request):
        return render(request, 'templates/audit/backreport.html')
    



    def fetchCusotmerPage(request):
        clusters = Cluster.objects.all()
        return render(request,"templates/audit/customerSelctionPage.html",{'clusters': clusters})

    

# Set up logging
    logger = logging.getLogger(__name__)


    
    
    
    def search_customer(request):
        query = request.GET.get('query', '')
        cluster_id = request.GET.get('cluster_id')
        
        customers = Customer.objects.all()
        if cluster_id:
            customers = customers.filter(cluster_id=cluster_id)
        if query:
            customers = customers.filter(nameOfOrganization__icontains=query)
        # print(customers)
        customers_list = [{
            'id': customer.id,
            'nameOfOrganization': customer.nameOfOrganization
        } for customer in customers]
        
        return JsonResponse({'customers': customers_list})

    def fetch_audits(request):
        customer_id = request.GET.get('customer_id')
        audits = Audit.objects.filter(customer_id=customer_id).values('id', 'yearStart','yearEnd')
        # print(audits)
        return JsonResponse({'audits': list(audits)})   # need to cahange this as per the fr logic 
    
            


    def generate_pdf(request):
        # Render HTML template to string
        audit_id = request.GET.get('audit_id')
        audit = get_object_or_404(Audit, id=audit_id)
        
        year = str(audit.yearEnd)
        year1 = f"{audit.yearStart}-{audit.yearEnd}"

        # Fetch main report and year report data
        mainReport1 = MainReport.objects.filter(audit=audit).first()
        yearReport1 = yearReportData.objects.filter(yearReports=mainReport1).first()
        
        audit2Id = None
        audit3Id = None
        audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
        
        audit2 = None
        audit3 = None

        # Finding previous audits
        for auditCheck in audits:
            if audit.yearStart == auditCheck['yearEnd']:
                audit2Id = auditCheck['id']
                audit2 = Audit.objects.get(id=audit2Id)
            elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                audit3Id = auditCheck['id']
                audit3 = Audit.objects.get(id=audit3Id)
                
        if audit2Id and not audit3Id :
                print("pp1")
                
                audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
                for auditCheck in audits:
                    if audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                        audit3Id = auditCheck['id']
                        audit3 = Audit.objects.get(id=audit3Id)
                
        mainReport2 = MainReport.objects.filter(audit=audit2).first() if audit2 else None
        yearReport2 = yearReportData.objects.filter(yearReports=mainReport2).first() if mainReport2 else None
        year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""

        # Fetch third year data
        mainReport3 = MainReport.objects.filter(audit=audit3).first() if audit3 else None
        yearReport3 = yearReportData.objects.filter(yearReports=mainReport3).first() if mainReport3 else None
        year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""



        print(yearReport1, yearReport2, yearReport3)
        print(year1, year2, year3)

        html_string = render_to_string( 'templates/audit/oneMoreTry.html',
            {
                'yearReport1': yearReport1,
                'yearReport2': yearReport2,
                'yearReport3': yearReport3,
                'year1': year1,
                'year2': year2,
                'year3': year3,
                'year': year,
                'audit': audit
            }
        )        
        base_url = request.build_absolute_uri('/')[:-1]  
        print("while printing",base_url)
        html_string = html_string.replace('src="/media/', f'src="{base_url}/media/')    

        config = pdfkit.configuration(wkhtmltopdf="packages/wkhtmltopdf/bin/wkhtmltopdf.exe")  # Update this path if necessary
        options = {
        'page-size': 'A4',
        'margin-top': '17mm',
        'margin-bottom': '18mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
        'encoding': 'UTF-8',
        'quiet': ''  # Suppress warnings
            }

        pdf = pdfkit.from_string(html_string, False, configuration=config, options=options)
        
        # Return response as a PDF file
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="output.pdf"'

        return response
    
                
    
    def mainReport(request): # type: ignore
        audit_id = request.GET.get('audit_id') # type: ignore
        audit = get_object_or_404(Audit, id=audit_id)

        year = str(audit.yearEnd)
        year1 = f"{audit.yearStart}-{audit.yearEnd}"

        # Fetch main report and year report data
        mainReport1 = MainReport.objects.select_related('audit').filter(audit=audit).first()
        yearReport1 = yearReportData.objects.select_related('yearReports').filter(yearReports=mainReport1).first()

        # Run formula calculations and ensure they are saved
        for func in [
            Fromula.openingClosingBalanceForCurrentYear,Fromula.carryFrowordToText,
            Fromula.total1,
            Fromula.formula48, Fromula.formula47, Fromula.formula49, 
            Fromula.formula50, Fromula.formula51, Fromula.formula52, Fromula.formula55,
            Fromula.Bformula45, Fromula.Bformula47, Fromula.Bformula49, 
            Fromula.Bformula50, Fromula.Bformula51, Fromula.Bformula52,Fromula.total1, Fromula.total2,
            Fromula.formulaA44,Fromula.formula55, Fromula.total3,Fromula.formula55
        ]:
            func(audit) # type: ignore
            audit.refresh_from_db()

        # Force reload the updated audit data
        audit.refresh_from_db()

        audit2Id = None
        audit3Id = None
        audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
        
        audit2, audit3 = None, None

        # Finding previous audits
        for auditCheck in audits:
            if audit.yearStart == auditCheck['yearEnd']:
                audit2Id = auditCheck['id']
                audit2 = Audit.objects.get(id=audit2Id)
            elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                audit3Id = auditCheck['id']
                audit3 = Audit.objects.get(id=audit3Id)

        if request.method == "POST": # type: ignore
            date_str = request.POST.get("date") # type: ignore
            observations = request.POST.get("observations") # type: ignore
            observations2 = request.POST.get("observations2") # type: ignore
            Udin = request.POST.get("Udin") # type: ignore
            
            formatted_date = None
            if date_str:
                try:
                    formatted_date = datetime.strptime(date_str, r"%Y-%m-%d").date()
                    audit.date = formatted_date
                    audit.observations = observations
                    audit.observations2 = observations2
                    audit.Udin = Udin
                    audit.save(update_fields=["date"])  # Ensure immediate commit
                    audit.save(update_fields=["observations"])
                    audit.save(update_fields=["observations2"])# Ensure immediate commit
                    audit.save(update_fields=["Udin"])
                except ValueError:
                    formatted_date = None
                    

            print(audit2)

            # Fetch updated reports
            yearReport1 = yearReportData.objects.filter(yearReports__audit=audit).first()
            yearReport2 = yearReportData.objects.filter(yearReports__audit=audit2).first() if audit2 else None
            yearReport3 = yearReportData.objects.filter(yearReports__audit=audit3).first() if audit3 else None
            year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""
            year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

            print(year1," - ",year2," - ",year3)
            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('EA', 'EB')):
                            field_name = f"{prefix}-{field.name}"
                            
                            value = request.POST.get(field_name) # type: ignore
                           
                            setattr(report, field.name, value if value else "")
                    report.save()

            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('A', 'B')):
                            field_name = f"{prefix}-{field.name}"
                            value = request.POST.get(field_name)
                            # print(field_name,'--',value)
                            setattr(report, field.name, int(value) if value else 0)
                    report.save()
            
            for func in [
            Fromula.openingClosingBalanceForCurrentYear,Fromula.carryFrowordToText,
            Fromula.total1,
            Fromula.formula48, Fromula.formula47, Fromula.formula49, 
            Fromula.formula50, Fromula.formula51, Fromula.formula52, Fromula.formula55,
            Fromula.Bformula45, Fromula.Bformula47, Fromula.Bformula49, 
            Fromula.Bformula50, Fromula.Bformula51, Fromula.Bformula52,Fromula.total1, Fromula.total2,
            Fromula.formulaA44,Fromula.formula55,Fromula.total3,Fromula.formula55
            ]:
                func(audit) # type: ignore
            audit.refresh_from_db()

            # Reload year reports to include formula updates
            main_report1 = MainReport.objects.filter(audit=audit).first()
            year_report1 = yearReportData.objects.filter(yearReports=main_report1).first() if main_report1 else None

            year_report2 = None
            if audit2:
                main_report2 = MainReport.objects.filter(audit=audit2).first()
                year_report2 = yearReportData.objects.filter(yearReports=main_report2).first() if main_report2 else None

            year_report3 = None
            if audit3:
                main_report3 = MainReport.objects.filter(audit=audit3).first()
                year_report3 = yearReportData.objects.filter(yearReports=main_report3).first() if main_report3 else None
            
            return render(request, r'templates/audit/oneMoreTry.html', { # type: ignore
                'yearReport1': year_report1, 
                'yearReport2': year_report2, 
                'yearReport3': year_report3,
                'year1': year1, 'year2': year2, 'year3': year3, 
                'year': year, 'audit': audit
            })
        # Ensure audits are properly assigned
        if not audit2Id and not audit3Id:
            setAuditFR(audit)
            for auditCheck in audits:
                if auditCheck['yearEnd'] == audit.yearStart:
                    audit2Id = auditCheck['id']
                    audit2 = Audit.objects.get(id=audit2Id)
                elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                    audit3Id = auditCheck['id']
                    audit3 = Audit.objects.get(id=audit3Id)
                    
        elif audit2Id and not audit3Id:
            setAuditFRSingleYear(audit)
            audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
            for auditCheck in audits:
                if auditCheck['yearEnd'] == audit.yearStart:
                    audit2Id = auditCheck['id']
                    audit2 = Audit.objects.get(id=audit2Id)
                elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                    audit3Id = auditCheck['id']
                    audit3 = Audit.objects.get(id=audit3Id)

        # Fetch second and third year data
        mainReport2 = MainReport.objects.filter(audit=audit2).first() if audit2 else None
        yearReport2 = yearReportData.objects.filter(yearReports=mainReport2).first() if mainReport2 else None
        year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""

        mainReport3 = MainReport.objects.filter(audit=audit3).first() if audit3 else None
        yearReport3 = yearReportData.objects.filter(yearReports=mainReport3).first() if mainReport3 else None
        year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

        return render(request, 'templates/audit/oneMoreTry.html', {
            'yearReport1': yearReport1, 'yearReport2': yearReport2, 'yearReport3': yearReport3,
            'year1': year1, 'year2': year2, 'year3': year3, 'year': year, 'audit': audit
        })

    def mainReport2(request): # type: ignore
        audit_id = request.GET.get('audit_id') # type: ignore
        audit = get_object_or_404(Audit, id=audit_id)

        year = str(audit.yearEnd)
        year1 = f"{audit.yearStart}-{audit.yearEnd}"

        # Fetch main report and year report data
        mainReport1 = MainReport.objects.select_related('audit').filter(audit=audit).first()
        yearReport1 = yearReportData.objects.select_related('yearReports').filter(yearReports=mainReport1).first()

        # Run formula calculations and ensure they are saved
        for func in [
            Fromula.openingClosingBalanceForCurrentYear,
            Fromula.total1,
            Fromula.formula48, Fromula.formula49, Fromula.formula49, 
            Fromula.formula50, Fromula.formula51, Fromula.formula52, Fromula.formula55,
            Fromula.Bformula45, Fromula.Bformula47, Fromula.Bformula49, 
            Fromula.Bformula50, Fromula.Bformula51, Fromula.Bformula52,Fromula.total1, Fromula.total2,
            Fromula.formulaA44,Fromula.formula55,Fromula.total3,Fromula.formula55,Fromula.openingClosingBalanceForCurrentYear
        ]:
            func(audit) # type: ignore
            audit.refresh_from_db()

        # Force reload the updated audit data
        audit.refresh_from_db()

        audit2Id = None
        audit3Id = None
        audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
        
        audit2, audit3 = None, None

        # Finding previous audits
        for auditCheck in audits:
            if audit.yearStart == auditCheck['yearEnd']:
                audit2Id = auditCheck['id']
                audit2 = Audit.objects.get(id=audit2Id)
            elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                audit3Id = auditCheck['id']
                audit3 = Audit.objects.get(id=audit3Id)

        if request.method == "POST": # type: ignore
            date_str = request.POST.get("date") # type: ignore
            observations = request.POST.get("observations") # type: ignore
            observations2 = request.POST.get("observations2") # type: ignore
            Udin = request.POST.get("Udin") # type: ignore
            
            formatted_date = None
            if date_str:
                try:
                    formatted_date = datetime.strptime(date_str, r"%Y-%m-%d").date()
                    audit.date = formatted_date
                    audit.observations = observations
                    audit.observations2 = observations2
                    audit.Udin = Udin
                    audit.save(update_fields=["date"])  # Ensure immediate commit
                    audit.save(update_fields=["observations"])
                    audit.save(update_fields=["observations2"])# Ensure immediate commit
                    audit.save(update_fields=["Udin"])
                except ValueError:
                    formatted_date = None
                    

            print(audit2)

            # Fetch updated reports
            yearReport1 = yearReportData.objects.filter(yearReports__audit=audit).first()
            yearReport2 = yearReportData.objects.filter(yearReports__audit=audit2).first() if audit2 else None
            yearReport3 = yearReportData.objects.filter(yearReports__audit=audit3).first() if audit3 else None
            year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""
            year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

            print(year1," - ",year2," - ",year3)
            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('EA', 'EB')):
                            field_name = f"{prefix}-{field.name}"
                            value = request.POST.get(field_name) # type: ignore
                            setattr(report, field.name, value if value else "")
                    report.save()

            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('A', 'B')):
                            field_name = f"{prefix}-{field.name}"
                            value = request.POST.get(field_name)
                            # print(field_name,'--',value)
                            setattr(report, field.name, int(value) if value else 0)
                    report.save()
            
            for func in [
            Fromula.openingClosingBalanceForCurrentYear,
            Fromula.total1,
            Fromula.formula48, Fromula.formula49, Fromula.formula49, 
            Fromula.formula50, Fromula.formula51, Fromula.formula52, Fromula.formula55,
            Fromula.Bformula45, Fromula.Bformula47, Fromula.Bformula49, 
            Fromula.Bformula50, Fromula.Bformula51, Fromula.Bformula52,Fromula.total1, Fromula.total2,
            Fromula.formulaA44,Fromula.formula55, Fromula.total3,Fromula.formula55,Fromula.openingClosingBalanceForCurrentYear
            ]:
                func(audit) # type: ignore
            audit.refresh_from_db()

            # Reload year reports to include formula updates
            main_report1 = MainReport.objects.filter(audit=audit).first()
            year_report1 = yearReportData.objects.filter(yearReports=main_report1).first() if main_report1 else None

            year_report2 = None
            if audit2:
                main_report2 = MainReport.objects.filter(audit=audit2).first()
                year_report2 = yearReportData.objects.filter(yearReports=main_report2).first() if main_report2 else None

            year_report3 = None
            if audit3:
                main_report3 = MainReport.objects.filter(audit=audit3).first()
                year_report3 = yearReportData.objects.filter(yearReports=main_report3).first() if main_report3 else None
            
            return render(request, r'templates/audit/newTry.html', { # type: ignore
                'yearReport1': year_report1, 
                'yearReport2': year_report2, 
                'yearReport3': year_report3,
                'year1': year1, 'year2': year2, 'year3': year3, 
                'year': year, 'audit': audit
            })
        # Ensure audits are properly assigned
        if not audit2Id and not audit3Id:
            setAuditFR(audit)
            for auditCheck in audits:
                if auditCheck['yearEnd'] == audit.yearStart:
                    audit2Id = auditCheck['id']
                    audit2 = Audit.objects.get(id=audit2Id)
                elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                    audit3Id = auditCheck['id']
                    audit3 = Audit.objects.get(id=audit3Id)
                    
        elif audit2Id and not audit3Id:
            setAuditFRSingleYear(audit)
            audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
            for auditCheck in audits:
                if auditCheck['yearEnd'] == audit.yearStart:
                    audit2Id = auditCheck['id']
                    audit2 = Audit.objects.get(id=audit2Id)
                elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                    audit3Id = auditCheck['id']
                    audit3 = Audit.objects.get(id=audit3Id)

        # Fetch second and third year data
        mainReport2 = MainReport.objects.filter(audit=audit2).first() if audit2 else None
        yearReport2 = yearReportData.objects.filter(yearReports=mainReport2).first() if mainReport2 else None
        year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""

        mainReport3 = MainReport.objects.filter(audit=audit3).first() if audit3 else None
        yearReport3 = yearReportData.objects.filter(yearReports=mainReport3).first() if mainReport3 else None
        year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

        return render(request, 'templates/audit/newTry.html', {
            'yearReport1': yearReport1, 'yearReport2': yearReport2, 'yearReport3': yearReport3,
            'year1': year1, 'year2': year2, 'year3': year3, 'year': year, 'audit': audit
        })

   
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def createAudit(request):
    #     if request.method == 'POST':
    #         auditType = request.POST.get('auditType')
    #         form = AuditForm(request.POST)
    #         if form.is_valid():
    #             audit = form.save(commit=False)
    #             collectionid = setAudit(auditType)
    #             audit.collection = collectionid
    #             audit.save()
    #         else :
    #             return JsonResponse({'status': 'error'})
            
    #         return JsonResponse({'status': 'success'})
        
    #     form = AuditForm()
     
    #     return render(request, 'templates\\audit\\auditForm.html', {'form': form,'types': AuditType.objects.all()})
    



























   #  this is written fot the br logic 
    # @csrf_exempt
    # def checkDetails(request):
    #     # if request.method == 'POST':
    #     # Get the year from the form
    #         audit_id = request.GET.get('audit_id')
    #         audit = get_object_or_404(Audit, id=audit_id)
    #         audityear = audit.year
            
    #         # audityear = request.POST.get('year')
    #         # print(f"Year submitted: {audityear}")  # Debugging

    #         # # Validate the audit record
    #         # audit = Audit.objects.filter(year=audityear).first()
    #         if not audit:
    #             print("Audit record not found")  # Debugging
    #             return JsonResponse({'error': 'Audit record not found'}, status=404)

    #         # Fetch all months for the given audit year
    #         months = Month.objects.filter(collectionId=audit.collection.id)
    #         print(f"Months fetched: {months}")  # Debugging

    #         # Fetch all BackendReport objects for the months
    #         reports = BackendReport.objects.filter(month__in=months)
    #         print(f"Reports fetched: {reports}")  # Debugging

    #         # Process the data for the template
    #         data = {}
    #         for report in reports:
    #             month = report.month.month
    #             title = report.title
    #             dict_data = report.dict
    #             pk = report.pk  # Include the primary key

    #             if month not in data:
    #                 data[month] = {}

    #             # Include the pk in the data structure
    #             data[month][title] = {
    #                 'pk': pk,  # Add the primary key
    #                 'dict': dict_data  # Include the dict data
    #             }

    #         # Convert data to a list of tuples for the template
    #         data_items = list(data.items())
    #         print(f"Data Items: {data_items}")  # Debugging

    #         # Pass the data to the template
    #         return render(request, 'templates/audit/report.html', {'data_items': data_items, 'year': audityear})

        # return render(request, 'templates/audit/report.html')

# this logic is to save the br 
    @csrf_exempt
    def save_report_value(request):
        if request.method == 'POST':
            try:
                
                # Parse the JSON data from the request
                data = json.loads(request.body)
                logger.info(f"Received data: {data}")  # Log the incoming data
                
                pk = data.get('pk')  # Primary key of the BackendReport object
                key = data.get('key')  # Key in the dict
                value = data.get('value')  # New value to save

                # Validate the required fields
                if not pk or not key or value is None:
                    logger.error("Missing required fields in request data")
                    return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

                # Fetch the BackendReport object
                try:
                    report = BackendReport.objects.get(pk=pk)
                    logger.info(f"Found report: {report}")
                except BackendReport.DoesNotExist:
                    logger.error(f"Report with pk={pk} not found")
                    return JsonResponse({'status': 'error', 'message': 'Report not found'}, status=404)

                # Update the dict value
                if not isinstance(report.dict, dict):
                    logger.error(f"Invalid dict field in report: {report.dict}")
                    return JsonResponse({'status': 'error', 'message': 'Invalid dict field'}, status=400)

                report.dict[key] = value
                report.save()

                logger.info(f"Updated report: {report.dict}")
                return JsonResponse({'status': 'success', 'message': 'Value saved successfully'})

            except json.JSONDecodeError:
                logger.error("Invalid JSON data in request")
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    
    
    @csrf_exempt
    def viewBackReportcomplete(request):
        if request.method == 'POST':
            audityear = request.POST.get('year')

            # Validate the audit record
            audit = Audit.objects.filter(year=audityear).first()
            if not audit:
                return JsonResponse({'error': 'Audit record not found'}, status=404)

            months = Month.objects.filter(collectionId=audit.collection.id)
            Coll = []

            for month in months:
                Brs = BackendReport.objects.filter(month=month)
                Coll.extend(Brs)  # Flattening the list instead of appending QuerySets

            # Convert objects to a JSON-friendly format
            data = [
                {
                    "pk": obj.pk,
                    "month": obj.month.id,
                    "title": obj.title,
                    "dict": obj.dict
                }
                for obj in Coll
            ]
            
            # print(data)
            return JsonResponse({"reports": data})  # Return a properly formatted JSON response

        return JsonResponse({'error': 'Invalid request method'}, status=400)