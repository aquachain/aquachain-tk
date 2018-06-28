def BlockFormatter(block):
    num = int(block['number'], 16)
    diff = int(block['difficulty'], 16)
    # timestamp = int(block['timestamp'], 16)
    miner = block['miner']
    blockhash = block['hash']
    return f'Block {num}: {blockhash}, with {len(block["transactions"])} tx, mined by {miner}, next difficulty {diff}'


class BlockCache:
    def __init__(self, *args, **kwargs):
        self.data = args
        self.ddata = kwargs
    def set(self, key, value):
        self.data[key] = value
    def get(self, key):
        return self.data[key]
    def clear(self):
        for i in self.data:
            del(self.data[i])
            print('\'leted:', i)
    def len(self):
        return len(self.data)
