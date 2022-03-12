from typing import List
from SHA256_utils import SHA256_utility_helper

class SHA256:
    @staticmethod
    def generate_SHA256_hash(word: str) -> str:
        hash_generator = SHA256_Generator()
        return hash_generator.get_SHA256_hash(word)

class SHA256_Generator:
    def __init__(self, helper: SHA256_utility_helper = SHA256_utility_helper()):
        self.hash_values = helper.get_hash_constants()
        self.round_constants = helper.get_round_value_constants()
        self.helper = helper
    
    def convert_string_to_binary(self, string: str = "") -> List[int]:
        '''
        Convert given string to a binary array
        '''
        int_array = self.helper.convert_string_to_int_array(string)
        size = len(int_array)
        binary_array = []
        for i in int_array:
            binary_array.append(self.helper.convert_int_to_binary(i))
        print(binary_array)

    def preprocess_binary_array(self, array: List[int]) -> List[int]:
        '''
        Convert given string to a binary form with length divisible by 512
        Last 64 bits should be original message length in binary form
        '''
        pass

    def create_message_schedule(self, message: list = []) -> List[str]:
        pass

    def compression(self, message: list = []) -> List[str]:
        pass

    def modify_hash_values(self, values = []) -> List[str]:
        pass

    def create_final_hash(self) -> str:
        pass

    def get_SHA256_hash(self, word: str) -> str:
        binary_array = self.convert_string_to_binary(word)