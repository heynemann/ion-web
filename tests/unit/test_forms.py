#from ion.forms import TextInput, PasswordInput
#''' 


#class LoginForm(Form):
#    username = TextField()
#    password = TextField(widget=PasswordInput)
#'''
#    
#def test_can_create_form():
#    form = LoginForm()
#    assert isinstance(form, LoginForm)

#def test_can_create_text_input():
#    _input = TextInput()
#    assert isinstance(_input, TextInput)
#    
#def test_text_input_render():
#    _input = TextInput()
#    assert _input.render() == u'<input type="text" />'
#    
#def test_create_password_input():
#    _input = PasswordInput()
#    assert isinstance(_input, PasswordInput)
#    
#def test_password_input_render():
#    _input = PasswordInput()
#    assert _input.render() == u'<input type="password" />'
#    
#def test_text_input_str_returns_render():
#    _input = TextInput()
#    assert str(_input) == u'<input type="text" />'
#    assert str(_input) == _input.render()

#def test_text_input_unicode_returns_render():
#    _input = TextInput()
#    assert unicode(_input) == u'<input type="text" />'
#    assert unicode(_input) == _input.render()
#    
#def test_password_input_str_returns_render():
#    _input = PasswordInput()
#    assert str(_input) == u'<input type="password" />'
#    assert str(_input) == _input.render()

#def test_password_input_unicode_returns_render():
#    _input = PasswordInput()
#    assert unicode(_input) == u'<input type="password" />'
#    assert unicode(_input) == _input.render()
