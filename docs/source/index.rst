.. skink documentation master file, created by
   sphinx-quickstart on Mon Dec  7 08:44:17 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ion
===

Introduction
------------

Ion is an MVC Web Framework meant to be simple and easy to use. No fancy admins or heavyweight architectures.

A simple server infrastructure and a combo of ORM and Template that adds spice to the same old MVC stuff.

Tools
-----

Ion uses VERY proven tools in order to achieve this. It's based on the very stable and mature CherryPy server. What this means is that Ion supports (as does CherryPy) multiple requests at the same time (multi-threaded), WSGI, Plugins and much more.

In the Object-Relational Mapping front, Ion is very well served by Canonical's Storm ORM. Canonical has done a great job in keeping what should be simple, simple. Still you have a LOT of firepower at your fingertips with Storm. Just reading it's tutorial should be enough to start coding. If you don't like Storm, feel free to use any other ORM you like. We won't try to force any tools on you (except cherrypy maybe, lol).

As for the template, I'll admit to being a little selfish. The teams in the company I work for are already VERY used to Django Templates, thus it made a lot of sense for me to use Jinja2, which is a templating engine that looks and feels a lot like Django's. It's REALLY simple to change the templating engine if you'd like to use something else. 

Why use Ion?
------------
Why yet another Web Framework?

We also added some cool stuff of our own. Ion features a VERY simple yet featureful controller. This means that you have Routes, Authentication, Event Bus and a lot more at your disposal, any time you need those. 

So we'll just start hacking our first controller and template and...

*WAIT ONE MINUTE RIGHT THERE! No tests??? What the hell do you think you are doing, sir?*

Ok, ok. Calm down, jeez! I'll write the test first. I was going to do it anyway! *yeah, right!*

Let's write a test for our action. Let's start with a unit (unwired) test::

    #I'll use Fudge to mock stuff since I'm doing that in Ion's codebase

    render_template = Fake(callable=True).with_args('some_action.html', some="args").returns('Hello World args')

    @with_patched_object(controllers.IndexController, "render_template", custom_render_template)
    @with_patched_object(controllers.IndexController, "store", fake_store)
    @with_fakes
    def test_some_action():
        ctrl = TestController()
        result = ctrl.some_action()

        assert result == "Hello World args"

I'll write a functional (wired) test now, just in case you get nervous::

    #retrieving root_dir and config files skipped for brevity
    def test_index_controller_index_action():
        server = Server(root_dir)

        server.start('tests/functional/config.ini', non_block=True)

        while not server.status == ServerStatus.Started:
            time.sleep(0.5)

        controller = IndexController()
        controller.server = server
        controller.context = server.context

        content = controller.some_action()

        assert "Hello World args" in content

Do you think I can write the controller code now? Ok, thank you! Here it goes::

    class TestController(Controller):
        @route("/something")
        def some_action(self):
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

This should be enough to entice you to check the rest of our docs.

Follow the Table of Contents below:

.. toctree::
   :maxdepth: 2

   requirements
   quickstart
   ion_events
   plugin_authoring

