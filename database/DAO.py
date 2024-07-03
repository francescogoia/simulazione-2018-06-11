from database.DB_connect import DBConnect



class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select year(s.`datetime`)as anno, count(s.id) as numAvvistamenti
            from sighting s 
            group by year(s.`datetime`)
            order by year(s.`datetime`) desc
        """
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append((row["anno"], row["numAvvistamenti"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct(s.state )
            from sighting s 
            where year(s.`datetime`) = %s
        """
        result = []
        cursor.execute(query, (anno, ))
        for row in cursor:
            result.append(row["state"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select s1.state as state1, s2.state as state2, s1.`datetime`, s2.`datetime`
            from sighting s1, sighting s2
            where year(s1.`datetime`) = %s and year(s1.`datetime`) = year(s2.`datetime`)
                and s1.state != s2.state
                and s2.`datetime` > s1.`datetime` 
            group by s1.state, s2.state
        """
        result = []
        cursor.execute(query, (anno, ))
        for row in cursor:
            result.append((row["state1"], row["state2"]))
        cursor.close()
        conn.close()
        return result










