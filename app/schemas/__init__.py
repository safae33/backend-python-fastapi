from app.schemas.request.accountworker import AccountWorker, Work
from app.schemas.request.newProcess import ScNewProcess


class Adaptors:

    @classmethod
    def new_process_to_accountworker_list(newProcess: ScNewProcess) -> list[AccountWorker]:
        result: list[AccountWorker] = []

        for account in newProcess.accounts:
            accountWorker = AccountWorker.construct()
            accountWorker.accountId = account.id
            for action in account.actions:
                tweetGroup = next(
                    (x for x in newProcess.tweetGroups if x.value == action.tweetGroupId), None)
                for index in tweetGroup.tweets:
                    work = Work.construct()
                    work.tweetUrl = newProcess.tweets[index].url
                    work.like = action.like
                    work.retweet = action.retweet
                    accountWorker.works.append(work)
                
