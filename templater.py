import logging

import os
import webapp2

import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/')))


class Templater(webapp2.RequestHandler):

  def get(self):

    ########## REDIRECTS ###########

    # ignore everything past the .
    templatePath = self.request.path.split('.')[0]

    # hard redirects actually refresh the page
    hardRedirects = {
      '/r': 'https://docs.google.com/document/d/1UB7mlQreqOiqDCILi_fsd2yi9WviFDcCQDJSTojlt6I/edit',
      '/scratchpad': 'https://docs.google.com/document/d/1EJMROj11Qsu0SyHQlUPCLSCgOc7v9uTKuRa5qRZFSI4/edit'
    }
    if templatePath in hardRedirects:
      self.redirect(hardRedirects[templatePath])
      return

    # soft redirects leave the url intact and load a template different than the name
    softRedirects = {
      '/': '/index',
    }
    if templatePath in softRedirects:
      templatePath = softRedirects[templatePath]

    # special case the homepage title and description
    if templatePath == '/index':
      pageTitle = 'Zach Maier @ zpm.me'
      pageUrl = 'https://www.zpm.me/'
      pageDescription = 'Links to zpm\'s profiles across the web'
    else:
      pageTitle = templatePath[1:] + ' @ zpm.me'
      pageUrl = 'https://www.zpm.me' + templatePath
      pageDescription = ''

    # for everything else, try to load the requested template
    # instead of 404'ing anywhere on the site, just redirect to home on failure
    try:
      template = JINJA_ENVIRONMENT.get_template(templatePath + '.html')
      finalHtml = template.render({
        'pageUrl': pageUrl,
        'pageTitle': pageTitle,
        'pageDescription': pageDescription
      })
    except jinja2.TemplateNotFound:
      self.redirect('/')
      return

    self.response.out.write(finalHtml)


## redirect the app to this to override the entire site
#class SOPA(webapp.RequestHandler):
#
#  def get(self):
#
#    content = open(os.path.join(os.path.dirname(__file__), 'content/sopa.html'), 'r')
#    self.response.out.write(content.read())


################################################################################


app = webapp2.WSGIApplication([
  ('/.*', Templater),
], debug=True)

