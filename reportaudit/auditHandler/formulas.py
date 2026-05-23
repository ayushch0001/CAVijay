

from django.shortcuts import get_object_or_404
from reportaudit.models import Audit, MainReport, yearReportData


class Fromula():
    
    @staticmethod
    def checkForYear(audit):    
         
      
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
               
                
                audits = list(Audit.objects.filter(customer=audit.customer).values('id', 'yearStart', 'yearEnd'))
                for auditCheck in audits:
                    if audit2 and auditCheck['yearEnd'] == audit2.yearStart:
                        audit3Id = auditCheck['id']
                        audit3 = Audit.objects.get(id=audit3Id)
                
        mainReport2 = MainReport.objects.filter(audit=audit2).first() if audit2 else None
        yearReport2 = yearReportData.objects.filter(yearReports=mainReport2).first() if mainReport2 else None
       

        # Fetch third year data
        mainReport3 = MainReport.objects.filter(audit=audit3).first() if audit3 else None
        yearReport3 = yearReportData.objects.filter(yearReports=mainReport3).first() if mainReport3 else None
        
        return yearReport1,yearReport2,yearReport3
    
    
    def openingClosingBalanceForCurrentYear(audit):
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)

        if yearReport2.B40 :
              yearReport1.A0 = yearReport2.B40
        if yearReport2.B41 :
             yearReport1.B0 = yearReport2.B41
        yearReport1.save()
    
    def carryFrowordToText(audit): # type: ignore
         yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
         if yearReport2.EA1 :
              yearReport1.EA1 = yearReport2.EA1
         if yearReport2.EA2 :
              yearReport1.EA2 = yearReport2.EA2
         if yearReport2.EB1 :
              print("getting B")
              yearReport1.EB1 = yearReport2.EB1
         if yearReport2.EB2 :
              yearReport1.EB2 = yearReport2.EB2

         yearReport1.save()
         yearReport2.save()

              
        
    
    def formula48(audit): # Saving from member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        yearReport2.A48 = yearReport3.A48 + yearReport2.A2
        yearReport2.save()
        yearReport1.A48 = yearReport2.A48 + yearReport1.A2 
        yearReport1.save()


    def formula49(audit): # Share capital paid by member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A49 = yearReport3.A49 + yearReport2.A3
        yearReport2.save()
        yearReport1.A49 = yearReport2.A49 + yearReport1.A3

        yearReport1.save()
        
    def formula50(audit): # CIF grant/loan outstanding to mission /CLF
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A50 = yearReport3.A50 + yearReport2.A1 - yearReport2.B31
        yearReport2.save()
        yearReport1.A50 = yearReport2.A50 + yearReport1.A1 - yearReport1.B31
     
        yearReport1.save()

    def formula51(audit): # CEF (SVEP) grant / loan outstanding to mission / CLF
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)   
        
        yearReport2.A51 = yearReport3.A51 + yearReport2.A5 - yearReport2.B32
        yearReport2.save()
        yearReport1.A51 = yearReport2.A51 + yearReport1.A5 - yearReport1.B32
    
        yearReport1.save()
        
    def formula52(audit): # Grant for promotion of PGs (including working capital and infrastructure)
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A52 = yearReport3.A52 + yearReport2.A6 - yearReport2.B34
        yearReport2.save()
        yearReport1.A52 = yearReport2.A52 + yearReport1.A6 - yearReport1.B34
      
        yearReport1.save()
        
    def formula53(audit): # Other grants received for on lending
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A53 = yearReport3.A53 + yearReport2.A7 - yearReport2.B35
        yearReport2.save()
        yearReport1.A53 = yearReport2.A53 + yearReport1.A7 - yearReport1.B35
    
        yearReport1.save()
        
    def formula54(audit): # MKSP / CMSA Tool Bank Fund
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A54 = yearReport3.A54 +  yearReport2.A30 
        yearReport2.save()

        yearReport1.A54 = yearReport2.A54 +    yearReport1.A30 
        yearReport1.save()
     
    def formula55(audit): # NPM Shop Budget
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A55 = yearReport3.A55 +  yearReport2.A25 
        yearReport2.save()

        yearReport1.A55 = yearReport2.A55 +    yearReport1.A25 
        yearReport1.save()

    def formula56(audit): # PMFME Budget
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A56 = yearReport3.A56 +  yearReport2.A26 
        yearReport2.save()

        yearReport1.A56 = yearReport2.A56 +    yearReport1.A226
        yearReport1.save()

    def formula57(audit): # Livelihood (Ajivika) Budget
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A57 = yearReport3.A57 +  yearReport2.A27 
        yearReport2.save()

        yearReport1.A57 = yearReport2.A57 +    yearReport1.A27
        yearReport1.save()
        
    def formula58(audit): # RF Budge
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.A58 = yearReport3.A58 +  yearReport2.A28 
        yearReport2.save()

        yearReport1.A58 = yearReport2.A58 +    yearReport1.A28
        yearReport1.save()

    def formula59(audit): # Remuneration Payable to CRPs/cadres
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        value1 = yearReport3.A59 +  yearReport2.A24 - yearReport2.B21 
        if value1 > 0 : yearReport2.A59 = value1 
        else :  yearReport2.B57 = value1
        yearReport2.save()

        value2 = yearReport2.A59 +    yearReport1.A24 - yearReport1.B21
        if value2 > 0 : yearReport1.A59 =  value2 
        else : yearReport1.B57 = value2
        yearReport1.save()

    def formula60(audit): # Members MGNREGA Amount Payable by VO
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)

        yearReport2.A60 = yearReport3.A60 +  yearReport2.A29 - yearReport2.B26 
        yearReport2.save()
        yearReport1.A60 = yearReport2.A60 +    yearReport1.A29 - yearReport1.B26
        yearReport1.save()

    def formula61(audit): # Remuneration Payable to CRPs/cadres
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        value1 = yearReport3.A61 +  yearReport2.A11 - yearReport2.B15 
        if value1 > 0 : yearReport2.A61 = value1 
        else : yearReport2.B60 = value1
        yearReport2.save()

        value2 = yearReport2.A61 +    yearReport1.A11 - yearReport1.B15
        if value2 > 0 : yearReport1.A61 =  value2 
        else : yearReport1.B60 = value2
        yearReport1.save()


    def formula62(audit): # Reserve Opening balance
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)

        yearReport1.A63 = yearReport1.B46
        yearReport2.A63 = yearReport2.B46
        yearReport3.A63 = yearReport3.B46

        yearReport1.A64 = yearReport1.A46
        yearReport2.A64 = yearReport2.A46
        yearReport3.A64 = yearReport3.A46

        yearReport2.A62 = yearReport3.A62 +  yearReport3.A63 - yearReport3.A64 - yearReport3.A65 
        yearReport2.save()
        yearReport1.A62 = yearReport2.A62 +  yearReport2.A63 - yearReport2.A64 - yearReport2.A65 
        yearReport1.save()





    def Bformula47(audit): # Fixed Assets (Capital) Opening balance
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.B47 = yearReport3.B47 + yearReport3.B1
        yearReport2.save()
        yearReport1.B47 = yearReport2.B47 + yearReport2.B1
      
        yearReport1.save()
        
    def Bformula50(audit): #CIF Loan Outstanding with member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        yearReport2.B50 = yearReport3.B50 + yearReport2.B27 - yearReport2.A31
        yearReport2.save()
        yearReport1.B50 = yearReport2.B50 + yearReport1.B27 - yearReport1.A31
    
        yearReport1.save()
    

    def Bformula51(audit): # CEF (SVEP) Loan Outstanding
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.B51 = yearReport3.B51 + yearReport2.B28 - yearReport2.A32
        yearReport2.save()
        yearReport1.B51 = yearReport2.B51 + yearReport1.B28 - yearReport1.A32
        yearReport1.save()
        
    def Bformula52(audit): # PG Loan Outstanding with member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        yearReport2.B52 = yearReport3.B52 + yearReport2.B29 - yearReport2.A36
        yearReport2.save()
        yearReport1.B52 = yearReport2.B52 + yearReport1.B29 - yearReport1.A36
     
        yearReport1.save()
        
    def Bformula53(audit): # Loan outstanding from the loans given from other grants
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.B53 = yearReport3.B53 + yearReport2.B30 - yearReport2.A37
        yearReport2.save()
        yearReport1.B53 = yearReport2.B53 + yearReport1.B30 - yearReport1.A37
   
        yearReport1.save()
         

    def Bformula54(audit): # VRF Loan Outstanding with member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.B54 = yearReport3.B54 + yearReport2.B20 - yearReport2.A33
        yearReport2.save()
        yearReport1.B54 = yearReport2.B54 + yearReport1.B20 - yearReport1.A33
   
        yearReport1.save()
    
    def Bformula55(audit): # PMFME Loan Outstanding with member organisations
        yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
        
        yearReport2.B55 = yearReport3.B55 + yearReport2.B33 - yearReport2.A34
        yearReport2.save()
        yearReport1.B55 = yearReport2.B55 + yearReport1.B33 - yearReport1.A34
   
        yearReport1.save()




        
        
    def total1(audit):
            yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
            
            yearReport1.A42 = yearReport1.A0 + yearReport1.B0 + yearReport1.A1 + yearReport1.A2 + yearReport1.A3 + yearReport1.A4 + yearReport1.A5 + yearReport1.A6 + yearReport1.A7 + yearReport1.A8 + yearReport1.A9 + yearReport1.A10 + yearReport1.A11 + yearReport1.A12 + yearReport1.A13 + yearReport1.A14 + yearReport1.A15 + yearReport1.A16 + yearReport1.A17 + yearReport1.A18 + yearReport1.A19 + yearReport1.A20 + yearReport1.A21 + yearReport1.A22 + yearReport1.A23 + yearReport1.A24 + yearReport1.A25 + yearReport1.A26 + yearReport1.A27 + yearReport1.A28 + yearReport1.A29 + yearReport1.A30 + yearReport1.A31 + yearReport1.A32 +
            yearReport1.A33 + yearReport1.A34 + yearReport1.A35 + yearReport1.A36 +  yearReport1.A37   
            
         
            yearReport1.B42 = yearReport1.B1 + yearReport1.B2 + yearReport1.B3 + yearReport1.B4 + yearReport1.B5 + yearReport1.B6 + yearReport1.B7 + yearReport1.B8 + yearReport1.B9 + yearReport1.B10 + yearReport1.B11 + yearReport1.B12 + yearReport1.B13 + yearReport1.B14 + yearReport1.B15 + yearReport1.B16 + yearReport1.B17 + yearReport1.B18 + yearReport1.B19 + yearReport1.B20 + yearReport1.B21 + yearReport1.B22 + yearReport1.B23 + yearReport1.B24 + yearReport1.B25 + yearReport1.B26 + yearReport1.B27 + yearReport1.B28 + yearReport1.B29 + yearReport1.B30 + yearReport1.B31 + yearReport1.B32 + yearReport1.B33 + yearReport1.B34 + yearReport1.B35 + yearReport1.B36 + yearReport1.B37 + yearReport1.B38 + yearReport1.B39 +
            yearReport1.B40 + yearReport1.B41 
             
            yearReport1.save()
            
            yearReport2.A42 = yearReport2.A0 + yearReport2.B0 + yearReport2.A1 + yearReport2.A2 + yearReport2.A3 + yearReport2.A4 + yearReport2.A5 + yearReport2.A6 + yearReport2.A7 + yearReport2.A8 + yearReport2.A9 + yearReport2.A10 + yearReport2.A11 + yearReport2.A12 + yearReport2.A13 + yearReport2.A14 + yearReport2.A15 + yearReport2.A16 + yearReport2.A17 + yearReport2.A18 + yearReport2.A19 + yearReport2.A20 + yearReport2.A21 + yearReport2.A22 + yearReport2.A23 + yearReport2.A24 + yearReport2.A25 + yearReport2.A26 + yearReport2.A27 + yearReport2.A28 + yearReport2.A29 + yearReport2.A30 + yearReport2.A31 + yearReport2.A32 +
            yearReport2.A33 + yearReport2.A34 + yearReport2.A35 + yearReport2.A36 +  yearReport2.A37  
            
         
            yearReport2.B42 = yearReport2.B1 + yearReport2.B2 + yearReport2.B3 + yearReport2.B4 + yearReport2.B5 + yearReport2.B6 + yearReport2.B7 + yearReport2.B8 + yearReport2.B9 + yearReport2.B10 + yearReport2.B11 + yearReport2.B12 + yearReport2.B13 + yearReport2.B14 + yearReport2.B15 + yearReport2.B16 + yearReport2.B17 + yearReport2.B18 + yearReport2.B19 + yearReport2.B20 + yearReport2.B21 + yearReport2.B22 + yearReport2.B23 + yearReport2.B24 + yearReport2.B25 + yearReport2.B26 + yearReport2.B27 + yearReport2.B28 + yearReport2.B29 + yearReport2.B30 + yearReport2.B31 + yearReport2.B32 + yearReport2.B33 + yearReport2.B34 + yearReport2.B35 + yearReport2.B36 + yearReport2.B37 + yearReport2.B38 + yearReport2.B39 +
            yearReport2.B40 + yearReport2.B41 
             
            yearReport2.save()
            
            
            yearReport3.A42 = yearReport3.A0 + yearReport3.B0 + yearReport3.A1 + yearReport3.A2 + yearReport3.A3 + yearReport3.A4 + yearReport3.A5 + yearReport3.A6 + yearReport3.A7 + yearReport3.A8 + yearReport3.A9 + yearReport3.A10 + yearReport3.A11 + yearReport3.A12 + yearReport3.A13 + yearReport3.A14 + yearReport3.A15 + yearReport3.A16 + yearReport3.A17 + yearReport3.A18 + yearReport3.A19 + yearReport3.A20 + yearReport3.A21 + yearReport3.A22 + yearReport3.A23 + yearReport3.A24 + yearReport3.A25 + yearReport3.A26 + yearReport3.A27 + yearReport3.A28 + yearReport3.A29 + yearReport3.A30 + yearReport3.A31 + yearReport3.A32 +
            yearReport3.A33 + yearReport3.A34 + yearReport3.A35 + yearReport3.A36 +  yearReport3.A37  
            
         
            yearReport3.B42 = yearReport3.B1 + yearReport3.B2 + yearReport3.B3 + yearReport3.B4 + yearReport3.B5 + yearReport3.B6 + yearReport3.B7 + yearReport3.B8 + yearReport3.B9 + yearReport3.B10 + yearReport3.B11 + yearReport3.B12 + yearReport3.B13 + yearReport3.B14 + yearReport3.B15 + yearReport3.B16 + yearReport3.B17 + yearReport3.B18 + yearReport3.B19 + yearReport3.B20 + yearReport3.B21 + yearReport3.B22 + yearReport3.B23 + yearReport3.B24 + yearReport3.B25 + yearReport3.B26 + yearReport3.B27 + yearReport3.B28 + yearReport3.B29 + yearReport3.B30 + yearReport3.B31 + yearReport3.B32 + yearReport3.B33 + yearReport3.B34 + yearReport3.B35 + yearReport3.B36 + yearReport3.B37 + yearReport3.B38 + yearReport3.B39 +
            yearReport3.B40 + yearReport3.B41
             
            yearReport3.save()
            
    def total2(audit):
            yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
            
            yearReport1.A45 =  yearReport1.A5 +yearReport1.A6 +yearReport1A7 + yearReport1.A8 + yearReport1.A9 + yearReport1.A10 + yearReport1.A11 + yearReport1.A12 + yearReport1.A13 + yearReport1.A14 + yearReport1.A16 + yearReport1.A17 + yearReport1.A18 
            yearReport1.save()

            yearReport2.A45 =  yearReport2.A5 +yearReport2.A6 +yearReport2A7 + yearReport2.A8 + yearReport2.A9 + yearReport2.A10 + yearReport2.A11 + yearReport2.A12 + yearReport2.A13 + yearReport2.A14 + yearReport2.A16 + yearReport2.A17 + yearReport2.A18 + yearReport2.A20 + yearReport2.A35 + yearReport2.A29 + yearReport2.A30
            yearReport2.save()
            
            
            yearReport1.B45 =  yearReport1.B8 + yearReport1.B9 + yearReport1.B17 + yearReport1.A22 + yearReport1.B10 + yearReport1.B12 + yearReport1.B13 + yearReport1.B14 + yearReport1.B15 + yearReport1.B16  + yearReport1.A19 + yearReport1.A20 
            yearReport1.save()

            
            yearReport2.B45 =  yearReport2.B8 + yearReport2.B9 + yearReport2.B17 +  yearReport2.A22 + yearReport2.B10 + yearReport2.B12 + yearReport2.B13 + yearReport2.B14 + yearReport2.B15 + yearReport2.B16  + yearReport2.A19 + yearReport2.A20 
            yearReport2.save()
                   
           
    def total3(audit): # type: ignore
            
            yearReport1,yearReport2,yearReport3 = Fromula.checkForYear(audit)
          
            yearReport1.A66 =  yearReport1.A47 + yearReport1.A48 + yearReport1.A49 + yearReport1.A50 + yearReport1.A51 + yearReport1.A52 + yearReport1.A53 + yearReport1.A54 + yearReport1.A55 + yearReport1.A56 + yearReport1.A57 + yearReport1.A58 + yearReport1.A59 + yearReport1.A60 + yearReport1.A61 + yearReport1.A62 + yearReport1.A63 - yearReport1.A64

            yearReport1.save()
            
            yearReport2.A66 =  yearReport2.A47 + yearReport2.A48 + yearReport2.A49 + yearReport2.A50 + yearReport2.A51 + yearReport2.A52 + yearReport2.A53 + yearReport2.A54 + yearReport2.A55 + yearReport2.A56 + yearReport2.A57 + yearReport2.A58 + yearReport2.A59 + yearReport2.A60 + yearReport2.A61 + yearReport2.A62 + yearReport2.A63 - yearReport2.A64

            yearReport2.save()
            
            yearReport1.B66 = yearReport1.B47 + yearReport1.B1 + yearReport1.B2 + yearReport1.B47  + yearReport1.B49 + yearReport1.B50 + yearReport1.B51 + yearReport1.B52 + yearReport1.B53 + yearReport1.B54 + yearReport1.B55 + yearReport1.B56 + yearReport1.B57 + yearReport1.B58 + yearReport1.B59 + yearReport1.B60 + yearReport1.B61 + yearReport1.B62 + yearReport1.B63 + yearReport1.B40 + yearReport1.B41 

            yearReport1.save()
            
     
            yearReport2.B66 = yearReport2.B47 + yearReport2.B1 + yearReport2.B2 + yearReport2.B47  + yearReport2.B49 + yearReport2.B50 + yearReport2.B51 + yearReport2.B52 + yearReport2.B53 + yearReport2.B54 + yearReport2.B55 + yearReport2.B56 + yearReport2.B57 + yearReport2.B58 + yearReport2.B59 + yearReport2.B60 + yearReport2.B61 + yearReport2.B62 + yearReport2.B63 + yearReport2.B40 + yearReport2.B41

            yearReport2.save()
            
    


            