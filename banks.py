import json
#maxWithdrawals = 1000
#banks = {'id': ['9999'], 'withdrawals': [1234], 'time': [0]}

#a_file = open("banks.json", "w")
#a_file = json.dump(banks, a_file)


def getBankData():
    with open('banks.json', 'r') as fp:
        dictionary = json.load(fp)
    return dictionary


def loadBankData(data):
    with open('banks.json', 'w') as fp:
        json.dump(data, fp)


