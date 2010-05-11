#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fudge import Fake, with_fakes, with_patched_object, clear_expectations
from fudge.inspector import arg

import cherrypy
import ion.controllers as ctrl
from ion.controllers import Controller, route, authenticated

def clear():
    ctrl.__CONTROLLERS__ = []
    ctrl.__CONTROLLERSDICT__ = {}

authenticated_cherrypy = Fake('cherrypy')
authenticated_cherrypy.has_attr(session={'authenticated_user':'user1'})

def test_can_create_controller():
    ctrl = Controller()
    assert ctrl

def test_controller_has_null_context_by_default():
    ctrl = Controller()

    assert not ctrl.context

def test_controller_has_null_server_by_default():
    ctrl = Controller()

    assert not ctrl.server

@with_fakes
def test_controller_has_empty_routes_by_default():
    clear_expectations()
    clear()
    class TestController(Controller):
        pass

    ctrl = TestController()

    assert ctrl.__routes__ is not None
    assert not ctrl.__routes__
    assert isinstance(ctrl.__routes__, list)

@with_fakes
def test_all_controllers_returns_all_imported_controllers():
    clear_expectations()
    clear()
    class TestController2(Controller):
        pass

    controllers = Controller.all()

    assert controllers
    assert len(controllers) == 1
    assert controllers[0] == TestController2

@with_fakes
def test_route_decorator_registers_route_information():
    clear_expectations()
    clear()
    class TestController(Controller):
        @route("/something")
        def SomeAction(self):
            pass

    assert TestController.__routes__

    #Example of a route
    #('SomeAction', {'route': '/something', 'method': 'SomeAction'})
    assert TestController.__routes__[0][0] == 'SomeAction'
    assert TestController.__routes__[0][1]['route'] == '/something'
    assert TestController.__routes__[0][1]['method'] == 'SomeAction'

@with_fakes
def test_route_decorator_registers_route_with_custom_name():
    clear_expectations()
    clear()
    class TestController(Controller):
        @route("/something", name="named_route")
        def SomeAction(self):
            pass

    assert TestController.__routes__

    assert TestController.__routes__[0][0] == 'named_route'
    assert TestController.__routes__[0][1]['route'] == '/something'
    assert TestController.__routes__[0][1]['method'] == 'SomeAction'

dispatcher = Fake("dispatcher")
dispatcher.expects("connect").with_args("test_SomeAction", "/something", controller=arg.any_value(), action="SomeAction")
@with_fakes
def test_register_routes():
    clear_expectations()
    clear()

    class TestController(Controller):
        @route("/something")
        def SomeAction(self):
            pass

    ctrl = TestController()

    ctrl.register_routes(dispatcher)

template_context = Fake('context').has_attr(settings=Fake('settings'))
template_context.settings.has_attr(Ion=Fake('ion'))
template_context.settings.Ion.has_attr(template_path="some/path/to/templates")

template_loader = Fake('template_loader')
environment = Fake(callable=True).with_args(loader=arg.any_value()).returns(template_loader)
package_loader = Fake(callable=True).with_args(arg.endswith("some/root/templates"))

template_fake = Fake('template')
template_loader.expects('get_template').with_args('some_file.html').returns(template_fake)
template_fake.expects('render').with_args(user="user1", some="args", settings=arg.any_value()).returns("expected")

@with_fakes
@with_patched_object(ctrl, "Environment", environment)
@with_patched_object(ctrl, "FileSystemLoader", package_loader)
@with_patched_object(ctrl, "cherrypy", authenticated_cherrypy)
def test_render_template():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.server = Fake('server')
    ctrl.server.has_attr(root_dir="some/root")
    ctrl.server.apps = []
    ctrl.server.has_attr(template_path="some/root/templates")
    ctrl.server.template_filters = {}
    ctrl.server.has_attr(context=template_context)
    content = ctrl.render_template("some_file.html", some="args")

    assert content == "expected"

template_context2 = Fake('context').has_attr(settings=Fake('settings'))
template_context2.settings.has_attr(Ion=Fake('ion'))
template_context2.settings.Ion.has_attr(template_path="/templates")

simpler_package_loader = Fake(callable=True).with_args(arg.endswith("some/root/templates"))

@with_fakes
@with_patched_object(ctrl, "Environment", environment)
@with_patched_object(ctrl, "FileSystemLoader", simpler_package_loader)
@with_patched_object(ctrl, "cherrypy", authenticated_cherrypy)
def test_render_template_in_folder_without_package():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.server = Fake('server')
    ctrl.server.has_attr(root_dir="some/root")
    ctrl.server.has_attr(template_path="some/root/templates")
    ctrl.server.apps = []
    ctrl.server.template_filters = {}
    ctrl.server.context = template_context2

    content = ctrl.render_template("some_file.html", some="args")

    assert content == "expected"

template_context3 = Fake('context').has_attr(settings=Fake('settings'))
template_context3.settings.has_attr(Ion=Fake('ion'))
template_context3.settings.Ion.has_attr(template_path="")

empty_package_loader = Fake(callable=True).with_args(arg.endswith('some/root/templates'))

@with_fakes
@with_patched_object(ctrl, "Environment", environment)
@with_patched_object(ctrl, "FileSystemLoader", empty_package_loader)
@with_patched_object(ctrl, "cherrypy", authenticated_cherrypy)
def test_render_template_in_folder_with_null_package():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.server = Fake('server')
    ctrl.server.has_attr(root_dir="some/root")
    ctrl.server.has_attr(template_path="some/root/templates")
    ctrl.server.apps = []
    ctrl.server.template_filters = {}
    ctrl.server.context = template_context3
    content = ctrl.render_template("some_file.html", some="args")

    assert content == "expected"

fake_session = "store"

@with_fakes
@with_patched_object(ctrl, "session", fake_session)
def test_controller_returns_store_from_sqlalchemy_tool_session():
    clear_expectations()
    clear()

    ctrl = Controller()
    assert ctrl.store == "store"

fake_cherrypy1 = Fake('cherrypy')
fake_cherrypy1.has_attr(session={})

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy1)
def test_controller_has_null_user_by_default():
    clear_expectations()
    clear()

    ctrl = Controller()

    assert not ctrl.user

fake_cherrypy2 = Fake('cherrypy')
fake_cherrypy2.has_attr(session={'authenticated_user':'some_user'})

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy2)
def test_controller_returns_thread_data_user():
    clear_expectations()
    clear()

    ctrl = Controller()

    assert ctrl.user == "some_user"

fake_cherrypy3 = Fake('cherrypy')
fake_cherrypy3.has_attr(session={})

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy3)
def test_controller_can_authenticate_user():
    clear_expectations()
    clear()

    ctrl = Controller()

    ctrl.login(user="auth_user")

    assert ctrl.user == "auth_user"

fake_cherrypy4 = Fake('cherrypy')
fake_cherrypy4.has_attr(session={})

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy4)
def test_controller_logoff_clears_user():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.login("some_random_user")
    ctrl.logoff()

    assert not ctrl.user

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy4)
def test_authenticated_decorator_checks_for_user():
    clear_expectations()
    clear()

    class TestController(Controller):
        @authenticated
        def some_action(self):
            pass

    ctrl = TestController()

    fake_server = Fake('server')
    ctrl.server = fake_server
    ctrl.server.context = Fake('context')

    ctrl.server.expects('publish').with_args('on_before_user_authentication', arg.any_value())
    ctrl.server.next_call('publish').with_args('on_user_authentication_failed', arg.any_value())

    ctrl.some_action()

fake_cherrypy5 = Fake('cherrypy')
fake_cherrypy5.has_attr(session={'authenticated_user':'user1'})

@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy5)
def test_authenticated_decorator_executes_function_when_user_exists():
    clear_expectations()
    clear()

    class TestController(Controller):
        @authenticated
        def some_action(self):
            return "some_action_result"

    ctrl = TestController()

    fake_server = Fake('server')
    ctrl.server = fake_server
    ctrl.server.context = Fake('context')

    ctrl.server.expects('publish').with_args('on_before_user_authentication', arg.any_value())
    ctrl.server.next_call('publish').with_args('on_user_authentication_successful', arg.any_value())

    result = ctrl.some_action()

    assert result == "some_action_result"

def test_controller_can_redirect():
    clear_expectations()
    clear()

    ctrl = Controller()

    try:
        ctrl.redirect("http://www.google.com")
    except cherrypy.HTTPRedirect, err:
        assert err.urls
        assert err.urls[0] == "http://www.google.com"
        return

    assert False, "Should not have gotten this far"


fake_cherrypy6 = Fake('cherrypy')
fake_cherrypy6.expects("session").raises(AttributeError("failed"))
@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy6)
def test_user_returns_none_when_attribute_error():
    clear_expectations()
    clear()

    ctrl = Controller()

    assert not ctrl.user

@with_fakes
def test_logging_does_nothing_if_verbose_is_false():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.server = Fake('server')
    ctrl.server.context = Fake('context')
    ctrl.server.context.has_attr(settings=Fake('settings'))
    ctrl.server.context.settings.has_attr(Ion=Fake('Ion'))
    ctrl.server.context.settings.Ion.expects('as_bool').with_args('verbose').returns(False)

    ctrl.log('bla')

fake_cherrypy7 = Fake('cherrypy')
fake_cherrypy7.expects("log")
@with_fakes
@with_patched_object(ctrl, "cherrypy", fake_cherrypy7)
def test_logging_calls_cherrypy_log_if_verbose_is_true():
    clear_expectations()
    clear()

    ctrl = Controller()
    ctrl.server = Fake('server')
    ctrl.server.context = Fake('context')
    ctrl.server.context.has_attr(settings=Fake('settings'))
    ctrl.server.context.settings.has_attr(Ion=Fake('Ion'))
    ctrl.server.context.settings.Ion.expects('as_bool').with_args('verbose').returns(True)

    ctrl.log('bla')

email_fake_server = Fake('server')
email_render_template = Fake(callable=True).with_args("email.html", some="argument").returns("some_body")
email_send_using_sendmail = Fake(callable=True).with_args("some@user", ["to@user"], "some email", "some_body", html=True).returns(0)
@with_fakes
@with_patched_object(ctrl.Controller, "render_template", email_render_template)
@with_patched_object(ctrl.Controller, "send_using_sendmail", email_send_using_sendmail)
def test_send_template_by_mail():
    clear_expectations()
    clear()

    email_fake_server.has_attr(template_path="/some/path")

    controller = Controller()
    controller.server = email_fake_server

    status = controller.send_template_by_mail("some@user", ["to@user"], "some email", "email.html", some="argument")

    assert status == 0

settings_health_check = Fake('settings')

@with_fakes
@with_patched_object(ctrl.Controller, "settings", settings_health_check)
def test_healthcheck_action():
    clear_expectations()
    clear()

    settings_health_check.Ion = Fake('Ion')
    settings_health_check.Ion.healthcheck_text = "CUSTOMTEXT"

    fake_server_health_check = Fake('server')
    fake_server_health_check.expects('test_connection').returns(True)

    controller = Controller()
    controller.server = fake_server_health_check

    assert controller.healthcheck() == "CUSTOMTEXT"

@with_fakes
@with_patched_object(ctrl.Controller, "settings", settings_health_check)
def test_healthcheck_action_returns_working_if_no_text_in_config():
    clear_expectations()
    clear()

    settings_health_check.Ion = Fake('Ion')
    settings_health_check.Ion.healthcheck_text = None

    fake_server_health_check = Fake('server')
    fake_server_health_check.expects('test_connection').returns(True)

    controller = Controller()
    controller.server = fake_server_health_check

    assert controller.healthcheck() == "WORKING"

@with_fakes
@with_patched_object(ctrl.Controller, "settings", settings_health_check)
def test_healthcheck_action_fails_if_database_not_found():
    clear_expectations()
    clear()

    settings_health_check.Ion = Fake('Ion')
    settings_health_check.Ion.healthcheck_text = None

    fake_server_health_check = Fake('server')
    controller = Controller()
    controller.server = fake_server_health_check

    fake_server_health_check.expects('test_connection').returns(False)
    fake_server_health_check.test_connection_error = ValueError('Fake error')

    try:
        controller.healthcheck()
    except RuntimeError, err:
        assert str(err) == "The connection to the database failed with error: Fake error"
        return

    assert False, "Should not have reached this far."

@with_fakes
def test_controller_cache_is_server_cache():
    clear_expectations()
    clear()

    fake_server = Fake('server')
    fake_server.cache = "cache"

    controller = Controller()
    controller.server = fake_server

    assert controller.cache == "cache"

def test_controller_settings_returns_none_if_no_server():
    controller = Controller()
    assert not controller.settings

template_loader2 = Fake('template_loader 2')
template_loader2.filters = {}
environment2 = Fake(callable=True).with_args(loader=arg.any_value()).returns(template_loader2)
package_loader2 = Fake(callable=True).with_args("template_path")

template_fake2 = Fake('template')
template_loader2.expects('get_template').with_args('template_file').returns(template_fake2)
template_fake2.expects('render').with_args(user=None, settings=arg.any_value()).returns("expected")

fake_settings_template_filter = Fake('settings')
@with_fakes
@with_patched_object(ctrl, "Environment", environment2)
@with_patched_object(ctrl, "FileSystemLoader", package_loader2)
@with_patched_object(Controller, "settings", fake_settings_template_filter)
def test_render_template_uses_all_server_template_filters():
    clear_expectations()
    clear()

    fake_server = Fake('server')
    fake_server.template_path = "template_path"
    fake_server.template_filters = {"some":lambda x: "y"}

    controller = Controller()
    controller.server = fake_server
    controller.server.apps = []

    result = controller.render_template("template_file")

    assert result == "expected"
