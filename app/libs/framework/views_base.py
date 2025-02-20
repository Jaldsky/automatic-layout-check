from typing import NoReturn

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class ViewBase(View):
    METHOD_NOT_ALLOWED_ERROR: str = 'Method Not Allowed'
    PROHIBITED_METHODS: tuple = ()

    def __getattr__(self, method_name: str) -> JsonResponse | NoReturn:
        if method_name in self.PROHIBITED_METHODS:
            return lambda request: JsonResponse({'error': self.METHOD_NOT_ALLOWED_ERROR}, status=405)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{method_name}'")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
