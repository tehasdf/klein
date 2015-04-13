from twisted.trial import unittest

from mock import Mock, patch

from klein.app import Klein
from klein.blueprint import Blueprint



class BlueprintTestCase(unittest.TestCase):
    def test_register(self):
        """
        Calling .register(app) on a blueprint calls the recorded functions with
        the setup state as an argument
        """
        app = Klein()
        blueprint = Blueprint()

        recorded = Mock()
        # add the `recorded` function to be called with a 'setup state' object
        # when the blueprint is registered
        blueprint.record(recorded)

        blueprint.register(app)
        # now the `recorded` function should've been called with a 'setup state'
        # object that has a .app attribute
        self.assertEqual(len(recorded.mock_calls), 1)

        _, record_args, record_kwargs = recorded.mock_calls[0]
        setup_state = record_args[0]
        self.assertIs(setup_state.app, app)


    def test_route(self):
        """
        Calling .route on a blueprint and then registering the blueprint has the
        exact same result as just calling .route on the app directly
        """
        def view_function(request):
            pass

        app = Klein()
        with patch.object(app, 'route') as original_app_route:
            app.route('/')(view_function)

        app = Klein()
        blueprint = Blueprint()
        blueprint.route('/')(view_function)
        with patch.object(app, 'route') as blueprint_app_route:
            blueprint.register(app)

        self.assertEqual(original_app_route.mock_calls,
            blueprint_app_route.mock_calls)
