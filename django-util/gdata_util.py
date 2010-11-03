# -*- coding: utf-8 -*-
#!/usr/bin/python


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time


class CalendarFactory:


  def __init__(self, email, password, calendar_id='nd7sddqgjn8g2i5grl6nf50hlg@group.calendar.google.com'):
    """Creates a CalendarService and provides ClientLogin auth details to it.
    The email and password are required arguments for ClientLogin.  The 
    CalendarService automatically sets the service to be 'cl', as is 
    appropriate for calendar.  The 'source' defined below is an arbitrary 
    string, but should be used to reference your name or the name of your
    organization, the app name and version, with '-' between each of the three
    values.  The account_type is specified to authenticate either 
    Google Accounts or Google Apps accounts.  See gdata.service or 
    http://code.google.com/apis/accounts/AuthForInstalledApps.html for more
    info on ClientLogin.  NOTE: ClientLogin should only be used for installed 
    applications and not for multi-user web applications."""

    self.cal_client = gdata.calendar.service.CalendarService()
    self.cal_client.email = email
    self.cal_client.password = password
    self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
    self.calendar_id = calendar_id
    self.cal_client.ProgrammaticLogin()


  def _DateRangeQuery(self, start_date='2009-06-12', end_date='2009-06-15'):
    """Retrieves events from the server which occur during the specified date
    range.  This uses the CalendarEventQuery class to generate the URL which is
    used to retrieve the feed.  For more information on valid query parameters,
    see: http://code.google.com/apis/calendar/reference.html#Parameters"""

    print 'Date range query for events on Primary Calendar: %s to %s' % (
        start_date, end_date,)
    query = gdata.calendar.service.CalendarEventQuery('nd7sddqgjn8g2i5grl6nf50hlg@group.calendar.google.com', 'private', 
        'full')
    query.start_min = start_date
    query.start_max = end_date 
    query.extq='[movie_id:133268]'

    query.feed = query.feed + "?extq=[movie_id:133268]"

    #query.setParam()
    print query.__dict__
	#  [name:value][name:value]

    request_feed = gdata.calendar.CalendarEventFeed()
    feed = self.cal_client.CalendarQuery(query)
    for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      for a_when in an_event.when:
        print '\t\tStart time: %s' % (a_when.start_time,)
        print '\t\tEnd time:   %s' % (a_when.end_time,)
        print '\t\tId      :   %s' % (an_event.id,)
      deleteEntry = an_event
      deleteEntry.batch_id = gdata.BatchId(text=an_event.id.text)
      request_feed.AddDelete(entry=deleteEntry)
      #self._DeleteEvent(an_event)

    # submit the batch request to the server
    response_feed = self.cal_client.ExecuteBatch(request_feed, 
      'https://www.google.com/calendar/feeds/%s/private/full/batch' % 'nd7sddqgjn8g2i5grl6nf50hlg@group.calendar.google.com' )

	

    # iterate the response feed to get the operation status
    for entry in response_feed.entry:
      print 'batch id: %s' % (entry.batch_id.text,)
      print 'status: %s' % (entry.batch_status.code,)
      print 'reason: %s' % (entry.batch_status.reason,)


  def execute_query(self,query):
      return self.cal_client.CalendarQuery(query)

  def execute_batch(self,request_feed,url_calendar):
      return self.cal_client.ExecuteBatch(request_feed, url_calendar )

  def create_event_entry(self, title='Tennis with Beth', 
	      content='Meet for a quick lesson', where='On the courts',
	      start_time=None, end_time=None, recurrence_data=None, calendar_id='default', extras = []):
	
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gdata.calendar.Where(value_string=where))

    if recurrence_data is not None:
      # Set a recurring event
      event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
    else:
      if start_time is None:
        # Use current time for the start_time and have the event last 1 hour
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
            time.gmtime(time.time() + 3600))
      event.when.append(gdata.calendar.When(start_time=start_time, 
          end_time=end_time))
    if extras:
        for name, value in extras:
            event.extended_property.append(
                gdata.calendar.ExtendedProperty(name=name, value=value))

    return event
	

  def _InsertEvent(self, title='Tennis with Beth', 
      content='Meet for a quick lesson', where='On the courts',
      start_time=None, end_time=None, recurrence_data=None,calendar_id='default'):
    """Inserts a basic event using either start_time/end_time definitions
    or gd:recurrence RFC2445 icalendar syntax.  Specifying both types of
    dates is not valid.  Note how some members of the CalendarEventEntry
    class use arrays and others do not.  Members which are allowed to occur
    more than once in the calendar or GData "kinds" specifications are stored
    as arrays.  Even for these elements, Google Calendar may limit the number
    stored to 1.  The general motto to use when working with the Calendar data
    API is that functionality not available through the GUI will not be 
    available through the API.  Please see the GData Event "kind" document:
    http://code.google.com/apis/gdata/elements.html#gdEventKind
    for more information"""
    
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gdata.calendar.Where(value_string=where))

    if recurrence_data is not None:
      # Set a recurring event
      event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
    else:
      if start_time is None:
        # Use current time for the start_time and have the event last 1 hour
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
            time.gmtime(time.time() + 3600))
      event.when.append(gdata.calendar.When(start_time=start_time, 
          end_time=end_time))



    event.extended_property.append(
          gdata.calendar.ExtendedProperty(name='movie_id', value='133268'))

    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/%s/private/full' % calendar_id)
    
    return new_event
   
  def _InsertSingleEvent(self, title='One-time Tennis with Beth',
      content='Meet for a quick lesson', where='On the courts',
      start_time=None, end_time=None):
    """Uses the _InsertEvent helper method to insert a single event which
    does not have any recurrence syntax specified."""

    new_event = self._InsertEvent(title, content, where, start_time, end_time, 
        recurrence_data=None, calendar_id=self.calendar_id)

    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)

    return new_event
    
  def _InsertSimpleWebContentEvent(self):
    """Creates a WebContent object and embeds it in a WebContentLink.
    The WebContentLink is appended to the existing list of links in the event
    entry.  Finally, the calendar client inserts the event."""

    # Create a WebContent object
    url = 'http://www.google.com/logos/worldcup06.gif'
    web_content = gdata.calendar.WebContent(url=url, width='276', height='120')
    
    # Create a WebContentLink object that contains the WebContent object
    title = 'World Cup'
    href = 'http://www.google.com/calendar/images/google-holiday.gif'
    type = 'image/gif'
    web_content_link = gdata.calendar.WebContentLink(title=title, href=href, 
        link_type=type, web_content=web_content)
        
    # Create an event that contains this web content
    event = gdata.calendar.CalendarEventEntry()
    event.link.append(web_content_link)

    print 'Inserting Simple Web Content Event'
    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/nd7sddqgjn8g2i5grl6nf50hlg@group.calendar.google.com/private/full')
    return new_event

  def _InsertWebContentGadgetEvent(self):
    """Creates a WebContent object and embeds it in a WebContentLink.
    The WebContentLink is appended to the existing list of links in the event
    entry.  Finally, the calendar client inserts the event.  Web content
    gadget events display Calendar Gadgets inside Google Calendar."""

    # Create a WebContent object
    url = 'http://google.com/ig/modules/datetime.xml'
    web_content = gdata.calendar.WebContent(url=url, width='300', height='136')
    web_content.gadget_pref.append(
        gdata.calendar.WebContentGadgetPref(name='color', value='green'))

    # Create a WebContentLink object that contains the WebContent object
    title = 'Date and Time Gadget'
    href = 'http://gdata.ops.demo.googlepages.com/birthdayicon.gif'
    type = 'application/x-google-gadgets+xml'
    web_content_link = gdata.calendar.WebContentLink(title=title, href=href,
        link_type=type, web_content=web_content)

    # Create an event that contains this web content
    event = gdata.calendar.CalendarEventEntry()
    event.link.append(web_content_link)

    print 'Inserting Web Content Gadget Event'
    new_event = self.cal_client.InsertEvent(event,
        '/calendar/feeds/default/private/full')
    return new_event

  def _DeleteEvent(self, event):
    """Given an event object returned for the calendar server, this method
    deletes the event.  The edit link present in the event is the URL used
    in the HTTP DELETE request."""

    self.cal_client.DeleteEvent(event.GetEditLink().href)


  def Run(self, delete='false'):
    """Runs each of the example methods defined above.  Note how the result
    of the _InsertSingleEvent call is used for updating the title and the
    result of updating the title is used for inserting the reminder and 
    again with the insertion of the extended property.  This is due to the
    Calendar's use of GData's optimistic concurrency versioning control system:
    http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
    """
    # Getting feeds and query results
    #self._PrintUserCalendars()
    #self._PrintOwnCalendars()
    #self._PrintAllEventsOnDefaultCalendar()
    #self._DateRangeQuery()
    self._DateRangeQuery()
    
    # Inserting and updating events
    #see = self._InsertSingleEvent()
    
 
def main():
  """Runs the CalendarExample application with the provided username and
  and password values.  Authentication credentials are required.  
  NOTE: It is recommended that you run this sample using a test account."""

  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw=", "delete="])
  except getopt.error, msg:
    print ('python calendarExample.py --user [username] --pw [password] ' + 
        '--delete [true|false] ')
    sys.exit(2)

  user = ''
  pw = ''
  delete = 'false'

  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a
    elif o == "--delete":
      delete = a

  if user == '' or pw == '':
    print ('python calendarExample.py --user [username] --pw [password] ' + 
        '--delete [true|false] ')
    sys.exit(2)

  sample = CalendarFactory(user, pw)
  sample.Run(delete)

if __name__ == '__main__':
  main()




















	
	

