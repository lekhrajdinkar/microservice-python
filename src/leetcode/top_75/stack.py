from typing import List


class Solution:

    # 2390 https://leetcode.com/problems/removing-stars-from-a-string/?envType=study-plan-v2&envId=leetcode-75
    def removeStars(self, s: str) -> str:
        print('\n--- removeStars ---', s)
        stack = []
        for c in s:
            if c != '*' :
                stack.append(c)
            elif c == '*' and stack:
                stack.pop()

        return ''.join(stack)

    # https://leetcode.com/problems/asteroid-collision/?envType=study-plan-v2&envId=leetcode-75
    # 735 asteroid-collision
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        print('\n=== asteroidCollision ===', asteroids)
        stk = []

        def explode(stk):
            print('current : ', stk)
            i=len(stk)-1
            ## same direction : no explosion
            if ((stk[i-1] > 0 and stk[i] > 0)  ## >> >>
                    or (stk[i-1] < 0 and stk[i] < 0)  # << <<
                    or (stk[i-1] < 0 and stk[i] > 0)): ## <<  >>
                print('skip - same direction : ', stk)
                #pass
            ## explosion  >> <<
            elif abs(stk[i-1]) == abs(stk[i]):  ## same size
                stk.pop()
                stk.pop()
            elif abs(stk[i-1]) > abs(stk[i]):   ## small
                stk.pop()
                #print ('pop after explosion : ', stk)
            elif abs(stk[i-1]) < abs(stk[i]):    ## big size
                keep=stk.pop()
                stk.pop()
                stk.append(keep)
                #print ('pop after explosion : ', stk)
                explode(stk)


        for  a in asteroids:
            if not stk:
                stk.append(a)
            else:
                stk.append(a)
                explode(stk)  # oppsite direction

        return stk

    ## https://leetcode.com/problems/decode-string/description/?envType=study-plan-v2&envId=leetcode-75
    ## 394 Decode String
    def decodeString(self, s: str) -> str:
            print('\n394=== decodeString ===', s)
            stack = []
            for c in s:
                if c == ']' and stack:
                    chars = ''
                    while True and stack:
                        nxt = stack.pop()
                        if nxt == '[': break
                        else: chars = nxt + chars

                    product = ''
                    while True and stack:
                        nxt = stack.pop()
                        if nxt.isalpha() or nxt == '[':
                            stack.append(nxt)
                            break
                        elif nxt.isdigit():
                            product += nxt
                    product = product[::-1]

                    print(f"🔹encountered ']' | {product} X {chars} ")
                    stack.append(int(product) * chars)
                else:
                    stack.append(c)
                print(stack)

            return ''.join(stack)

# ===================

print('✔️2390', Solution().removeStars("leet**cod*e"))
print('✔️2390', Solution().removeStars("erase*****"))

print('✔️735', Solution().asteroidCollision([5,10,-5]))
print('✔️735', Solution().asteroidCollision([8,-8]))
print('✔️735', Solution().asteroidCollision([10, 2, -5]))

print('✔️394', Solution().decodeString("3[a]2[bc]"))
print('✔️394', Solution().decodeString("3[a2[c]]"))
print('✔️394', Solution().decodeString("2[ab3[cd]]4[xy]"))
#print('✔️394', Solution().decodeString("10[leetcode]"))
#print('❌394', Solution().decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef"))

