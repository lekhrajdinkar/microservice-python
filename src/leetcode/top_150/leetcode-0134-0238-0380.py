# 380 https://leetcode.com/problems/insert-delete-getrandom-o1/?envType=study-plan-v2&envId=top-interview-150
class RandomizedSet:

    def __init__(self):
        self.data = []

    def insert(self, val: int) -> bool:
        #if self.data.index(val) == -1:
        if val not in self.data:
            self.data.append(val)
            return True
        else:
            return False

    def remove(self, val: int) -> bool:
        if val in self.data:
            self.data.remove(val)
            return True
        else:
            return False

    def getRandom(self) -> int:
        if self.data is not None:
            import random
            r = random.randint(0, len(self.data)-1)
            return self.data[r]
        else:
            return None

# Your RandomizedSet object will be instantiated and called as such:
obj = RandomizedSet()
print(obj.insert(1))
print(obj.insert(10))
print(obj.insert(100))
print(obj.remove(2))
print(obj.remove(2))
print(obj.getRandom())

# with dict
class RandomizedSet2:

    def __init__(self):
        self.data = {}

    def insert(self, val: int) -> bool:
        if val not in self.data.keys():
            self.data[val]=None
            return True
        else:
            return False

    def remove(self, val: int) -> bool:
        if val in self.data.keys():
            del self.data[val]
            return True
        else:
            return False

    def getRandom(self) -> int:
        if self.data is not None:
            import random
            r = random.randint(0, len(self.data.keys())-1)
            return list(self.data.keys())[r]
        else:
            return None

# 238 https://leetcode.com/problems/product-of-array-except-self/description/?envType=study-plan-v2&envId=top-interview-150
class Solution238:
    def productExceptSelf(self, nums):
        result = []
        n = len(nums)
        for i in range(n):
            temp =1
            for j in range(n):
                if i != j:
                    temp *= nums[j]
            result.append(temp)
        return result

    def productExceptSelf_2(self, nums):
        n = len(nums)
        res = [1] * n,
        for i in range(n):
            res[i] *= nums[i]

        return res

print(Solution238().productExceptSelf([1, 2, 3, 4, 5]))
print(Solution238().productExceptSelf([1,2,3,4]))
print(Solution238().productExceptSelf([0,0]))

class Solution134:
    def canCompleteCircuit(self, gas, cost) -> int:
        n = len(gas)
        print('\ngas:',gas)
        print('cost:',cost)
        for start in range(n):
            tank = gas[start]
            if tank == 0:
                continue
            print(f"\nstarting from station: {start} with tank:{tank} ")
            for j in range(n):
                idx = (start + j) % n
                next_s = (idx) % n
                print(f"\tCan further travel to next station?? travel cost {cost[next_s]} but tank:{tank} ")
                if tank < cost[next_s]:
                    print("🔻skip")
                    break
                elif j == n - 1:
                    return start

                # travelled to next
                tank = tank - cost[idx] + gas[(next_s+1)%n]
                print(f"\ttravelled to next station:{(next_s+1)%n}, now tank:{tank} ( -- travel-cost {cost[idx]} , ++ filled {gas[(next_s+1)%n]} ")


        return -1

#print(Solution134().canCompleteCircuit([2,3,4], [3,4,3]))
print(Solution134().canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2]))