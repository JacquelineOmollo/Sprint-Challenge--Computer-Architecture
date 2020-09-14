import sys

HLT = 0b00000001  # Halt
LDI = 0b10000010  # Set the value of a register to an integer
PRN = 0b01000111  # Print
MUL = 0b10100010  # Multiply
ADD = 0b10100000  # ADD
SUB = 0b10100001  # Subtraact
POP = 0b01000110  # Pop off stack
PUSH = 0b01000101 # push to stack
CMP = 0b10100111 # handled by the ALU
JMP = 0b01010101 # Jump
JEQ = 0b01010101 
JNE = 0b01010110
RET = 0b00010001 # Return from subroutine
CALL = 0b01010000
E = 0b00000111 
AND = 0b10101000


class CPU:
       
    def __init__(self):
        self.ram = [0] * 256 # 256 bytes
        self.reg = [0] * 8 # 8 register
        self.pc = 0 # program counter
        self.running = True # boolean value t check on and off
        self.flag = [0] * 8  #holds flag reg
     
        
        self.branch_table = {}
        self.branch_table[LDI] = self.LDI
        self.branch_table[PRN] = self.PRN
        self.branch_table[HLT] = self.HLT
        self.branch_table[POP] = self.POP
        self.branch_table[PUSH] = self.PUSH
        self.branch_table[CALL] = self.CALL
        self.branch_table[MUL] = self.MUL
        self.branch_table[ADD] = self.ADD
        self.branch_table[SUB] = self.SUB
        self.branch_table[CMP] = self.CMP
        self.branch_table[JEQ] = self.JEQ
        self.branch_table[JNE] = self.JNE
        self.branch_table[RET] = self.RET
        
        
    def ram_read(self, address):
        # This will accept the address to read and return the value stored
        return self.ram[address]

    def ram_write(self, address, value):
        # This will accept the value to write
        self.ram[address] = value 


    def load(self):
        address = 0

        # We'll open the files
        with open("sctest.ls8", "r") as file:
            # Loop through our file
            for line in file:
                # We'll split the string to a list using the "#" as the separator, and strip to remove spaces at the beginning and at the end of a string
                line = line.split("#")[0].strip()

                if line == "":
                    continue
                try:
                    num = int(line, 2)
                except ValueError:
                    continue
                self.ram_write(address, num)
                address += 1

    def alu(self, op, reg_a, reg_b):
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
           self.reg[reg_a] -= self.reg[reg_b]

        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]

        elif op == "CMP":
            if reg_a == reg_b:
                self.flag[E] = HLT
            else:
                self.flag[E] = False
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def run(self):
        while self.running:
            #Reads memory for reg and stores results in IR
            IR = self.ram_read(self.pc)
            #Reads bytes with pc+1
            flag = (IR & 0b00010000) >> 4
            operand_a = self.ram_read(self.pc + 1)
             #Reads bytes with pc+2
            operand_b = self.ram_read(self.pc + 2)
            self.branch_table[IR](operand_a, operand_b)
            if flag == 0:
                self.pc += 1 + (IR >> 6)
                

    def LDI(self, operand_a, operand_b):
            self.reg[operand_a] = operand_b
               
    def PRN(self, operand_a, operand_b):
            print(self.reg[operand_a])

    def HLT(self, _,__):
            self.running = False
                   
    def POP(self, reg_address, __):
            SP =self.reg[7]
            value = self.ram[SP]
            self.reg[reg_address] = value
            self.reg[7] += 1
    
    def PUSH(self, operand_a,__):
            self.reg[7] -= 1
            SP = self.reg[7]
            value = self.reg[operand_a]  
            self.ram[SP] = value  
            
    def CALL(self, operand_a, operand_b):
            return_address = operand_b

            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = address

            reg_num = self.ram[operand_a]
            subroutine = self.reg[reg_num]

            self.pc = subroutine

    def JEQ(self, operand_a,__):
        if self.flag[E] == HLT:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def JNE(self, operand_a,__):
        if self.flag[E] == False:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def JMP(self, operand_a,__):
        self.pc = self.reg[operand_a]

    def RET(self):
        subroutine = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        self.pc == subroutine

    def CMP(self, operand_a, operand_b):
        reg1 = self.reg[operand_a]
        reg2 = self.reg[operand_b]
        self.alu("CMP", operand_a, operand_b)
        
    def MUL(self, operand_a, operand_b):
            self.alu("MUL", operand_a, operand_b)

    def ADD(self, operand_a, operand_b):
            self.alu("ADD", operand_a, operand_b)

    def SUB(self, operand_a, operand_b):
            self.alu("SUB",operand_a, operand_b)

