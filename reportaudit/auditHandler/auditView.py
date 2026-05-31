
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
from reportaudit.models import BackendReport, Cluster ,Customer ,AuditType ,Audit, MainReport, Month, ObservationTablerows, yearReportData
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

        observationTable1 = []
        observationTable2 = []

        for i in range(1, 11):
                row_name = f"table1Row{i}"
                try:
                    if ObservationTablerows.objects.get(audit=audit, observationTable=1, name=row_name):
                        observationTable1.append(ObservationTablerows.objects.get(audit=audit, observationTable=1, name=row_name))
             
                except ObservationTablerows.DoesNotExist:
                    # observationTable1.append(None)        
                    print("")

            # for getting 2nd table data (POST)
        for i in range(1, 11):
                row_name = f"table2Row{i}"
                try:
                    if ObservationTablerows.objects.get(audit=audit, observationTable=2, name=row_name):
                        observationTable2.append(ObservationTablerows.objects.get(audit=audit, observationTable=2, name=row_name))
                    
                except ObservationTablerows.DoesNotExist:
                    # observationTable2.append(None)        
                    print("")

        print(len(observationTable1),len(observationTable2))

           
        html_string = render_to_string( 'templates/audit/oneMoreTry.html',
            {
                'yearReport1': yearReport1,
                'yearReport2': yearReport2,
                'yearReport3': yearReport3,
                'year1': year1,
                'year2': year2,
                'year3': year3,
                'year': year,
                'audit': audit,
                'observationTable1' : observationTable1,
                'observationTable2':observationTable2,
            }
        )        
        base_url = request.build_absolute_uri('/')[:-1]  
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
          
    
    # def mainReport(request): # type: ignore
    #     audit_id = request.GET.get('audit_id') # type: ignore
    #     audit = get_object_or_404(Audit, id=audit_id)

    #     year = str(audit.yearEnd)
    #     year1 = f"{audit.yearStart}-{audit.yearEnd}"

    #     # Fetch main report and year report data
    #     mainReport1 = MainReport.objects.select_related('audit').filter(audit=audit).first()
    #     yearReport1 = yearReportData.objects.select_related('yearReports').filter(yearReports=mainReport1).first()

    #     # Run formula calculations and ensure they are saved
    #     for func in [
    #         Fromula.openingClosingBalanceForCurrentYear,Fromula.carryFrowordToText,
    #         Fromula.total1,
    #         Fromula.formula48, Fromula.formula49, 
    #         Fromula.formula50, Fromula.formula51, Fromula.formula52,Fromula.formula53,Fromula.formula54, Fromula.formula55,Fromula.formula56,Fromula.formula57,Fromula.formula58,
    #         Fromula.formula59,Fromula.formula60,Fromula.formula61,Fromula.formula62,
    #         Fromula.Bformula47, Fromula.Bformula50, Fromula.Bformula51, 
    #         Fromula.Bformula52, Fromula.Bformula53, Fromula.Bformula54, Fromula.Bformula55,Fromula.total1, Fromula.total2,Fromula.formula46,Fromula.formula67,Fromula.Bformula58,Fromula.Bformula59,Fromula.formula62,Fromula.total3
    #         ]:
    #         func(audit) # type: ignore
    #         audit.refresh_from_db()

    #     # Force reload the updated audit data
    #     audit.refresh_from_db()

    #     audit2Id = None
    #     audit3Id = None
    #     audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
        
    #     audit2, audit3 = None, None

    #     # Finding previous audits
    #     for auditCheck in audits:
    #         if audit.yearStart == auditCheck['yearEnd']:
    #             audit2Id = auditCheck['id']
    #             audit2 = Audit.objects.get(id=audit2Id)
    #         elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
    #             audit3Id = auditCheck['id']
    #             audit3 = Audit.objects.get(id=audit3Id)

    #     if request.method == "POST": # type: ignore
    #         date_str = request.POST.get("date") # type: ignore
    #         observations = request.POST.get("observations") # type: ignore
    #         observations2 = request.POST.get("observations2") # type: ignore
    #         Udin = request.POST.get("Udin") # type: ignore
            
    #         formatted_date = None
    #         if date_str:
    #             try:
    #                 formatted_date = datetime.strptime(date_str, r"%Y-%m-%d").date()
    #                 audit.date = formatted_date
    #                 audit.observations = observations
    #                 audit.observations2 = observations2
    #                 audit.Udin = Udin
    #                 audit.save(update_fields=["date"])  # Ensure immediate commit
    #                 audit.save(update_fields=["observations"])
    #                 audit.save(update_fields=["observations2"])# Ensure immediate commit
    #                 audit.save(update_fields=["Udin"])
    #             except ValueError:
    #                 formatted_date = None
                    

    #         print(audit2)

    #         # Fetch updated reports
    #         yearReport1 = yearReportData.objects.filter(yearReports__audit=audit).first()
    #         yearReport2 = yearReportData.objects.filter(yearReports__audit=audit2).first() if audit2 else None
    #         yearReport3 = yearReportData.objects.filter(yearReports__audit=audit3).first() if audit3 else None
    #         year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""
    #         year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

    #         print(year1," - ",year2," - ",year3)
    #         for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
    #             if report:
    #                 for field in report._meta.fields:
    #                     if field.name.startswith(('EA', 'EB')):
    #                         field_name = f"{prefix}-{field.name}"
                            
    #                         value = request.POST.get(field_name) # type: ignore
                           
    #                         setattr(report, field.name, value if value else "")
    #                 report.save()

    #         for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
    #             if report:
    #                 for field in report._meta.fields:
    #                     if field.name.startswith(('A', 'B')):
    #                         field_name = f"{prefix}-{field.name}"
    #                         value = request.POST.get(field_name)
    #                         # print(field_name,'--',value)
    #                         setattr(report, field.name, int(value) if value else 0)
    #                 report.save()
            
    #         for func in [
    #         Fromula.openingClosingBalanceForCurrentYear,Fromula.carryFrowordToText,
    #         Fromula.total1,
    #         Fromula.formula48, Fromula.formula49, 
    #         Fromula.formula50, Fromula.formula51, Fromula.formula52,Fromula.formula53,Fromula.formula54, Fromula.formula55,Fromula.formula56,Fromula.formula57,Fromula.formula58,
    #         Fromula.formula59,Fromula.formula60,Fromula.formula61,Fromula.formula62,
    #         Fromula.Bformula47, Fromula.Bformula50, Fromula.Bformula51, 
    #         Fromula.Bformula52, Fromula.Bformula53, Fromula.Bformula54, Fromula.Bformula55,Fromula.total1, Fromula.total2,Fromula.formula46,Fromula.formula67,Fromula.Bformula58,Fromula.Bformula59,Fromula.formula62,Fromula.total3
    #         ]:
    #             func(audit) # type: ignore
    #         audit.refresh_from_db()

    #         # Reload year reports to include formula updates
    #         main_report1 = MainReport.objects.filter(audit=audit).first()
    #         year_report1 = yearReportData.objects.filter(yearReports=main_report1).first() if main_report1 else None

    #         year_report2 = None
    #         if audit2:
    #             main_report2 = MainReport.objects.filter(audit=audit2).first()
    #             year_report2 = yearReportData.objects.filter(yearReports=main_report2).first() if main_report2 else None

    #         year_report3 = None
    #         if audit3:
    #             main_report3 = MainReport.objects.filter(audit=audit3).first()
    #             year_report3 = yearReportData.objects.filter(yearReports=main_report3).first() if main_report3 else None
            
    #         return render(request, r'templates/audit/oneMoreTry.html', { # type: ignore
    #             'yearReport1': year_report1, 
    #             'yearReport2': year_report2, 
    #             'yearReport3': year_report3,
    #             'year1': year1, 'year2': year2, 'year3': year3, 
    #             'year': year, 'audit': audit
    #         })
    #     # Ensure audits are properly assigned
    #     if not audit2Id and not audit3Id:
    #         setAuditFR(audit)
    #         for auditCheck in audits:
    #             if auditCheck['yearEnd'] == audit.yearStart:
    #                 audit2Id = auditCheck['id']
    #                 audit2 = Audit.objects.get(id=audit2Id)
    #             elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
    #                 audit3Id = auditCheck['id']
    #                 audit3 = Audit.objects.get(id=audit3Id)
                    
    #     elif audit2Id and not audit3Id:
    #         setAuditFRSingleYear(audit)
    #         audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
    #         for auditCheck in audits:
    #             if auditCheck['yearEnd'] == audit.yearStart:
    #                 audit2Id = auditCheck['id']
    #                 audit2 = Audit.objects.get(id=audit2Id)
    #             elif audit2 and auditCheck['yearEnd'] == audit2.yearStart:
    #                 audit3Id = auditCheck['id']
    #                 audit3 = Audit.objects.get(id=audit3Id)

    #     # Fetch second and third year data
    #     mainReport2 = MainReport.objects.filter(audit=audit2).first() if audit2 else None
    #     yearReport2 = yearReportData.objects.filter(yearReports=mainReport2).first() if mainReport2 else None
    #     year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""

    #     mainReport3 = MainReport.objects.filter(audit=audit3).first() if audit3 else None
    #     yearReport3 = yearReportData.objects.filter(yearReports=mainReport3).first() if mainReport3 else None
    #     year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

    #     return render(request, 'templates/audit/oneMoreTry.html', {
    #         'yearReport1': yearReport1, 'yearReport2': yearReport2, 'yearReport3': yearReport3,
    #         'year1': year1, 'year2': year2, 'year3': year3, 'year': year, 'audit': audit
    #     })

    def mainReport(request): # type: ignore
        audit_id = request.GET.get('audit_id') # type: ignore
        audit = get_object_or_404(Audit, id=audit_id)

        observationTable1 = []
        observationTable2 = []

        year = str(audit.yearEnd)
        year1 = f"{audit.yearStart}-{audit.yearEnd}"

        # Fetch main report and year report data
        mainReport1 = MainReport.objects.select_related('audit').filter(audit=audit).first()
        yearReport1 = yearReportData.objects.select_related('yearReports').filter(yearReports=mainReport1).first()

        # Run formula calculations and ensure they are saved
        formula_list = [
            Fromula.openingClosingBalanceForCurrentYear, Fromula.carryFrowordToText, Fromula.total1,
            Fromula.formula48, Fromula.formula49, Fromula.formula50, Fromula.formula51, Fromula.formula52, 
            Fromula.formula53, Fromula.formula54, Fromula.formula55, Fromula.formula56, Fromula.formula57, 
            Fromula.formula58, Fromula.formula59, Fromula.formula60, Fromula.formula61, Fromula.formula62,
            Fromula.Bformula47, Fromula.Bformula50, Fromula.Bformula51, Fromula.Bformula52, Fromula.Bformula53, 
            Fromula.Bformula54, Fromula.Bformula55, Fromula.Bformula56, Fromula.total1, Fromula.total2, Fromula.formula46, 
            Fromula.formula67, Fromula.Bformula58, Fromula.Bformula59, Fromula.formula62, Fromula.total3
        ]

        for func in formula_list:
            func(audit) # type: ignore
            audit.refresh_from_db() # type: ignore

        audit.refresh_from_db() # type: ignore

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
            obs_select_1 = request.POST.get("obs_select_1") == "True" # type: ignore
            obs_select_2 = request.POST.get("obs_select_2") == "True" # type: ignore
            obs_select_3 = request.POST.get("obs_select_3") == "True" # type: ignore
            obs_select_4 = request.POST.get("obs_select_4") == "True" # type: ignore
            obs_select_5 = request.POST.get("obs_select_5") == "True" # type: ignore
            obs_select_6 = request.POST.get("obs_select_6") == "True" # type: ignore
            obs_select_7 = request.POST.get("obs_select_7") == "True" # type: ignore
            obs_select_8 = request.POST.get("obs_select_8") == "True" # type: ignore

            print(obs_select_1," observation nai ara kyu")

            # DYNAMIC EXTRACTION & ASSIGNMENT FOR ROW B CHECKBOXES
            for i in range(1, 11):
                t1_key = f"table1Row{i}B"
                t1_val = request.POST.get(t1_key) # type: ignore
                setattr(audit, t1_key, True if t1_val == "True" else False)

                t2_key = f"table2Row{i}B"
                t2_val = request.POST.get(t2_key) # type: ignore
                setattr(audit, t2_key, True if t2_val == "True" else False)

            audit.observationRequired = obs_select_1
            if obs_select_2: 
                audit.observationP1 = obs_select_2
                table1row1 = ObservationTablerows.objects.create(audit=audit, observationTable=1, name='table1row1')
                audit.table1Row1B = True
                table1row1.save()
                
            else : audit.observationP1 = False
                
            audit.observationP2 = obs_select_3
            audit.observationP3 = obs_select_4
            audit.observationP4 = obs_select_5
            audit.observationP5 = obs_select_6
            audit.observationP6 = obs_select_7
            if obs_select_8: 
                audit.observationP7 = obs_select_8
                table2row1 = ObservationTablerows.objects.create(audit=audit, observationTable=2, name='table2row1')
                audit.table2Row1B = True
                table2row1.save()
                
            
            else : audit.observationP7 = False
            audit.save()
            observationValue1 = request.POST.get("observationValue1") # type: ignore
            observationValue2 = request.POST.get("observationValue2") # type: ignore
            observationValue3 = request.POST.get("observationValue3") # type: ignore
            observationValue4 = request.POST.get("observationValue4") # type: ignore
            observationValue5 = request.POST.get("observationValue5") # type: ignore
            observationValue6 = request.POST.get("observationValue6") # type: ignore

            if observationValue1: audit.observationValue1 = observationValue1
            if observationValue2: audit.observationValue2 = observationValue2
            if observationValue3: audit.observationValue3 = observationValue3
            if observationValue4: audit.observationValue4 = observationValue4
            if observationValue5: audit.observationValue5 = observationValue5
            if observationValue6: audit.observationValue6 = observationValue6

            # for getting boolean value for table 1
            for i in range(1, 11):
                key_name = f"table1Row{i}B"
                col_avil = request.POST.get(key_name) # type: ignore
                if col_avil:
                    setattr(audit, key_name, col_avil)

            # for getting boolean value for table 2
            for i in range(1, 11):
                key_name = f"table2Row{i}B"
                col_avil = request.POST.get(key_name) # type: ignore
                if col_avil:
                    setattr(audit, key_name, col_avil)

            # for getting the row value for table 1
            for i in range(1, 11):
                row_name = f"table1Row{i}"
                col1_data = request.POST.get(f"{row_name}_col1") # type: ignore
                if col1_data:
                    obj, created = ObservationTablerows.objects.get_or_create(
                        audit=audit, name=row_name, observationTable=1
                    )
                    if not created:
                        obj.observationTable = 1
                    obj.col1 = col1_data
                    obj.col2 = request.POST.get(f"{row_name}_col2") # type: ignore
                    obj.col3 = request.POST.get(f"{row_name}_col3") # type: ignore
                    obj.save()
                else :
                    ObservationTablerows.objects.filter(
                        audit=audit, name=row_name, observationTable=1
                    ).delete()
                

            # for getting the row value for table 2
            for i in range(1, 11):
                row_name = f"table2Row{i}"
                col1_data = request.POST.get(f"{row_name}_col1") # type: ignore
                if col1_data:
                    obj, created = ObservationTablerows.objects.get_or_create(
                        audit=audit, name=row_name, observationTable=2
                    )
                    if not created:
                        obj.observationTable = 2
                    obj.col1 = col1_data
                    obj.col2 = request.POST.get(f"{row_name}_col2") # type: ignore
                    obj.col3 = request.POST.get(f"{row_name}_col3") # type: ignore
                    obj.col4 = request.POST.get(f"{row_name}_col4") # type: ignore
                    obj.col5 = request.POST.get(f"{row_name}_col5") # type: ignore
                    
                    obj.save()
                else :
                    ObservationTablerows.objects.filter(
                        audit=audit, name=row_name, observationTable=2).delete()
                    

                    
                
            audit.save()
            
            # for getting 1st table data (POST)
            for i in range(1, 11):
                row_name = f"table1Row{i}"
                try:
                    observationTable1.append(ObservationTablerows.objects.get(audit=audit, observationTable=1, name=row_name))
             
                except ObservationTablerows.DoesNotExist:
                    observationTable1.append(None)

            # for getting 2nd table data (POST)
            for i in range(1, 11):
                row_name = f"table2Row{i}"
                try:
                    observationTable2.append(ObservationTablerows.objects.get(audit=audit, observationTable=2, name=row_name))
                    
                except ObservationTablerows.DoesNotExist:
                    observationTable2.append(None)        

           

            if date_str:
                try:
                    audit.date = datetime.strptime(date_str, r"%Y-%m-%d").date()
                    audit.observations = observations
                    audit.observations2 = observations2
                    audit.Udin = Udin
                    audit.save(update_fields=["date", "observations", "observations2", "Udin"])
                except ValueError:
                    pass

            yearReport1 = yearReportData.objects.filter(yearReports__audit=audit).first()
            yearReport2 = yearReportData.objects.filter(yearReports__audit=audit2).first() if audit2 else None
            yearReport3 = yearReportData.objects.filter(yearReports__audit=audit3).first() if audit3 else None
            year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""
            year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('EA', 'EB')):
                            setattr(report, field.name, request.POST.get(f"{prefix}-{field.name}", ""))
                    report.save()

            for prefix, report in [('year1', yearReport1), ('year2', yearReport2), ('year3', yearReport3)]:
                if report:
                    for field in report._meta.fields:
                        if field.name.startswith(('A', 'B')):
                            val = request.POST.get(f"{prefix}-{field.name}") # type: ignore
                            setattr(report, field.name, int(val) if val else 0)
                    report.save()
            
            for func in formula_list:
                func(audit) # type: ignore
            audit.refresh_from_db() # type: ignore

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
                'yearReport1': year_report1, 'yearReport2': year_report2, 'yearReport3': year_report3,
                'year1': year1, 'year2': year2, 'year3': year3, 'year': year, 'audit': audit,
                'observationTable1': observationTable1,
                'observationTable2': observationTable2,
            })

        # Ensure audits are properly assigned (GET Path Setup)
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

        # for getting get type table 1 (GET)
        for i in range(1, 11):
            row_name = f"table1Row{i}"
            try:
                observationTable1.append(ObservationTablerows.objects.get(audit=audit, observationTable=1, name=row_name))
            except ObservationTablerows.DoesNotExist:
                observationTable1.append(None)

        # for getting get type table 2 (GET) - FIXED: Target changed from table1 to table2
        for i in range(1, 11):
            row_name = f"table2Row{i}"
            try:
                observationTable2.append(ObservationTablerows.objects.get(audit=audit, observationTable=2, name=row_name))
            except ObservationTablerows.DoesNotExist:
                observationTable2.append(None)

        mainReport2_obj = MainReport.objects.filter(audit=audit2).first() if audit2 else None
        yearReport2 = yearReportData.objects.filter(yearReports=mainReport2_obj).first() if mainReport2_obj else None
        year2 = f"{audit2.yearStart}-{audit2.yearEnd}" if audit2 else ""

        mainReport3_obj = MainReport.objects.filter(audit=audit3).first() if audit3 else None
        yearReport3 = yearReportData.objects.filter(yearReports=mainReport3_obj).first() if mainReport3_obj else None
        year3 = f"{audit3.yearStart}-{audit3.yearEnd}" if audit3 else ""

        return render(request, 'templates/audit/newTry.html', {
            'yearReport1': yearReport1, 'yearReport2': yearReport2, 'yearReport3': yearReport3,
            'year1': year1, 'year2': year2, 'year3': year3, 'year': year, 'audit': audit,
            'observationTable1': observationTable1,
            'observationTable2': observationTable2,
        })

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
        if request.method == 'POST': # type: ignore
            audityear = request.POST.get('year') # type: ignore

            # Validate the audit record
            audit = Audit.objects.filter(year=audityear).first()
            if not audit:
                return JsonResponse({'error': 'Audit record not found'}, status=404)

            months = Month.objects.filter(collectionId=audit.collection.id) # type: ignore
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