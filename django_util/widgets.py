# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words

from django.db.models import get_model
from django.utils import simplejson
from tagging.models import Tag

from string import Template

from django.template.loader import render_to_string

class SharpTemplate(Template):
	delimiter = "FF#"

class ForeignKeySearchInput(forms.HiddenInput):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input 
    instead in a <select> box.
    """
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
            'js/jquery/jquery.bgiframe.min.js',
            'js/jquery/jquery.ajaxQueue.js',
            'js/jquery/jquery.autocomplete.js'
        )

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        return truncate_words(obj, 14)

    def __init__(self, rel, search_fields, attrs=None):
        self.rel = rel
        self.search_fields = search_fields
        super(ForeignKeySearchInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(ForeignKeySearchInput, self).render(name, value, attrs)
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        return rendered + mark_safe(u'''
            <style type="text/css" media="screen">
                #lookup_%(name)s {
                    padding-right:16px;
                    background: url(
                        %(admin_media_prefix)simg/admin/selector-search.gif
                    ) no-repeat right;
                }
                #del_%(name)s {
                    display: none;
                }
            </style>
<input type="text" id="lookup_%(name)s" value="%(label)s" />
<a href="#" id="del_%(name)s">
<img src="%(admin_media_prefix)simg/admin/icon_deletelink.gif" />
</a>
<script type="text/javascript">
            if ($('#lookup_%(name)s').val()) {
                $('#del_%(name)s').show()
            }
            $('#lookup_%(name)s').autocomplete('../search/', {
                extraParams: {
                    search_fields: '%(search_fields)s',
                    app_label: '%(app_label)s',
                    model_name: '%(model_name)s',
                },
            }).result(function(event, data, formatted) {
                if (data) {
                    $('#id_%(name)s').val(data[1]);
                    $('#del_%(name)s').show();
                }
            });
            $('#del_%(name)s').click(function(ele, event) {
                $('#id_%(name)s').val('');
                $('#del_%(name)s').hide();
                $('#lookup_%(name)s').val('');
            });
            </script>
        ''') % {
            'search_fields': ','.join(self.search_fields),
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'model_name': self.rel.to._meta.module_name,
            'app_label': self.rel.to._meta.app_label,
            'label': label,
            'name': name,
        }



class AjaxCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input 
    instead in a <select> box.
    """
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
            'js/jquery/jquery.bgiframe.min.js',
            'js/jquery/jquery.ajaxQueue.js',
            'js/jquery/jquery.autocomplete.js',
			'js/jquery/jquery.form.js'
        )

#    def label_for_value(self, value):
#        key = self.rel.get_related_field().name
#        obj = self.rel.to._default_manager.get(**{key: value})
#        return truncate_words(obj, 14)

#   def __init__(self, rel, search_fields, attrs=None):
#        self.rel = rel
#        self.search_fields = search_fields
#        super(ForeignKeySearchInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(AjaxCheckboxSelectMultiple, self).render(name, value, attrs)
#        if value:
#            label = self.label_for_value(value)
#        else:
#            label = u''
        extra = mark_safe(u'''
			<script type="text/javascript">
            	$(document).ready(function() {
				   $('#id_prog_type').change(function(){
						
						$.post("../get_form_part/", $('#proginstance_form').formSerialize() ,
						  function(data){
						    $('#ul_prog_schedule').html(data);
						  });
					}
					);
				 });
				
            </script>
        '''	% {
		            'name': u'nono',
		        }
		)	
				
        #print extra		
        #print rendered
        #return rendered
        return mark_safe("<div id='ul_prog_schedule'>") + rendered + mark_safe("</div>")+ extra



class TabularCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    class Media:
        css = {
            'all': ('',)
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
        )


    def render(self, name, value, attrs=None):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        import pdb

        #str_values = set([force_unicode(v) for v in value])
        #output = super(TabularCheckboxSelectMultiple, self).render(name, value, attrs)

        keys = [  tuple(label.split('|')) for id, label in self.choices ]
        ids = [  id for id, label in self.choices ]        
        temp = zip(keys,ids)
       # pdb.set_trace()
        tabular_choices = dict(temp)
        #pdb.set_trace()
        output = ""
        #return output + render_to_string("widget/tabular_checkbox_select_multiple.html", { 'name': 'John', 'columns':['M','J','V','S','D','L','M' ], 'rows' : ['15:00','15:15','20:30','20:45'],'values':[('15:00','M')]})
        return output + render_to_string("widget/tabular_checkbox_select_multiple.html", { 'name': name, 'columns':self.attrs['columns'], 'rows' : self.attrs['rows'],'choices':tabular_choices, 'values':value})



class AjaxTabularCheckboxSelectMultiple(TabularCheckboxSelectMultiple):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input 
    instead in a <select> box.
    """
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
            'js/jquery/jquery.bgiframe.min.js',
            'js/jquery/jquery.ajaxQueue.js',
            'js/jquery/jquery.autocomplete.js',
			'js/jquery/jquery.form.js'
        )


    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(AjaxTabularCheckboxSelectMultiple, self).render(name, value, attrs)
#        if value:
#            label = self.label_for_value(value)
#        else:
#            label = u''
        extra = mark_safe(u'''
			<script type="text/javascript">
            	$(document).ready(function() {
				   $('#id_prog_type').change(function(){

						$.post("../get_form_part/", $('#proginstance_form').formSerialize() ,
						  function(data){
						    $('#ul_prog_schedule').html(data);
						  });
					}
					);
				 });

            </script>
        '''	% {
		            'name': u'nono',
		        }
		)	

        #print extra		
        #print rendered
        #return rendered
        return mark_safe("<div id='ul_prog_schedule'>") + mark_safe(rendered) + mark_safe("</div>")+ extra



class AutoCompleteTagInput(forms.TextInput):
	

    class Media:
        css = {
            'all': ('jquery.autocomplete.css',)
        }
        js = (
            'lib/jquery.js',
            'lib/jquery.bgiframe.min.js',
            'lib/jquery.ajaxQueue.js',
            'jquery.autocomplete.js'
        )

    def __init__(self, Model, attrs=None):
        self.model = Model
        super(AutoCompleteTagInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(self.model)
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, tag_list))


class AjaxSearchInput(forms.TextInput):
    class Media:
        css = {
            'all': ()
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
            'js/jquery/jquery.bgiframe.min.js',
            'js/jquery/jquery.ajaxQueue.js',
            'js/jquery/jquery.autocomplete.js',
			'js/jquery/jquery.form.js'
        )

    def render(self, name, value, attrs=None):
        output = super(AjaxSearchInput, self).render(name, value, attrs)
        
        return output + mark_safe(u'''
			<input type='button' name='search_movie' id='search_movie' value='search'/>
			<script type="text/javascript">

				//alert('bob');
            	$(document).ready(function() {
					$('#search_movie').click(function(){

						$.post("../get_form_part/", $('#movie_form').formSerialize() ,
						  function(data){
						    $('.movies_id').html(data);
						  });
					}
					);
				  	
				 });
            </script>''' )




class CalendarWeekInput(forms.TextInput):
    class Media:
        css = {
            'all': ('css/smoothness/jquery-ui-1.8.5.custom.css',)
        }
        js = (
            'js/jquery/jquery-1.3.2.js',
            'js/jquery/jquery.ui.core.js',
            'js/jquery/jquery.ui.widget.js',
            'js/jquery/jquery.ui.datepicker.js',
        )

    def render(self, name, value, attrs=None):
        output = super(CalendarWeekInput, self).render(name, value, attrs)

        t = SharpTemplate(u'''
			<input type="text" id="FF#{attr_id}_datepicker" >
		
			<script>
			$(document).ready(function() {
				$( "#FF#{attr_id}_datepicker" ).datepicker({
					showWeek: true,
					firstDay: 3,
					showOn:'button',
					//buttonImage: ".//images/calendar.gif",
					//buttonImageOnly: true,
					onSelect: function(dateText, inst) {  



						var date = $.datepicker.parseDate(
								inst.settings.dateFormat ||
								$.datepicker._defaults.dateFormat,
								dateText, inst.settings );

						var day = $.datepicker.formatDate('D',date,inst.settings);
						var year = $.datepicker.formatDate('yy',date,inst.settings);

						var week_no = parseInt($.datepicker.iso8601Week( date ));
						if (day === 'Mon' || day === 'Tue')
						{
							week_no--;
							if (week_no == 0) 
							{

								week_no = 53;
							}
						}

						// $('#year').val(year) ;  
						$('#FF#{attr_id}').val(week_no) ;  
					} ,
				});
			});
			</script>''' )
			
        d = dict(attr_id=attrs['id'])	
        return output + mark_safe(t.safe_substitute(d))