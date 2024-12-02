import csv

def csvWriterTool(data: str):
    with open('./Outputs/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Writing the rows to the file
        writer.writerows(data)