import pendulum
from jina import Executor, requests
from docarray import DocList
from typing import Dict, List

from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    EnrichRequestDoc,
    EnrichResponseDoc,
)
from core.logging import logger
from core.models.utils import post_service_log

from .vtrc_facebook.vtrc_executor import VetricFacebookAPI
from .slinks_facebook.slinks_executor import SocialLinksFacebookAPI



class FacebookAPI(Executor):

    source = "facebook"

    default_search_fields = [
        ['f_name', 'l_name', 'work'],
        ['f_name', 'l_name', 'city'],
        ['f_name', 'l_name', 'education'],
        ['email_address'],
    ]
    default_rare_name_fields = ['f_name', 'l_name']

    @requests(on="/search")
    async def search(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        _docs = []
        resource_name = parameters.get(
            "name", parameters.get("kwargs", {}).get("name"))
        if not resource_name and self.source in parameters.get("source", []):
            resource_name = "{}_{}".format(
                parameters.get("resource"), self.source)
        if not resource_name:
            self.logger.debug(f"Skip {self.source} search for candidates")  # noqa
            return DocList[SearchResponseDoc](_docs)

        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="FacebookAPI",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from "
                        f"FacebookAPI search entry: {str(e)}")

        '''
        # NOTE: backward compatibility. should removed soon
        if flow_step == 'enrich':
            for doc in docs:
                result_list = await self.enrich(doc)
                if result_list:
                    _docs = _docs + result_list
            _docs = DocList[FacebookEnrichDoc](_docs)
        else:
        '''
        for doc in docs:
            # TODO: turn back event notification
            # search = await SearchEventModel.get(doc.search_id)
            # search.status = "Started"
            # await search.save()
            self.logger.info(f"FacebookAPI /search "
                             f"id:{doc.search_id} urn:{doc.urn}")
            search_fields = parameters.get(
                'search_fields', parameters.get(
                    'kwargs', {}).get('search_fields')
            )
            if not search_fields:
                search_fields = self.default_search_fields
            rare_name_search_fields = parameters.get(
                'rare_name_search_fields', parameters.get(
                    'kwargs', {}).get('rare_name_search_fields'))
            if not rare_name_search_fields:
                rare_name_search_fields = self.default_rare_name_fields
            if doc.is_rare_name:
                search_fields.append(rare_name_search_fields)
            for search_field in search_fields:
                result_list = await self._search(doc,
                                                 resource_name,
                                                 q=search_field)
                if result_list:
                    self.logger.debug(f"Found {len(result_list)} {self.source} candidates for {doc.name}")  # noqa
                    _docs = _docs + result_list
                else:
                    self.logger.debug(f"No found {self.source} candidates for {doc.name}")  # noqa
        for _doc in _docs:
            _doc.source = self.source
        end_time = pendulum.now()
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="FacebookAPI",
                        search_step="search",
                        message="Finished in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from "
                        f"FacebookAPI search out: {str(e)}")
        return DocList[SearchResponseDoc](_docs)

    async def _search(
        self, doc: SearchRequestDoc, resource_name: str, q: List
    ) -> List[SearchResponseDoc]:
        if ((doc.resource == "vetric" and resource_name == "vetric_facebook")
                or (not doc.resource and resource_name == "vetric_facebook")):
            query_parts = [
                val if isinstance(val, str) else item
                for elem in q
                if (val := getattr(doc, elem)) is not None
                for item in (val if isinstance(val, list) else [val])
            ]
            query_strs = [" ".join(combo) for combo in zip(
                *[[part] if isinstance(part, str) else part for
                  part in query_parts])]
            for query in query_strs:
                doc.query = query
                vetric_api = VetricFacebookAPI()
                return await vetric_api.search(doc)
        if (doc.resource == "social_links" and
                resource_name == "socialinks_facebook"):
            slinks_api = SocialLinksFacebookAPI(doc)
            return await slinks_api._search(doc)

    @requests(on="/enrich")
    async def enrich(
        self,
        docs: DocList[EnrichRequestDoc],
        parameters: Dict,
        **kwards
    ) -> DocList[EnrichResponseDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="FacebookAPI",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from "
                        f"FacebookAPI enrich entry: {str(e)}")
        resource = parameters.get("resource")
        _docs = []
        for doc in docs:
            self.logger.info(f"FacebookAPI /enrich "
                             f"id:{doc.search_id} urn:{doc.urn}")
            if not doc.source == self.source:
                continue
            doc.resource = resource
            if result_doc := await self._enrich(doc):
                result_doc.source = self.source
                _docs.append(result_doc)
        end_time = pendulum.now()
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="FacebookAPI",
                        search_step="enrich",
                        message="Finished in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from "
                        f"FacebookAPI enrich out: {str(e)}")
        return DocList[EnrichResponseDoc](_docs)

    async def _enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc | None:
        if doc.resource == "vetric":
            vetric_api = VetricFacebookAPI()
            return await vetric_api.enrich(doc)
