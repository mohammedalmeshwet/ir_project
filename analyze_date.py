import datefinder

import json

def do_findDate(contentAFile):
    try:
        match = datefinder.find_dates(contentAFile, source=1)


        for item in match:
            #print("date is:", item)
            replacement = ""

            if item[1].len() > 4:
                replacement += month_processor(item[0].month)
                replacement += " "

            contentAFile = contentAFile.replace(item[1], replacement)

    except:
        pass

    return contentAFile



def month_processor(month):
    f = open('month.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    return data[month]