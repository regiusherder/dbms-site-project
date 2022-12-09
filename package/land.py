from flask_restful import Resource, Api, request
from package.model import conn

class Lands(Resource):
    """It contain all the api carryign the activity with aand specific land"""

    def get(self):
        """Api to retive all the data from the database"""
        print("reached here")
        lands = conn.execute("SELECT * FROM land  ORDER BY land_id DESC").fetchall()
        return lands


    def post(self):
        """api to add the land in the database"""
        landInput = request.get_json(force=True)
        type=landInput['type']
        size=landInput['size']
        cost=landInput['cost']
        location=landInput['location']
        project_id=landInput['project_id']
        if cost>=0 and size>=0:
            print("reached here")
            landInput['land_id']=conn.execute('''INSERT INTO land(type,size,cost,location,project_id)
                VALUES(?,?,?,?,?)''', (type,size,cost,location,project_id)).lastrowid
            conn.commit()
        else:
            raise Exception("negative value detected")
        return landInput

class Land(Resource):
    """It contains all apis doing activity with the single land entity"""

    def get(self,id):
        """api to retrive details of the data by it id"""

        land = conn.execute("SELECT * FROM land WHERE land_id=?",(id,)).fetchall()
        return land

    def delete(self,id):
        """api to delete the data by its id"""

        conn.execute("DELETE FROM land WHERE land_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the land by it id"""

        landInput = request.get_json(force=True)
        type=landInput['type']
        size=landInput['size']
        cost=landInput['cost']
        location=landInput['location']
        project_id=landInput['project_id']
        conn.execute("UPDATE land SET type=?,size=?,cost=?,location=?,project_id=? WHERE land_id=?",
                     (type,size,cost,location,project_id,id))
        conn.commit()
        return landInput