import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

from django.http import HttpResponse

# from tweet_gather import go

# RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

# def _valid_result(res):
#     """Validate results returned by find_courses."""
#     (HEADER, RESULTS) = [0, 1]
#     ok = (isinstance(res, (tuple, list)) and
#           len(res) == 2 and
#           isinstance(res[HEADER], (tuple, list)) and
#           isinstance(res[RESULTS], (tuple, list)))
#     if not ok:
#         return False

#     n = len(res[HEADER])

#     def _valid_row(row):
#         return isinstance(row, (tuple, list)) and len(row) == n
#     return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)


# def _valid_military_time(time):
#     return (0 <= time < 2400) and (time % 100 < 60)


# def _load_column(filename, col=0):
#     """Load single column from csv file."""
#     with open(filename) as f:
#         col = list(zip(*csv.reader(f)))[0]
#         return list(col)


# def _load_res_column(filename, col=0):
#     """Load column from resource directory."""
#     return _load_column(os.path.join(RES_DIR, filename), col=col)


# def _build_dropdown(options):
#     """Convert a list to (value, caption) tuples."""
#     return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]


# BUILDINGS = _build_dropdown([None] + _load_res_column('building_list.csv'))
# DAYS = _build_dropdown(_load_res_column('day_list.csv'))
# DEPTS = _build_dropdown([None] + _load_res_column('dept_list.csv'))


# class IntegerRange(forms.MultiValueField):
#     def __init__(self, *args, **kwargs):
#         fields = (forms.IntegerField(),
#                   forms.IntegerField())
#         super(IntegerRange, self).__init__(fields=fields,
#                                            *args, **kwargs)

#     def compress(self, data_list):
#         if data_list and (data_list[0] is None or data_list[1] is None):
#             raise forms.ValidationError('Must specify both lower and upper '
#                                         'bound, or leave both blank.')

#         return data_list


# class EnrollmentRange(IntegerRange):
#     def compress(self, data_list):
#         super(EnrollmentRange, self).compress(data_list)
#         for v in data_list:
#             if not 1 <= v <= 1000:
#                 raise forms.ValidationError(
#                     'Enrollment bounds must be in the range 1 to 1000.')
#         if data_list and (data_list[1] < data_list[0]):
#             raise forms.ValidationError(
#                 'Lower bound must not exceed upper bound.')
#         return data_list


# class TimeRange(IntegerRange):
#     def compress(self, data_list):
#         super(TimeRange, self).compress(data_list)
#         for v in data_list:
#             if not _valid_military_time(v):
#                 raise forms.ValidationError(
#                     'The value {:04} is not a valid military time.'.format(v))
#         if data_list and (data_list[1] < data_list[0]):
#             raise forms.ValidationError(
#                 'Lower bound must not exceed upper bound.')
#         return data_list


# RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
#                                                   forms.widgets.NumberInput))


# class BuildingWalkingTime(forms.MultiValueField):
#     def __init__(self, *args, **kwargs):
#         fields = (forms.IntegerField(),
#                   forms.ChoiceField(label='Building', choices=BUILDINGS,
#                                     required=False),)
#         super(BuildingWalkingTime, self).__init__(
#             fields=fields,
#             *args, **kwargs)

#     def compress(self, data_list):
#         if len(data_list) == 2:
#             if data_list[0] is None or not data_list[1]:
#                 raise forms.ValidationError(
#                     'Must specify both minutes and building together.')
#             if data_list[0] < 0:
#                 raise forms.ValidationError(
#                     'Walking time must be a non-negative integer.')
#         return data_list

class BinSize(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(required=True),
                  forms.ChoiceField(label='Units', choices=UNITS,
                                    required=True))
        super(BinSize, self).__init__(
            fields=fields,
            *args, **kwargs)

MODES = [('Past', 'Past'), ('Live', 'Live')]
UNITS = [('Minutes', 'Minutes'), ('Hours', 'Hours'), ('Days', 'Days')]

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search terms',
        max_length=500,
        help_text='e.g. #DemDebate',
        required=True)
    mode = forms.ChoiceField(
        label='Mode',
        choices=MODES,
        help_text='Past: Tweets in past 7 days. Live: Tweets from now',
        required=True)
    bins = BinSize(
        label='Time Block Size',
        help_text='Length of each time block (Min: 1 min, Max: 1 day)',
        widget=forms.widgets.MultiWidget(
            widgets=(forms.widgets.NumberInput,
                     forms.widgets.Select(choices=UNITS))))
    # timespan = 

    # Set error msg -> 0 days, 7 days
    # Deal with incompatible times



    # enrollment = EnrollmentRange(
    #     label='Enrollment (lower/upper)',
    #     help_text='e.g. 1 and 40',
    #     widget=RANGE_WIDGET,
    #     required=False)
    # time = TimeRange(
    #     label='Time (start/end)',
    #     help_text='e.g. 1000 and 1430 (meaning 10am-2:30pm)',
    #     widget=RANGE_WIDGET,
    #     required=False)
    # time_and_building = BuildingWalkingTime(
    #     label='Walking time:',
    #     help_text='e.g. 10 and RY (at most a 10-min walk from Ryerson)',
    #     required=False,
    #     widget=forms.widgets.MultiWidget(
    #         widgets=(forms.widgets.NumberInput,
    #                  forms.widgets.Select(choices=BUILDINGS))))
    # dept = forms.ChoiceField(label='Department', choices=DEPTS, required=False)
    # days = forms.MultipleChoiceField(label='Days',
    #                                  choices=DAYS,
    #                                  widget=forms.CheckboxSelectMultiple,
    #                                  required=False)
    # show_args = forms.BooleanField(label='Show args_to_ui',
    #                                required=False)


def home(request):
    context = {}
    display_text_box = 'Welcome to Mapping Twitter Trends. This website will...testing this.'
    print(HttpResponse(display_text_box))
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        # if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            # args = {}
            # args['query'] = form.cleaned_data['query']
            # args['mode'] - form.cleaned_data['mode']
            # if form.cleaned_data['query']:
            #     args['terms'] = form.cleaned_data['query']
            # enroll = form.cleaned_data['enrollment']
            # if enroll:
            #     args['enroll_lower'] = enroll[0]
            #     args['enroll_upper'] = enroll[1]
            # time = form.cleaned_data['time']
            # if time:
            #     args['time_start'] = time[0]
            #     args['time_end'] = time[1]

            # days = form.cleaned_data['days']
            # if days:
            #     args['day'] = days
            # dept = form.cleaned_data['dept']
            # if dept:
            #     args['dept'] = dept

            # time_and_building = form.cleaned_data['time_and_building']
            # if time_and_building:
            #     args['walking_time'] = time_and_building[0]
            #     args['building'] = time_and_building[1]

            # if form.cleaned_data['show_args']:
            #     context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

#             try:
#                 res = go(args)
#             except Exception as e:
#                 print('Exception caught')
#                 bt = traceback.format_exception(*sys.exc_info()[:3])
#                 context['err'] = """
#                 An exception was thrown in find_courses:
#                 <pre>{}
# {}</pre>
#                 """.format(e, '\n'.join(bt))

#                 res = None
    else:
        form = SearchForm()

#     # Handle different responses of res
#     if res is None:
#         context['result'] = None
#     elif isinstance(res, str):
#         context['result'] = None
#         context['err'] = res
#         result = None
#     elif not _valid_result(res):
#         context['result'] = None
#         context['err'] = ('Return of find_courses has the wrong data type. '
#                           'Should be a tuple of length 4 with one string and '
#                           'three lists.')
#     else:
#         columns, result = res

#         # Wrap in tuple if result is not already
#         if result and isinstance(result[0], str):
#             result = [(r,) for r in result]

#         context['result'] = result
#         context['num_results'] = len(result)
#         context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'index.html', context)
