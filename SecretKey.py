n, m = map(int, input().split())

# Read grid
grid = []
for _ in range(n):
    grid.append(input().split())

# Length of secret key
T = int(input())

# Number of clues
I = int(input())

# blocked[t] = list of rectangles where position at time t cannot be
blocked = [[] for _ in range(T + 1)]

for _ in range(I):
    t = int(input())
    x1, y1, x2, y2 = map(int, input().split())

    # Convert to 0-based indexing
    x1 -= 1
    y1 -= 1
    x2 -= 1
    y2 -= 1

    blocked[t].append((x1, y1, x2, y2))


def is_allowed(r, c, time):
    """
    Returns True if cell (r,c) is not inside
    any forbidden rectangle for this time.
    """

    for x1, y1, x2, y2 in blocked[time]:
        if x1 <= r <= x2 and y1 <= c <= y2:
            return False

    return True


# Find all cells that are allowed at every time
allowed = [[] for _ in range(T + 1)]

for time in range(1, T + 1):
    for r in range(n):
        for c in range(m):
            if is_allowed(r, c, time):
                allowed[time].append((r, c))

    # No possible cell at this time
    if not allowed[time]:
        print("Not enough clues")
        exit()


# Four possible movements
directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]


# Store unique possible secret keys
answers = set()


def dfs(time, r, c, visited, word):
    # If complete key is formed
    if time == T:
        answers.add(word)

        # More than one possible key means answer is not unique
        return

    next_time = time + 1

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        # Outside grid
        if nr < 0 or nr >= n or nc < 0 or nc >= m:
            continue

        # Cannot visit same cell again
        if (nr, nc) in visited:
            continue

        # Cell must satisfy clues for next time
        if not is_allowed(nr, nc, next_time):
            continue

        visited.add((nr, nc))

        dfs(
            next_time,
            nr,
            nc,
            visited,
            word + grid[nr][nc]
        )

        visited.remove((nr, nc))

        # We only need to know whether there is more than one answer
        if len(answers) > 1:
            return


# Start from every allowed cell at time 1
for r, c in allowed[1]:
    visited = {(r, c)}

    dfs(
        1,
        r,
        c,
        visited,
        grid[r][c]
    )

    if len(answers) > 1:
        break


# Final result
if len(answers) == 1:
    print(next(iter(answers)))
else:
    print("Not enough clues")