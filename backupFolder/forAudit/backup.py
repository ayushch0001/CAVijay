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

    #     # return render(request, 'templates/audit/report.html')