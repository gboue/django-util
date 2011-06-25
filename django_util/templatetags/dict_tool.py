# -*- coding: utf-8 -*-
from django import template
from django.template import Library
from django.template import Node, NodeList, Template, Context, Variable,VariableDoesNotExist
from django.utils import safestring 
register = template.Library()
from datetime import *


register = Library()


@register.inclusion_tag('kino/value.html',takes_context=True)
def dict_value(context, schedule_dates):

	actual_movie = context["movie"]
	first_schedule = schedule_dates[actual_movie.id][0]


	return  {
	        'value': first_schedule.prog_instance.is_3D ,
			'info': "3D",
	    }