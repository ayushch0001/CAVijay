from urllib import request
from django.shortcuts import redirect, render
from reportaudit.forms import auditTypeForm
import json
from django.http import JsonResponse
from reportaudit.models import AuditType


class auditTypeView :
    
    def create_audit_type(request):
        if request.method == 'POST':
            form = auditTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else :
            form = auditTypeForm()
            return render(request, r'templates\\module\\auditType.html', {'form': form})
        