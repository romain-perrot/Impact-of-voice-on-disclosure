######################### import ##########################

import analyse
import os
import csv


######################## functions ########################

"""
brief  : opening a file .txt
input  : file_path : path to the file we want to open
return : return the open file
"""
def read_text_file(file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text


"""
brief  : retrieve the text from all file of a folder
input  : folder_path : path to the folder we want to work on
return : return the text as a dictionnary with the name of the file as key and the inside as attribut
"""
def read_text_files_in_folder(folder_path):
    file_texts = {}
    # loop for every file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # making sure that it s really a file to avoid any issue
        if os.path.isfile(file_path):
            text = read_text_file(file_path)
            # making sure the file is not empty
            if text:
                # putting in the dictionnary
                file_texts[file_name] = text
    return file_texts


"""
brief  : creating the dictionnary of the text's file
return : return the dictionnary with a number as key and a list [n° iterview, voice, question, answer] as attribut
"""
def retrieve_dic():
    dic = {}
    cpt = 0
    # mgoing through every interview folders
    for i in range (1,11):
        path = "code/data/interview/interview"+str(i)+"/"
        order = read_text_file(path+"voices.txt")[:-1].split(" ")
        # going through the 4 part of the interviews
        for j in range (0,4):
            Npath = path+order[j]
            ans = read_text_files_in_folder(Npath)
            keys = ans.keys()
            # generating the list [n° iterview, voice, question, answer] for every file
            for key in keys :
                test = [i, order[j], key, ans[key]]
                cpt+=1
                # adding to the dictionnary 
                dic[cpt] = test
    return dic



"""
brief  : making the analysis on the results
input  : L : list as [n° iterview, voice, question, answer]
return : list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
"""
def create_results(L):
    lenght = analyse.count_words(L[-1])                 # retrieving the lenght of the answer
    real_lenght = len(analyse.remove_stop_words(L[-1])) # retieving the number of meaningful words
    sentiment = analyse.analyze_sentiment(L[-1])        # retriving the sentiment of the answer
    emotion = analyse.analyze_emotion(L[-1])            # retriving the emotion of the answer
    l = L + [lenght, real_lenght, sentiment, emotion]
    if l[0] == 10 or l[0] == 5:                         # adding if native or not
        return l + ["yes"]
    else : 
        return l + ["no"]



"""
brief  : saving the results in a csv file
input  : data : list of list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
         filename : name of the csv file
"""
def write_to_csv(data, filename):
    # list for the header's name
    header = ["interview", "voice", "question", "answer", "length", "real length", "emotion", "sentiment", "native"]
    # creating and filling the csv
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


"""
brief  : create the list in the right format
output : list of list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
"""
def final_list():
    final = []                                 # return list
    dic = retrieve_dic()                       # retrieving the dictionnary
    print(create_results(dic[2]))
    for key in dic.keys():                     # going through the whole dictionnary
        print(key)
        final.append(create_results(dic[key])) # filling the list as intended
    return final



"""
brief  : save the data
input : data : list of list as [n° iterview, voice, question, answer, length of the answer, length without stop words, sentiment, emotion, native or not]
"""
def generate_CSV(data):
    filename = 'code/data/result.csv'
    write_to_csv(data, filename)
    print(f"CSV file '{filename}' has been created successfully.")


"""
brief  : launch all process to have the right csv file to work on
"""
def main():
    Flist = final_list()
    generate_CSV(Flist)


#################### main part ################################################

main()
    

