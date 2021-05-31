from pydantic import BaseModel
from typing import List


class WorkDefinition(BaseModel):
    like: bool
    retweet: bool
    # mention: bool = False


class Work(BaseModel):
    tweetUrl: str
    definition: WorkDefinition


class AccountWorker(BaseModel):
    """
    worker başlaması için tek bir accounta ait iş bildirimi.
    """
    accountId: str
    works: List[Work]

# {
#   "userId": "",
#   "accountId": "1",
#   "works": [
#     {
#       "tweetUrl": "amangorunmeyelm/status/1354905663890198531",
#       "definition": {
#         "like": true,
#         "retweet": true
#       }
#     },
#     {
#       "tweetUrl": "amangorunmeyelm/status/1353450809963458560",
#       "definition": {
#         "like": true,
#         "retweet": false
#       }
#     },
#     {
#       "tweetUrl": "amangorunmeyelm/status/1352392616390885382",
#       "definition": {
#         "like": true,
#         "retweet": true
#       }
#     }
#   ]
# }
