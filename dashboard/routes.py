import dashboard.controllers as controllers


def setup_routes(app):
    app.router.add_get('/ws/update_depth', controllers.ws_order_book_update_depth)
    app.router.add_get('/', controllers.index)
