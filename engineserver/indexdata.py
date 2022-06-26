import engineserver.cleanup

class SearchDatabase:
    def __init__(self, database_data=None) -> None:
        self.database = database_data if database_data else {}



    def fetch_contents(self) -> None: pass

    def load_db(self, database_path="database/sites.sdb") -> None: 
        db_file = open(database_path).readlines()
        db_cont = [line.rstrip() for line in db_file]

        for line in db_cont:
            line_data = line.split()
            key = line_data[0]
            values = []

            for value in line_data[1:]: values.append(value)
            for value in values: self.add_value(key, value)

            

    def save_db(self, database_name="database/sites.sdb"):
        with open(database_name, "w") as db_file: 
            for key, value in self.database.items():
                db_file.write(key + " ")

                for site in value:
                    db_file.write(site + " ")
                
                db_file.write("\n")

    def fetch_value(self, key) -> None: 
        if key not in self.database.keys(): return None
        return self.database[key]

    def add_value(self, key, value) -> None: 
        if key not in self.database.keys(): self.database[key] = []
        self.database[key].append(value)


    def search(self, query: str):
        query_data = query.split()
        results = []


        for current_query in query_data:
            if current_query not in self.database.keys(): continue #If its not here, continue
            else: results.append(self.database[current_query])

        return results
                



class DescriptionDatabase:
    def __init__(self, database_data=None) -> None:
        self.database = database_data if database_data else {}



    def fetch_contents(self) -> None: return self.database

    def load_db(self, database_path="database/sitesdata.sdb") -> None: 
        db_file = open(database_path).readlines()
        db_cont = [line.rstrip() for line in db_file]

        for current_value in db_cont:
            value_data = current_value.split()
            url = value_data[0]
            title = value_data[1]
            desc  = value_data[2]

            self.add_value(url, title, desc)
        

    def save_db(self, database_name="database/sitesdata.sdb"):
        with open(database_name, "w") as db_file: 
            #print(self.database.items())
            for key, value in self.database.items():
                site_data = value

                db_file.write(key + " ")

                db_file.write(site_data["title"] + " ")
                db_file.write(site_data["desc"])

                db_file.write("\n")
        
        engineserver.cleanup.cleanup_database()        

    def fetch_value(self, url) -> None: 
        if url not in self.database.keys(): return None
        return self.database[url]

    def add_value(self, url: str, title: str, desc: str) -> None: 
        if url not in self.database.keys(): self.database[url] = []

        url = url.replace(" ", "%20").replace("\n", "&#10")
        desc = desc.replace(" ", "%20").replace("\n", "&#10")
        title = title.replace(" ", "%20").replace("\n", "&#10")

        self.database[url] = {"url": url, "title": title, "desc": desc}
        