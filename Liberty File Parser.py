global the_cells

def parser(x):
    file = open(x)
    file2 = open(x)
    lines = file.readlines()
    try:
        
        z, a = get_cell_names(lines)
        y = get_function_names(lines, a)
        
        footprints = get_footprint(lines, a)
        s = get_sequential(lines,a)
        l = get_latch(lines, a) 
        the_cells = make_cells(z,y,footprints, s, l)
        print(the_cells)
        map_cells(the_cells)
        
        
        
    finally:
        file.close()
    
    


def get_cell_names(lib_file):
    cell_names = []
    list = lib_file
    count_c = 0
    cell_divisions = []
    isComment = False
    for x in list:
        length = len(x)
        for y in range(length):
            if x[y:y+2] == '/*':
                isComment = True
                #print(isComment)
            #Assuming no nested comments symbols
                
            if x[y:y+2] == '*/':
                isComment = False
            if x[y:y+6] == 'cell (' and isComment == False:
                cell_divisions.append(list.index(x))
                count_c=count_c+1
                name_end = x.find(')')
                cell_names.append(x[y+6:name_end])
     
    return cell_names, cell_divisions

def get_function_names(lib_file, cell_positions):
    function_names = []
    function_count=0
    list = lib_file
    
    cell_divisions = cell_positions
    cell_divisions.append(len(list))
    
    function_found = False
    
    for p in range(len(cell_divisions)-1):
        function_found = False
        eachcell_function = [] 
        for a in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(a)
            for b in range(length):
                if a[b:b+13] == ' function : "':
                    
                    function_found = True
                    function_count=function_count+1
                    function_end = a.find('";')
                    f = a[b+13:function_end]
                    eachcell_function.append(f)
        if function_found == False:
            function_names.append("No function")
        else:
            function_names.append(eachcell_function)
    
          
    return function_names                    

def get_footprint(lib_file, cell_positions):
    footprint_names = []
    footprint_count=0
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+18] == 'cell_footprint : "' and isComment == False:
                    footprint_count = footprint_count+1
                    name_end = x.find('";')
                    footprint_names.append(x[y+18:name_end])
                    

    return footprint_names
    
            

def get_sequential(lib_file, cell_positions):
    sequential_cells = []
    #footprint_count=0
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        seq_info = []
        isSequential = False
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x) 
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                    #print(isComment)
                #Assuming no nested comments symbols
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+4] == "ff (" and isComment == False:# number of functions: if 2 functions then Q
                    isSequential = True
                if x[y:y+14] == 'clocked_on : "' and isComment == False and isSequential == True: #Clock: I
                    clock_end = x.find('";')
                    seq_info.append(x[y+14:clear_end])
                if x[y:y+10] == 'preset : "' and isComment == False and isSequential == True: #Preset: S
                    preset_end = x.find('";')
                    seq_info.append(x[y+10:preset_end])
                if x[y:y+9] == 'clear : "' and isComment == False and isSequential == True: #Clear: R
                    clear_end = x.find('";')
                    seq_info.append(x[y+9:clear_end])
                if x[y:y+4] == "ff (" and isComment == False:# number of functions: if 2 functions then Q
                    seq_fun_end = x.find('")')
                    seq_info.append(x[y+4:seq_fun_end])
                    isSequential = True                                                     
                if x[y:y+14] == 'next_state : "' and isComment == False and isSequential == True: #Next State - nothing yet
                    state_end = x.find('";')
                    seq_info.append(x[y+14:state_end])
        
        sequential_cells.append(seq_info)
    print(sequential_cells)
    return sequential_cells
                    
def get_latch(lib_file, cell_positions):
    latch_cells = []
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        latch_info = []
        isLatch = False
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+7] == "latch (" and isComment == False:# number of functions: if 2 functions then Q
                    latch_fun_end = x.find('")')
                    latch_info.append(x[y+7:latch_fun_end])
                    isLatch = True
                if x[y:y+10] == 'data_in : "' and isComment == False and isLatch == True:
                    latch_data_end = x.find('")')
                    latch_info.append(x[y+10:latch_data_end])
                if x[y:y+9] == 'clear : "' and isComment == False and isLatch == True:
                    latch_clear_end = x.find('";')
                    latch_info.append(x[y+9:latch_clear_end])
                if x[y:y+10] == 'preset : "' and isComment == False and isLatch == True: #Preset: S
                    latch_preset_end = x.find('";')
                    latch_info.append(x[y+10:latch_preset_end])
                if x[y:y+10] == 'enable : "' and isComment == False and isLatch == True: #Enable: I
                    latch_enable_end = x.find('";')
                    latch_info.append(x[y+10:latch_enable_end])
        latch_cells.append(latch_info)
    print(latch_cells)
    return(latch_cells) 
                
    
                
    
    
def make_cells(cells, functions, footprints, sequential, latch):
   
    cell_dict = {}
    for x in cells:
        cell_info = []
        cell_info.append(functions[cells.index(x)])
        cell_info.append(footprints[cells.index(x)])
        cell_info.append(sequential[cells.index(x)])
        cell_info.append(latch[cells.index(x)])
        cell_dict[x] = cell_info
    return cell_dict
        
        
def map_cells(cells):
    for x in cells:
        
        if cells[x][2] == [] and cells[x][3] == []:
            print("Print not sequential/latch")
        elif cells[x][3] != []:
            cell_type = "LATCH"
            for y in cells[x][3]:
                if y == "!GATE_N":
                    cell_type+='I'
            for y in cells[x][3]:
                if y == "!S":
                    cell_type+='S'
            for y in cells[x][3]:
                if y == "!RESET_B":
                    cell_type+='R'
            for y in cells[x][3]:
                if y == '"IQ","IQ_N':
                    cell_type+='Q'
            print(cell_type)
        else:
            cell_type = "DFF"
            for y in cells[x][2]:
                if y == "!CL":#SHOULD BE !CLK_N SOMETHING WRONG IN GET_SEQUENTIAL
                    cell_type+='I'
            for y in cells[x][2]:
                if y == "!SET_B":
                    cell_type+='S'
            for y in cells[x][2]:
                if y == "!RESET_B":
                    cell_type+='R'
            for y in cells[x][2]:
                if y == '"IQ","IQ_N':
                    cell_type+='Q'
                
            print(cell_type)
            
                
    
    
parser("sky130_Test2.lib")
