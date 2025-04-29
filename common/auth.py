import time
import os
import jwt


class AuthToken:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.strip()
        self.algorithms = "HS256"

    def generate(self, data: dict, expired_seconds: int = 300) -> str:
        payload = data;
        payload["exp"] = int(time.time()) + expired_seconds
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithms);

    def retrieve(self, token: str):
        payload = jwt.decode(token.strip(), self.secret_key, algorithms=[self.algorithms])
        del payload["exp"]
        return payload

    def generate_auth_headers(self, data: dict, expired_seconds: int = 300) -> str:
        payload = data;
        payload["exp"] = int(time.time()) + expired_seconds

        gateway_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.generate(data, expired_seconds)}"
        }

        return gateway_headers;
