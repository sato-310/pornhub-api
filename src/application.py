from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

import inject

from domain import Video


class IVideoSearchService(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: str) -> List[Video]:
        pass


@dataclass
class VideoModel:
    id: int
    title: str
    thumbnail_url: str
    view_key: str


class IGetVideoListQuery(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, search: str) -> List[VideoModel]:
        pass


class GetVideoListQuery(IGetVideoListQuery):
    _video_search_service = inject.attr(IVideoSearchService)

    def execute(self, search: str) -> List[VideoModel]:
        videos = self._video_search_service.execute(search)
        if not videos:
            return []

        result = []
        for video in videos:
            search_result_model = VideoModel(
                video.id,
                video.title,
                video.thumbnail_url,
                video.view_key
            )

            result.append(search_result_model)

        return result
