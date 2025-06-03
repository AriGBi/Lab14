from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from stores s 

            """

        cursor.execute(query)
        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(store_id):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders o
                    where o.store_id =%s 

                """

        cursor.execute(query, (store_id,))
        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchi(maxGiorni, store_id, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.ID1 as id1, t.ID2 as id2, (oi1.quantita+oi2.quantita) as peso
        from ( select o.order_id as ID1, o2.order_id as ID2, o.order_date as data1, o2.order_date as data2
         from orders o, orders o2
        where o.order_id>o2.order_id  and datediff(o.order_date, o2.order_date)<%s and o.store_id=o2.store_id and o.store_id=%s and o.order_date-o2.order_date>0
        )t , (select oi.order_id as id, sum(oi.quantity) as quantita
        from order_items oi 
        group by oi.order_id) oi1, (select oi.order_id as id, sum(oi.quantity) as quantita
        from order_items oi 
        group by oi.order_id )oi2
        where t.ID1=oi1.id and t.ID2=oi2.id
        group by t.ID1, t.ID2
                        """

        cursor.execute(query, (maxGiorni,store_id))
        for row in cursor:
            result.append(Arco(idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

