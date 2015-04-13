================================================
Example -- Modular applications using blueprints
================================================

.. code-block:: python

    # main.py

    from klein import Klein

    from users import users_blueprint

    app = Klein()
    users_blueprint.register(app, url_prefix='/users')


.. code-block:: python

    # users.py
    from klein import Blueprint

    users_blueprint = Blueprint()

    @users_blueprint.route('/')
    def list_all_users(request):
        return ['user 1', 'user 2']
