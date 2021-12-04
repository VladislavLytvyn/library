from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderFiltersForm, FormFromModelOrder
from author.models import Author
from authentication.models import CustomUser
from book.models import Book
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
import datetime
from django.urls import reverse_lazy


get_all_orders = Order.get_all()


def get_all(request):
    context = {}
    context['form'] = OrderFiltersForm()
    if request.method == 'GET':
        context['orders'] = get_all_orders
    elif request.method == 'POST':
        form = OrderFiltersForm(request.POST)
        search_param = int(form['search_param'].value()) if form['search_param'].value() else None
        get_select_value = form['filter_methods'].value()
        if get_select_value == "not return in time":
            context['orders'] = unpunctual_users()
        elif get_select_value == "show specific user books":
            context['orders'] = show_orders_of_specific_user(search_param)
        elif get_select_value == "all sort be create date":
            context['orders'] = Order.objects.all().order_by('created_at')
        elif get_select_value == "all sort by planed date":
            context['orders'] = Order.objects.all().order_by('plated_end_at')
        else:
            context['orders'] = get_all_orders
    return render(request, 'order/order.html', context)


def show_orders_of_specific_user(get_input_value):
    result = []
    for elem in Order.get_all():
        if elem.user.id == get_input_value:
            result.append(elem)
    return result


def unpunctual_users():
    now = datetime.datetime.now().timestamp()
    result = []
    for elem in Order.get_all():
        if elem.end_at:
            if elem.end_at.timestamp() > elem.plated_end_at.timestamp():
                result.append(elem)
        else:
            if elem.plated_end_at.timestamp() < now:
                result.append(elem)
    return result


class OrderFormView(FormView):
    form_class = FormFromModelOrder
    template_name = "order/order_form.html"
    success_url = reverse_lazy("order_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def view_order(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'GET':
        form_order = FormFromModelOrder(instance=order)
        return render(request, 'order/change_order.html', {'order': order, 'form_order': form_order})
    else:
        try:
            form_order = FormFromModelOrder(request.POST, instance=order)
            form_order.save()
            return redirect('order')
        except ValueError:
            return render(request, 'order/change_order.html', {'order': order,
                                                               'form_order': form_order,
                                                               'error': 'Bad information'})


def delete_order(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order')
