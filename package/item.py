from flask_restful import Resource, Api, request
from package.model import conn

class Items(Resource):
    """It contain all the api carryign the activity with aand specific item"""

    def get(self):
        """Api to retive all the data from the database"""
        print("reached here")
        items = conn.execute("SELECT * FROM item  ORDER BY item_id DESC").fetchall()
        return items


    def post(self):
        """api to add the item in the database"""
        itemInput = request.get_json(force=True)
        type=itemInput['type']
        quantity=itemInput['quantity']
        cost=itemInput['cost']
        project_id=itemInput['project_id']

        print("reached here")
        if int(cost)>=0 or int(quantity)>=0:
            itemInput['item_id']=conn.execute('''INSERT INTO item(type,quantity,cost,project_id)
            VALUES(?,?,?,?)''', (type,quantity,cost,project_id)).lastrowid
        else:
            raise Exception("negative value detected")
        conn.commit()
        return itemInput

class Item(Resource):
    """It contains all apis doing activity with the single item entity"""

    def get(self,id):
        """api to retrive details of the data by it id"""

        item = conn.execute("SELECT * FROM item WHERE item_id=?",(id,)).fetchall()
        return item

    def delete(self,id):
        """api to delete the data by its id"""

        conn.execute("DELETE FROM item WHERE item_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the item by it id"""

        itemInput = request.get_json(force=True)
        type=itemInput['type']
        quantity=itemInput['quantity']
        cost=itemInput['cost']
        project_id=itemInput['project_id']
        conn.execute("UPDATE item SET type=?,quantity=?,cost=?,project_id=? WHERE item_id=?",
                     (type,quantity,cost,project_id,id))
        conn.commit()
        return itemInput