import subprocess
import threading

from django.http import HttpResponse
from django.shortcuts import render, redirect
import time
from multiprocessing import Process, Pool

# Create your views here.
from aml_assess.models import Customer, Sanction, Application, PEP, PotentialMatch


def index(request):
    applications = Application.objects.all()
    application = Application.objects.get(customer_id=1)
    # subprocess.run(verify_sanctions(application.id))

    # pool.map(verify_sanctions,[application.id])
    context = {"applications": applications}
    return render(request, "aml_assess/list-applications.html", context=context)


"""

This function accepts the application id as a parameter and fetches customer information. the customer is matched against the list od
of persons who have sanctions on them. The names are matched on first and last names. This can be expanded to include more parameters.
"""


def verify_sanctions(args):
    app_id = args
    outcome = False
    status = 'No sanction found'
    time.sleep(10)  # Sleep for 10 seconds
    application = Application.objects.get(pk=app_id)
    sanctioned_list = Sanction.objects.all()  # Fetch list of sanctioned persons

    customer = Customer.objects.get(id=application.customer.id)

    for i in sanctioned_list:
        if i.full_name() == customer.full_name():
            outcome = True
            status = 'Please verify match'
            PotentialMatch.objects.create(
                application=application,
                check='sanction',
                id_match=i.id
            )
    application.sanctioned = outcome
    application.status = status
    application.save()


"""

This function accepts the application id as a parameter and fetches customer information. The customer is matched against the list of
of persons who have are politically exposed. The names are matched on first and last names. This can be expanded to include more parameters.
"""


def verify_pep(args):
    outcome = False
    status = 'Not a PEP'
    app_id = args
    time.sleep(10)  # Sleep for 10 seconds

    pep_list = PEP.objects.all()  # Fetch list of pep persons
    application = Application.objects.get(id=app_id)

    for i in pep_list:
        if i.full_name() == application.customer.full_name():
            outcome = True
            status = 'PEP match found'
            PotentialMatch.objects.create(
                application=application,
                check='pep',
                id_match=i.id
            )
    application.pep = outcome
    application.status = status
    application.save()


"""

This function accepts the application id as a parameter and fetches customer information. the customer is profiled to checks
 if they are PEP and if their income is less than 25K
"""


def risk_assessment(args):
    app_id = args
    time.sleep(10)  # Sleep for 10 seconds

    application = Application.objects.get(id=app_id)
    if not application.pep:
        status = 'Approved'
    elif application.pep and application.customer.monthly_income < 25000:  # Check if the customer has is not PEP with income less than 25 K
        status = 'Denied'
    else:
        status = 'Approved'
    application.status = status
    application.save()


"""

This function creates a new customer and posts them to the database. After the customer has been saved, the assessment process begins by submitting 
the customer details to be checked against the sanctioned persons list.
"""


def new_application(request):
    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        monthly_income = request.POST['monthly_income']

        customer = Customer.objects.create(  # create new customer
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            monthly_income=monthly_income
        )
        application = Application.objects.create(  # create a new application
            customer=customer,
            status='Checking Sanctioned List',
        )
        thread = threading.Thread(target=verify_sanctions,
                                  args=[application.id])  # verify if the the customer is sanctioned
        thread.daemon = True
        thread.start()
        return redirect('index')
    else:
        return render(request, "aml_assess/add-application.html")


"""

This function accepts the application takes the id of the customer's application and fetches the customer details and 
details regarding their applications
"""


def view_application(request, pk):
    application = Application.objects.get(pk=pk)
    matches = PotentialMatch.objects.filter(application_id=application.id, match=True)
    potential_matches_list = []
    for i in matches:
        if i.check == 'sanction':
            sanction_match = Sanction.objects.get(pk=i.id_match)
            potential_matches_list.append(sanction_match)
        if i.check == 'pep':
            pep_match = PEP.objects.get(pk=i.id_match)
            potential_matches_list.append(pep_match)
    context = {"application": application, "matches": potential_matches_list}
    return render(request, "aml_assess/view-application.html", context=context)


"""

This function accepts request and application id from the user initiates the process of checking if the customer is on the PEP list
"""


def submit_pep(request, pk):
    application = Application.objects.get(pk=pk)
    application.status = 'Checking PEP List'
    application.save()
    thread = threading.Thread(target=verify_pep,
                              args=[application.id])  # Check if the customer is a PEP
    thread.daemon = True
    thread.start()
    return redirect('index')


"""

This function accepts request and application id from the user, and allows the user to reject an application by the 
customer because their are on the sanctioned list

"""


def deny_application(request, pk):
    application = Application.objects.get(pk=pk)

    application.status = 'Denied'
    application.save()
    return redirect('index')


"""

This function accepts request and application id from the user. 
This function allows the user to reject a potential match found in the Sanctioned people's list
"""


def reject_match(request, pk):
    # Reject match found during the search through the sanctioned list

    application = Application.objects.get(pk=pk)
    application.sanctioned = False
    application.status = 'Checking PEP List'
    application.save()
    match = PotentialMatch.objects.get(application_id=application.id)
    match.match = False
    match.save()
    thread = threading.Thread(target=verify_pep,
                              args=[application.id])  # Check if the customer is a PEP
    thread.daemon = True
    thread.start()
    return redirect('index')


"""

This function accepts request and application id from the user. 
This function allows the user to reject a potential match found in the PEP list
"""


def reject_pep_match(request, pk):
    # Reject match found during the search through the sanctioned list

    application = Application.objects.get(pk=pk)
    application.pep = False
    application.status = 'Performing Risk Assessment'
    application.save()

    match = PotentialMatch.objects.get(application_id=application.id)
    match.match = False
    match.save()

    thread = threading.Thread(target=risk_assessment,
                              args=[application.id])  # Check if the customer presents acceptable to the the business
    thread.daemon = True
    thread.start()
    return redirect('index')

"""

This function accepts request and application id from the user. 
This function allows the user to initiate the risk assessment process for the customer
"""
def submit_risk_assessment(request, pk):
    application = Application.objects.get(pk=pk)
    application.status = 'Performing Risk Assessment'
    application.save()
    thread = threading.Thread(target=risk_assessment,
                              args=[application.id])  # Check if the customer presents acceptable to the the business
    thread.daemon = True
    thread.start()
    return redirect('index')
