def reverse_number(num):
  # Reverse the number
  reverse = str(num)[::-1]
  # Return the number
  return int(reverse)

## Example usage:
print(reverse_number(1223)) # Output: 3221
print(reverse_number(987654321)) # Output: 123456789

#Response 1 is better because it comes closer to satisfying the requirement of writing the integer in
# reverse than Response 2. Once the error is corrected by converting the num to a string, the function
# will work correctly. In Response 2, the AI seems to have used the wrong meaning of "opposite;"
# it interpreted it to mean negative rather than what the user wanted, namely the digits written in the
# opposite order.