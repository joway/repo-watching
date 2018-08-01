import base64


class File:
    def __init__(self, raw_file):
        self.content = base64.b64decode(raw_file.content).decode('utf-8')
        self.sha = raw_file.sha
