import requests
import asyncio
import random
from pathlib import Path

class DigitalSignature():
    async def get_public_values(self, server_port: int):
        uri = f"http://localhost:{server_port}/digital-signature-param"
        response = requests.get(uri)

        if response.status_code == 200:
            data = response.json()
            self.a = data['a']
            self.p = data['p']
            self.q = data['q']
        else:
            raise Exception("Failed to get public values")
    
    def generate_public_key(self):
        self.__public_key = pow(self.a, -self.__private_key, self.p)

    def generate_private_key(self):
        self.__private_key = random.randint(0, self.q)
    
    def generate_keypair(self):
        self.generate_private_key()
        self.generate_public_key()
        return (self.__public_key, self.__private_key)
    
    def save_public_key(self, pkey_path: Path):
        if not pkey_path.exists():
            pkey_path.write_text(str(self.__public_key))
        else:
            raise FileExistsError("Could not save public key")
    
    def save_private_key(self, pkey_path: Path):
        if not pkey_path.exists():
            pkey_path.write_text(str(self.__private_key))
        else:
            raise FileExistsError("Could not save private key")
    
    def get_public_key(self):
        return self.__public_key
    
    def get_private_key(self):
        return self.__private_key

async def main():
    digital_signature = DigitalSignature()
    print("getting public values...")
    await digital_signature.get_public_values(9999)
    for _ in range(10):
        print(digital_signature.generate_keypair())

        
if __name__ == "__main__":
    asyncio.run(main())
