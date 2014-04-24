class BetterMock:

    def __init__(self):
        self.calls = []
        self.stubs = []

    def __getattr__(self, attr_name):
        def relay_call(*args):
            return self.record_call(attr_name, *args)
        return relay_call

    def record_call(self, method_name, *args):
        call = Call(method_name, args=list(args))
        self.calls.append(call)
        result = self.__stubbed_result_or_none(call)
        return result

    def stub_method(self, method_name, return_value):
        stub = Stub(method_name, return_value)
        self.stubs.append(stub)
        pass

    def get_call_to(self, method_name):
        call_matcher = Call(method_name)
        try:
            call_index = self.calls.index(call_matcher)
            return self.calls[call_index]
        except ValueError:
            return None

    def __stubbed_result_or_none(self, call):
        for stub in self.stubs:
            if call.name == stub.name:
                return stub.value
        return None


class Call:

    def __init__(self, name, args=None):
        self.name = name
        self.args = args

    def __eq__(self, other):
        return self.name == other.name


class Stub:
    def __init__(self, name, value):
        self.name = name
        self.value = value


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

    def and_return(self, value):
        self.mock.stub_method(self.method_name, value)

    def __get_relevant_call_from_mock(self, method_name):
        call_found = self.mock.get_call_to(method_name) or None
        if not call_found:
            raise MethodNotCalledError('Method "%s" was not called on object' % method_name)
        return call_found


def expect(mock_object, method_name):
    return Invokable(mock_object, method_name)


def spy_on(mock_object, method):
    return Invokable(mock_object, method)


class ArgumentsMissingError(Exception):
    pass


class MethodNotCalledError(Exception):
    pass