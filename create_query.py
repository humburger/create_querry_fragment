import os, re

"""
    creates query for ArcGis Pro application for VMD or Forms exports
        code for now is draft-like
    can use for workbench too
    can use for excel column data (sort of)
"""

# pārbauda vai sarakstā ir tikai unikālas vērtības
# https://datascienceparichay.com/article/python-check-if-all-elements-in-a-list-are-unique/ at 08.02.2023.
#
def unique_values(input_list):
    temp = []
    for str in input_list:
        # ja jaunveidotajā sarakstā atrodas minētā vērtība, tad visam oriģ sarakstam nav vērtības kā oriģinālas
        if str in temp:
            return False
        # ja vērtība tiek sastapta pirmo reizi, tad tā tiek noglabāta kpoijas sarakstā vēlākam salīdzinājumam
        temp.append(str)
    return True

# for IN query VMD datu ieguvei
def create_for_IN_querry_VMD():
    global in_data
    global out_data
    
    i = 0
    j = len(in_data) - 1
    for value in in_data:
    
        # puts first bracket
        # if str == in_data[0]:
        if i == 0:
            out_data = "(" + str(value) 
        
        # in string end puts closing bracket
        # ja dati ir vienādi, tad izliek arī pēdējo iekavu
        # elif str == in_data[len(in_data) - 1]:
        elif i == j:
            out_data = out_data + ", \n" + str(value) + ")" # for IN query VMD datu ieguvei
            
        else:
            out_data = out_data + ", \n" + str(value) # for IN query VMD datu ieguvei
            
        i = i + 1
        
# anketu  GUID numerācijas, kas ir string vērtības
def create_for_IN_querry_GUID():
    global in_data
    global out_data
    
    i = 0
    j = len(in_data) - 1
    for value in in_data:
    
        # puts first bracket
        # if str == in_data[0]:
        if i == 0:
            out_data = "(" + "'" + str(value)
            
        # in string end puts closing bracket
        # ja dati ir vienādi, tad izliek arī pēdējo iekavu
        # elif str == in_data[len(in_data) - 1]:
        elif i == j:
            out_data = out_data + "', \n'" + str(value) + "')"
            
        else:            
            out_data = out_data + "', \n'" + str(value)
            
        i = i + 1

# MySQL Workbench dabas datu koordinātu atrašanai tiem, kam tie ar pirmo reizi neuzrādas
# datus manuāli iekopē no excel faila pirmajām kolonām input failā un tad no tā faila arī izveido sql vaicājuma fragemntu, ko pielieto sql tukšo koord meklēšanai
def create_for_empty_coord_querry():
    global in_data
    global out_data
    
    i = 0
    j = len(in_data) - 1
    tmp = []
    for value in in_data:
        tmp = value.split("\t")

        # print(tmp)
        
        # observation object id
        obs_obj_id = tmp[0]
        
        # observation data id
        obs_dta_id = tmp[1]
        
        # puts first bracket
        # if str == in_data[0]:
        if i == 0:
            out_data = f"(oob.id = {obs_obj_id} and d.id = {obs_dta_id})\n"
            
        # in string end puts closing bracket
        # ja dati ir vienādi, tad izliek arī pēdējo iekavu
        # elif str == in_data[len(in_data) - 1]:
        elif i == j:
            out_data += f"or (oob.id = {obs_obj_id} and d.id = {obs_dta_id})"
            
        else:            
            out_data += f"or (oob.id = {obs_obj_id} and d.id = {obs_dta_id})\n"
            
        i = i + 1
        
def get_empty_coords():    
    # output faila datus manuāli iekopē excel failā, kad ir zināms, ka secība no Mysql workspace sakrīt ar objectid un id pāriem
    global in_data
    global out_data
    
    # īsti nezinu, bet koordinātu skaitļa ciparu skaits ir 6 un vairāk
    regEx_coords = r"\d{6,}"
    
    # both ids together
    objid_id = []
    # pirmie divi no input faila vērtībā ir id vēr'tibas lai var vieglāk pārbaudīt, vai izdrukātās kordinātas atbilst id vērtību secībai
    # ja nebūtu id pirms koord vēr'tibām, tad min_index_x būtu 0, jeb pirmā list vēr'tiba, ko nolasa no faila rindas
    min_index_x = 2
    min_index_y = min_index_x + 1
    
    x_coord = []
    y_coord = []
    
    i = 0
    j = len(in_data) - 1
    tmp = []
    
    for value in in_data:
        match = []
        tmp = value.replace("@pix_x:775@pix_y:608@circle_id:110@", "")
        match = re.findall(regEx_coords, str(tmp))
        
        objid_id.append(f"{match[0]}\t{match[1]}")

        # print(f"match: {match}")
        
        # salīdzina atrasto vērtību saraksta garumu, nevis indexu skaitu
        if len(match) > 2 + min_index_x:
            arr_x = []
            arr_y = []
            long_x = ""
            long_y = ""
            
            # atrod visus x-us
            for k, l in enumerate(match):
                if (k == min_index_x):
                    long_x += f"{match[k]}"
                elif (k > min_index_x and k % 2 == 0) and k < len(match) - 1:
                    long_x += f", {match[k]}"
            
            # atrod visus y-kus
            for k, l in enumerate(match):
                if (k == min_index_y):
                    long_y += f"{match[k]}"
                elif (k > min_index_y and k % 2 != 0):
                    long_y += f", {match[k]}"
            
            # pievienoju string, kā list vērtību, lai vēlāk ir vieglāk apstrādāt tos datus, kur vienā indeksā ir vairākas koords
            arr_x.append(long_x)
            x_coord.append(arr_x)
            
            arr_y.append(long_y)
            y_coord.append(arr_y)
            
            # print(f"long_x: {long_x}")
            # print(f"long_y: {long_y}")
            
        if len(match) == 2 + min_index_x:
            
            x_coord.append(match[min_index_x])
            y_coord.append(match[min_index_y])
            
    for i, value in enumerate(x_coord):
        # out_data += f"{str(objectid[i])}\t{str(id[i])}\t"
        out_data += f"{str(objid_id[i])}\t{str(x_coord[i])}\t{str(y_coord[i])}\n"
        
    out_data = out_data.replace("'", "")
    out_data = out_data.replace("[", "")
    out_data = out_data.replace("]", "")
    
    # print(out_data)

directory = fr'{os.getcwd()}\input\\'

# input_file_str = "8545_27000.txt"
# output_file_str = "out_8545_27000.txt"

input_file_str = "input.txt"
output_file_str = "output.txt"

file_not_found = False
in_data = []
out_data = ""

try:
    # r -> read data from file
    # r+ -> read and modify data in file
    input_file = open(directory + input_file_str, "r")
    
    # rewrites file to empty
    output_file = open(directory + output_file_str, "w")
    output_file.write("")
    output_file.close()
    
    # opens file for new data
    output_file = open(directory + output_file_str, "a")
    
    # # """
    # # šis bloks darbosies tikai tad, kad input failā ir integer vērtības (VMD eksportam)
    # # 'readlines' can work with data by for loop as in lists
    # for line in input_file.readlines():
       # # konvertēju uz integer veidu, jo max() korekti darbojas ar skaitļiem, nevis string, kas darbojas, kā windows direktorijas uzvedība ar folderu nosaukumiem un datumiem;
        # in_data.append(int(line.strip()))
        
    # # atrod lielāko vērtību, lai tālāk salīdzināk, ka neko zemāku par šo nav jāņem SQL vaicājumā
    # print(max(in_data)) # darbina tikai tad, kad darbojas ar int vērtībām
    
    # # atrod mazāko vērtību, lai var norādīt, ka ir jāņem visus, kas ir lielāki par šo... varbūt izdodas
    # print(min(in_data)) # darbina tikai tad, kad darbojas ar int vērtībām
    
    # # """
    
    # """
    # versija, kad input failā ir Biotopa GUID vērtības (anketu eksportam), kas ir string
    for line in input_file.readlines():
        in_data.append(line.strip())
    
    # """
    
    # drošībai tiek parbaudīts vai visas atdotās vērtības ir unikālas
    print(unique_values(in_data)) # takes a little too much time
		
    # print(in_data)
    
### datu izdrukai citā failā, lai var iegūt lietojamu tekstu priekš SQL vaicājuma    
    # lai skaitītu līdzi masīva vērtību skaitam pēc indeksiem [0..n]
    
    # create_for_IN_querry_VMD()
    create_for_IN_querry_GUID()
    # create_for_empty_coord_querry()
    # get_empty_coords()
	
    output_file.write(out_data)
###

except FileNotFoundError as not_found_err:
    file_not_found = True
    print(not_found_err)
finally:
    if file_not_found == False:
        input_file.close()
        output_file.close()


		
