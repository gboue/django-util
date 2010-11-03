from django.http import HttpResponsePermanentRedirect, HttpResponseGone

def redirect_to(request, url, convert_funcs=None, **kwargs):
    """
    A version of django.views.generic.simple.redirect_to which can handle
    argument conversion. The 'convert_funcs' parameter is a dictionary mapping
    'kwargs' keys to a function. The 'kwargs' value is run through the function
    before the redirect is applied.

    Mostly, this is useful for converting a parameter to an int before passing
    it back to the redirect for formatting via %02d, for example.
    """
    if not url:
        return HttpResponseGone()
    if convert_funcs:
        for name, fn in convert_funcs.items():
            if name in kwargs:
                kwargs[name] = fn(kwargs[name])
    return HttpResponsePermanentRedirect(url % kwargs)

