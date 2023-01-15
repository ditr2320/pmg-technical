import sys
import pandas as pd
import os

def validFile(arg):
    if os.path.isfile(os.path.join('fixtures', arg)): # check if file exists
        file_path = os.path.join("fixtures", arg) 
        if os.path.getsize(file_path) == 0: # check if file is empty
            return False
    else:
        return False
    return True # returns true if file exists and is not empty

def main():
    args = sys.argv[1:]
    result = pd.DataFrame()

    for arg in args:
        if validFile(arg):
            file_path = os.path.join("fixtures", arg) 
            df = pd.read_csv(file_path)
            df['filename'] = arg # add column to specify filename
            result = pd.concat([result, df], join='outer') #merge dfs
        else:
            print(f'{arg} does not exist or is empty')

    if len(result) > 0:
        output_path = os.path.join("out", "combined.csv")
        result.to_csv(output_path, index=False)
    else:
        print("No files were read.")

if __name__ == "__main__":
    main()
