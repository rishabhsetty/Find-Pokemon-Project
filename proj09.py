#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################

    #  Computer Project #9

    #

    #  Multiple functions retrieving data for a nested dictonary that is created from read file function

    #    user inputs options 1-3 to get certain data about from the dictionary or q to stop
    #   

    #    loops until user enters q to quit

    # 

    #       
    

    ###########################################################"""
import csv
from operator import itemgetter

EFFECTIVENESS = {"0.25": "super effective", "0.5": "effective", "1":"normal", "2":"weak", "4":"super weak", "0":"resistant"}
MATCHUP_TYPES = {"resistant", "super effective", "effective", "normal",
                 "weak", "super weak"}


PROMPT = '''

\nTo make a selection, please enter an option 1-3:\n
\tOPTION 1: Find Pokemon
\tOPTION 2: Find Pokemon From Abilities
\tOPTION 3: Find Matchups
\nEnter an option: '''
#opens one file that will be converted to a dictionary
def open_file(s):
    """WRITE DOCSTRING HERE"""
    file_not_found = True
    while file_not_found:#while loop for user to input correct file
        file_name = input("Please enter a {} filename: ".format(s))
        try:
            file_pointer = open(file_name,"r", encoding="utf-8")
            file_not_found = False#boolean variable to determine the file 
        except FileNotFoundError:
            print("This {} file does not exist. Please try again.".format(s))
            file_not_found = True
    return file_pointer
#function to get the abilities as a set
def abilities(string):
    abilities=set()
    string= string.strip("[")
    string= string.strip("]")
    string= string.split(",")
    for l in string:
        l=l.replace("'", "")
        l=l.strip(" ")
        abilities.add(l)
    return abilities    
   
#takes the information from the data and creates a nested dictionary
def read_file(fp):
    """WRITE DOCSTRING HERE"""
    main_dict={}
    types_list = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost',
              'grass', 'ground', 'ice', 'normal', 'poison', 'psychic', 'rock', 'steel', 'water']
    reader=csv.reader(fp)
    next(reader,None)
    
    for line in reader:
        main_key=int(line[39])
        if line[37]!="":
            types_key=(line[36],line[37])
            
        else:   
            line[37]= None
            types_key=(line[36],line[37])
        name_key=line[30]
        string=line[0]
        ab=abilities(string)
        hp=int(line[28])
        capture_rate=int(line[23])
        weight=float(line[38])
        speed=int(line[35])
        legend=line[40]
        if legend=="0":
            legend=False
        if legend=="1":
            legend=True
        name_list= [{"super effective" :set(), "effective" : set(), "normal": set(), "weak" :set(),"super weak" :set(), "resistant" : set()}]    
        for column_number in range(1,19):
            effectiveness_value = line[column_number]
            effectiveness_category = EFFECTIVENESS[effectiveness_value]
            types_list_index = column_number - 1
            this_type = types_list[types_list_index]
            name_list[0][effectiveness_category].add(this_type)    
        name_list.append(ab)
        name_list.append(hp)
        name_list.append(capture_rate)
        name_list.append(weight)
        name_list.append(speed)
        name_list.append(legend)

        if main_key not in main_dict:
            main_dict[main_key]={types_key:{name_key:name_list}}
        else:
            
            if types_key not in main_dict[main_key]: 
                main_dict[main_key][types_key]={name_key:name_list}
            else:
                if name_key not in main_dict[main_key][types_key]:
                    main_dict[main_key][types_key][name_key]= name_list  
                
    
    return main_dict
        
        
# creates a smaller dictionary based on the name of the pokemon
def find_pokemon(pokedex, names):
    
    
    d={}
    for i in iter(names):
        for k in pokedex:
            for v in pokedex[k]:
                for name in pokedex[k][v]:
                    if i in pokedex[k][v]:
                        d[i]=[pokedex[k][v][i][1],pokedex[k][v][i][2],pokedex[k][v][i][3],pokedex[k][v][i][4],pokedex[k][v][i][5],pokedex[k][v][i][6],k,v]
    return d                
            
           
           
                
        

   
#displays the name using the information in find_pokemon    
def display_pokemon(name, info):
    
   
   
    if info[7][1]==None:
        
        type1=(info[7][0])
    else:
        
        type1=info[7][0]+", "+info[7][1]
    j=""    
    sortlist=list(info[0])
    sortlist=sorted(sortlist)
    for i in sortlist:
        j+= (i+", ")
    
    if info[5]==True:
        
        islegend="\tLegendary" 
    else:
        
        islegend="\tNot Legendary"
    r="\n{}\n\tGen: {}\n\tTypes: {}\n\tAbilities: {}\n\tHP: {}\n\tCapture Rate: {}\n\tWeight: {}\n\tSpeed: {}\n{}".format(name,info[6],type1,j[:-2],info[1],info[2],info[3],info[4],islegend)
    print(r)
    return r

    
#returns the set of pokemon with an ability
def find_pokemon_from_abilities(pokedex, abilities):
    s=set()
    s1=set()
    for i in iter(abilities):
        for k in pokedex:
            for v in pokedex[k]:
                for name in pokedex[k][v]:
                    for l1 in pokedex[k][v][name]:
                        if i in pokedex[k][v][name][1]:
                            s.add(name)
                        else:
                            s1.add(name)
    finals=s-s1                        
    return finals                       
                    
                    
    
    
   
#drills down inside the dictionary to find types that are associated with a pokemon, then returns the pokemon with its typing                   
def find_matchups(pokedex, name, matchup_type):
    L=[]
    set1=set()
    for k in pokedex:
        for v in pokedex[k]:
            if name in pokedex[k][v]:
                for l1 in pokedex[k][v][name]:
                    for j in pokedex[k][v][name][0]:
                        if j==matchup_type: 
                            
                            for k1 in pokedex:
                                for v1 in pokedex[k1]: 
                                    if v1[1]==None: 
                                        v2=[v1[0],0]
                                    else:
                                        v2=[v1[0],v1[1]]
                                    for name1 in pokedex[k1][v1]:
                                        for i in list(pokedex[k][v][name][0][matchup_type]):
                                            if i==v2[0] or i==v2[1]:
                                                tup1=(name1,v1)
                                                set1.add(tup1)
    for r in iter(set1):
        if r[1][1]==None:
            new=(r[1][0],)
            r=(r[0],new)
        L.append(r)
    finall=sorted(L,key=itemgetter(0))  
    if finall==[]:
        return None
    return finall   
#converts the user inputs into sets
def toset(string):
    string=string.split(",")
    set5=set()
    for i in string:
        i=i.strip(" ")
        set5.add(i)
       
    return set5
 
        
       
                                        
   
#main loop with three options and each options refers to a specific function created
def main():
    print("Welcome to your personal Pokedex!\n")
    fp = open_file("pokemon")
    pokedex = read_file(fp)
    L5=[]
    for j in pokedex:
        for j1 in pokedex[j]:
            for j2 in pokedex[j][j1]:
                L5.append(j2)
               
    EFFECTIVENESS = {"0.25": "super effective", "0.5": "effective", "1":"normal", "2":"weak", "4":"super weak", "0":"resistant"}
    main_input=input(PROMPT)
    while main_input.isdigit()==False or int(main_input)>3 :
        print("Invalid option {}".format(main_input))
        main_input=input(PROMPT)
    while main_input.lower()!="q":
        if main_input=="1":
            op1= input("\nEnter a list of pokemon names, separated by commas: ")
            newop=toset(op1)
            poke1=find_pokemon(pokedex,newop)
            poke2=sorted(list(poke1.keys()))
            for g in poke2:
                display_pokemon(g, poke1[g])
            main_input=input(PROMPT)
        if main_input=="2":
            op2=input("Enter a list of abilities, separated by commas: ")
            newop1=toset(op2)
            abil1=find_pokemon_from_abilities(pokedex, newop1)
            abil2=sorted(list(abil1))    
            jk=""
            for f in abil2:  
                jk+= f+", "
            print("Pokemon:",jk[:-2])    
            main_input=input(PROMPT)
        if main_input=="3":
            op3=input("Enter a pokemon name: ")
            op4=input("Enter a matchup type: ")
            while op4 not in EFFECTIVENESS.values() or op3 not in L5:
                print("Invalid input")
                main_input=input(PROMPT)
                if main_input=="1":
                    op1= input("\nEnter a list of pokemon names, separated by commas: ")    
                if main_input=="2":
                    op2=input("Enter a list of abilities, separated by commas: ")   
                if main_input=="3":
                    op3=input("Enter a pokemon name: ")
                    op4=input("Enter a matchup type: ")    
            match_list=find_matchups(pokedex, op3, op4)
            match_list1=sorted(match_list,key=itemgetter(0))
            if match_list1!=None:
                for n in match_list1:
                    if len(n[1])!=1:
                        print("{}: {}, {}".format(n[0],n[1][0],n[1][1]))
                    else:
                        print("{}: {}".format(n[0],n[1][0]))
            
            main_input=input(PROMPT)
            
    

if __name__ == "__main__":
    main()   