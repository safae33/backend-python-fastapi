from pydantic import BaseModel


class ScTweet(BaseModel):
    url: str
    profilePicUrl: str
    name: str
    username: str
    text: str


class ScTweetGroup(BaseModel):
    id: int
    tweets: list[int]


class ScAction(BaseModel):
    tweetGroupId: int
    like = False
    retweet = False


class ScAccount(BaseModel):
    id: int
    name: str
    username: str
    profilePicUrl: str
    actions: list[ScAction]


class ScNewProcess(BaseModel):
    tweets: list[ScTweet]
    tweetGroups: list[ScTweetGroup]
    accounts: list[ScAccount]
