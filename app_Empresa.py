from flask import Flask, Response,request
from  pymongo import MongoClient
import json
from bson.objectid import ObjectId


app = Flask(__name__)

# Connection with Mongo_Db
uri = "mongodb+srv://ricardofreitas:0BuxJlKWA0nwmoG4@google-cloud-sp.zgqqa.mongodb.net/test"
client = MongoClient(uri)
db = client.Empresas


@app.route("/companies", methods=['GET'])
def get_some_companies():
    try:
        data = list(db.company.find())
        for company_id in data:
            company_id["_id"] = str(company_id["_id"])
        print(data)
        return  Response( response = json.dumps(data), status =200,mimetype= "application/json")


    except Exception as ex:
        print(ex)
        return  Response( response = json.dumps({"message": "can't read companies"}), status =500,mimetype= "application/json")


########################################################################################
@app.route("/companies", methods=['POST'])
def create_company():
    try:
        company ={ "name": request.form["name"], "city":request.form["city"],"cnpj": request.form["cnpj"],"contact": request.form["contact"],"telephone": request.form["telephone"]}
        dbResponse = db.company.insert_one(company)
        print(dbResponse.inserted_id)
        return Response( response = json.dumps({"message": "company created","id":f"{dbResponse.inserted_id}"}), status =200,mimetype= "application/json")

    except Exception as ex:
        print(ex)
########################################################################################
@app.route("/companies/<id>", methods=['PUT'])
def update_company(id):
    try:
        dbResponse = db.company.update_one(
         {"_id": ObjectId(id)},{"$set":{"name": request.form ["name"]}})
        if dbResponse.modified_count == 1:
            return Response( response = json.dumps({"message": "company update "}), status =200,mimetype= "application/json")

        else:
            return Response( response = json.dumps({"message": "nothing to update"}), status =500,mimetype= "application/json")

    except Exception as ex:
        print(ex)

#######################################################################################
@app.route("/companies/<id>", methods=['DELETE'])
def delete_company(id):
    try:
        dbResponse = db.company.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response( response = json.dumps({"message": "company delete ", "id": f"{id}"}), status =200,mimetype= "application/json")

        else:
            return Response( response = json.dumps({"message": "company not delete ", "id": f"{id}"}), status =500,mimetype= "application/json")

    except Exception as ex:
        print(ex)
        return Response( response = json.dumps({"message": "sorry cannot delete company"}), status =500,mimetype= "application/json")
######################################################################################

if __name__ == "__main__":
    app.run()
