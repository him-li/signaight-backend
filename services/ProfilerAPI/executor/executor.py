import pendulum
from jina import Executor, requests
from docarray import DocList
from typing import Dict, List

from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    ActiveSearchRequestDoc,
    ActiveSearchResponseDoc,
)
from core.logging import logger
from core.models.utils import post_service_log

from .grayfox.grfx_executor import GrayfoxAPI



class ProfilerAPI(Executor):

    resource = 'grayfox'

    @requests(on="/search")
    async def search(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        _docs = []
        source_name = parameters.get("source")
        if 'grayfox' not in source_name:
            self.logger.debug(f"Skip {self.resource} search for candidates")
            return DocList[SearchResponseDoc](_docs)

        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ProfilerAPI",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")

        for doc in docs:
            self.logger.info(f"ProfilerAPI /search id:{doc.search_id} "
                             f"urn:{doc.urn}")
            if doc.email_address or doc.phone_number:
                result_list = await self._search(doc)
                if result_list:
                    self.logger.debug(
                        (f"Found {len(result_list)} {self.resource} candidates"
                         " for {doc.name}"))
                    _docs = _docs + result_list
                else:
                    self.logger.debug(
                        f"No found {self.resource} candidates for {doc.name}")
        for _doc in _docs:
            _doc.resource = self.resource
        end_time = pendulum.now()
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ProfilerAPI",
                        search_step="search",
                        message="Finished in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return DocList[SearchResponseDoc](_docs)

    @requests(on="/active_search")
    async def active_search(
        self,
        docs: DocList[ActiveSearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[ActiveSearchResponseDoc]:
        _docs = []
        source_name = parameters.get("source")
        if 'grayfox' not in source_name:
            self.logger.debug(f"Skip {self.resource} search for candidates")
            return DocList[ActiveSearchResponseDoc](_docs)

        for doc in docs:
            self.logger.info(f"ProfilerAPI /active_search id:{doc.search_id} "
                             f"urn:{doc.urn}")
            result_list = await self._active_search(doc)
            if result_list:
                logger.debug(
                    (f"Found {len(result_list)} {self.resource} candidates"
                        " for {doc.title}"))
                _docs = _docs + result_list
            else:
                logger.debug(
                    f"No found {self.resource} candidates for {doc.title}")
        for _doc in _docs:
            _doc.resource = self.resource
        return DocList[ActiveSearchResponseDoc](_docs)

    async def _search(
        self, doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        grfx_api = GrayfoxAPI()
        return await grfx_api.search(doc)

    async def _active_search(
            self,
            doc: ActiveSearchRequestDoc
    ) -> List[ActiveSearchResponseDoc]:
        grfx_api = GrayfoxAPI()
        return await grfx_api.active_search(doc)
