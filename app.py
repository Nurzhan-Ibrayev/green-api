from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {}
    if request.method == 'POST':
        form_data = request.form.to_dict()
        id_instance = form_data.get('idInstance')
        api_token_instance = form_data.get('apiTokenInstance')

        phone_number_mes = form_data.get('phoneNumberMessage')
        phone_mes = form_data.get('phoneMessage')
        phone_number_file = form_data.get('phoneNumberFile')
        file_url = form_data.get('fileUrl')
        file_name = form_data.get('fileName')
        
        if id_instance:
            api_url = f"https://{id_instance[:4]}.api.greenapi.com"

        if 'get_settings' in form_data:
            result = get_settings(api_url, id_instance, api_token_instance)
        elif 'get_state_instance' in form_data:
            result = get_state_instance(api_url, id_instance, api_token_instance)
        elif 'send_message' in form_data:
            if phone_number_mes:
                result = send_message(api_url, id_instance, api_token_instance, phone_number_mes, phone_mes)
            else:
                result = "Phone number is required for sending a message."
        elif 'send_file_by_url' in form_data:
            if phone_number_file and file_url:
                result = send_file_by_url(api_url, id_instance, api_token_instance, phone_number_file, file_url, file_name)
            else:
                result = "Both phone number and file URL are required for sending a file by URL."

    return render_template('index.html', result=result, form_data=form_data)

def get_settings(api_url, id_instance, api_token_instance):
    url = f"{api_url}/waInstance{id_instance}/getSettings/{api_token_instance}"
    response = requests.get(url)
    return response.json()

def get_state_instance(api_url, id_instance, api_token_instance):
    url = f"{api_url}/waInstance{id_instance}/getStateInstance/{api_token_instance}"
    response = requests.get(url)
    return response.text

def send_message(api_url, id_instance, api_token_instance, phone_number, phone_mes):
    url = f"{api_url}/waInstance{id_instance}/sendMessage/{api_token_instance}"
    
    payload = {
        "chatId": f"{phone_number}@c.us",
        "message": f"{phone_mes}"
        }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return response.text

def send_file_by_url(api_url, id_instance, api_token_instance, phone_number, file_url, file_name):
    url = f"{api_url}/waInstance{id_instance}/sendFileByUrl/{api_token_instance}"
    payload = {
        "chatId": f"{phone_number}@c.us",
        "urlFile": file_url,
        "fileName": file_name,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
