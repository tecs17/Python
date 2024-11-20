import os
import sys
def count_extensions(dir):
    try:
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"The directory {dir} does not exist")
        extensions = {}
        for root,_,files in os.walk(dir):
            try:
                for file in files:
                    file_path=os.path.join(root,file)
                    _, ext = os.path.splitext(file)
                    if ext: 
                        if ext in extensions:
                            extensions[ext]+=1
                        else:
                            extensions[ext]=1
            except FileNotFoundError as fnf_error:
                print(fnf_error)
            except PermissionError as p_error:
                print(p_error)
            except Exception as e:
                print(e)
        for ext,count in extensions.items():
            print(f"{ext or "No extension"}: {count}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(e)

if len(sys.argv)!=2:
        print("insuficient arguments")
else:
    count_extensions(sys.argv[1])
