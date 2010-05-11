from datetime import datetime

from ion.controllers import Controller, route

class HelloController(Controller):

    @route('/hello')
    def index(self):
        return self.render_template("hello.html", date=datetime.now())
