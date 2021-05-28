from flask import Flask, Response,request
from  pymongo import MongoClient
import json
from bson.objectid import ObjectId


app = Flask(__name__)

# Connection with Mongo_Db
uri = "mongodb+srv://ricardofreitas:0BuxJlKWA0nwmoG4@google-cloud-sp.zgqqa.mongodb.net/test"
client = MongoClient(uri)
db = client.Curriculos


@app.route("/curriculos", methods=['GET'])
def buscar_curriculos():
    try:
        data = list(db.Curriculo.find())
        for curriculo_id in data:
            curriculo_id["_id"] = str(curriculo_id["_id"])
        print(data)
        return  Response( response = json.dumps(data), status =200,mimetype= "application/json")


    except Exception as ex:
        print(ex)
        return  Response( response = json.dumps({"message": "Não foi possível buscar os curriculos"}), status =500,mimetype= "application/json")


########################################################################################
@app.route("/curriculos", methods=['POST'])
def criar_curriculo():
    try:
        curriculo ={ "nome": request.form["nome"], "email":request.form["email"],"telefone": request.form["telefone"],"endereco": request.form["endereco"],"cidade": request.form["cidade"],"idade": request.form["idade"],"resumo": request.form["resumo"] }
        dbResponse = db.Curriculo.insert_one(curriculo)
        print(dbResponse.inserted_id)
        return Response( response = json.dumps({"message": "Curriculo criado","id":f"{dbResponse.inserted_id}"}), status =200,mimetype= "application/json")

    except Exception as ex:
        print(ex)
########################################################################################
@app.route("/curriculos/<id>", methods=['PUT'])
def atualizar_curriculo(id):
    try:
        dbResponse = db.Curriculo.update_one(
         {"_id": ObjectId(id)},{"$set":{"nome": request.form ["nome"]}})
        if dbResponse.modified_count == 1:
            return Response( response = json.dumps({"message": "Curriculo atualizado "}), status =200,mimetype= "application/json")

        else:
            return Response( response = json.dumps({"message": "nada para atualizar"}), status =500,mimetype= "application/json")

    except Exception as ex:
        print(ex)

#######################################################################################
@app.route("/curriculos/<id>", methods=['DELETE'])
def deletar_curriculo(id):
    try:
        dbResponse = db.Curriculo.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response( response = json.dumps({"message": "Curriculo deletado", "id": f"{id}"}), status =200,mimetype= "application/json")

        else:
            return Response( response = json.dumps({"message": "Curriculo não deletado ", "id": f"{id}"}), status =500,mimetype= "application/json")

    except Exception as ex:
        print(ex)
        return Response( response = json.dumps({"message": "Desculpe não posso deletar o curriculo"}), status =500,mimetype= "application/json")
######################################################################################

if __name__ == "__main__":
    app.run()
