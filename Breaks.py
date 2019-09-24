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
