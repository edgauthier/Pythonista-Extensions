# coding: utf-8

import appex
import dialogs
import re
import urllib.parse

def open_url(url):
  from objc_util import UIApplication, nsurl
  app=UIApplication.sharedApplication()
  app._openURL_(nsurl(url))

def fill_placeholders(action_in):
  # Find placeholders
  known_placeholders = set()
  placeholders = []
  fields = []
  for placeholder_match in re.finditer(u"«(.+?)»", action_in):
    placeholder = placeholder_match.group(1)
    if placeholder not in known_placeholders:
      known_placeholders.add(placeholder)
      placeholders.append(placeholder)
      fields.append({'type': 'text', 'title': placeholder, 'key': placeholder})

  action_out = action_in

  # Substitute the placeholders
  if len(placeholders) == 0:
    if dialogs.alert(u"No template placeholders were found.", u"""
If your project text has placeholders (that look like «this»), this script will prompt for values you'd like to substitute for them.
""", u"Continue") != 1:
      return

  else:
#    print fields
    values = dialogs.form_dialog(title='', fields=fields, sections=None)
#    print values
    if values:
      for key in values:
        action_out = re.sub(u"«" + key + u"»", values[key], action_out)
    else:
      return None

  return action_out

def main():
  if not appex.is_running_extension():
    print('Running in Pythonista app, using test data...\n')
    text = u"""
- «project_name» @parallel(false) @due(«due»)
- This task needs to be done at least 1 week before «project_name» is due @due(«due» -1w)
- This task needs to be done at least 2 days before «project_name» is due @due(«due» -2d)
"""
  else:
    text = '\n'.join(appex.get_text().split('\n')[1:])
  if text:
#    print 'Input text: %s' % text
    out = fill_placeholders(text)
    if out == None:
      return
#    print('\nPlaceholders filled:\n{}'.format(out))
    encoded_text = urllib.parse.quote(out)
    omnifocus_url = "omnifocus:///paste?target=projects&content=%s" % encoded_text
#    print '\nOmniFocus URL = %s\n' % omnifocus_url
    appex.finish()
    open_url(omnifocus_url)
  else:
    print('No input text found.')

if __name__ == '__main__':
  main()

