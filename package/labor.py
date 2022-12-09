from flask_restful import Resource, Api, request
from package.model import conn

class Labors(Resource):
    """It contain all the api carryign the activity with aand specific labor"""

    def get(self):
        """Api to retive all the data from the database"""
        print("reached here")
        labors = conn.execute("SELECT * FROM labor  ORDER BY labor_id DESC").fetchall()
        return labors


    def post(self):
        """api to add the labor in the database"""
        laborInput = request.get_json(force=True)
        type=laborInput['type']
        quantity=laborInput['quantity']
        salary=laborInput['salary']
        project_id=laborInput['project_id']

        print("reached here")
        if int(salary)>=0 or int(quantity)>=0:
            laborInput['labor_id']=conn.execute('''INSERT INTO labor(type,quantity,salary,project_id)
            VALUES(?,?,?,?)''', (type,quantity,salary,project_id)).lastrowid
        else:
            raise Exception("negative value detected")
        conn.commit()
        return laborInput

class Labor(Resource):
    """It contains all apis doing activity with the single labor entity"""

    def get(self,id):
        """api to retrive details of the data by it id"""

        labor = conn.execute("SELECT * FROM labor WHERE labor_id=?",(id,)).fetchall()
        return labor

    def delete(self,id):
        """api to delete the data by its id"""

        conn.execute("DELETE FROM labor WHERE labor_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the labor by it id"""

        laborInput = request.get_json(force=True)
        type=laborInput['type']
        quantity=laborInput['quantity']
        salary=laborInput['salary']
        project_id=laborInput['project_id']
        conn.execute("UPDATE labor SET type=?,quantity=?,salary=?,project_id=? WHERE labor_id=?",
                     (type,quantity,salary,project_id,id))
        conn.commit()
        return laborInput