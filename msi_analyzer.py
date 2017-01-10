from msi_analyzer_class import MSI_File

msi_files = []

def get_lines(input_file):
    with open(input_file,'r') as f:
        for line in f:
            yield line

msi_files = [MSI_File(line) for line in get_lines('filtered.txt') if line != '\n']

