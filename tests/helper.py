class MyMock:

    def __init__(self):
        self.calls = []

    def __getattr__(self, attr_name):
        def relay_call(*args):
            self.record_call(attr_name, *args)
        return relay_call

    def record_call(self, method_name, *args):
        call = Call(method_name, args=list(args))
        self.calls.append(call)


class Call:

    def __init__(self, name, args=None):
        self.name = name
        self.args = args

    def __eq__(self, other):
        return self.name == other.name


class Invokable:

    def __init__(self, mock, method_name):
        self.mock = mock
        self.method_name = method_name

    # FIXME: Finds only arguments for the first call that matches the method_name
    def to_have_been_called_with(self, *args):
        relevant_call = self.__get_relevant_call_from_mock(self.method_name)
        args_missing = []
        for arg in list(args):
            if not relevant_call.args.__contains__(arg):
                args_missing.append(arg)
        if args_missing:
            raise ArgumentsMissingError('Arguments %s not used in call to "%s"' % (str(args_missing), self.method_name))

    def to_have_been_called(self):
        self.__get_relevant_call_from_mock(self.method_name)

    def __get_relevant_call_from_mock(self, method_name):
        call_matcher = Call(method_name)
        try:
            call_index = self.mock.calls.index(call_matcher)
            return self.mock.calls[call_index]
        except ValueError:
            raise MethodNotCalledError('Method "%s" was not called on object' % method_name)


def expect(mock_object, method_name):
    return Invokable(mock_object, method_name)


class ArgumentsMissingError(Exception):
    pass


class MethodNotCalledError(Exception):
    pass