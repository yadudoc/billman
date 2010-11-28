#!/usr/bin/python
__author__ = 'yadudoc1729@gmail.com (Yadu Nand B)'

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
  
import os
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

from PyQt4 import QtGui
from PyQt4 import QtCore

# Global variables
COST = 0
START_DATE = ""
END_DATE = ""
# 


class CalendarExample:

  def __init__(self, email, password):
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
    self.cal_client.ProgrammaticLogin()

  # This function has been modified
  def _DateRangeQuery(self, start_date='2007-01-01', end_date='2007-07-01'):
    """Retrieves events from the server which occur during the specified date
    range.  This uses the CalendarEventQuery class to generate the URL which is
    used to retrieve the feed.  For more information on valid query parameters,
    see: http://code.google.com/apis/calendar/reference.html#Parameters"""
			
    #print 'Searching in dates for events on Primary Calendar: %s to %s' % (
    #    start_date, end_date,)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 
        'full', "Billman")

    bill = []
    dates = []

    query.start_min = start_date
    query.start_max = end_date 
    feed = self.cal_client.CalendarQuery(query)
    for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      #print '%s. %s' % (i, an_event.title.text,)
      billdetail = '%s' % (an_event.title.text)
      billdetail = billdetail.upper()
      billdetail = billdetail.replace("BILLMAN","")
      billdetail = billdetail.replace(" ","")
      bill.append(billdetail);
      for a_when in an_event.when:
        #print 'Start time: %s' % (a_when.start_time,)
        billdate = '%s %s' % (an_event.title.text,a_when.start_time)
        dates.append(billdate)
        #print 'End time:   %s' % (a_when.end_time,)
     
    cost = 0 ;
    for i in range(0,len(bill)):
      #print dates[i]
      if ( "B" in bill[i] ):
        cost = cost + 20
      if ( "L" in bill[i] ):
        cost = cost + 30
      if ( "D" in bill[i] ):
        cost = cost + 30
        
    COST = cost
    START_DATE = start_date
    END_DATE = end_date 

    #print "cost calculated = ",cost
    #print "Bill amount for the month %s to %s := %s"%(start_date,end_date,cost)
    

     
  def _AddReminder(self, event, minutes=10):
    """Adds a reminder to the event.  This uses the default reminder settings
    for the user to determine what type of notifications are sent (email, sms,
    popup, etc.) and sets the reminder for 'minutes' number of minutes before
    the event.  Note: you can only use values for minutes as specified in the
    Calendar GUI."""

    for a_when in event.when:
      if len(a_when.reminder) > 0:
        a_when.reminder[0].minutes = minutes
      else:
        a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes))

    print 'Adding %d minute reminder to event' % (minutes,)
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)


  def Run(self, delete='false'):
    """Runs each of the example methods defined above.  Note how the result
    of the _InsertSingleEvent call is used for updating the title and the
    result of updating the title is used for inserting the reminder and 
    again with the insertion of the extended property.  This is due to the
    Calendar's use of GData's optimistic concurrency versioning control system:
    http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
    """

    self._DateRangeQuery("2010-11-01","2010-12-01")
  

class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #self.setGeometry(300, 300, 350, 80)

        
        self.setWindowTitle('InputDialog')
        self.resize(250, 190)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


        # Set start date 
        label = QtGui.QLabel('Start date',self);
        label.move(20,10)
        self.label1 = QtGui.QLineEdit(self)    
        self.label1.setText("2010-11-01")
        self.label1.move(100, 10)
        
        # Set end date
        label = QtGui.QLabel('End date',self);
        label.move(20,40)
        self.label1 = QtGui.QLineEdit(self)
        #self.label2.setText("2010-12-01")
        self.label1.move(100, 40)
        
        # Reading Username
        label = QtGui.QLabel('Username',self);
        label.move(20,70)
        self.label1 = QtGui.QLineEdit(self)
        self.label1.move(100, 70)

        # Reading Password
        label = QtGui.QLabel('Password',self);
        label.move(20,100)
        self.label2 = QtGui.QLineEdit(self)
        self.label2.move(100, 100)
        
        # Output to the app
        label = QtGui.QLabel('Bill amount',self);
        label.move(20,130) 
        self.label3 = QtGui.QLineEdit(self)
        self.label3.move(100,130)

        # Sync button
        self.button = QtGui.QPushButton('Sync', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(170, 160)        
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()
                
        
    def showDialog(self):
        # text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')       
        #sample = CalendarExample(user, pw)
        #sample.Run(delete)
        user = self.label1.text()
        pw   = self.label2.text()
        # resize window to accommodate output

  	self.label3.setText("Results")	  		              
        self.label1.setText("Done!")
        self.label2.setText(self.label1.text())
    

def main():
  app = QtGui.QApplication(sys.argv)
  idlg = InputDialog()
  idlg.show()
  app.exec_()
	
	            
if __name__ == "__main__": 
  main()
