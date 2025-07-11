from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from reportaudit.forms import ClusterForm, customerForm
import json
from django.http import JsonResponse
from reportaudit.models import Cluster, Customer
from django.contrib.auth.decorators import login_required

class customerView :
    
    def createCustomer(request):
        if request.method == 'POST':
            form = customerForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('home')
        else :
            form = customerForm()
            return render(request, r'templates\\module\\customer.html', {'form': form})
        
        
        
    def get_customers_by_cluster(request):
        cluster_id = request.GET.get('cluster_id')
        customers = Customer.objects.filter(cluster_id=cluster_id).values('id', 'nameOfOrganization')
        return JsonResponse({'customers': list(customers)})
    
    
    def list_customers(request):
        customers = Customer.objects.select_related('cluster').all()
        return render(request, r'templates\\module\\list_customers.html', {'customers': customers})
    
    @login_required
    def edit_customer(request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        if request.method == 'POST':
            form = customerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('list_customers')  # replace with your actual list page name
        else:
            form = customerForm(instance=customer)
        return render(request, r'templates\\module\\customer.html', {'form': form})
    @login_required
    def delete_customer(request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return redirect('list_customers')  # replace with your actual list page name
       
    def list_clusters(request):
        clusters = Cluster.objects.all()
        return render(request, r'templates\\module\\list_clusters.html', {'clusters': clusters})



    def createCluster(request):
        if request.method == 'POST':
            form = ClusterForm(request.POST)
            
            if form.is_valid():
                    form.save()
            return render(request,r"templates\\audit\\cluster.html",{'form':form})
        else :
            form = ClusterForm(request.POST)
            return render(request,r"templates\\audit\\cluster.html",{'form':form})


    # Edit View
    @login_required
    def edit_cluster(request, pk):
        cluster = get_object_or_404(Cluster, pk=pk)
        if request.method == 'POST':
            form = ClusterForm(request.POST, instance=cluster)
            if form.is_valid():
                form.save()
                return redirect('list_clusters')
        else:
            form = ClusterForm(instance=cluster)
        return render(request,r"templates\\audit\\cluster.html",{'form':form})

    # Delete View
    @login_required
    def delete_cluster(request, pk):
        cluster = get_object_or_404(Cluster, pk=pk)
        cluster.delete()
        return redirect('list_clusters')
        