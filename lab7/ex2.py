import sys
import os

def rename_files (dir):
    try:
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"The directory {dir} does not exist")
        index=0
        for root,_,files in os.walk(dir):
            for file in files:
                index+=1
                file_fullname=os.path.join(root,file)
                file_name, ext= os.path.splitext(file)
                new_file_name=f"{file_name}{index}{ext}"
                new_fullname=os.path.join(root,new_file_name)
                try:
                    os.rename(file_fullname,new_fullname)
                except PermissionError as e:
                     print (f"The file {file} can not be renamed.{e}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"An unexpected error occured: {e}")
if len(sys.argv) == 2:
    rename_files(sys.argv[1])
else:
    print("insuficient arguments")
