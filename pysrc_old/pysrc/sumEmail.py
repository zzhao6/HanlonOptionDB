import collections

SumEmail = collections.namedtuple('SumEmail', ['date', \
                                               'starttime', \
                                               'spenttime', \
                                               'endtime', \
                                               'RDERoundLst', \    # records number of RDE after each round
                                               'TimeoutLst', \     # records number of timeout err after each round
                                               'numReq', \         # total number of requests
                                               'numComp', \        # total number of completed requests
                                               'numErr', \         # total number of error received
                                               'errLst', \]        # err message list


