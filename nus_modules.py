from mods_lib import *

def nusmod_list(filename):
    '''
    #Dictionary of nus modules of format
    {<module code>:
        {
            {(class type, class code):
                Schedule for that class}
               :
               }
               
            {(class type 2, class code 2):
                Schedule for that class}
               :
               }
            }
            :
        }#End of all classes for the module
    }#End of module list
    ''' 
    translate={'Tutorial Type 2': "TUT2", 'Recitation': 'REC', 'Packaged Tutorial': 'PTUT', 'Packaged Lecture': 'PLEC', 'Seminar-Style Module Class': "SEM",'Design Lecture': "DLEC", 'Laboratory' : 'LAB', "Lecture" : "LEC", "Tutorial":"TUT", 'Sectional Teaching':"SEC"}
    lst = ["ModuleCode","Timetable"]
    all_modules = {}
    mods = read_json(filename)
    for i in mods:
        tmp = dict(filter(lambda x:x[0] in  lst, tuple(i.items())))
        if "Timetable" in tmp.keys():
            a = tmp["Timetable"]
            b = {}
            for i in a:
                if i["LessonType"] in translate.keys():
                    key = (translate[i["LessonType"]],i["ClassNo"])
                    del i["LessonType"]
                    del i["ClassNo"]
                    del i["Venue"] #delete venue from list
                    weird = ("Orientation Week", "Recess Week", 'r', '')
                    if i["WeekText"] == "Every Week":
                        i["WeekText"] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
                    elif i["WeekText"] == "Even Week":
                        i["WeekText"] = [2,4,6,8,10,12]
                    elif i["WeekText"] == "Odd Week": 
                        i["WeekText"] = [1,3,5,7,9,11,13]
                    elif i["WeekText"] in weird:
                        i["WeekText"] = []
                    else:
                        try:
                            i["WeekText"] = list(map(lambda x:int(x),(i["WeekText"]).split(",")))
                        except:
                            i["WeekText"] = [1,2,3,4,5,6,7,8,9,10,11,12,13]
                    if key in b:
                        b[key].append(dict(i.items()))
                    else:
                        b[key] = [i]
                else:
                    print( (tmp["ModuleCode"],i["LessonType"],i))
                    
            all_modules[tmp["ModuleCode"]] = b
    return all_modules

#Convert JSON to dictionary
def read_json(filename):
    datafile = open(filename, 'r',  encoding='utf-8')
    return json.loads(datafile.read())
