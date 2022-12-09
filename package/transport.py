from flask_restful import Resource, Api, request
from package.model import conn

class Transports(Resource):
    """It contain all the api carryign the activity with aand specific transport"""

    def get(self):
        """Api to retive all the data from the database"""
        print("reached here")
        transports = conn.execute("SELECT * FROM transport  ORDER BY transport_id DESC").fetchall()
        return transports


    def post(self):
        """api to add the transport in the database"""
        transportInput = request.get_json(force=True)
        type=transportInput['type']
        quantity=transportInput['quantity']
        rental_cost=transportInput['rental_cost']
        project_id=transportInput['project_id']

        print("reached here")
        transportInput['transport_id']=conn.execute('''INSERT INTO transport(type,quantity,rental_cost,project_id)
            VALUES(?,?,?,?)''', (type,quantity,rental_cost,project_id)).lastrowid
        conn.commit()
        return transportInput

class Transport(Resource):
    """It contains all apis doing activity with the single transport entity"""

    def get(self,id):
        """api to retrive details of the data by it id"""

        transport = conn.execute("SELECT * FROM transport WHERE transport_id=?",(id,)).fetchall()
        return transport

    def delete(self,id):
        """api to delete the data by its id"""

        conn.execute("DELETE FROM transport WHERE transport_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the transport by it id"""

        transportInput = request.get_json(force=True)
        type=transportInput['type']
        quantity=transportInput['quantity']
        rental_cost=transportInput['rental_cost']
        project_id=transportInput['project_id']
        conn.execute("UPDATE transport SET type=?,quantity=?,rental_cost=?,project_id=? WHERE transport_id=?",
                     (type,quantity,rental_cost,project_id,id))
        conn.commit()
        return transportInput