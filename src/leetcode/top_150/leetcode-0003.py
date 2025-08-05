## ✅ 3 Longest Substring Without Repeating Characters
## https://leetcode.com/problems/longest-substring-without-repeating-characters/submissions/1699188270/

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        print("\n","="*10,'start', s)
        n = len(s)
        tracker: dict = {}
        for i in range(n):
            substr = s[i]
            tracker[substr] = len(substr)
            for j in range(i+1, n):
                if s[j] not in substr:
                    substr = s[i:j+1]
                    tracker[substr] = len(substr)
                    #print(tracker)
                else :
                    break
        print(tracker)
        return 0 if not tracker else max(tracker.values())

print(Solution().lengthOfLongestSubstring("abcabcbb"))
print(Solution().lengthOfLongestSubstring("bbbbb"))
print(Solution().lengthOfLongestSubstring("pwwkew"))
print(Solution().lengthOfLongestSubstring(" "))

"""


========== start abcabcbb
{'a': 1, 'ab': 2, 'abc': 3, 'b': 1, 'bc': 2, 'bca': 3, 'c': 1, 'ca': 2, 'cab': 3, 'cb': 2}
3

========== start bbbbb
{'b': 1}
1

========== start pwwkew
{'p': 1, 'pw': 2, 'w': 1, 'wk': 2, 'wke': 3, 'k': 1, 'ke': 2, 'kew': 3, 'e': 1, 'ew': 2}
3

========== start
{' ': 1}
1

"""
