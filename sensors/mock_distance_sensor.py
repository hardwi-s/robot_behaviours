class MockDistanceSensor:
    def __init__(self, name='mock_distance'):
        self._name = name

    def get_value(self):
        return 20.0

    def get_name(self):
        return self._name

    def reset(self):
        pass
