import flask
import os
import json
from flask import request, session
from flask_assistant import Assistant, ask, tell, event, build_item
from flask_mail import Mail, Message

application = flask.Flask(__name__)
application.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'listadecomprabot@gmail.com',
	MAIL_PASSWORD = os.environ["EMAIL_PASS"]
	)
class ListToBuy(object):
    def __init__(self):
        self.list_to_buy = []

    def addProd(self,params):
        self.list_to_buy.append(params)

    def getProds(self):
        return self.list_to_buy

    def clear_list(self):
        self.list_to_buy = []
listBuy = ListToBuy()
assist = Assistant(application, project_id='listacompra-byoreq')
mail = Mail(application)



@assist.action('Añade a la lista Producto')
def webhook():
    print("*********WEBHOOK CALL**************", flush=True)
    req = json.loads(json.dumps(request.json))
    qres= req["queryResult"]
    params = qres['parameters']['Products']
    listBuy.addProd(params)
    speech = "Añadido a la lista, " + params
    return ask(speech)

@assist.action('Terminada la lista')
def endlist():
    print("*********WEBHOOK CALL**************", flush=True)
    
    if len(listBuy.getProds()) > 0:
        list_buy = ', '.join(listBuy.getProds())
        speech = "Perfecto, tienes en la lista "+ list_buy +". ¿Me dejas que te sugiera algo?. Una amborgesa"
    else:
        speech = "No tienes productos en la lista..."

    resp = ask(speech)

    print(resp,flush=True)
    #list_to_buy = []
    return ask(speech)


@assist.action('Respuesta sugerencia negativa')
def answer_neg():
    return ask('No lo añado entonces. ¿Podrías decirme tu correo para enviarte la lista?')

@assist.action('Dar email')
def email_act():
    print("*********WEBHOOK CALL**************", flush=True)
    req = json.loads(json.dumps(request.json))
    qres= req["queryResult"]
    params = qres['parameters']['Email']

    list_buy = ', '.join(listBuy.getProds())
    msg = Message("Lista de la Compra",
                    sender="listadecomprabot@gmail.com",
                    recipients=[params],
                    body="Lista de la compra: " + list_buy)
    try:
        mail.send(msg)
    except Exception as e:
	    print("Error con el correo: " + str(e), flush=True) 
    listBuy.clear_list()
    return tell("Gracias, lo enviaré a ese correo.")



@assist.action('Respuesta sugerencia afirmativa')
def answer_af():
    listBuy.addProd('amborgesa')
    list_buy = ', '.join(listBuy.getProds())
    return ask('Vale añado amborgesa a la lista. La lista seria: ' + list_buy +' .¿Podrías decirme tu correo para enviarte la lista?')

if __name__ == "__main__":
    application.run(debug=True,port=os.environ["PORT"])


