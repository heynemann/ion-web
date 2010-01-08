.. skink documentation master file, created by
   sphinx-quickstart on Mon Dec  7 08:44:17 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ion
===

Ion is an MVC Web Framework meant to be simple and easy to use. No fancy admins or heavyweight architectures.

A simple server infrastructure and a combo of ORM and Template that adds spice to the same old MVC stuff.

Ion uses VERY proven tools in order to achieve this. It's based on the very stable and mature CherryPy server. What this means is that Ion supports (as does CherryPy) multiple requests at the same time (multi-threaded), WSGI, Plugins and much more.

In the Object-Relational Mapping front, Ion is very well served by Canonical's Storm ORM. Canonical has done a great job in keeping what should be simple, simple. Still you have a LOT of firepower at your fingertips with Storm. Just reading it's tutorial should be enough to start coding. If you don't like Storm, feel free to use any other ORM you like. We won't try to force any tools on you (except cherrypy maybe, lol).

As for the template, I'll admit to being a little selfish. The teams in the company I work for are already VERY used to Django Templates, thus it made a lot of sense for me to use Jinja2, which is a templating engine that looks and feels a lot like Django's. It's REALLY simple to change the templating engine if you'd like to use something else. 

We also added some cool stuff of our own. Ion features a VERY simple yet featureful controller. This means that you have Routes, Authentication, Event Bus and a lot more at your disposal, any time you need those. Let me show a controller sample::

    class TestController(Controller):
        @route("/something")
        def SomeAction(self):
            return self.render_template("some_action.html", some="args")

This very simple controller creates a route at http://localhost:8082/something that renders a template called some_action.html with the "some" parameter with value of "args". This means we can use the "some" variable in our template as seen here:

.. code-block:: html

    <html>
        <head>
            <title>Test</title>
        </head>
        <body>
            <p>Hello World {{ some }}</p>
        </body>
    </html>

This template will render "Hello World args" as the result of the template processing.

This should be enought to entice you to check the rest of our docs.

Follow the Table of Contents below:

.. toctree::
   :maxdepth: 2

   requirements
   quickstart
   ion_events
   plugin_authoring

