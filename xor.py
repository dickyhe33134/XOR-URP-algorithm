from pathlib import Path
import sys
from functools import lru_cache

if len(sys.argv) != 3:
    print("Usage: python xor.py <input_file.txt> <output_file.txt>")
    print("Example: python xor.py f.txt result.txt")
    sys.exit(1)

input_file = sys.argv[1]   # First argument after xor.py
output_file = sys.argv[2]  # Second argument


inBase_folder='testcase'  #folder for input testcase
outBase_folder='testcaseoutput'  #opp folder
def read_text_file(filename):
    file_path = Path(inBase_folder) / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None


text = read_text_file(input_file) #read

if text is None or len(text) < 4:
    print(f"Failed to read or parse {input_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ERROR: Could not read input file\n")
    sys.exit(1)

# Safe parsing
try:
    vars_num = int(text[0])
    F_cubes = int(text[1])
    length = vars_num

    F = []
    for i in range(F_cubes):
        row = [int(char) for char in text[2 + i] if char.isdigit()]
        F.append(row)

    G_cubes = int(text[2 + F_cubes])
    G = []
    for i in range(G_cubes):
        row = [int(char) for char in text[3 + F_cubes + i] if char.isdigit()]
        G.append(row)

except Exception as e:
    print(f"Parsing error in {input_file}: {e}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ERROR: Parsing failed\n")
    sys.exit(1)
## G and F cubelists are formed

#use irucache to memorize same takein to speedup
@lru_cache(maxsize=None)
def cofactor(M_tuple,var,polarity):
    M = [list(cube) for cube in M_tuple]
    length=len(M)
    for i in range(length):
        if M[i] != [] :
            if M[i][var]==polarity:
                M[i][var]=2
            elif M[i][var]==(1-polarity):
                M[i]=[]
        else :
            continue
    return tuple(tuple(cube) for cube in M)
## finish defying cofactor

def intersact(M, P):
    if not M or not P:
        return []        
    out = []
    for p_cube in P:
        for m_cube in M:
            line = [2] * length ##faster preload
            conflict = False            
            for i in range(length):
                m = m_cube[i]
                p = p_cube[i]
                if m == 2:
                    line[i] = p
                elif p == 2 or m == p:
                    line[i] = m
                else:
                    conflict = True
                    break                    
            if not conflict:
                out.append(line)                
    return out

def union(M, P):
    merged = set(tuple(cube) for cube in M) | set(tuple(cube) for cube in P)
    return [list(cube) for cube in merged]

def duplicate(K):
    for x in K:
        seen=[]
        duplicate=[]
        if x not in seen:
            seen.append(x)
        else:
            duplicate.append(x)
    return [seen,duplicate]     

def split_var_cube(var, polarity):
    cube = [2] * length
    cube[var] = polarity
    return cube

@lru_cache(maxsize=None)
def complement(M_tuple,depth=0):
    M=[list(cube) for cube in M_tuple]
    ##print(f"Depth {depth}: Entering complement with M = {M}")
    if [[]]*len(M) == M:                                   
        return [length * [2]]
    
    # Check if it contains the universal cube
    universal = [2] * length
    if universal in M:
        return []

#   Find the best split var
    c0_counts = [0] * length
    c1_counts = [0] * length

    for c in M:
        if not c:
            continue
        for v in range(length):
            if c[v] == 0:
                c0_counts[v] += 1
            elif c[v] == 1:
                c1_counts[v] += 1

    best_var = 0
    best_score = -1
    best_score_balance = float('inf') 
    
    for v in range(length):
        score1 = c0_counts[v] + c1_counts[v]
        score2 = abs(c0_counts[v] - c1_counts[v])
        
        if score1 > best_score:
            best_score = score1
            best_score_balance = score2
            best_var = v
        elif score1 == best_score:
            if score2 < best_score_balance:
                best_score_balance = score2
                best_var = v 

#   find cof
    cof_1=cofactor(tuple(tuple(c) for c in M),best_var,1)
    cof_0=cofactor(tuple(tuple(c) for c in M),best_var,0)

#   input compl    
    if len(cof_1)>=1:
        cof_1=complement(cof_1,depth+1)
    if len(cof_0)>=1:
        cof_0=complement(cof_0,depth+1)

#   left right   
    left=cof_1
    if left==[length*[2]]:
        left=[split_var_cube(best_var,1)]
    elif left==[]:
        left=[]
    else:
        left=intersact(left,[split_var_cube(best_var,1)])

    right=cof_0
    if right==[length*[2]]:
        right=[split_var_cube(best_var,0)]
    elif right==[]:
        right=[]
    else:
        right=intersact(right,[split_var_cube(best_var,0)])
    ##print("DEBUG - left  before intersact:", left)
    ##print("DEBUG - right before intersact:", right)
    result= union(left,right)
    ##print("union result is:",result)
    return result

# Compute complements
F_comp = complement(tuple(tuple(c) for c in F))
G_comp = complement(tuple(tuple(c) for c in G))

# F XOR G = (F · ~G) + (~F · G)
term1 = intersact(F, G_comp)
term2 = intersact(F_comp, G)
xor_result = union(term1, term2)

# Output
def output_files(file):
    file_path=Path(outBase_folder)/file
    ##print("Final XOR result:", xor_result)
    with open(file_path, 'w', encoding='utf-8') as f:
        if xor_result!=[]:
            f.write('variable length: '+str(len(xor_result[0]))+'\n')
            f.write('cube length: '+str(len(xor_result))+'\n')
            f.write('XOR output cubelist: \n')
            for cube in xor_result:
                f.write(' '.join(map(str, cube)) + '\n')
        else:
            f.write('empty list, they are identical.\n'+str(xor_result))
    print(f"Success! Result written to {output_file}")
output_files(output_file)
            
        
