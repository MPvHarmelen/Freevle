from datetime import datetime, date
from functools import wraps
from freevle import app

from flask import url_for, request, redirect, render_template
from werkzeug.exceptions import NotFound

def permalink(function):
    @wraps(function)
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        return url_for(endpoint, **values)
    return inner

def archived_view(endpoint, template):
    def wrapper(function):
        @wraps(function)
        def inner(year=None, month=None, *args, **kwargs):
            # Redirect get request
            url_kwargs = {}
            year_arg = request.args.get('year', False)
            if year_arg != False:
                url_kwargs['year'] = year_arg
                month_arg = request.args.get('month', False)
                if month_arg != False and year_arg:
                    url_kwargs['month'] = month_arg
                try:
                    for k,v in url_kwargs.items():
                        url_kwargs[k] = int(v) if v is not '' else None
                except ValueError as e:
                    if not app.config['DEBUG']:
                        raise NotFound
                    else:
                        raise NotFound(e)
                else:
                    return redirect(url_for(endpoint, **url_kwargs))
            oldest_date, items_in_year, kwargs = function(
               year,
               month,
               *args,
               **kwargs
            )
            min_year = oldest_date.year\
                       if oldest_date is not None\
                       else date.today().year
            today = date.today()
            this_year = today.year
            years = range(min_year, this_year + 1)

            # Make months list
            month_list = []
            if year:
                items_in_year = items_in_year.all()
                if not len(items_in_year):
                    raise NotFound
                oldest_month = items_in_year[-1].date_published.month
                newest_month = items_in_year[0].date_published.month
                this_day = today.day
                for month_delta in range(newest_month - oldest_month + 1):
                    temp_date = datetime.strptime(
                        '{}-{}-{}'.format(
                            this_year,
                            oldest_month + month_delta,
                            this_day
                        ),
                        '%Y-%m-%d'
                    )
                    month_list.append(
                        (temp_date.strftime('%m').lstrip('0'), temp_date.strftime('%B'))
                    )
            return render_template(template,
                                   years=years,
                                   month_list=month_list,
                                   current_year=year,
                                   current_month=str(month),
                                   **kwargs
            )
        return inner
    return wrapper
