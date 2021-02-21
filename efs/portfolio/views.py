import decimal

from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import *
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer


now = timezone.now()


def home(request):
    return render(request, 'portfolio/home.html',
                  {'portfolio': home})


def logout(request):
    auth_logout(request)
    return redirect('/home')


#
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # logger.info("123")
                return redirect('/home')

    form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                  {'customers': customer})

@login_required
def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customer})
    else:
        form = CustomerForm()
        # print("Else")
    return render(request, 'portfolio/customer_new.html', {'form': form})



@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
    stock = Stock.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/stock_list.html', {'stocks': stock})


@login_required
def stock_new(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html',
                          {'stocks': stocks})
    else:
        form = StockForm()
        # print("Else")
    return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            # stock.customer = stock.id
            stock.updated_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
    else:
        # print("else")
        form = StockForm(instance=stock)
    return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return redirect('portfolio:stock_list')


@login_required
def investment_list(request):
    investment = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investment})


@login_required
def investment_new(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.acquired_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(acquired_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html',
                          {'investments': investments})
    else:
        form = InvestmentForm()
        # print("Else")
    return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            # stock.customer = stock.id
            investment.updated = timezone.now()
            investment.save()
            investments = Investment.objects.filter(acquired_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
        # print("else")
        form = InvestmentForm(instance=investment)
        return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')

@login_required
def mutual_fund_list(request):
    mutual_fund = MutualFund.objects.filter()
    return render(request, 'portfolio/mutualfund_list.html',
                  {'mutual_funds': mutual_fund})


@login_required
def mutual_fund_edit(request, pk):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    if request.method == "POST":
        # update
        form = MutualFundForm(request.POST, instance=mutual_fund)
        if form.is_valid():
            mutual_fund = form.save(commit=False)
            mutual_fund.save()
            mutual_funds = MutualFund.objects.filter()
            return render(request, 'portfolio/mutualfund_list.html',
                          {'mutual_funds': mutual_funds})
    else:
        # edit
        form = MutualFundForm(instance=mutual_fund)
    return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@login_required
def mutual_fund_delete(request, pk):
    mutual_fund = get_object_or_404(MutualFund, pk=pk)
    mutual_fund.delete()
    return redirect('portfolio:mutualfund_list')


@login_required
def mutual_fund_new(request):
    if request.method == "POST":
        form = MutualFundForm(request.POST)
        if form.is_valid():
            mutual_fund = form.save(commit=False)
            mutual_fund.created_date = timezone.now()
            mutual_fund.save()
            mutual_funds = MutualFund.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/mutualfund_list.html',
                          {'mutual_funds': mutual_funds})
    else:
        form = MutualFundForm()
        # print("Else")
    return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutual_funds = MutualFund.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    # overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    sum_current_mutual_fund_value = 0
    sum_initial_mutual_fund_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

        sum_recent_investments = sum_recent_value.get('recent_value__sum')
        sum_acquired_investments = sum_acquired_value.get('acquired_value__sum')

        portfolio_initial_total = sum_of_initial_stock_value + sum_acquired_investments
        portfolio_current_total = sum_current_stocks_value + sum_recent_investments

    for mutual_fund in mutual_funds:
        sum_current_mutual_fund_value += mutual_fund.current_mutual_fund_value()
        sum_initial_mutual_fund_value += mutual_fund.initial_mutual_fund_value()


    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                        'investments': investments, 'stocks': stocks,
                                                        'sum_acquired_value': sum_acquired_value,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'portfolio_initial_total': portfolio_initial_total,
                                                        'portfolio_current_total': portfolio_current_total,
                                                        'sum_recent_investments': sum_recent_investments,
                                                        'sum_acquired_investments': sum_acquired_investments,
                                                        'sum_current_mutual_fund_value': sum_current_mutual_fund_value,
                                                        'sum_initial_mutual_fund_value': sum_initial_mutual_fund_value,
                                                        'mutual_funds': mutual_funds,
                                                        })

# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):
    def get(self, request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)

