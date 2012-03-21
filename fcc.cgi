#!/usr/bin/python

import cgi

# use this to enable debug output
import cgitb; cgitb.enable()


print "Content-Type: text/html"
print
print "<html>"
print "<body>"

print "<h1>Using the CGI module</h1>"

print "<form method='post'>"

# standard single line text field
print "text_field:"
print "<input type='text' name='text_field' value='' />"
print "<br />"

# hidden field (not editable by user - though they can if they really want)
print "<input type='hidden' name='hidden_field' value='a hidden value' />"

# check box field
print "checkbox_field:"
print "<input type='checkbox' name='checkbox_field' value='ticked' />"
print "<br />"

# radio buttons
print "radio_field_field:"
print "<input type='radio' name='radio_field' value='left' />"
print "<input type='radio' name='radio_field' value='right' />" 
print "<br />"

# select box
print "select_field: "
print "<select name='select_field'>"
print "<option value='selected_one'>one</option>"
print "<option value='selected_two'>two</option>"
print "<option value='selected_three'>three</option>"
print "</select>"
print "<br />"

# text area
print "text_area:<br />"
print "<textarea name='text_area' rows='5' cols='20'></textarea>"
print "<br />"

print "<input type='submit' value='submit form' />"
print "</form>"

form = cgi.FieldStorage()
print "<h2>Parameters</h2>"
print "<ul>"
for field_name in form:
	field=form[field_name]
	print "<li>"
	print field.name
	print " = "
	print cgi.escape(repr(field.value))
	print "</li>"
print "</ul>"

print "</body>"
print "</html>"
