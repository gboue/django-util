
from django.template import Library
from django.template import Node, NodeList, Template, Context, Variable,VariableDoesNotExist

register = Library()

def tuple_inlist(x,y,thelist):
    """
    Indicate whether the tuple (x,y) is in the list
    """
    
    return (x,y) in thelist

#def dict_value(key,thedict):
#    """
#    Indicate whether the tuple (x,y) is in the list
#    """#
#
#    return thedict[key]
#
#register.tag(dict_value)

def do_upper(parser, token):
    nodelist = parser.parse(('endupper',))
    parser.delete_first_token()
    return UpperNode(nodelist)

class UpperNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()


class TupleInListNode(Node):
    child_nodelists = ('nodelist_true',)

    def __init__(self, thelist, x, y, nodelist_true):
        self.nodelist_true = nodelist_true
        self.x = Variable(x)
        self.y = Variable(y)
        self.t = Variable(thelist)

    def __repr__(self):
        return "<TupleInList node>"

    def render(self, context):
        import pdb
        
        try:
            actual_x = self.x.resolve(context)
            actual_y = self.y.resolve(context)
            self.thelist = self.t.resolve(context)
            self.key = (actual_x,actual_y)
        except VariableDoesNotExist:
            self.key = None

        #pdb.set_trace()
        context.push()
        
        #context['tuple_value'] = "kiki"
        if self.key and self.key in self.thelist:
            try:
                context.update({'tuple_value':self.thelist[self.key]})
            except:
	            pass
            result = self.nodelist_true.render(context)
        else:
            result = ""
        context.pop()
        return result

#@register.tag(name="if")
def do_iftupleinlist(parser, token):
    """
    
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, thelist, x, y = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]

    nodelist_true = parser.parse(('endiftupleinlist'))
    token = parser.next_token()    
    return TupleInListNode(thelist,x,y, nodelist_true)
do_if = register.tag("iftupleinlist", do_iftupleinlist)