import json
import traceback
import sys
import csv
import os
import pandas as pd

from django.shortcuts import render
from django import forms

# tweet_gather.py, mapper.py must be inside the website folder
from tweet_gather import collect_data
from mapper import map_data

# RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

MODES = [('past', 'Past'), ('live', 'Live')]
UNITS = [('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days')]

# min_int, max_int, min_dur, max_dur
# structured this way for easy readability/modification
PAST_LIMITS = ((1, "minutes"),
               (1, "days"),
               (2, "minutes"),
               (7, "days"))
LIVE_LIMITS = ((1, "minutes"),
               (1, "hours"),
               (2, "minutes"),
               (6, "hours"))

class TimeSelector(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(required=True),
                  forms.ChoiceField(label='Units', choices=UNITS,
                                    required=True))
        super(TimeSelector, self).__init__(
            fields=fields,
            *args, **kwargs)

    def compress(self, data_list):
        # if len(data_list) == 2:
        #     if data_list[0] is None or not data_list[1]:
        #         raise forms.ValidationError(
        #             'Must specify both minutes and building together.')
        #     if data_list[0] < 0:
        #         raise forms.ValidationError(
        #             'Walking time must be a non-negative integer.')
        return data_list


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
    bins = TimeSelector(
        label='Time Interval',
        help_text='Length of each time block interval',
        widget=forms.widgets.MultiWidget(
            widgets=(forms.widgets.NumberInput,
                     forms.widgets.Select(choices=UNITS))))
    duration = TimeSelector(
        label='Duration',
        help_text='How far back/forward in time should we track tweets?',
        widget=forms.widgets.MultiWidget(
            widgets=(forms.widgets.NumberInput,
                     forms.widgets.Select(choices=UNITS))))


def convert_time(number, units):
    '''
    Converts time inputs to an interger number of minutes.
    Inputs:
        number(int): a user-inputted integer
        units(str): hours, minutes, or days

    Output: (int) number of minutes
    '''
    multiplier = 1
    if units == 'hours':
        multiplier *= 60
    if units == 'days':
        multiplier *= 60 * 24

    return number * multiplier


def validate_inputs(mode, interval, duration):
    '''
    Checks to see if the inputs are within the given lower and upper bounds
    for the query type.
    Inputs:
        mode (str): "past" (search historical tweets) or "live" (stream tweets)
        interval (int): size of time bins (minutes)
        duration (int): total length of time to collect data from (minutes)
    Outputs:
        errors: list of error messages (or empty list if no errors)
    '''
    # load parameter limits in minutes form
    limits = []
    if mode == "past":
        parameters = PAST_LIMITS
    if mode == "live":
        parameters = LIVE_LIMITS
    for parameter in parameters:
        num, unit = parameter
        mins = convert_time(num, unit)
        limits.append(mins)

    # check for errors and append messages
    errors = []
    if interval < limits[0]:
        time, units = parameters[0]
        msg = "Interval size must be at least {} {}".format(time, units)
        errors.append(msg)
    if interval > limits[1]:
        time, units = parameters[1]
        msg = "Interval size must be less than {} {}".format(time, units)
        errors.append(msg)
    if duration < limits[2]:
        time, units = parameters[2]
        msg = "Total duration must be at least {} {}".format(time, units)
        errors.append(msg)
    if duration > limits[3]:
        time, units = parameters[3]
        msg = "Total duration must be less than {} {}".format(time, units)
        errors.append(msg)

    return errors


def home(request):
    '''
    This is the master function is called by the page itself. It takes the
    inputs given by the user into the form, processes them, and calls the
    necessary functions.
    '''
    context = {}
    data = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data into inputs
            search_term = form.cleaned_data['query']
            mode = form.cleaned_data['mode']
            bin_num, bin_unit = form.cleaned_data['bins']
            dur_num, dur_unit = form.cleaned_data['duration']
            interval = convert_time(bin_num, bin_unit)
            duration = convert_time(dur_num, dur_unit)

            # check limit validity
            errors = validate_inputs(mode, interval, duration)
            if len(errors) == 0:
                try:
                    data = collect_data(search_term, mode, interval, duration)
                    print("got data")
                except Exception as e:
                    print('Exception caught')
                    bt = traceback.format_exception(*sys.exc_info()[:3])
                    context['err'] = """
                    An exception was thrown in find_courses:
                    <pre>{}{}</pre>""".format(e, '\n'.join(bt))
                    data = None
                    print("exception thrown")
            else:
                print("Input error:")
                for error in errors:
                    print(error)
                context['err'] = errors
                data = None
    else:
        form = SearchForm()
        print("idk")

    # handle different responses of data
    if data is None:
        context['map'] = None
        context['array'] = None
        print('no data')
    else:
        # call mapper, returns image filenames
        colnames = []
        for index, dic in enumerate(data):
            colnames.append(str(index))
        filename = search_term
        context['map'] = map_data(data, colnames, filename, show_plot=False)
        # print(context['map'])

        # format as a dataframe
        data_array = pd.DataFrame(data)
        # data_array = data_array.transpose()
        # name the bins
        data_array = data_array.to_html()
        context['array'] = data_array
        # print(context['array'])

    context['form'] = form
    return render(request, 'index.html', context)
