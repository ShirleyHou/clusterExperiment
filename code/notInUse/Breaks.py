from htba import htb
import jenkspy
breaks = jenkspy.jenks_breaks(road_density, nb_class=4)
#breaks = [0]+htb(road_density)
#print(breaks)
def process(value):
    global breaks
    n = len(breaks)-1
    while(value<breaks[n] and n>0):
        n-=1
    return n
# processed = {}
# for i in road_density:
#     val = process(i)
#     print(i, val)
#     processed[val] = processed.get(val,0)+1
# print(processed)
# print(breaks)
# plt.figure(figsize = (10,8))
# hist = plt.hist(road_density, bins=100, align='left', color='g')
# for b in breaks:
#     plt.vlines(b, ymin=0, ymax = max(hist[0]))
# plt.show()


def minimum(grid):
    N = len(grid)
    v = set()

    def valid(i, j):
        return i >= 0 and i < N and j >= 0 and j < N and grid[i][j] != 1

    def find(x1, y1, x2, y2, h):

        if not valid(x1, y1) or not valid(x2, y2) or (x1, y1, x2, y2) in v:
            return float('inf')
        elif (x1 == N - 1 and y1 == N - 2 and x2 == N - 1 and y2 == N - 1):
            return 0
        v.add((x1, y1, x2, y2))

        options = []

        if h:  # horizontaol
            if valid(x2, y2 + 1):  # right
                options.append((x1, y1 + 1, x2, y2 + 1, h))

            if valid(x1 + 1, y1) and valid(x2 + 1, y2):
                options.append((x1 + 1, y1, x2 + 1, y2, h))

            if valid(x1 + 1, y1) and valid(x2 + 1, y2):
                nx1 = x1;
                ny1 = y1;
                nx2 = x2 + 1
                ny2 = y2 - 1;
                nh = False
                options.append((nx1, ny1, nx2, ny2, nh))
        else:  # vertical
            if (valid(x1, y1 + 1) and valid(x2, y2 + 1)):  # right
                options.append((x1, y1 + 1, x2, y2 + 1, h))
            if (valid(x2 + 1, y2))  # down
                options.append((x1 + 1, y1, x2 + 1, y2, h))
            if (valid(x1, y1 + 1) and valid(x2, y2 + 1)):
                nx1 = x1;
                ny1 = y1;
                nx2 = x2 - 1
                ny2 = y2 + 1;
                nh = True
                options.append((nx1, ny1, nx2, ny2, nh))
        min_find = float('inf')
        for i in options:
            min_find = min(min_find, find(i[0], i[1], i[2], i[3], i[4]))
        return min_find + 1

    res = find(0, 0, 0, 1, True)
    if res == float('inf'):
        return -1
    else:
        return res


print(minimum([[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
               [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0], [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]]
              ))