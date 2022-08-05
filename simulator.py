from sys import flags

#utility func to convert decimal to 8bit binary
# def dec28(a):
#    print(format(a,'08b'), end=' ')
#    return

memory=[]
with open("/home/mo/Desktop/CO_Assignment/instructions.txt",'r') as f:
    memory = f.readlines()
regs=[0000000000000000,0000000000000000,0000000000000000,0000000000000000,0000000000000000,0000000000000000,0000000000000000,0000000000000000]

#FLAGS
regs[7]="0000000000000000"

# def reg_display(a):
#   for i in range(7):
#     print(dec28(regs[i]), end=' ')
  

def flag_reset(flag_):

  flag_[0:-1] = "0000000000000000"
  return
  
def set_flag_overflow(flag_):
  
  flag_[-4]='1'
  return

def set_lt_overflow(flag_):

  flag_[-3] = '1'
  return

def set_gt_overflow(flag_):

  flag_[-2]='1'
  return

def set_equal_overflow(flag_reg):

  flag_reg[-1]='1'
  return
  

def add(a,b,c):
  regs[c]=regs[a] + regs[b]
  if(regs[c]>2**16-1):
    set_flag_overflow(regs[7])

def sub(a,b,c):
  regs[c]=regs[a] - regs[b]
  if(regs[c]>1111111 or regs[c]<0):
    set_flag_overflow(regs[7])

def movB(a,b):
  regs[a]=b

def movC(a,b):
  if b==7:
    regs[a]==int(regs[b],2)
  else:
    regs[b]=regs[a]

def ld(a,b):
  regs[a]=memory[b]

def st(a,b):
  memory[b]=regs[a]

def mul(a,b,c):
  regs[c]=regs[a] * regs[b]
  
def div(a,b):
  regs[0]=a//b
  regs[1]=a%b

def rs(a,b):
  regs[a]=regs[a] // (2**b)

def ls(a,b):
  regs[a]=regs[a] * (2**b)

def xor(a,b,c):
  regs[c]=regs[a] ^ regs[b]   

def oor(a,b,c):
  regs[c]=regs[a] | regs[b]

def andd(a,b,c):
  regs[c]=regs[a] & regs[b]

def nott(a,b):
  regs[b]= ~regs[a]

def cmpp(a,b):
  if regs[a]>regs[b]:
    set_gt_overflow(regs[7])
  elif regs[a]<regs[b]:
    set_lt_overflow(regs[7])
  elif regs[a]==regs[b]:
    set_equal_overflow(regs[7])


d={"10000":"A","10001":"A","10010":"B","10011":"C","10100":"D","10101":"D","10110":"A","10111":"C","11000":"B","11001":"B","11010":"A","11011":"A","11100":"A","11101":"C","11110":"C","11111":"E","01100":"E","01101":"E","01111":"E","01010":"F"}
dfunc={"10000":add,"10001":sub,"10010":movB,"10011":movC,"10100":ld,"10101":st,"10110":mul,"10111":div,"11000":rs,"11001":ls,"11010":xor,"11011":oor,"11100":andd,"11101":nott,"11110":cmpp}

h=len(memory)
ratio=["10001","10000","10110","11110"]
for i in range(0,h):
    opcode=memory[i][:5]
    if d[opcode]=="A":
      a = int(memory[i][7:10],2)  
      b = int(memory[i][10:13],2)
      c = int(memory[i][13:],2)
      dfunc[opcode](a,b,c)

    elif d[opcode]=="B":
      a=int(memory[i][5:8],2)
      b=int(memory[i][8:],2)
      dfunc[opcode](a,b)

    elif d[opcode]=="C":
      a = int(memory[i][10:13],2)
      b = int(memory[i][13:],2)
      dfunc[opcode](a,b)

    elif d[opcode]=="D":
      a=int(memory[i][5:8],2)
      b=int(memory[i][8:],2)
      dfunc(opcode)(a,b)

    elif d[opcode]=="E":
      a=int(memory[i][8:],2)
      if opcode=="11111":
        i=a
      elif opcode=="01100":
        if regs[7][-3]=="1":
          i=a
      elif opcode=="01101":
        if regs[7][-2]=="1":
          i=a
      elif opcode=="01111":
        if regs[7][-1]=="1":
          i=a
    elif d[opcode]=="F":
      break
    if opcode==10011 and int(memory[i][13:],2)==7:
      continue
    if opcode not in ratio:
      flag_reset(regs[7])

    print(format(i,'08b'), end=' ')
    for i in range(7):
      print(format(regs[i],'016b'), end=' ')
    print(regs[7])