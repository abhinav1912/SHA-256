from SHA256_utils import SHA256_utility_helper
from SHA import SHA256

test_helper = SHA256_utility_helper()
test_object = SHA256.generate_SHA256_hash("hello world")
print(test_object)