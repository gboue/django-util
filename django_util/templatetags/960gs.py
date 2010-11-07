# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def extra_css_class(forloop):
	
	res = ""
	if forloop['first']:
		res = "alpha"
		
	elif forloop['last']:
		res = "omega"

	return res



#import re
#from django.template import Library, Node
#from django.db.models import get_model
#
#class gs960Node(template.Node):
#
#    def __init__(self, format_string, var_name):
#        self.format_string = format_string
#        self.var_name = var_name
#
#    def render(self, context):
#        context[self.var_name] = datetime.datetime.now().strftime(self.format_string)
#        return ''
#
#@register.tag(name="960gs_extra_class")
#def compute_960gs_extra_class(parser, token):
#    # This version uses a regular expression to parse tag contents.
#    try:
#        # Splitting by None == splitting by spaces.
#        tag_name, arg = token.contents.split(None, 1)
#    except ValueError:
#        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
#    m = re.search(r'(.*?) as (\w+)', arg)
#    if not m:
#        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
#    token_params , var_name = m.groups()
#    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
#        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
#    return gs960Node(format_string[1:-1], var_name)
#
#	
#
#class LatestContentNode(Node):
#	
#    def __init__(self, model, num, varname):
#        self.num, self.varname = num, varname
#        self.model = get_model(*model.split('.'))
#
#    def render(self, context):
#        context[self.varname] = self.model._default_manager.all()[:self.num]
#        return ''
#
#def get_latest(parser, token):
#    bits = token.contents.split()
#    if len(bits) != 5:
#        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
#    if bits[3] != 'as':
#        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
#    return LatestContentNode(bits[1], bits[2], bits[4])
#
#get_latest = register.tag(get_latest)
#
#
#class FormatTimeNode(template.Node):
#    def __init__(self, date_to_be_formatted, format_string):
#        self.date_to_be_formatted = template.Variable(date_to_be_formatted)
#        self.format_string = format_string
#
#    def render(self, context):
#        try:
#            actual_date = self.date_to_be_formatted.resolve(context)
#            return actual_date.strftime(self.format_string)
#        except template.VariableDoesNotExist:
#            return ''
#
###