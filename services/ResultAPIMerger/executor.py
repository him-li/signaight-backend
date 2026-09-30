import pendulum
from jina import Executor, requests
from docarray import DocList

from core.documents import SearchResponseDoc, EnrichResponseDoc
from core.logging import logger
from core.models.utils import post_service_log


class ResultAPIMerger(Executor):

    @requests(on="/search")
    async def search_merger(
        self,
        docs: DocList[SearchResponseDoc],
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        if not docs:
            logger.error("ResultAPIMerger: received empty docs list")
            return DocList[SearchResponseDoc]()
        try:
            post_service_log(
                search_id=docs[0].search_id,
                urn=docs[0].urn,
                executor="ResultAPIMerger",
                search_step="enrich",
                message=f"Merging initiated with {len(docs)}",
                docs_count=len(docs),
                step_point="entry",
            )
        except Exception as e:
            logger.error(
                f"Unable to send service log from ResultAPIMerger "
                f"search merging initiated: {str(e)}")
        start_time = pendulum.now()
        _docs = DocList[SearchResponseDoc]()
        skipped_docs_count = 0
        for doc in docs:
            if doc.source or doc.source is not None:
                _docs.append(doc)
            else:
                skipped_docs_count += 1
        end_time = pendulum.now()
        try:
            post_service_log(
                search_id=_docs[0].search_id,
                urn=_docs[0].urn,
                executor="ResultAPIMerger",
                search_step="search",
                message=("Finished {} in {:.2f} seconds. "
                         "Skiped empty {} docs").format(
                    len(_docs),
                    end_time.int_timestamp - start_time.int_timestamp,
                    skipped_docs_count),
                docs_count=len(_docs),
                step_point="out",
                step_duration_microseconds=end_time.diff(
                    start_time)._to_microseconds()
            )
        except Exception as e:
            logger.error(
                f"Unable to send service log from ResultAPIMerger "
                f"search finished: {str(e)}")
        return _docs

    @requests(on="/enrich")
    async def enrich_reducer(
        self,
        docs: DocList[EnrichResponseDoc],
        **kwargs
    ) -> DocList[EnrichResponseDoc]:
        if not docs:
            logger.error("ResultAPIMerger /enrich: received empty docs list")
            return DocList[EnrichResponseDoc]()
        try:
            post_service_log(
                search_id=docs[0].search_id,
                urn=docs[0].urn,
                executor="ResultAPIMerger",
                search_step="enrich",
                message=f"Merging initiated with {len(docs)}",
                docs_count=len(docs),
                step_point="out",
            )
        except Exception as e:
            logger.error(
                f"Unable to send service log from ResultAPIMerger "
                f"enrich merging initiated: {str(e)}")
        start_time = pendulum.now()
        _docs = DocList[EnrichResponseDoc]()
        skipped_docs_count = 0
        for doc in docs:
            if doc.source or doc.source is not None:
                _docs.append(doc)
            else:
                skipped_docs_count += 1

        end_time = pendulum.now()
        try:
            post_service_log(
                search_id=_docs[0].search_id,
                urn=_docs[0].urn,
                executor="ResultAPIMerger",
                search_step="enrich",
                message=("Finished {} in {:.2f} seconds. "
                         "Skiped empty {} docs").format(
                    len(_docs),
                    end_time.int_timestamp - start_time.int_timestamp,
                    skipped_docs_count),
                docs_count=len(_docs),
                step_point="out",
                step_duration_microseconds=end_time.diff(
                    start_time)._to_microseconds()
            )
        except Exception as e:
            logger.error(
                f"Unable to send service log from ResultAPIMerger "
                f"enrich finished: {str(e)}")
        return _docs
