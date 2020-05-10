import inject
from bottle import Bottle

from infrastracture import IVideoSearchService, VideoSearchService, IWebClient, WebClient
from service import PornhubController, ErrorController
from application import IGetVideoListQuery, GetVideoListQuery


def config(binder):
    binder.bind(IWebClient, WebClient())
    binder.bind(IVideoSearchService, VideoSearchService())
    binder.bind(IGetVideoListQuery, GetVideoListQuery())


if __name__ == "__main__":
    app = Bottle()

    inject.configure(config)

    pornhub_controller = PornhubController()

    app.get("/pornhub/v1/search")(pornhub_controller.get_search)

    error_controller = ErrorController()

    app.error(400)(error_controller.error400)
    app.error(404)(error_controller.error404)
    app.error(503)(error_controller.error503)

    app.run(host="0.0.0.0", port=8080)
