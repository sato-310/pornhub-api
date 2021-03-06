import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

import inject
import requests
from bs4 import BeautifulSoup

from application import IVideoSearchService
from domain import Video


@dataclass
class Response:
    status_code: int
    body: str

    def is_successful(self) -> bool:
        return self.status_code == 200


class IWebClient(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url) -> Response:
        pass


class WebClient(IWebClient):
    def get(self, url) -> Response:
        try:
            response = requests.get(url)
        except Exception as e:
            raise RuntimeError(e)

        return Response(response.status_code, response.text)


class VideoSearchService(IVideoSearchService):
    _web_client = inject.attr(IWebClient)

    SEARCH_RESULT_PAGE_URL = "https://www.pornhub.com/video/search?search={query}&page={page}"

    def count_by_query(self, query) -> int:
        url = self.SEARCH_RESULT_PAGE_URL.format(query=query, page=1)

        response = self._web_client.get(url)
        if not response.is_successful():
            return 0

        html = response.body

        count = self._extract_hit_num_from_html(html)

        return count

    @staticmethod
    def _extract_hit_num_from_html(html: str) -> int:
        soup = BeautifulSoup(html, 'html.parser')

        div = soup.find("div", class_="showingCounter")

        counter_string = div.text.strip()

        count = int(re.match("Showing .* of (.*)", counter_string).group(1))

        return count

    def find_by_query(self, query: str, count: int, offset: int) -> List[Video]:
        page_start = offset // 20 + 1
        page_end = (offset + count) // 20 + 1

        start_element = offset % 20
        end_element = (offset + count) % 20

        results = []
        for page in range(page_start, page_end + 1):
            url = self.SEARCH_RESULT_PAGE_URL.format(query=query, page=page)

            response = self._web_client.get(url)
            if not response.is_successful():
                raise RuntimeError()

            html = response.body

            videos = self._extract_video_data_from_html(html)
            if page == page_start and page == page_end:
                videos = videos[start_element:end_element]
            elif page == page_start:
                videos = videos[start_element:]
            elif page == page_end:
                videos = videos[:end_element]

            results += videos

        return results

    @staticmethod
    def _extract_video_data_from_html(html: str) -> List[Video]:
        soup = BeautifulSoup(html, 'html.parser')

        try:
            pc_video_list_items = soup.find("div", class_="nf-videos").find_all("li", class_="pcVideoListItem")
        except AttributeError:
            return []

        videos = []
        for pc_video_list_item in pc_video_list_items:
            try:
                id = int(pc_video_list_item["data-id"])
                view_key = pc_video_list_item["_vkey"]

                img = pc_video_list_item.find("img")

                thumbnail_url = img["data-thumb_url"]
                title = img["title"]
            except (AttributeError, KeyError):
                continue

            videos.append(Video(id, title, thumbnail_url, view_key))

        return videos
