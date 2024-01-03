
batchCounter = -1
batchCounter2 = 0

for i in range(20):
    batchCounter = (batchCounter + 1) % 10
    batchCounter2 = (batchCounter2 + 9) % 10
    print(batchCounter, batchCounter2)