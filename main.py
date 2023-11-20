import hashlib
import random
import socket
import threading
import time
from keep_alive import keep_alive

keep_alive()


class MoneroSoloMiner:
    def __init__(self, wallet_address, host, port):
        self.wallet_address = wallet_address
        self.host = host
        self.port = port

        self.nonces = set()
        self.found_blocks = 0

        self.threads = 1

    def mine(self):
        while True:
            nonce = random.randint(0, 2**32)

            if nonce not in self.nonces:
                hash = hashlib.sha256(nonce.to_bytes(32, byteorder="big")).hexdigest()

                if hash.startswith("0000000000000000000000000000000000000000000000000000000000000000"):
                    block_header = hashlib.sha256(hash.encode()).hexdigest()
                    block_data = "0000000000000000000000000000000000000000000000000000000000000000"
                    block = block_header + block_data

                    connection = socket.create_connection((self.host, self.port))
                    connection.sendall(block.encode())
                    connection.close()

                    self.found_blocks += 1
                    print("Found a block!")
                    break

            else:
                self.nonces.add(nonce)

    def start(self):
        while True:
            t = threading.Thread(target=self.mine)
            t.daemon = True
            t.start()

            if self.found_blocks > 0:
                break

        print("Exiting...")


def main():
    wallet_address = "42uESmGzAFqjhuDaVby5S12cxnHSo2NMoWQxUcXgJqYKbj6NkupFJxUZkxrYt6oatsAnnzkFuHPH5GhmaVJt2b4H8LXreY1"
    host = "localhost"
    port = 18080

    miner = MoneroSoloMiner(wallet_address, host, port)
    miner.start()

    while True:
        command = input("Enter command: ")

        if command == "stop":
            # Verander de `if`-voorwaarde in `and`
            if self.found_blocks > 0 and command == "stop":
                miner.stop()
                break


if __name__ == "__main__":
    main()
