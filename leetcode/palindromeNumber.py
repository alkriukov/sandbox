def isPalindrome(x: int) -> bool:
    result = False
    if x >= 0:
        digits = [int(d) for d in str(x)]
        length = len(digits)
        for i in range(length // 2):
            if digits[i] != digits[length - 1 - i]:
                break
        else:
            result = True
    return result

def test_isPalindrome():
    assert isPalindrome(121)
    assert isPalindrome(12321)
    assert isPalindrome(11)
    assert isPalindrome(9)
    assert isPalindrome(0)
    assert not isPalindrome(-121)
    assert not isPalindrome(10)

isPalindrome(0)

"""
Given an integer x, return true if x is a palindrome, and false otherwise.

Example 1:
    Input: x = 121
    Output: true
    Explanation: 121 reads as 121 from left to right and from right to left.
Example 2:
    Input: x = -121
    Output: false
    Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
Example 3:
    Input: x = 10
    Output: false
    Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
Constraints:
    -2**31 <= x <= 2**31 - 1
"""