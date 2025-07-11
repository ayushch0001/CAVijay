from django.urls import path


from .views import home, register ,login_view, logout_view,process_values,get_dropdown_data,update_dropdown_data,home2
from reportaudit.auditHandler.auditView import auditView
# from reportaudit.auditHandler.auditView import viewBackReportcomplete_re
# from reportaudit.auditHandler.auditView import update_json_data
from reportaudit.auditType.auditTypeview import auditTypeView
from reportaudit.customerHandler.customerview import customerView
from reportaudit.backendReport.backendviews import backendView


urlpatterns = [
    path('', home, name='home'),  # Home page
    # path('', home2, name='home'),
    path('register/', register, name='register'),  # Register page
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('check/', process_values, name='check'),
    path('dropdown/', get_dropdown_data, name='dropdown'),
    path('update/', update_dropdown_data, name='update'),
    
    
    #customer
    path('createCustomer/', customerView.createCustomer, name='createCustomer'),
    
    #auditType
    path('createAuditType/', auditTypeView.create_audit_type, name='createAuditType'),
    
    #backendReport
     path('createBackend/', backendView.createBackendreport, name='createBackend'),
     
    #audit
    path('createAudit/', auditView.createAudit, name='createAudit'),
    # path('viewAudits/', auditView.viewAuditsOfCustomers, name='viewAudits'),
    path('viewBackReport/', auditView.viewBackReportcomplete, name='viewBackReport'),
    path('report_view/', auditView.report_view, name='report_view'),
    # path('update/', auditView.update_Backreport, name='update'),
    
    
    # # design
    # path('report_new/', auditView.report_new, name='report_new'),
    # path('report_new2/', auditView.report_new2, name='report_new2'),
    # path('view_json_data/', auditView.viewBackReportcomplete_re, name='report_agarin'),
    # path('update_json_data/', auditView.update_json_data, name='update_json_data'),
    
        #sample one no need of this 
    # path('report/', auditView.checkDetails, name='report'),
    path('report/', auditView.mainReport, name='report'),
    path('details/', auditView.fetchCusotmerPage, name='details'),
    path('save-report-value/', auditView.save_report_value, name='save_report_value'),
    path('search-customer/', auditView.search_customer, name='search_customer'),
    path('fetch-audits/', auditView.fetch_audits, name='fetch_audits'),
    path('generate_pdf/', auditView.generate_pdf, name='generate_pdf'),
    path('createCluster/', customerView.createCluster, name='createCluster'),
    path('get-customers-by-cluster/', auditView.get_customers_by_cluster, name='get_customers_by_cluster'),
    
    path('list-audits/', auditView.audit_list_view, name='list_audits'),
    path('get-customers/', customerView.get_customers_by_cluster, name='get_customers_by_cluster'),

    # You can later add:
    path('edit-audit/<int:audit_id>/', auditView.edit_audit, name='edit_audit'),
    path('delete-audit/<int:audit_id>/', auditView.delete_audit, name='delete_audit'),
    
    path('customers/', customerView.list_customers, name='list_customers'),
    path('edit-customer/<int:pk>/', customerView.edit_customer, name='edit_customer'),
    path('delete-customer/<int:pk>/', customerView.delete_customer, name='delete_customer'),
    
    
    path('clusters/', customerView.list_clusters, name='list_clusters'),
    path('edit-cluster/<int:pk>/', customerView.edit_cluster, name='edit_cluster'),
    path('delete-cluster/<int:pk>/', customerView.delete_cluster, name='delete_cluster'),
]


