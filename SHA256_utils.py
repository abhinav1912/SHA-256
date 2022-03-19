from typing import List

class SHA256_utility_helper:
    def __init__(self):
        pass

    def get_hash_constants(self) -> tuple:
        return tuple(self.initialize_constants([
            '0x6a09e667',
            '0xbb67ae85',
            '0x3c6ef372',
            '0xa54ff53a',
            '0x510e527f',
            '0x9b05688c',
            '0x1f83d9ab',
            '0x5be0cd19'
        ]))

    def get_round_value_constants(self) -> List[str]:
        return self.initialize_constants([
            '0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5',
            '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5',
            '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3',
            '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174',
            '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc',
            '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da',
            '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7',
            '0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967',
            '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13',
            '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85',
            '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3',
            '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070',
            '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5',
            '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3',
            '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208',
            '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2'
        ])

    def initialize_constants(self, values):
        binaries = [bin(int(v, 16))[2:] for v in values]
        words = []
        for binary in binaries:
            word = []
            for b in binary:
                word.append(int(b))
            words.append(self.fillZeros(word, 32, 'BE'))
        return words
    
    def fillZeros(self, bits, length=8, endian='LE'):
        l = len(bits)
        if endian == 'LE':
            for i in range(l, length):
                bits.append(0)
        else: 
            while l < length:
                bits.insert(0, 0)
                l = len(bits)
        return bits
    
    def convert_string_to_int_array(self, string: str = "") -> List[int]:
        int_array = []
        for i in string:
            int_array.append(ord(i))
        return int_array
    
    def convert_int_to_binary(self, number: int, length: int = 8) -> str:
        binary = bin(number)[2:]
        return binary.zfill(length)
    
    def binary_to_hexadecimal(self, value):
        value = ''.join([str(x) for x in value])
        binaries = []
        for d in range(0, len(value), 4):
            binaries.append('0b' + value[d:d+4])
        hexes = ''
        for b in binaries:
            hexes += hex(int(b ,2))[2:]
        return hexes
    
    def split_array_in_chunks(self, array: List[int], chunk_size: int = 64) -> List[int]:
        chunked_array = []
        for i in range(0, len(array), chunk_size):
            chunked_array.append(array[i:i+chunk_size])
        return chunked_array
    
    def rotate_right(self, array: List[int], shift: int) -> List[int]:
        return array[-shift:] + array[:-shift]
    
    def shift_right(self, array: List[int], shift: int) -> List[int]:
        return shift*[0] + array[:-shift]

    def add(self, i, j):
        #takes to lists of binaries and adds them
        length = len(i)
        sums = list(range(length))
        #initial input needs an carry over bit as 0
        c = 0
        for x in range(length-1,-1,-1):
            #add the inout bits with a double xor gate
            sums[x] = self.xorxor(i[x], j[x], c)
            #carry over bit is equal the most represented, e.g., output = 0,1,0 
            # then 0 is the carry over bit
            c = self.maj(i[x], j[x], c)
        #returns list of bits 
        return sums

    #truth condition is integer 1
    def isTrue(self, x): return x == 1

    #simple if 
    def if_(self, i, y, z): return y if self.isTrue(i) else z

    #and - both arguments need to be true
    def and_(self, i, j): return self.if_(i, j, 0)
    def AND(self, i, j): return [self.and_(ia, ja) for ia, ja in zip(i,j)] 

    #simply negates argument
    def not_(self, i): return self.if_(i, 0, 1)
    def NOT(self, i): return [self.not_(x) for x in i]

    #retrun true if either i or j is true but not both at the same time
    def xor(self, i, j): return self.if_(i, self.not_(j), j)
    def XOR(self, i, j): return [self.xor(ia, ja) for ia, ja in zip(i, j)]

    #if number of truth values is odd then return true
    def xorxor(self, i, j, l): return self.xor(i, self.xor(j, l))
    def XORXOR(self, i, j, l): return [self.xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]

    #get the majority of results, i.e., if 2 or more of three values are the same 
    def maj(self, i,j,k): return max([i,j,], key=[i,j,k].count)