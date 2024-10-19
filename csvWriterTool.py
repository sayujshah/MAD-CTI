import csv
from typing import Annotated

def csvWriterTool(file_name: Annotated[str, 'File name'], data: Annotated[str, 'Provided agent output data']):
    rows = [line.split(',') for line in data.strip().split('\n')]
    
    with open('./Outputs/' + file_name, mode='w+', newline='') as file:
        writer = csv.writer(file)
        # Writing the rows to the file
        writer.writerows(rows)