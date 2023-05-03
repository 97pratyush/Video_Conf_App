from PySide6.QtCore import QObject, Property, Signal

class UserDetails(QObject):
    valueChanged = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._user_id = ""
        self._full_name = ""

    # Define a property with a getter and setter method
    def get_user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def get_name(self):
        return self._full_name

    def set_name(self, full_name):
        self._full_name = full_name

    user_id = Property(str, get_user_id, set_user_id, notify=valueChanged)
    name = Property(str, get_name, set_name, notify=valueChanged)