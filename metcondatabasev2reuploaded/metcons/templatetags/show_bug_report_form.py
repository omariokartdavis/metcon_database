from django import template
from metcons.forms import BugReportForm

register = template.Library()

@register.inclusion_tag('bug_report_form.html')
def show_bug_report_form():
    form = BugReportForm()
    return {'form': form}