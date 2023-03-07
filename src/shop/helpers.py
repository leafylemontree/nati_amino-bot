import time
import uuid

def timestamp():
    return int(time.time() * 1000)

def getDonationList(amount):
    if amount > 500:
        donation = [500 for i in range(amount // 500 )]
        donation.append(amount % 500)
    else:
        donation = [amount % 500]
    return donation

def postFormatString(postType, name):
    s = f'la wiki' if postType == 'wiki' else 'el blog' 
    return f'{s} {name}'
