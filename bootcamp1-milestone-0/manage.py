import os

from flask_script import Manager

from milestone import create_app as app 

manager  = Manager(app)

if __name__ == '__main__':
    manager.run()