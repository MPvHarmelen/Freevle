from . import bp

@bp.route('/<object_slug>')
def timetable_view(object_slug):
    """Show timetable with any potential homework in it, starting with today."""

@bp.route('/<object_slug>/print')
def timetable_print(object_slug):
    """
    Show timetable without homework, starting on this week's first day.

    ORGANIZER_WEEK_STARTS_ON and ORGANIZER_WEEK_ENDS_ON are defined in
    the root config of your Flask app.

    """

@bp.route('/edit-homework/')
@bp.route('/edit-homework/<course_slug>')
def planner_edit(course_slug=None):
    """
    Create, edit or delete homework.

    Empty homework is generated according to the timetable.

    """

from . import models
tables = [x for x in dir(models) if type(x) == type(models.db.Model)]

@bp.route('/admin/')
def organizer_admin():
    """Shows an overview of editable tables."""

for model in tables:
    name = model.__tablename__
#    @bp.route('/' + name + '/')
     # TODO: Think of something to not write sixteen identical views.
