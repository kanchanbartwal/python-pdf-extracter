import os,re,csv

from os import walk

def list_files(directory, extension):
        for (dirpath, dirnames, filenames) in walk(directory):
            return (os.path.join(dirpath,f) for f in filenames if f.endswith('.' + extension))

def get_value(var):
    value = {}
    for key,val in pattern.items():
        value_slot = re.search(val,var).group(0)
        processed_list = [v.strip() for v in value_slot.split("\n") if len(v.strip())>0]
        if key=="amount":
            processed_list = processed_list[2:6]
        else:
            processed_list = processed_list[1:5]

        if len(processed_list)<4:
            processed_list.extend([0]*(4-len(processed_list)))

        value[key] = processed_list
    
    return value

def initialize_csv(output_file):
    os.remove(output_file) if os.path.exists(output_file) else None
    file_obj = csv.writer(open(output_file,'w'))
    return file_obj

def write_in_csv(value_dict,file):
    file_obj.writerow([file])
    file_obj.writerow(csv_header)
    rows = zip(*value_dict.values())

    for row in rows:
        file_obj.writerow(list(row))

    file_obj.writerow([])

if __name__=="__main__":
    pattern = {"reading_slot":"(?s)(?=SLOT).*?(?=TOTAL)",
            "last_reading":"(?s)(?=READNIG).*?(?=MF)",
          "unit_rate":"(?s)(?=RS/UNIT).*?(?=AMOUNT)",
          "amount":"(?s)(?=AMOUNT).*?(?=OTHER)"
            }
    directory = "files"
    output_file='data.csv'
    csv_header = ["reading_slot","last_reading","unit_rate","amount"]
    file_obj = initialize_csv(output_file)


    files = list_files(directory, "pdf")
    for file in files:
        print("{} Processing... ".format(file))
        try:
            var = os.popen('pdf2txt.py {file}'.format(file=file)).read()
            value = get_value(var)

            write_in_csv(value,file.split("/")[-1])
        except Exception as e:
            file_obj.writerow([file.split("/")[-1],str(e)])
            file_obj.writerow([])

