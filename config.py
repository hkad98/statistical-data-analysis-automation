from gooddata_sdk import GoodDataSdk
from gooddata_pandas import GoodPandas

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    __host = os.getenv("HOST", "http://localhost:3000")
    __token = os.getenv("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
    sdk = GoodDataSdk.create(host_=__host, token_=__token)
    pandas = GoodPandas(host=__host, token=__token)
    workspace_id = os.getenv("WORKSPACE_ID", "demo")
