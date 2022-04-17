# # Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
#
#
# class Solution:
#     def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
#         a = str(l1.val).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
#
#         b = str(l2.val).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
#         c = str(int(a) + int(b))
#         return list(c)[::-1]
#
#
# Solutions = Solution()
# a = Solutions.addTwoNumbers(l1=ListNode([2, 4, 3]), l2=ListNode([5, 6, 4]))
import gmpy2
import binascii

p = 282164587459512124844245113950593348271
q = 366669102002966856876605669837014229419
c = 0xad939ff59f6e70bcbfad406f2494993757eee98b91bc244184a377520d06fc35
n = p*q
e = 65537
d = gmpy2.invert(e, (p - 1) * (q - 1))
# d = gmpy2.invert(e,n) # 求逆元，de = 1 mod n
m = gmpy2.powmod(c, d, n)
print(binascii.unhexlify(hex(m)[2:]).decode(encoding="utf-8"))
print(type(binascii.unhexlify(hex(m)[2:])))
