#################################  import  ############################################

import csv
from collections import defaultdict
from tabulate import tabulate
import os
from statsmodels.multivariate.manova import MANOVA
import pandas as pd
import matplotlib.pyplot as plt


################################  functions  ########################################


"""
brief  : retriving the data from a csv file
input : filename : name of the csv we want to open
output : list of list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
"""
def read_csv(filename):
    data = []                  # list for stocking the data
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:     # going through all rows
            data.append(row)
    return data


"""
brief  : create a list with only valuable intel
input : csv_data : list of list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
output : list of list as [n° interview, voice, mean of length, mean of length without stop words, native or not]
"""
def create_lists_from_csv(csv_data):
    grouped_data = defaultdict(list)
    for row in csv_data:                                                                   # going through all data
        interview_number, voice = row[0], row[1]                                           # retrieving key data
        length, real_length = int(row[4]), int(row[5])                                     #retrieving attribut data
        native = row[8]
        key = (interview_number, voice)
        grouped_data[key].append((length, real_length, native))

    result = []                                                                            # result list
    for key, values in grouped_data.items():
        interview_number, voice = key
        lengths = [length for length, _, _ in values]
        real_lengths = [real_length for _, real_length, _ in values]
        native = [native for _,_,native in values]
        mean_length = sum(lengths) / len(lengths)                                          # calcul of mean
        mean_real_length = sum(real_lengths) / len(real_lengths)                           # same
        result.append([interview_number, voice, mean_length, mean_real_length, native[0]]) # creating the list
    return result


"""
brief  : split the list every 4 elements
input : lst : list of list as [n° interview, voice, mean of length, mean of length without stop words, native or not]
output : list of list in the same format but organise by interview
"""
def split_list(lst):
    return [lst[i:i+4] for i in range(0, len(lst), 4)]


"""
brief  : generate the table of results
input : lst : list of list as [n° interview, voice, mean of length, mean of length without stop words, native or not]
"""
def print_table_per_interview(lst):
    table_folder = 'code/data/Table/ByInterview'
    os.makedirs(table_folder, exist_ok=True) # create folder if needed
    l = split_list(lst)
    for el in l :                            # going through all data
        interview_number = el[0][0]
        headers = ["Interview", "Voice", "Mean Length", "Mean Real Length", "Native"]
        table = tabulate(el, headers=headers)
        filename = os.path.join(table_folder, f"{interview_number}.txt")
        with open(filename, 'w') as file:    # saving table
            file.write("Interview Number: " + interview_number + "\n")
            file.write(table)



"""
brief  : generate the table of results
input : lst : list of list as [n° interview, voice, mean of length, mean of length without stop words, native or not]
"""
def print_table_per_voice(lst):
    person_data = defaultdict(lambda: {'count': 0, 'sum_col3': 0, 'sum_col4': 0})
    # Iterate through the data to calculate sums
    for entry in lst:
        person = entry[1]
        col3_value = entry[2]
        col4_value = entry[3]
        person_data[person]['count'] += 1
        person_data[person]['sum_col3'] += col3_value
        person_data[person]['sum_col4'] += col4_value
    # Calculate means and organize the results into the desired format
    result = []
    for person, values in person_data.items():
        mean_col3 = values['sum_col3'] / values['count']
        mean_col4 = values['sum_col4'] / values['count']
        result.append([person, mean_col3, mean_col4])
    # save data
    table_folder = 'code/data/Table/ByVoices'
    os.makedirs(table_folder, exist_ok=True)
    table = tabulate(result, headers=["Voice", "Mean length", "Mean real length"], tablefmt="grid")
    filename = os.path.join(table_folder, "ByVoices.txt")
    with open(filename, 'w') as file:
        file.write("By voices \n")
        file.write(table)


"""
brief  : doing the manova analysis
input : data : raw data directly extracted from the csv
"""
def manova(data):
    df = pd.DataFrame(data, columns=['Interview', 'Voice', 'Mean_length', 'Mean_real_length', 'Native'])
    # Filter out the non-numeric columns
    numeric_cols = ['Interview', 'Mean_length', 'Mean_real_length']
    numeric_df = df[numeric_cols]
    # Convert strings to floats
    numeric_df[['Mean_length', 'Mean_real_length']] = numeric_df[['Mean_length', 'Mean_real_length']].apply(pd.to_numeric)
    # Perform MANOVA
    maov = MANOVA.from_formula('Mean_length + Mean_real_length ~ Interview', data=numeric_df)
    print(maov.mv_test())
    manova_results = str(maov.mv_test())
    # save data results to file
    table_folder = 'code/data/Table/Manova'
    os.makedirs(table_folder, exist_ok=True)
    filename = os.path.join(table_folder, "Manova.txt")
    with open(filename, 'w') as file:
        file.write("Manova study \n")
        file.write(manova_results)


########################## Generation of pie chart ##########################################    

#### global variable ####
filename = 'code/data/result.csv' 
csv_data = read_csv(filename)
lists = create_lists_from_csv(csv_data)
sentiment_list = []
sentiment_dict = {}


for row in csv_data:
        # Extract name and sentiment from the row
        name = row[1]
        sentiment = row[7]
        # Append the name and sentiment to the list
        sentiment_list.append([name, sentiment])
        if name not in sentiment_dict:
                sentiment_dict[name] = []
            # Append the sentiment to the list associated with the name
        sentiment_dict[name].append(sentiment)
    # Convert the dictionary to the desired list format
sentiment_list = [[name] + sentiments for name, sentiments in sentiment_dict.items()]

# constraint to have alays the same colour on the different pie chart
sentiment_colors = {
    'neutral': 'blue',
    'approval': 'green',
    'gratitude': 'yellow',
    'joy': 'orange',
    'optimism': 'red',
    'caring': 'purple',
    'disappointment': 'brown',
    'nervousness': 'pink',
    'love': 'cyan',
    'remorse': 'salmon',
    'admiration': 'magenta',
    'excitement': 'teal',
    'desire': 'lime',
    'confusion': 'olive',
    'disapproval': 'gray'
    
}


"""
brief  : generate the pie chart for sentiment or analysis
input  : sentiment : list of list as [voice, sentiment]
         voice : voice 
"""
def create_circular_diagram(sentiment_list, voice):
    # Filter the sentiment list for the specified voice
    filtered_list = [entry for entry in sentiment_list if entry[0] == voice]
    # Count the occurrences of each sentiment for the specified voice
    sentiment_counts = {}
    for entry in filtered_list:
        for sentiment in entry[1:]:
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
            else:
                sentiment_counts[sentiment] = 1
    # Prepare data for the pie chart
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    # Create the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, startangle=140, autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f'Emotion Distribution for {voice}')
    plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), borderaxespad=0.5)
    plt.show()


###### main #######
voices_to_plot = ['pixie', 'robot', 'megan', 'william']

for voice in voices_to_plot:
    create_circular_diagram(sentiment_list, voice)
