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

import sys
import os

from fudge import Fake, with_fakes, with_patched_object, clear_expectations
from fudge.inspector import arg

import cherrypy
from ion.storm_tool import *

def test_cherrypy_storm_tool_gets_created():
    assert isinstance(cherrypy.tools.storm, StormTool)

request_fake_1 = Fake('request')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_1)
def test_storm_tool_setup_returns_on_static_dir():
    clear_expectations()

    request_fake_1.has_attr(config = Fake('config'))
    request_fake_1.config.expects('get').with_args('tools.staticdir.on', False).returns(True)

    tool = StormTool(None, None)
    tool._setup()

request_fake_2 = Fake('request')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_2)
def test_storm_tool_setup_returns_on_static_file():
    clear_expectations()

    request_fake_2.has_attr(config = Fake('config'))
    request_fake_2.config.expects('get').with_args('tools.staticdir.on', False).returns(False)
    request_fake_2.config.next_call('get').with_args('tools.staticfile.on', False).returns(True)

    tool = StormTool(None, None)
    tool._setup()

request_fake_3 = Fake('request')
tool_fake_1 = Fake('Tool')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_3)
@with_patched_object(cherrypy, "Tool", tool_fake_1)
def test_storm_tool_setup_returns_on_static_file():
    clear_expectations()

    request_fake_3.has_attr(config = Fake('config'))
    request_fake_3.config.expects('get').with_args('tools.staticdir.on', False).returns(False)
    request_fake_3.config.next_call('get').with_args('tools.staticfile.on', False).returns(False)

    request_fake_3.has_attr(hooks = Fake('hooks'))
    request_fake_3.hooks.expects('attach').with_args('before_handler', StormHandlerWrapper, priority=100)

    tool = StormTool(None, None)

    tool_fake_1.expects('_setup').with_args(tool)

    tool._setup()

def test_wrapper_has_HttpRedirect_exception_skipped():
    assert StormHandlerWrapper.to_skip
    assert StormHandlerWrapper.to_skip[0] == cherrypy.HTTPRedirect

request_fake_4 = Fake('request')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_4)
def test_wrapper_instance_init():
    clear_expectations()
    request_fake_4.has_attr(handler="next_handler")

    wrapper = StormHandlerWrapper()

    assert wrapper.nexthandler == "next_handler"

request_fake_5 = Fake('request')
handler_fake_1 = Fake(callable=True).returns('RESULT')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_5)
def test_wrapper_instance_call():
    clear_expectations()
    request_fake_5.has_attr(handler=handler_fake_1)

    wrapper = StormHandlerWrapper()

    result = wrapper.__call__()

    assert request_fake_5.rolledback == False
    assert result == "RESULT"

request_fake_6 = Fake('request')
handler_fake_2 = Fake(callable=True).raises(cherrypy.HTTPRedirect('some_url'))

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_6)
def test_wrapper_instance_call_does_nothing_if_exception_is_HttpRedirect():
    clear_expectations()
    request_fake_6.has_attr(handler=handler_fake_2)

    wrapper = StormHandlerWrapper()

    try:
        result = wrapper.__call__()
    except cherrypy.HTTPRedirect:
        return

    assert False, "Should have raised HTTPRedict"

request_fake_7 = Fake('request')
handler_fake_3 = Fake(callable=True).raises(ValueError('some_url'))
log_fake_1 = Fake(callable=True).with_args(arg.endswith('ValueError: some_url\n'), "STORM")
thread_data_fake_1 = Fake('thread_data')
thread_data_fake_1.has_attr(store=Fake('store'))
thread_data_fake_1.store.expects('rollback')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_7)
@with_patched_object(cherrypy, "thread_data", thread_data_fake_1)
@with_patched_object(cherrypy, "log", log_fake_1)
def test_wrapper_instance_call_does_nothing_if_exception_is_HttpRedirect():
    clear_expectations()
    request_fake_7.has_attr(handler=handler_fake_3)

    wrapper = StormHandlerWrapper()

    try:
        result = wrapper.__call__()
    except ValueError:
        assert request_fake_7.rolledback
        return

    assert False, "Should have raised ValueError"

request_fake_8 = Fake('request')
thread_data_fake_2 = Fake('thread_data')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_8)
@with_patched_object(cherrypy, "thread_data", thread_data_fake_2)
def test_do_commit_commits_if_not_rolled_back():
    clear_expectations()
    request_fake_8.has_attr(rolledback=False)
    thread_data_fake_2.has_attr(store=Fake('store'))
    thread_data_fake_2.store.expects('commit')

    do_commit()

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_8)
def test_do_commit_does_not_commit_if_rolled_back():
    clear_expectations()
    request_fake_8.has_attr(rolledback=True)

    do_commit()

request_fake_9 = Fake('request')
thread_data_fake_3 = Fake('thread_data')
log_fake_2 = Fake(callable=True).with_args(arg.endswith('ValueError: FakeValue\n'), 'STORM')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_9)
@with_patched_object(cherrypy, "thread_data", thread_data_fake_3)
@with_patched_object(cherrypy, "log", log_fake_2)
def test_do_commit_commits_if_not_rolled_back():
    clear_expectations()
    request_fake_9.has_attr(rolledback=False)
    thread_data_fake_3.has_attr(store=Fake('store'))
    thread_data_fake_3.store.expects('commit').raises(ValueError("FakeValue"))
    thread_data_fake_3.store.expects('rollback')

    do_commit()

request_fake_10 = Fake('request')
response_fake_1 = Fake('response')

@with_fakes
@with_patched_object(cherrypy, "request", request_fake_10)
@with_patched_object(cherrypy, "response", request_fake_10)
def test_try_commit_attaches_on_end_request_if_stream_available():
    clear_expectations()

    response_fake.has_attr(stream=True)
    request_fake_10.has_attr(hooks=Fake("hooks"))
    request_fake_10.hooks.expects('attach').with_args('on_end_request', do_commit)

    try_commit()

#def try_commit():
#    if cherrypy.response.stream:
#        cherrypy.request.hooks.attach('on_end_request', do_commit)
#    else:
#        if isinstance(cherrypy.response.body, types.GeneratorType):
#            cherrypy.response.collapse_body()
#        do_commit()
