# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup,ICantBelieveItsBeautifulSoup,MinimalSoup
from markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from template_utils.markup import formatter
from typogrify.templatetags.typogrify import typogrify
import re

def typygmentdown(text, **kwargs):
    """
    Given a string of text using Markdown syntax, applies the
    following transformations:
    
    1. Searches out and temporarily removes any raw ``<code>``
       elements in the text.
    2. Applies Markdown and typogrify to the remaining text.
    3. Applies Pygments highlighting to the contents of the removed
       ``<code>`` elements.
    4. Re-inserts the ``<code>`` elements and returns the result.
    
    The Pygments lexer to be used for highlighting is determined by
    the ``class`` attribute of each ``<code>`` element found; if none
    is present, it will attempt to guess the correct lexer before
    falling back on plain text.
    
    The following keyword arguments are understood and passed to
    markdown if found:
    
    * ``extensions``
    
    Markdown's ``safe_mode`` argument is *not* passed on, because it
    would cause the temporary ``<code>`` elements in the text to be
    escaped.
    
    The following keyword arguments are understood and passed to
    Pygments if found:
    
    * ``linenos``
    
    The removal, separate highlighting and re-insertion of the
    ``<code>`` elements is necessary because Markdown and SmartyPants
    do not reliably avoid formatting text inside these elements;
    removing them before applying Markdown and typogrify means they
    are in no danger of having extraneous HTML or fancy punctuation
    inserted by mistake.
    
    Original implementation by user 'blinks' as snippet #119 at
    djangosnippets: http://www.djangosnippets.org/snippets/119/. This
    version makes the following changes:

    * The name of the function is now ``typygmentdown``.
    * The argument signature has changed to work better with the
      ``template_utils`` formatter.
    * The ``extensions`` and ``linenos`` arguments are looked for and
      passed to Markdown and Pygments, respectively.
    * The function is registered with the ``template_utils``
      formatter.
    
    """

    #soup = BeautifulSoup(unicode(text))
    #code_blocks = soup.findAll(u'code')
    #for block in code_blocks:
    #    block.replaceWith(u'<code class="removed"></code>')

    text2 = unicode(text)
    code_blocks = []
    converted = []
    start = 0
    end = len(text2)

    # loop over every tag
    reg = re.compile(u'<code.*?code>', re.X  | re.DOTALL)
    for m in reg.finditer(text2):

        # ignore comments
		#if not re.match(r'^!--(.*)--',tag):
        block = m.group(0)
        start_block = m.start()
        end_block = m.end()

        code_blocks.append(block)
        
        if start < start_block:
            converted.append(text2[start:(start_block-1)])

        converted.append(u'<code class="removed"></code>')
        start = end_block + 1

    if start < end:
	    converted.append(text2[start:end])


    htmlized = typogrify(markdown(u''.join(converted), extensions=kwargs.get('extensions', [])))



    ##typogrify()
    soup = ICantBelieveItsBeautifulSoup(htmlized)
    empty_code_blocks, index = soup.findAll('code', 'removed'), 0
    formatter = HtmlFormatter(cssclass='typygmentdown', linenos=kwargs.get('linenos', False))


    for block in code_blocks:
        
        #import pdb
        #pdb.set_trace()

        m = re.search(u"class=\"(?P<class_name>\w+)\">(?P<block_content>.*)</code>", block, re.DOTALL)
       
        block_content = u''
        if m:
            block_group = m.groupdict()
            block_content =  block_group['block_content']
            language = block_group['class_name']
        else:
            language = 'text'
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
        except ValueError, e:
            try:
                lexer = guess_lexer(block.renderContents())
            except ValueError, e:
                lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')

        #block_soup = MinimalSoup(block)
        empty_code_blocks[index].replaceWith(
                highlight(block_content, lexer, formatter))
        index = index + 1
    # This is ugly, but it's the easiest way to kill extraneous paragraphs Markdown inserts.
    return unicode(soup).replace('<p><div', '<div').replace('</div>\n\n</p>', '</div>\n\n')

formatter.register('typygmentdown', typygmentdown)
