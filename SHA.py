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
            binary_array += [int(bit) for bit in self.helper.convert_int_to_binary(i)]
        return binary_array

    def preprocess_binary_array(self, array: List[int]) -> List[int]:
        '''
        Convert given string to a binary form with length divisible by 512
        Last 64 bits should be original message length in binary form
        '''
        length = len(array)
        message_len = [int(bit) for bit in self.helper.convert_int_to_binary(length, 64)]
        array.append(1)
        if length < 448:
            array += [0]*(448-length-1)
            array += message_len
        elif 448 <= length <= 512:
            array += [0]*(1024-length-1)
            array[-64:] = message_len
        else:
            while len(array) % 512:
                array.append(0)
            array[-64:] = message_len
        return array

    def create_message_schedule(self, message: list = []) -> List[int]:
        for chunk in message:
            array = self.helper.split_array_in_chunks(chunk, 32)
            for i in range(48):
                array.append([0 for j in range(32)])
            for i in range(16, 64):
                s0 = self.helper.XORXOR(self.helper.rotate_right(array[i-15], 7), self.helper.rotate_right(array[i-15], 18), self.helper.shift_right(array[i-15], 3) ) 
                s1 = self.helper.XORXOR(self.helper.rotate_right(array[i-2], 17), self.helper.rotate_right(array[i-2], 19), self.helper.shift_right(array[i-2], 10))
                array[i] = self.helper.add(self.helper.add(self.helper.add(array[i-16], s0), array[i-7]), s1)
        return array

    def compression(self, message: list = []) -> tuple:
        a,b,c,d,e,f,g,h = self.hash_values
        for j in range(64):
            S1 = self.helper.XORXOR(self.helper.rotate_right(e, 6), self.helper.rotate_right(e, 11), self.helper.rotate_right(e, 25) )
            ch = self.helper.XOR(self.helper.AND(e, f), self.helper.AND(self.helper.NOT(e), g))
            temp1 = self.helper.add(self.helper.add(self.helper.add(self.helper.add(h, S1), ch), self.round_constants[j]), message[j])
            S0 = self.helper.XORXOR(self.helper.rotate_right(a, 2), self.helper.rotate_right(a, 13), self.helper.rotate_right(a, 22))
            m = self.helper.XORXOR(self.helper.AND(a, b), self.helper.AND(a, c), self.helper.AND(b, c))
            temp2 = self.helper.add(S0, m)
            h = g
            g = f
            f = e
            e = self.helper.add(d, temp1)
            d = c
            c = b
            b = a
            a = self.helper.add(temp1, temp2)
        return (a,b,c,d,e,f,g,h)

    def modify_hash_values(self, values = []) -> List[str]:
        a,b,c,d,e,f,g,h = values
        h0,h1,h2,h3,h4,h5,h6,h7 = self.hash_values
        h0 = self.helper.add(h0, a)
        h1 = self.helper.add(h1, b)
        h2 = self.helper.add(h2, c)
        h3 = self.helper.add(h3, d)
        h4 = self.helper.add(h4, e)
        h5 = self.helper.add(h5, f)
        h6 = self.helper.add(h6, g)
        h7 = self.helper.add(h7, h)

        return [h0,h1,h2,h3,h4,h5,h6,h7]

    def create_final_hash(self, values) -> str:
        digest = ''
        for val in values:
            digest += self.helper.binary_to_hexadecimal(val)
        return digest

    def get_SHA256_hash(self, word: str) -> str:
        binary_array = self.convert_string_to_binary(word)
        preprocessed_array = self.preprocess_binary_array(binary_array)
        chunks = self.helper.split_array_in_chunks(preprocessed_array, 512)
        message = self.create_message_schedule(chunks)
        compressed_message = self.compression(message)
        modified_values = self.modify_hash_values(compressed_message)
        hash = self.create_final_hash(modified_values)
        return hash