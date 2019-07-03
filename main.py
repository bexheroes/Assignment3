
import sys

get_input = sys.argv[1]

myfile = open(get_input,"r")
mydict =  dict()
outfile = open("out.txt","w")
outfile.close()

def do_it(something):
    outfile = open("out.txt","a")
    outfile.write(something+"\n")
    print(something)
    outfile.close()

for row in myfile:
    if len(row)>8:
        row_parts = row.split()
        instruction = row_parts[0]
        if(instruction=="CREATEHALL"):
            count_commands = len(row_parts) - 1
            if count_commands>2:
                do_it("Error: Too much parameters for creating a hall!")
            elif count_commands<2:
                do_it("Error: Not enough parameters for creating a hall!!")
            elif count_commands==2:
                hall_name = row_parts[1]
                if hall_name in mydict:
                    do_it("Warning: Cannot create the hall for the second time. The cinema has already "+hall_name)
                else:
                    rows_columns=row_parts[2]
                    if "x" in rows_columns:
                        rows_columns_split = rows_columns.split("x")
                        split_control = len(rows_columns_split)
                        if split_control!=2:
                            do_it("Error: Column and Row format must be number x number")
                        else:
                            rows = rows_columns_split[0]
                            columns = rows_columns_split[1]

                            count_now = 0
                            myarray = ["0","1","2","3","4","5","6","7","8","9"]
                            for k in str(rows):
                                if k in myarray:
                                    count_now+=1
                            count_now2 = 0
                            for k in str(columns):
                                if k in myarray:
                                    count_now2+=1

                            if len(str(rows))==count_now and len(str(columns))==count_now2:

                                rows = int(rows_columns_split[0])
                                columns = int(rows_columns_split[1])

                                if rows>26:
                                    do_it("Warning: Cannot create more than 26 rows for a hall")
                                else:
                                    hall = []
                                    for i in range(int(rows)):
                                        line_hall = []
                                        for j in range(int(columns)):
                                            line_hall.append(["free","undefined","undefined"])
                                        hall.append(line_hall)
                                    mydict[hall_name] = hall
                                    do_it("Hall \'"+hall_name+"\' having "+str(rows*columns)+" seats has been created")
                            else:
                                do_it("Error: Column and Row format must be number x number")
                    else:
                        do_it("Error: Column and Row format must be number x number")
        elif(instruction=="SELLTICKET"):
            customer_name = row_parts[1]
            fare_type = row_parts[2]
            if fare_type=="full" or fare_type=="student":
                which_hall =  row_parts[3]
                if which_hall in mydict:
                    count_commands = len(row_parts) - 4
                    if count_commands > 0 :
                        for i in range(count_commands):
                            asl_i = int(i + 4)
                            seat = row_parts[asl_i]
                            alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                            if seat[0] in alphabet:
                                which_row = alphabet.index(seat[0])
                                seat_without_row = seat[1:]
                                if "-" in seat_without_row:
                                    range_now = seat_without_row.split("-")
                                    range_start = int(range_now[0])
                                    range_end = int(range_now[1])-1
                                    max_row = len(mydict[which_hall])
                                    max_column = len((mydict[which_hall])[0])

                                    if max_row<=which_row:
                                        do_it("Error: Hall \""+which_hall+"\" has less row than the specified index "+seat+"! ")
                                    else:
                                        if(range_start>=0):
                                            if(range_end>=max_column):
                                                do_it("Error: The hall \""+which_hall+"\" has less column than the specified index "+seat+"! ")
                                            else:
                                                obtain = (mydict[which_hall])[which_row]
                                                is_free = 0
                                                for c in range(range_end-range_start+1):
                                                    if obtain[range_start+c][0]=="free":
                                                        is_free+=1
                                                if is_free == (range_end-range_start+1):
                                                    for c in range(range_end-range_start+1):
                                                        obtain[range_start+c][0]="full"
                                                        obtain[range_start+c][1]=customer_name
                                                        obtain[range_start+c][2]=fare_type
                                                    mydict[which_hall][which_row]=obtain
                                                    do_it("Success: "+customer_name+" has bought "+seat+" at "+which_hall+" ")
                                                else:
                                                    do_it("Warning: The seats "+seat+" cannot be sold to "+customer_name+" due some of them have already been sold!")
                                else:
                                    control_list = ["0","1","2","3","4","5","6","7","8","9"]
                                    count_something = 0
                                    for q in seat_without_row:
                                        if q in control_list:
                                            count_something+=1
                                    if count_something==len(seat_without_row):
                                        which_column = int(seat_without_row)
                                        max_row = len(mydict[which_hall])
                                        max_column = len((mydict[which_hall])[0])
                                        if which_row>=max_row:
                                            do_it("Error: The hall \""+which_hall+"\" has less row than the specified index "+seat+"! ")
                                        else:
                                            if(which_column>=max_column):
                                                do_it("Error: The hall \""+which_hall+"\" has less column than the specified index "+seat+"! ")
                                            else:
                                                obtain = (mydict[which_hall])[which_row]
                                                if obtain[which_column][0] == "free":
                                                    obtain[which_column][0] = "full"
                                                    obtain[which_column][1]=customer_name
                                                    obtain[which_column][2]=fare_type
                                                    mydict[which_hall][which_row] = obtain
                                                    do_it("Success: "+customer_name+" has bought "+seat+" at "+which_hall+" ")
                                                else:
                                                    do_it("Warning: The seat "+seat+" cannot be sold to "+customer_name+" since it was already sold!")
                                    else:
                                        do_it("Error: This \""+seat+"\" is out of seat format ")
                            else:
                                do_it("Error: This cinema hall doesn't include a seat like "+seat+" ")
                    else:
                        do_it("Error: You don't specified any seats to sell ")
                else:
                    do_it("Error: "+which_hall+" is not created yet so you can't sell ticket at this cinema hall ")
            else:
                do_it("Error: You should define fare type as student or full ")
        elif(instruction=="CANCELTICKET"):
            which_hall = row_parts[1]
            if which_hall in mydict:
                count_commands = len(row_parts) - 2
                for i in range(count_commands):
                    asl_i = i + 2
                    seat = row_parts[asl_i]
                    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                    if seat[0] in alphabet:
                        which_row = alphabet.index(seat[0])
                        seat_without_row = seat[1:]
                        if "-" in seat_without_row:
                            range_now = seat_without_row.split("-")
                            range_start = int(range_now[0])
                            range_end = int(range_now[1])
                            max_row = len(mydict[which_hall])
                            max_column = len((mydict[which_hall])[0])
                            if max_row<=which_row:
                                do_it("Error: The hall \""+which_hall+"\" has less row than the specified index "+seat+"! ")
                            else:
                                if(range_start>=0):
                                    if(range_end>=max_column):
                                        do_it("Error: The hall \""+which_hall+"\" has less column than the specified index "+seat+"! ")
                                    else:
                                        obtain = (mydict[which_hall])[which_row]
                                        is_free = 0
                                        for c in range(range_end-range_start+1):
                                            if obtain[range_start+c][0]=="full":
                                                is_free+=1
                                        if is_free>0:
                                            for c in range(range_end-range_start+1):
                                                full_seat_name = seat[0] + str(range_start+c)
                                                if obtain[range_start+c][0]== "free":
                                                    do_it("The seat "+full_seat_name+" at \""+which_hall+"\" has already been free! Nothing to cancel")
                                                else:
                                                    obtain[range_start+c][0]="free"
                                                    obtain[range_start+c][1]="undefined"
                                                    obtain[range_start+c][2]="undefined"
                                                    mydict[which_hall][which_row]=obtain
                                                    do_it("Success: The seat "+full_seat_name+" at "+which_hall+" has been canceled and now ready to sell again")
                                        else:
                                            do_it("The seats "+seat+" at \""+which_hall+"\" has already been free! Nothing to cancel")
                        else:
                            control_list = ["0","1","2","3","4","5","6","7","8","9"]
                            count_something = 0
                            for q in seat_without_row:
                                if q in control_list:
                                    count_something+=1
                            if count_something==len(seat_without_row):
                                which_column = int(seat_without_row)
                                max_row = len(mydict[which_hall])
                                max_column = len((mydict[which_hall])[0])
                                if(which_column>=max_column):
                                    do_it("Error: The hall \""+which_hall+"\" has less column than the specified index "+seat+"! ")
                                else:
                                    obtain = (mydict[which_hall])[which_row]
                                    if obtain[which_column][0] == "full":
                                        obtain[which_column][0] = "free"
                                        obtain[which_column][1] = "undefined"
                                        obtain[which_column][2] = "undefined"
                                        mydict[which_hall][which_row] = obtain
                                        do_it("Success: The seat "+seat+" at "+which_hall+" has been canceled and now ready to sell again")
                                    else:
                                        do_it("Error: The seat "+seat+" at \""+which_hall+"\" has already been free! Nothing to cancel")
                            else:
                                do_it("Error: This \""+seat+"\" is out of seat format to cancel ")
                    else:
                        do_it("Error: This cinema hall doesn't include a seat like "+seat+" to cancel ")
            else:
                do_it("Error: This hall \""+which_hall+"\" is not valid ")
        elif(instruction=="BALANCE"):
            count_commands = len(row_parts) - 1
            for i in range(count_commands):
                asl_i = i + 1
                hall = row_parts[asl_i]
                if hall in mydict:
                    count_student = 0
                    count_full = 0
                    all=mydict[hall]
                    for m in all:
                        for n in range(len(m)):
                            fare = m[n][2]
                            if fare=="student" :
                                count_student+=1
                            elif fare=="full":
                                count_full+=1
                    outfile = open("out.txt","a")
                    outfile.write("Hall report of \""+hall+"\" \n")
                    print("Hall report of \""+hall+"\" ")
                    outfile.write("-------------------------\n")
                    print("-------------------------")
                    outfile.write("Sum of students = "+str(count_student*5)+", Sum of full fares = "+str(count_full*10)+", Overall = "+str(count_student*5+count_full*10)+"\n")
                    print("Sum of students = "+str(count_student*5)+", Sum of full fares = "+str(count_full*10)+", Overall = "+str(count_student*5+count_full*10)+"")

                else:
                    do_it("Error: This cinema hall \""+hall+"\" is not exist")
        elif(instruction=="SHOWHALL"):
            hall = row_parts[1]
            if(len(row_parts)>2):
                do_it("SHOWHALL has more than 2 parameter")
            else:
                alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                if hall in mydict:
                    data = mydict[hall]
                    do_it("Printing hall layout of "+hall)
                    for i in range(len(data),0,-1):
                        real_i = i - 1
                        sub_data = mydict[hall][real_i]
                        mytext = ""
                        mytext = mytext + alphabet[real_i]
                        for j in sub_data:
                            if j[0]=="free":
                                mytext = mytext + " X "
                            else:
                                if j[2]=="student":
                                    mytext = mytext + " S "
                                else:
                                    mytext = mytext + " F "
                        do_it(mytext)
                    count_column = len(mydict[hall][0])
                    mytext2 = " "
                    for t in range(count_column):
                        if(t>9):
                            mytext2 = mytext2 + "" + str(t) + " "
                        else:
                            mytext2 = mytext2 + " " + str(t) + " "
                    do_it(mytext2)
                else:
                    do_it("Error: This cinema hall \""+hall+"\" is not exist")
