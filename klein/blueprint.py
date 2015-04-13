from collections import namedtuple


SetupState = namedtuple('SetupState', ['blueprint', 'app', 'options'])


def _record_route(state, f, *args, **kwargs):
    state.app.route(*args, **kwargs)(f)


class Blueprint(object):
    def __init__(self):
        self._recorded_registrations = []

    def register(self, app, **options):
        setup_state = SetupState(self, app, options)
        for fn, args, kwargs in self._recorded_registrations:
            fn(setup_state, *args, **kwargs)

    def route(self, *args, **kwargs):
        def deco(f):
            route_args = [f] + args
            self._recorded_registrations.append((_record_route, route_args, kwargs))
            return f
        return deco
