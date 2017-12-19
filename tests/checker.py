inp = open("input.txt","r")
outp = open("output.txt","r")

inp.readline()
width = int(inp.readline())
lizard_cnt = int(inp.readline())


inpgrid = []

# read input and check sizes
for _ in range(width):
  inpgrid.append(list(inp.readline().strip()))
  if(len(inpgrid[-1]) != width):
    exit("input width did not match")

if(len(inpgrid) != width):
  exit("input height did not match")


res = outp.readline()
if(res == "FAIL"):
  exit("says fail")


print "says ok"

# read output grid and check sizes
outpgrid = []
for line in outp:
  outpgrid.append(list(line[:-1]))
  if(len(outpgrid[-1]) != width):
    exit("output width did not match")

if(len(outpgrid) != width):
  exit("output height did not match")

# tree location check
i = 0
while i<width:
  j=0
  while j < width:
    if((inpgrid[i][j] == '2' and outpgrid[i][j] != '2') or (inpgrid[i][j] != '2' and outpgrid[i][j] == '2')):
      exit("missing or extra tree in output " + str((i,j)))
    j+=1
  i+=1


# lizard count check
lc = 0
lizard_locs = []
i = 0
while(i<width):
  j = 0
  while(j<width):
    if(outpgrid[i][j] == '1'):
      lc+=1
      lizard_locs.append((i,j))
    j+=1
  i+=1

if(lc != lizard_cnt):
  exit("lizard count did not match")

#check if there is anything different than 0, 1 or 2
for i in outpgrid:
  for j in i:
    if(j!= '0' and j!='1' and j!='2'):
      exit("unexpected character in output")


# checks if lizard at (i,j) attacks lizard at (k,p)
def attacks(grid, (i,j), (k,p)):
  if(grid[i][j] != '1'):
    return False
  if(grid[k][p] != '1'):
    return False

  #same row
  if(i==k):
    MIN = min(j,p)
    MAX = max(j,p)
    is_good = False

    while(MIN<=MAX):
      if(grid[i][MIN] == '2'):
        is_good = True
      MIN+=1

    return not is_good


  #same column
  if(j==p):
    MIN = min(i,k)
    MAX = max(i,k)
    is_good = False
    while(MIN<=MAX):
      if(grid[MIN][j] == '2'):
        is_good = True
      MIN+=1

    return not is_good


  #diagonal with slope 1
  if(abs(float((k-i))/(p-j) - 1) < 0.00000001):
    MINx = min(i,k)
    MINy = min(p,j)
    MAXy = max(p,j)
    is_good = False
    while(MINy <= MAXy):
      if(grid[MINx][MINy] == '2'):
        is_good = True;
      MINy+=1
      MINx+=1

    return not is_good

  #diagonal with slope -1
  if(abs(float((k-i))/(p-j) + 1) < 0.00000001):
    MINx = min(i,k)
    MAXy = max(j,p)
    MAXx = max(i,k)
    is_good = False
    while(MINx<=MAXx):
      if(grid[MINx][MAXy] == '2'):
        is_good = True
      MINx+=1
      MAXy-=1

    return not is_good

  return False

#check if lizards attack each other
for (i,j) in lizard_locs:
  for (k,p) in lizard_locs:
    if(i == k and j == p):
      continue
    if(attacks(outpgrid, (i,j), (k,p))):
      exit("attack!: " + str((i,j)) + " " + str((k,p)))


print ("you are good")

inp.close()
outp.close()
