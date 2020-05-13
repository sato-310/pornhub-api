import json

import inject
from bottle import abort, request, response

from application import IGetVideoCountQuery, IGetVideoListQuery, VideoModel


class PornhubController:
    DEFAULT_RESULTS_PER_PAGE = 20

    _get_video_count_query = inject.attr(IGetVideoCountQuery)
    _get_video_list_query = inject.attr(IGetVideoListQuery)

    def get_search(self) -> str:
        query = request.query.get("q")
        if not query:
            abort(400, "Required parameter 'q' missing.")

        try:
            total_results = self._get_video_count_query.execute(query)

            videos = self._get_video_list_query.execute(query)
        except Exception as e:
            abort(503, "Failed to get video data from pornhub.")

        data = {
            "page_info": {
                "total_results": total_results,
                "results_per_page": self.DEFAULT_RESULTS_PER_PAGE
            },
            "items": [
                {
                    "id": video.id,
                    "title": video.title,
                    "thumbnail_url": video.thumbnail_url,
                    "view_key": video.view_key
                } for video in videos
            ]
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
