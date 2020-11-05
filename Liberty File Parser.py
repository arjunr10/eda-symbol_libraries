global the_cells

def parser(x):# Main function
    file = open(x)#Open liberty file
    #file2 = open(x)
    lines = file.readlines()# Read liberty file(Each element in this list is a line of liberty file
    try:       
        z, a = get_cell_names(lines)
        y = get_function_names(lines, a)
        footprints = get_footprint(lines, a)
        s = get_sequential(lines,a)
        l = get_latch(lines, a)
        pins = get_pin(lines, a)
        the_cells = make_cells(z,y,footprints, s, l, pins)
        g, t = map_cells(the_cells)
        make_library(g, the_cells, t)
        
        
    finally:
        file.close()
    
    


def get_cell_names(lib_file):# Takes liberty file and returns list of the cell names and a list of the indexes diving the liberty file into different sections for each cell
    cell_names = []#Call name lists
    list = lib_file
    count_c = 0
    cell_divisions = []#List contiang sections of the liberty file(stores indicies)
    isComment = False 
    for x in list:
        length = len(x)
        for y in range(length):
            if x[y:y+2] == '/*':#Making sure its not a comment
                isComment = True    
            if x[y:y+2] == '*/':
                isComment = False
            if x[y:y+6] == 'cell (' and isComment == False:#Capturing cell name
                cell_divisions.append(list.index(x))
                count_c=count_c+1
                name_end = x.find(')')
                cell_names.append(x[y+6:name_end])
     
    return cell_names, cell_divisions

def get_function_names(lib_file, cell_positions):# Returns list of functions 
    function_names = []
    function_count=0
    list = lib_file
    
    cell_divisions = cell_positions
    cell_divisions.append(len(list))#Last value in cell divisions is the last index of lib fil
    
    function_found = False
    
    for p in range(len(cell_divisions)-1):
        function_found = False
        eachcell_function = [] 
        for a in list[cell_divisions[p]:cell_divisions[p+1]]:# For every section(cell) in the liberty file
            length = len(a)
            for b in range(length):
                if a[b:b+13] == ' function : "':# Find the function line
                    
                    function_found = True
                    function_count=function_count+1
                    function_end = a.find('";')
                    f = a[b+13:function_end]
                    #print(f)
                    new_f = ""
                    for letter in f:
                        if letter != " ":
                            new_f = new_f+letter
                            
                    p_list = []
                    for letter in new_f:
                        if letter == "(" or letter == ")":
                            p_list.append(letter)
                

                    if new_f[0] == "(" and new_f[len(new_f)-1] == ")" and len(p_list) < 3:
                        new_f = new_f[1:len(new_f)-1]
                    eachcell_function.append(new_f)
        if function_found == False:
            function_names.append("No function")
        else:
            function_names.append(eachcell_function)#cells might have more than 1 function, so each element is a list with the function
    
          
    return function_names                    

def get_footprint(lib_file, cell_positions):#Gets footrpints
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
    
            

def get_sequential(lib_file, cell_positions):#Returns flip flops information in a list, and the element is empty if the cell is not a flip flop
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
    return sequential_cells
                    
def get_latch(lib_file, cell_positions):#Returns latches information in a list, and the element is empty if the cell is not a latch
    latch_cells = []
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):#Searching in each section
        latch_info = []
        isLatch = False
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':#Checking comments
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
    return(latch_cells) 

def get_pin(lib_file, cell_positions):#Returns a list of the pin names for each cell
    pin_cells = []
    lines = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        pin_info = [[],[]]#Seperating pins by input and output
        for x in lines[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+7] == ' pin ("' and isComment == False:
                    direction_found = False
                    pin_end = x.find('")')
                    for c in lines[lines.index(x):cell_divisions[p+1]]:
                        line_length = len(c)
                        direction = ""
                        for b in range(line_length):
                            if c[b:b+13] == 'direction : "' and isComment == False and direction_found == False:
                                direction_found = True
                                dir_end = c.find('";')
                                direction = c[b+13:dir_end]
                        if direction == "input":
                            pin_info[0].append(x[y+7:pin_end])
                        if direction == "output":
                            pin_info[1].append(x[y+7:pin_end])
        pin_cells.append(pin_info)
    return pin_cells
                    
    
                
    
    
def make_cells(cells, functions, footprints, sequential, latch, pins):# Returns a dictionary wihere cell name is key and all other infromation is the value
   
    cell_dict = {}
    for x in cells:
        cell_info = []
        cell_info.append(functions[cells.index(x)])#0
        cell_info.append(footprints[cells.index(x)])#1
        cell_info.append(sequential[cells.index(x)])#2
        cell_info.append(latch[cells.index(x)])#3
        cell_info.append(pins[cells.index(x)])#4
        cell_dict[x] = cell_info
    return cell_dict
        
        
def map_cells(cells):#Returns dictionary where the key is the value 
    temp_names = []
    temp_dict = {}
    for e in cells:
        j = e[1:len(e)-1]
        temp_dict[e] = j
        temp_names.append(j)
    print(temp_dict)
    gate_type = {}
    file_gate = open("gate_list.txt")
    gates = file_gate.readlines()
    for x in cells:
        
        if cells[x][2] == [] and cells[x][3] == []:#Identifying if cell is non-sequential
            for name in gates:
                length = len(name)
                for y in range(length):
                     if name[y:y+2] == 'Y=':
                         if cells[x][0][0] == name[y+2:length-1]:
                             cell_name_end = name.find("\t")
                             gate_type[x] = name[:cell_name_end]
                         
                
            
        elif cells[x][3] != []:#Identifying if the cell is flop flop
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
            gate_type[x] = cell_type
        else:#Identifying if the cell is a latch
            cell_type = "DFF"
            for y in cells[x][2]:
                if y == "!CL":
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
                
            gate_type[x] = cell_type
    #print(gate_type)
    return gate_type, temp_dict
            
                
def make_library(gates, cells, names):#Writing to the KiCad sym file for each cell to create the liberty file. 
    print(gates)
    library = open("Library_Gates.txt")
    lines = library.readlines()
    library.close
    path = 'C:\\Users\\arjun\\OneDrive\\Documents\\Comp Sci Internship\\Sample_Library\\Test1.kicad_sym'
    sym = open(path, 'a')
    for gate in gates:
        gate = gate.strip('"')
        print(gate)
    
    for gate in gates:
        sym_lines = []
        for x in lines:
            
            if gates[gate] + "\n" == x:
                
                gate_start = lines.index(x)+1
                gate_end = ""
                found_end = False
                count = 0
                for c in lines[gate_start:]:
                    count = count+1
                    if c == "END\n" and found_end == False:
                        gate_end = lines[gate_start:].index(c)
                        found_end = True
                        
                
                for a in lines[gate_start:gate_start+gate_end]:
                    sym_lines.append(a)
                for g in range(len(sym_lines)):
                    for b in range(len(sym_lines[g])):
                        if sym_lines[g][b:b+len(gates[gate])] == gates[gate]:
                            sym_lines[g] = sym_lines[g][:b] + names[gate] + sym_lines[g][b+len(gates[gate]):]
                                   

                for l in sym_lines:
                    
                    l = l.replace(gates[gate], gate)
                pin_count = 0
                for t in range(len(sym_lines)):
                    for p in range(len(sym_lines[t])):
                        if sym_lines[t][p:p+14] == "pin input line":  
                            start = sym_lines[t+1].index('"')
                            temp = sym_lines[t+1][:start+1]+ cells[gate][4][0][pin_count] + sym_lines[t+1][start+2:]
                            sym_lines[t+1] = temp

                            pin_count = pin_count+1
                for line in sym_lines:
                    print(line)
                    sym.write(line)
                
                    
                
    sym.write(")")
                        
    
        

parser("sky130_Test4.lib")
