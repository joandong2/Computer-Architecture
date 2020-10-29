"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # registers
        self.ram = [0] * 256  # ram/bytes of memory
        self.pc = 0  # program counter, starts at 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
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
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

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

    # INSTRUCTIONS

    # 10000010 # LDI R0,8   ASSIGN INTEGER TO REGISTER, so R0 == self.reg[0], assign 8 which is instruction ln.75
    # 00000000              self.reg[0]
    # 00001000              self.reg[0] = 8
    # 01000111 # PRN R0     PRINT R0 == self.reg[0]
    # 00000000              self.reg[0]
    # 00000001 # HLT        HALT

    def run(self):
        """Run the CPU."""

        # binaries that will be inserted through registry
        LDI = 130  # 10000010
        PRN = 71  # 01000111
        HLT = 1  # 00000001

        running = True
        while running:  # computer always running

            # point to the first instructions in ram
            command = self.ram[self.pc]
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            # points to the first registry
            operand_a = self.ram_read(self.pc + 1)
            # points to 8 in our instructions, (ln. 75)
            operand_b = self.ram_read(self.pc + 2)

            # Set the value of a register to an integer.
            if command == LDI:
                self.reg[operand_a] = operand_b
                # 3 commands to reach next PRN (ln. 73-75)
                self.pc += 3

            # Print numeric value stored in the given register.
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2  # 2 commands to reach HLT (ln. 76-77)

            # Halt the CPU (and exit the emulator).
            elif command == HLT:
                running = False
                self.pc += 1
