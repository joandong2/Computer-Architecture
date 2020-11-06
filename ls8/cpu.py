"""CPU functionality."""

# python3 ls8.py examples/mult.ls8

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # registers
        self.ram = [0] * 256  # ram/bytes of memory
        self.pc = 0  # program counter, starts at 0
        self.sp = 7  # R7 is reserved as the stack pointer (SP)

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        # program = []

        memory_address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                line_split = line.split("#")
                command = line_split[0].strip()
                if command == '':
                    continue
                command_num = int(command, 2)
                # program.append(command_num)
                self.ram[memory_address] = command_num
                memory_address += 1

        for instruction in self.ram:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]  # ex: self.ram[255]

    def ram_write(self, address, value):
        self.ram[address] = value  # ex: self.ram[255] = 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # binaries that will be inserted through registry
        LDI = 130  # 10000010
        PRN = 71  # 01000111
        HLT = 1  # 00000001
        MUL = 162  # 10100010
        PUSH = 69  # 01000101
        POP = 70  # 01000110
        RET = 17  # 00010001
        CALL = 80  # 01010000
        ADD = 160  # 10100000

        running = True
        while running:  # computer always running

            # point to the first instructions in ram
            command = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Set the value of a register to an integer.
            if command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            # Print numeric value stored in the given register.
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            # needed for LN.26 in call.ls8
            elif command == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            elif command == MUL:
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3

            elif command == PUSH:
                # decrement the SP
                self.reg[self.sp] -= 1

                #get_num = self.ram_read(self.pc + 1)
                value = self.reg[operand_a]

                current_stack = self.reg[self.sp]
                self.ram[current_stack] = value
                self.pc += 2

            elif command == POP:
                #get_num = self.ram_read(self.pc + 1)
                self.reg[operand_a] = self.ram[self.reg[self.sp]]

                # add to SP value
                self.reg[self.sp] += 1
                self.pc += 2

            elif command == CALL:
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[self.sp], self.pc + 2)
                self.pc = self.reg[operand_a]
                # print('hello')

            elif command == RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1

            # Halt the CPU (and exit the emulator).
            elif command == HLT:
                running = False
                self.pc += 1
