import sys

# helper functions to convert hex numbers
def hx(n):
    return hex(int(n, 16))
def hX(n):
    return int(n,16)

# main loop
def __main__():
    point = 0           # pointer
    instruc = []        # list of instructions
    labels = {}         # points in the instructions to jump to
    stacks = {hex(x):[] for x in range(256)} # stacks 
    
    # variable for skipping
    skip = False
    
    # register
    r = hex(0)
    
    # getting instructions
    while i := input():
        instruc.append(i)
    
    while point < len(instruc):
        # ignore command if skip
        if not skip:
            i = instruc[point]
            
            # Program Control
            if i[0] == '0':
                if i[1] == '0':
                    labels[hx(i[2:])] = point
                if i[1] == '1':
                    point = labels[hx(i[2:])]
                if i[1] == '2':
                    temp = stacks[hx(i[2:4])]
                    point = stacks[temp]
                if i[1] == '3':
                    if stacks[hx(i[2:4])].pop() != hex(0): skip = True
                if i[1] == '4':
                    exit(f'exited with status code {i[2:]}')
            
            # I/O
            if i[0] == '1':
                if i[1] == '0':
                    stacks[hx(i[2:4])].append(hex(ord(sys.stdin.read(1))))
                # only the 10AB__ function is used in the attachment given by the problem
                
                if i[1] == '1':
                    stacks[hx(i[2:4])].append(hex(int(sys.stdin.read(1))))
                if i[1] == '2':
                    print(stacks[hx(i[2:4])].pop())
                if i[1] == '3':
                    print(chr(hX(stacks[hx(i[2:4])].pop())))
                if i[1] == '4':
                    print("".join([chr(hX(stacks[hx(i[2:4])].pop())) for _ in range(len(stacks[hx(i[2:4])]))]))
            
            # Math Operations
            if i[0] == '2':
                if i[1] == '0':
                    r = hx(i[2:])
                if i[1] == '1':
                    x = hX(stacks[hx(i[2:4])].pop())
                    y = hX(stacks[hx(i[2:4])].pop())
                    stacks[hx(i[2:4])].append(hex(x+y))
                if i[1] == '2':
                    x = hX(stacks[hx(i[2:4])].pop())
                    y = hX(stacks[hx(i[2:4])].pop())
                    stacks[hx(i[2:4])].append(hex(x-y))
                if i[1] == '3':
                    x = hX(stacks[hx(i[2:4])].pop())
                    y = hX(stacks[hx(i[2:4])].pop())
                    stacks[hx(i[2:4])].append(hex(x*y))
                if i[1] == '4':
                    x = hX(stacks[hx(i[2:4])].pop())
                    y = hX(stacks[hx(i[2:4])].pop())
                    stacks[hx(i[2:4])].append(hex(x//y))
                if i[1] == '5':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[2:4])].append(hex(x**y))
                if i[1] == '6':
                    r = hex(int(random(0,hx(i[2:]))))
            
            # Logic Control
            if i[0] == '3':
                if i[1] == '0':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex(int(x==y)))
                if i[1] == '1':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex(int(x>y)))
                if i[1] == '2':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex(int(x<y)))
                if i[1] == '3':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex(int(hX(x) or hX(y))))
                if i[1] == '4':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex(int(hX(x) and hX(y))))
                if i[1] == '5':
                    x = stacks[hx(i[2:4])].pop()
                    y = stacks[hx(i[2:4])].pop()
                    stacks[hx(i[4:6])].append(hex((int(hX(x)) + int(hX(y))) % 2))
                if i[1] == '6':
                    stacks[hx(i[2:4])].append(hex(int(r == hex(0))))
    
            # Other Commands
            if i[0] == '4':
                if i[1] == '0':
                    stacks[hx(i[2:4])].append(r)
                    r = hex(0)
                if i[1] == '1':
                    r = stacks[hx(i[2:4])].pop()
                if i[1] == '2':
                    r = stacks[hx(i[2:4])][-1]
                if i[1] == '3':
                    r = len(stacks[hx(i[2:4])])
        
        # reset skip
        else: skip = False
        # increment pointer
        point += 1

if __name__ == '__main__':
    __main__()
