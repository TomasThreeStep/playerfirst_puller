import mysql.connector
from mysql.connector import connect
from pandas.core.config_init import sql_engine_doc


class Database:
    """Simple Class to make Accessing Databases easier, should be extended to be used"""
    def __init__(self,database):

        # with open("./src/mode", 'r')  as file:
        #     content = file.read().strip()
        #     if content == "Test":
        self.host = '34.70.1.204'
            # else:
        # self.host = '10.113.193.4'



        self.user = 'root'
        self.password = 'df?.z8KhF-l+c$^k'
        self.database = database

        self.connect()

    def connect(self):
        print("CONNECTING!!")
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def run_select(self, table_name, cols,where=None):
        """Runs Select with a list of cols, a table name, and an optional where statement. Returns List of Dictionary objects"""
        colStr = ""
        for col in cols:
            colStr +=  f"`{col}`,"
        colStr = colStr[0:len(colStr)-1]

        if where != None:
            sqlQuery = "SELECT %s FROM `%s` where %s;"%(colStr,table_name,where)
        else:
            sqlQuery = "SELECT %s FROM `%s`"%(colStr,table_name)

        self.cursor.execute(sqlQuery)

        rows = self.cursor.fetchall()

        dict_data = []
        for row in rows:
            dict = {}
            for i in range(0,len(cols)):
                dict[cols[i]] = row[i]
            dict_data.append(dict)

        return dict_data

    def run_email_select(self):

        sqlQuery = """
        SELECT 
        usr.`Login Email Address`,
        usr.`email_class`,
        usr.`email_conference`,
        usr.`email_offered_by`,
        usr.`email_position`,
        usr.`email_state`
        FROM football_4.database_users usr INNER JOIN football_4.database_colleges col ON usr.`Employers Name` = col.`id` 
        where usr.`get_daily_update` = 1 AND col.`trial_expire_date` > NOW() and usr.`active` = 1;
        """

        self.cursor.execute(sqlQuery)

        rows = self.cursor.fetchall()

        dict_data = []
        for row in rows:
            dict_data.append({
                "Login Email Address": row[0],
                "email_class": row[1],
                "email_conference": row[2],
                "email_offered_by": row[3],
                "email_position": row[4],
                "email_state": row[5],
            })
        return dict_data

    def run_distinct_select(self, table_name, cols,where=None):
        """Runs Select with a list of cols, a table name, and an optional where statement. Returns List of Dictionary objects"""
        colStr = ""
        for col in cols:
            colStr +=  f"`{col}`,"
        colStr = colStr[0:len(colStr)-1]

        if where != None:
            sqlQuery = "SELECT DISTINCT %s FROM `%s` where %s;"%(colStr,table_name,where)
        else:
            sqlQuery = "SELECT DISTINCT %s FROM `%s`"%(colStr,table_name)

        self.cursor.execute(sqlQuery)

        rows = self.cursor.fetchall()

        dict_data = []
        for row in rows:
            dict = {}
            for i in range(0,len(cols)):
                dict[cols[i]] = row[i]
            dict_data.append(dict)

        return dict_data

    def run_query(self,query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            connect()

            self.cursor.execute(query)
            self.connection.commit()

    def run_search(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()



class UCDatabase(Database):
    def __init__(self,database_name):
        self.database_name = database_name
        try:
            print("OPENING CONNECTION!!")
            super().__init__(
            database_name,
            )
        except:

            print("Trying Second!!")
            super().__init__(
                database_name,
            )



    def get_all_offers(self):
        return self.run_select("database_collegeoffers", [
            "Player ID",
            "school_name",
            "offer_date",
            "state",
        ],"`state` = 'offer'")

    def get_offers(self,player_id):
        return self.run_select("database_collegeoffers", [
            "Player ID",
            "school_name",
            "offer_date",
            "state",
        ], f"`Player ID` = '%s'" % player_id)

    def get_players(self):
        return self.run_select("database_masterlist", [
            "Player ID",
            "First",
            "Last",
            "Class",
            "School Name",
            "State",
            "Position Played",
            "Detailed College Offers",
            "College Offers",
            "Position Projected",
            "Player Head Shot",
            "Dbkey",
            "Player Twitter",
            "twoFourLocation",
            "timeline_scrape_url",
            "main_scrape_url",
            "Featured Player",
            "Modified"
        ], "`Detailed College Offers` IS NOT NULL ORDER BY `twoFourChecked` ASC, `Player ID` DESC;")

    def get_lookup_players(self):
        return self.run_select("database_masterlist", [
            "Player ID",
            "First",
            "Last",
            "Class",
            "School Name",
            "State",
            "Position Played",
            "Detailed College Offers",
            "College Offers",
            "Position Projected",
            "Player Head Shot",
            "Dbkey",
            "Player Twitter",
            "twoFourLocation",
            "timeline_scrape_url",
            "main_scrape_url",
            "Modified"
        ], "`class` >= 2026")

    def get_players_no_links(self):
        return self.run_select("database_masterlist", [
            "Player ID",
            "First",
            "Last",
            "Class",
            "School Name",
            "State",
            "Position Played",
            "Detailed College Offers",
            "College Offers",
            "Position Projected",
            "Player Head Shot",
            "Dbkey",
            "Player Twitter",
            "twoFourLocation",
            "timeline_scrape_url",
            "main_scrape_url",
            "Modified"
        ], "`class` >= 2026 AND `class` < 2030 AND `Detailed College Offers` IS NULL ORDER BY `Player ID` DESC")


    def get_players_with_links(self):
        return self.run_select("database_masterlist", [
            "Player ID",
            "First",
            "Last",
            "Class",
            "School Name",
            "State",
            "Position Played",
            "Detailed College Offers",
            "College Offers",
            "Position Projected",
            "Player Head Shot",
            "Dbkey",
            "Player Twitter",
            "Modified"
        ], "`Detailed College Offers` IS NOT NULL AND `class` >= 2025")



class CollegeNamesDatabase(Database):
    def __init__(self):
        try:
            super().__init__(
                "two_four_seven_name_match",
            )
        except:
            super().__init__(
                "two_four_seven_name_match",
            )


    def get_names(self):
        names = self.run_select("compare_colleges", [
            "uc_name",
            "two_four_seven_name",
            "avoided_words",
            "college_projection"
        ],)
        names.sort(key=lambda name: len(name["two_four_seven_name"]),reverse=True)
        return names




class ProxyDatabase(Database):
    def __init__(self):
        try:
            print("OPENING CONNECTION!!")
            super().__init__(
            "proxies",
            )
        except:

            print("Trying Second!!")
            super().__init__(
                'proxies',
            )

    def get_proxy_ips(self, claim_name, claim_number):

        all_list = self.run_distinct_select("cloud_proxies", [
            "internal_ip",
            "ip_address",
            "claimed_by"
        ])

        remaining_ips = []
        good_ret = []

        for ip in all_list:
            if ip["claimed_by"] == claim_name:
                good_ret.append(ip)
            else:
                remaining_ips.append(ip)
            if len(good_ret) >= claim_number:
                return good_ret

        for ip in remaining_ips:
            if ip["claimed_by"] is None and ip["claimed_by"] != "":
                self.run_query(f""" UPDATE proxies.cloud_proxies SET `claimed_by` = "{claim_name}" WHERE `ip_address` = "{ip["ip_address"]}" """)
                good_ret.append(ip)

            if len(good_ret) >= claim_number:
                return good_ret

        return all_list

    def delete_ip(self, internal_ip):
        self.run_query(f'DELETE FROM proxies.cloud_proxies where `internal_ip` = "{internal_ip}"')

    def delete_all_ips(self):
        self.run_query(f'DELETE FROM proxies.cloud_proxies')
