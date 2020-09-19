
#csv_path = "/skating2.0/skating2_data/train_skating63.csv"
#output_csv = "/skating2.0/skeleton_script/label_train_skating63.csv"
csv_path = "/skating2.0/skating2_data/val_skating63.csv"
output_csv = "/skating2.0/skeleton_script/label_val_skating63.csv"
with open(csv_path, "r") as f, open(output_csv, "w") as outfile:
    for line in f.readlines():
        line = line.strip()
        print(line)
        full_file_name, frame_num, label = line.split(" ")
        file_name = full_file_name.split("/")[-1]
        class_name = file_name.split("_n")[0]
        save_line = [class_name, file_name, frame_num, label]
        save_line = ",".join(save_line) + "\n"
        outfile.write(save_line)


        

