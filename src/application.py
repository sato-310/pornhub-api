from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

import inject

from domain import Video


class IVideoSearchService(metaclass=ABCMeta):
    @abstractmethod
    def count_by_query(self, query) -> int:
        pass

    @abstractmethod
    def find_by_query(self, query: str) -> List[Video]:
        pass


@dataclass
class VideoModel:
    id: int
    title: str
    thumbnail_url: str
    view_key: str


class IGetVideoCountQuery(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: str) -> int:
        pass


class IGetVideoListQuery(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: str) -> List[VideoModel]:
        pass


class GetVideoCountQuery(IGetVideoCountQuery):
    _video_search_service = inject.attr(IVideoSearchService)

    def execute(self, query: str) -> int:
        return self._video_search_service.count_by_query(query)


class GetVideoListQuery(IGetVideoListQuery):
    _video_search_service = inject.attr(IVideoSearchService)

    def execute(self, query: str) -> List[VideoModel]:
        videos = self._video_search_service.find_by_query(query)
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
