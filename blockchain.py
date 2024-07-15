import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", 100)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] == "0" * self.difficulty:
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def create_new_block(self, data):
        previous_block = self.get_latest_block()
        previous_proof = previous_block.proof
        proof = self.proof_of_work(previous_proof)
        new_block = Block(len(self.chain), previous_block.hash, time.time(), data, proof)
        self.add_block(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            previous_proof = previous_block.proof
            current_proof = current_block.proof
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

# Test the Blockchain
blockchain = Blockchain()
print("Mining block 1...")
blockchain.create_new_block("Block 1 Data")

print("Mining block 2...")
blockchain.create_new_block("Block 2 Data")

for block in blockchain.chain:
    print(f"Index: {block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Proof: {block.proof}")
    print(f"Hash: {block.hash}")
    print("\n")

print(f"Blockchain valid? {blockchain.is_chain_valid()}")


