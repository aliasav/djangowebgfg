from django.utils.safestring import mark_safe
from django.template import Library
import jsonpickle
import json
from django.core.serializers.json import DjangoJSONEncoder


register = Library()

@register.filter(is_safe=True)
def js(obj):
    '''template tag to convert a python object to
    a json parsable object to be used in static js
    files
    '''
    obj = json.dumps(obj, cls=DjangoJSONEncoder)
    return jsonpickle.encode(obj)
