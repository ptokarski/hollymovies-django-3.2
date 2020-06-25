from django.contrib import messages
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin


class TitleMixin(ContextMixin):

    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        title = self.get_title()
        if title is not None:
            result['title'] = title
        return result


class SuccessMessagedFormMixin(FormMixin):

    success_message = None

    def get_success_message(self):
        return self.success_message

    def form_valid(self, form):
        result = super().form_valid(form)
        success_message = self.get_success_message()
        if success_message is not None:
            messages.success(self.request, success_message)
        return result
