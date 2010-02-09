================
Testing Ion Apps
================

Unit Tests
==========

Testing Controller Actions
--------------------------

Placeholder

Testing Models
--------------

Placeholder

Functional Tests
==========

Testing Controller Actions
--------------------------

In order to write functional tests for your actions you can either write the needed infrastructure for your test or you can use Ion's test helper for it. We'll explore Ion's helper.

Let's create the test for the index of our website::

    from ion.test_helpers import ServerHelper

    def test_index_action()
        server = ServerHelper(root_dir, 'controller_config2.ini')
        controller = server.ctrl(IndexController)
        content = controller.index()

        assert "Home Page" in content

This test runs Ion's server, gets a wired controller, calls the index action and asserts the contents.

Testing Models
--------------

Placeholder

Testing Routes
--------------

Placeholder

