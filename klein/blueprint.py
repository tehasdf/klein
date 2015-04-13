from collections import namedtuple



SetupState = namedtuple('SetupState', ['blueprint', 'app', 'options'])



def _record_route(state, f, *args, **kwargs):
    state.app.route(*args, **kwargs)(f)



def _record_handle_errors(state, f, *args, **kwargs):
    state.app.handle_errors(*args, **kwargs)(f)



class Blueprint(object):
    def __init__(self):
        self._recorded_registrations = []

    def register(self, app, **options):
        setup_state = SetupState(self, app, options)
        for fn, args, kwargs in self._recorded_registrations:
            fn(setup_state, *args, **kwargs)

    def record(self, fn, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self._recorded_registrations.append((fn, args, kwargs))

    def route(self, *args, **kwargs):
        def deco(f):
            route_args = [f] + list(args)
            self.record(_record_route, route_args, kwargs)
            return f
        return deco

    def handle_errors(self, f_or_exception, *additional_exceptions, **kwargs):
        if not isinstance(f_or_exception, type) or not issubclass(f_or_exception, Exception):
            return self.handle_errors(Exception)(f_or_exception)

        def deco(f):
            handle_errors_args = [f, f_or_exception] + list(additional_exceptions)
            self.record(_record_handle_errors, handle_errors_args, kwargs)
            return f
        return deco
