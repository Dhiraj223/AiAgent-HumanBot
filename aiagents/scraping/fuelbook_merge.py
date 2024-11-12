def merge_text_files(file_list, output_file):
    merged_content = ""

    for i, file_name in enumerate(file_list):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                merged_content += "\n".join([line.strip() for line in content.splitlines() if line.strip()])

        except FileNotFoundError:
            print(f"Warning: {file_name} not found.")
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(merged_content)
        print(f"All files have been merged into {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__" :
    file_list = [rf"data\fuelbook\webpage-content{i}.txt" for i in range(1, 20)]
    output_file = r'data\knowledgebase.txt'
    merge_text_files(file_list, output_file)
