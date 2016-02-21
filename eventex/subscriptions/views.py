from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):

    if request.method == 'POST':
        return create(request)
    else: #if GET method then shows a empty form
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form' : form})

    #send email
    template_name = 'subscriptions/subscription_email.txt'
    context = form.cleaned_data
    subject = 'Confirmação de inscrição'
    from_ = settings.DEFAULT_FROM_EMAIL
    to = form.cleaned_data['email']

    _send_mail(subject, from_, to, template_name, context)

    #Sucess feedback
    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
   return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
        body = render_to_string(template_name=template_name, context=context)
        mail.send_mail(subject, body, from_, [from_, to])