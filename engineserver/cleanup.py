def cleanup_database():
    db_lines = open("./database/sites.sdb").readlines()
    db_lines = [line.rstrip() for line in db_lines]

    with open("./database/sites.sdb", "w") as file:
        for current_line in db_lines:
            line_unique = []
            line_data = current_line.split()
            
        
            
            for current_value in line_data:
                if current_value not in line_unique: 
                    line_unique.append(current_value)
        
            for value in line_unique:
                file.write(value + " ")

            file.write("\n")