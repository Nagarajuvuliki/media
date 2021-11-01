from rest_framework.pagination import PageNumberPagination
from django.conf import settings



class CustomPagination(PageNumberPagination):
    page_size = settings.PAGE_SIZE
    page_size_query_param = 'size'
    max_page_size = settings.MAX_PAGE_SIZE

    def next_link(self):
        return self.get_next_link()
    
    def previous_link(self):
        return self.get_previous_link()
    
    def total_records(self):
        return self.page.paginator.count

    def current_page_number(self):
        return self.page.number






def paginator_function(self, queryset, **kwargs):
    # print(self.pagination_class)

    _paginator = None
    _final_data = {}
    if self.pagination_class is not None:
        _paginator = self.pagination_class()
        paginated_queryset = _paginator.paginate_queryset(queryset, self.request, view=self)
        if paginated_queryset is not None:
            if 'serializer' in kwargs:
                data = kwargs.get('serializer')(paginated_queryset, many=True).data
            else:
                data = paginated_queryset
            _final_data = {
                'total': _paginator.total_records(),
                'current_page': _paginator.current_page_number(),
                'next': _paginator.next_link(),
                'previous': _paginator.previous_link(),
                'data': data
            }
            return _final_data
        _final_data = {'data': []}
    _final_data = {'data': 'unable to import Pagination Class'}
    return _final_data

