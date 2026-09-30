import importlib
import pathlib
from jina import Deployment

executor_dir_path = pathlib.Path(__file__).parent.resolve()
cls = getattr(importlib.import_module('executor'), executor_dir_path.name)

with Deployment(uses=cls, protocol=['GRPC'], port=55961) as dep:
    dep.block() # serve forever
