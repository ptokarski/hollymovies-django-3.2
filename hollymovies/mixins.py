from django.views.generic.base import ContextMixin


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
