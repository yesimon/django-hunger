from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from hunger.models import InvitationCode
from hunger.forms import InviteSendForm
from hunger.utils import setting, now
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


class InviteView(FormView):
    """
    Allow a user to send invites.
    """
    template_name = 'hunger/request_invite.html'
    form_class = InviteSendForm
    success_url = reverse_lazy('hunger-verified')

    def form_valid(self, form):
        valid_code = InvitationCode.objects.get(owner=self.request.user,
                                                num_invites__gt=0)
        form.instance.code = valid_code
        form.instance.invited = now()
        form.save()

        return super(InviteView, self).form_valid(form)

    def form_invalid(self, form):
        return super(InviteView, self).form_valid(form)

class NotBetaView(TemplateView):
    """
    Display a message to the user after the invite request is completed
    successfully.
    """
    template_name='hunger/not_in_beta.html'


class VerifiedView(TemplateView):
    """
    Display a message to the user after the invite request is completed
    successfully.
    """
    template_name='hunger/verified.html'


class InvalidView(TemplateView):
    """
    Display a message to the user that the invitation code is
    invalid or has already been used.
    """
    template_name='hunger/invalid.html'


def verify_invite(request, code):
    response = redirect(setting('HUNGER_VERIFIED_REDIRECT'))
    response.set_cookie('hunger_code', code)
    return response
