from SHA256_utils import SHA256_utility_helper
from SHA import SHA256

root_string = "hello world"
helper = SHA256_utility_helper()
hash_value = SHA256.generate_SHA256_hash(root_string)
print(hash_value)