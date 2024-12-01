FILE_NAME = "example"
FILE_NAME = "input"



with open(FILE_NAME) as file:
    cnt = 0
    cnt2 = 0
    for line in file:
        #ranges = tuple( for s in line.strip().split(","))
        r1,r2 = tuple(tuple(int(a) for a in s.split("-")) for s in line.strip().split(","))
        
        # r1 is always "smaller"
        if (r1[0] > r2[0] or (r1[0] == r2[0] and r1[1] > r2[1])):
            r1,r2 = r2,r1
        
        print(r1[0], r2[0])
        
        if ((r2[0] == r1[0] and r1[1] <= r2[1]) or
            (r1[0] <= r2[0] <= r1[1] and r1[0] <= r2[1] <= r1[1])):
            cnt += 1
            
            
        if r1[1] >= r2[0]:
            cnt2 += 1
        
    #chunks = sorted(sum(int(n) for n in g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    print("Part One: In how many assignment pairs does one range fully contain the other?")
    print(cnt)
    
    print()
    print("Part Two: In how many assignment pairs do the ranges overlap?")
    print(cnt2)
