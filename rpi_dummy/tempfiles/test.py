ctr=0
blues=[]
reds=[]
with open('EDSA_test','r') as f:
    for line in f:
        ctr+=1
        coords = line.strip().split(' ')
        if ctr < 43:
            blues.append(coords)
        else:
            reds.append(coords)
    f.close()

with open('coords.js','w') as f:
    f.write('var blues='+str(blues))
    f.write('\n')
    f.write('var reds='+str(reds))


