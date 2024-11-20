import sys
import os

def print_contents(path,extension):
    try:
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory '{path}' does not exist")
        if not extension.startswith("."):
            raise ValueError(f"The extention is not valid.") 
        for (root,_,files) in os.walk(path):
            for fileName in files:
                full_fileName = os.path.join(root,fileName)
                if full_fileName[-len(extension):] == extension:
                    try:
                        with open (full_fileName,'r',encoding='utf-8') as f:
                            print (f"The content in the {full_fileName} is:\n")
                            print(f.read())
                    except Exception as e:
                        print(f"Error reading faile {full_fileName}: {e}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as v_error:
        print(v_error)
    except Exception as e:
        print(f"An unexpected error occured: {e}")

        
if len(sys.argv) == 3:
    path = sys.argv[1]
    extension = sys.argv[2]
    print_contents(path,extension)
else:
    print("insuficient arguments")
