from typing import List

class SHA256:
    def __init__(self, helper: SHA256_utility):
        self.hash_values = helper.get_hash_constants()
        self.round_constants = helper.get_round_value_constants()

    def convert_string_to_binary(self, string: str = "") -> List[int] :
        pass

    def create_message_schedule(self, message: list = []) -> List[str]:
        pass

    def compression(self, message: list = []) -> List[str]:
        pass

    def modify_hash_values(self, values = []) -> List[str]:
        pass

    def create_final_hash(self) -> str:
        pass

    @staticmethod
    def generate_SHA256_hash(word: str) -> str:
        pass