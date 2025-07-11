
from reportaudit.backendReport.backendReportService import setAllBr
from reportaudit.models import Audit, MainReport, Month, Collection, yearReportData

# this is for the br logic 

# def setAudit(auditType):
#      # pura flow rhega yahi pe--------------
#         # collection bna 
#         colle = Collection.objects.create()
#         months = ['April','May','June','July','Agust','September','Octuber','Nevember','December','January','Febrauary','March','Total']
#         # months ka pura list collection me add kar 
#         for i, monthName in zip(range(1, 14), months):
#             month = Month.objects.create(month=monthName, collectionId=colle)
#             print(month, " - -  ", i)
#             setAllBr(month, auditType)
#         return colle
            
        # fir br me months ko add kar 
        # yha pe function call karke all br get karke uska list chayiye (month,type) return queryset -- is function ko 12 chaenge taki bbara barr humara month mil jye of usi months me collection ko attache kar denge 



#  this is for the fr logic 
def setAuditFR(auditC):
    #  jo year dalega uske phele do sall ka report hai ki nai ye dekhna hai 
    #  agar hai to uska fetch karna hai or publich krnahai 
    #  agar nai hai to create krna hi or fir publish krna hai 

    mainReport1 = MainReport.objects.create(audit = auditC)
    yearReportData.objects.create(yearReports= mainReport1)
    
    audits = Audit.objects.filter(customer=auditC.customer).all()
    allyears = []
    for auditI in audits :
        allyears.append(int(auditI.yearEnd))
        
    if int(auditC.yearStart) in allyears:
            pass
    else:
            auditOne = Audit.objects.create(yearEnd = auditC.yearStart, yearStart= int(auditC.yearStart)-1,customer = auditC.customer,Udin = auditC.Udin)
            mainReport2 = MainReport.objects.create(audit = auditOne)
            yearReportData.objects.create(yearReports= mainReport2)
            
            auditTwo = Audit.objects.create(yearEnd = auditOne.yearStart, yearStart= int(auditOne.yearStart)-1,customer = auditC.customer,Udin = auditC.Udin)
            mainReport3 = MainReport.objects.create(audit = auditTwo)
            yearReportData.objects.create(yearReports= mainReport3)
        
    
    
    # 1.fetch the year
    
def setAuditFRSingleYear(auditC):
   
        
        audits = Audit.objects.filter(customer=auditC.customer).all()
        allyears = []
        for auditI in audits :
                allyears.append(int(auditI.yearEnd))
                
        if int(auditC.yearStart-2) in allyears:
                print("yes")
                pass
        else:
       
                auditTwo = Audit.objects.create(yearEnd = auditC.yearStart-1, yearStart= int(auditC.yearStart)-2,customer = auditC.customer,Udin = auditC.Udin)
                mainReport3 = MainReport.objects.create(audit = auditTwo)
                yearReportData.objects.create(yearReports= mainReport3)