import sys
import inputs

#Main Function of the program. This is the entry point to the software
def main():
    args = inputs.entry_inputs()
    args = inputs.inputs_treatment(args)

main()