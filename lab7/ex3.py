import os
import sys
def calculate_size_of_directory(dir):
    try:
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"The directory {dir} does not exist")
        size=0
        for root,_,files in os.walk(dir):
            for file in files:
                file_path=os.path.join(root,file)
                try:
                    size+=os.path.getsize(file_path)
                except FileNotFoundError as fnf_error:
                    print(fnf_error)
                except PermissionError as p_error:
                    print(p_error)
                except Exception as e:
                    print(e)
        print(f"The size of the directory is: {size}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except PermissionError as p_error:
        print(p_error)
    except Exception as e:
        print(e)

if len(sys.argv)!=2:
        print("insuficient arguments")
else:
    calculate_size_of_directory(sys.argv[1])
