import django_filters
from django.db import models

from app.models import VideoDetailModel


class CategoryFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(CategoryFilter, self).__init__(*args, **kwargs)
        self.form.fields['categories'].widget.attrs['onchange'] = 'submit();'
        self.form.fields['categories'].widget.attrs['class'] = 'js-select2'
        self.form.fields['categories'].empty_label = "All Category"
        self.form.fields['title'].widget.attrs['class'] = 'au-input au-input--xl'
        self.form.fields['title'].widget.attrs['placeholder'] = 'Search for videos'
        self.form.fields['title'].widget.attrs['name'] = 'search'

    class Meta:
        model = VideoDetailModel
        fields = ['categories', 'title']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                }
            }
        }
