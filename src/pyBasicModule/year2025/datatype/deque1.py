from collections import deque

dq = deque([1, 2, 3])
dq.append(4)
dq.appendleft(0)
print("📥 After append:", dq)

dq.pop()
dq.popleft()
print("📤 After pops:", dq)

dq.rotate(1)
print("🔄 Rotate right:", dq)

dq.rotate(-1)
print("🔄 Rotate left:", dq)


"""
| 📦 Function     | 🧾 Syntax          | 💡 Description             |
| --------------- | ------------------ | -------------------------- |
| `append(x)`     | `dq.append(4)`     | Add to right               |
| `appendleft(x)` | `dq.appendleft(0)` | Add to left                |
| `pop()`         | `dq.pop()`         | Remove from right          |
| `popleft()`     | `dq.popleft()`     | Remove from left           |
| `rotate(n)`     | `dq.rotate(1)`     | Rotate right (`-n` = left) |

✅ Tip: Use deque for queues, stacks, sliding windows, and O(1) pop from both ends.

"""