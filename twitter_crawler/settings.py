import os


def load_settings(mode='dev'):
    if mode == 'dev':
        os.environ['DB_HOST'] = "10.40.60.191"
        os.environ['DB_NAME'] = "pointloc"
        os.environ['DB_PASS'] = "pointloc"
        os.environ['DB_USER'] = "pointloc"
        os.environ['TWITTER_KEY'] = "LvJmX55Gbw02s9sqP7JpsQTJ6"
        os.environ['TWITTER_SECRET'] = "GVyobjOh9SLSmcl21qF0zvWdCGKhSSWJoz5hFKOld5XFFDZiTG"
        os.environ['TWITTER_TOKEN'] = "123597227-BVO4fNDGQS0AADFhwz8yH2TSqZJOoZ7nf4Aw8a57"
        os.environ['TWITTER_TOKEN_SECRET'] = "HWqNhdRKzgyg1E3SimL6YyWb8MQ9gDQCPIsYagXvbFdcD"
        os.environ['INDICO_KEY'] = "f90bbbb220baaa2637ec24c0b657deb6"
        os.environ['INDICO_KEY'] = "a763d4a213b000e0bb356b136e6ea628"
