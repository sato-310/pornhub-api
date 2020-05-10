import json

import inject
from bottle import abort, request, response

from application import IGetVideoListQuery, VideoModel


class PornhubController:
    _get_video_list_query = inject.attr(IGetVideoListQuery)

    def get_search(self) -> str:
        query = request.query.get("q")
        if not query:
            abort(400, "Required parameter 'q' missing.")

        try:
            videos = self._get_video_list_query.execute(query)
        except Exception as e:
            abort(503, "Failed to get video data from pornhub.")

        data = {
            "kind": "pornhub#searchListResponse",
            "items": [{
                "id": video.id,
                "title": video.title,
                "thumbnailUrl": video.thumbnail_url,
                "viewKey": video.view_key
            } for video in videos]
        }

        response_body = json.dumps(data, ensure_ascii=False)

        response.headers["Content-Type"] = "application/json; charset=utf-8"

        return response_body


class ErrorController:
    def error400(self, error) -> str:
        return self._error(error)

    def error404(self, error) -> str:
        return self._error(error)

    def error503(self, error) -> str:
        return self._error(error)

    @staticmethod
    def _error(error) -> str:
        response.headers["Content-Type"] = "application/json; charset=utf-8"

        return json.dumps({"error": error.status_code, "error_description": error.body}, ensure_ascii=False)
