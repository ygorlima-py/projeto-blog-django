from urllib.parse import urlencode


def build_canonical_url(request, path, page_obj=None):
    """Use the route URL, retaining only the current pagination page."""
    if page_obj is not None and page_obj.number > 1:
        path = f'{path}?{urlencode({"page": page_obj.number})}'

    return request.build_absolute_uri(path)
