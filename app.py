import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuración de la cuenta
SUBDOMAIN = "crypnita"  # Cambia por tu subdominio
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNmMzAzNWFlNTBiYWQwNDRiMjEzNWZhOTA0ZDU1MjdhMjhmZTE5NDRkYzEwMTE2YzQ3NjM3Nzc3ODcxYTYyZjI4Zjg5ZmMyYjJiNGMzM2EyIn0.eyJhdWQiOiI4MzRkODQ5Mi1kYzM4LTRlODMtYjA2Zi02NDBiMTE3Y2ExNTgiLCJqdGkiOiJjZjMwMzVhZTUwYmFkMDQ0YjIxMzVmYTkwNGQ1NTI3YTI4ZmUxOTQ0ZGMxMDExNmM0NzYzNzc3Nzg3MWE2MmYyOGY4OWZjMmIyYjRjMzNhMiIsImlhdCI6MTc0MDA4MzQ1NiwibmJmIjoxNzQwMDgzNDU2LCJleHAiOjE3NTEyNDE2MDAsInN1YiI6IjEyNzQ5NzM1IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjM0MjAwODcxLCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZjg5MDY2MDktNzRhOS00YTM1LWJkZjAtMzBmMDkzYzQyYWYxIiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.AyhqWQVJ1dceWfxqj1QgvYITikZ9L3J0qpvuPEVcwBYyXqRJxkgAyogm-4BpofvhsGCTp0kd31MKcGlBq55SgnO63r818LHszNuO1jOfhTab3YbKGvNlKpBPAEMQj4Kaz7JoOzyE_yDnxQ-5AvUR3RWGpkxjG2e83Xz8quexrPApamMi2nxqBeLVaySiOmx7ax6AFfqyzDKZyiHMOf3XHCxr4jMAk-468NzLeqY_ZmphuT8Cld19ufMN4qa0XhO0a44OKPkoqeE8KTuSmiAYdA3f5Py4viHx9n9BtmjyW6owirco0FD1Z_uCVX6IZbUR_8Hck6qSJY3-z_iZmj4Rmg"  # Cambia por tu token de acceso


# URLs base para la API de Kommo
BASE_CONTACT_CUSTOMFIELDS_URL = f"https://{SUBDOMAIN}.kommo.com/api/v4/contacts/custom_fields"
BASE_LEAD_CUSTOMFIELDS_URL = f"https://{SUBDOMAIN}.kommo.com/api/v4/leads/custom_fields"
BASE_LEAD_COMPLEX_URL = f"https://{SUBDOMAIN}.kommo.com/api/v4/leads/complex"

# Encabezados de la solicitud para la autenticación
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def get_valid_location_ids():
    """Obtiene los IDs y valores para el campo Localidad"""
    url = f"{BASE_LEAD_CUSTOMFIELDS_URL}/459956"  # ID del campo Localidad
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        field_info = response.json()
        return [{"id": enum["id"], "value": enum["value"]} for enum in field_info.get("enums", [])]
    return []

def get_valid_shift_ids():
    """Obtiene los IDs y valores para el campo Turnos"""
    url = f"{BASE_LEAD_CUSTOMFIELDS_URL}/460300"  # ID del campo Turnos
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        field_info = response.json()
        return [{"id": enum["id"], "value": enum["value"]} for enum in field_info.get("enums", [])]
    return []

def get_valid_person_type_ids():
    """Obtiene los IDs y valores para el campo Tipo de Persona"""
    url = f"{BASE_CONTACT_CUSTOMFIELDS_URL}/459358"  # ID del campo Tipo de Persona
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        field_info = response.json()
        return [{"id": enum["id"], "value": enum["value"]} for enum in field_info.get("enums", [])]
    return []

def get_contact_field_ids():
    """Obtiene los IDs de los campos personalizados para teléfono y email de contactos"""
    response = requests.get(BASE_CONTACT_CUSTOMFIELDS_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error al obtener campos personalizados: {response.status_code}")
        return None, None

    custom_fields_response = response.json()
    custom_fields = custom_fields_response.get("_embedded", {}).get('custom_fields', [])

    # Imprime la respuesta completa para ver cómo están estructurados los campos
    print("Respuesta de los campos personalizados de contacto:", custom_fields_response)

    phone_field_id = None
    email_field_id = None

    for field in custom_fields:
        # Si sabes el código de los campos de teléfono y correo, puedes usarlos para identificarlos
        if field.get('code') == 'PHONE':  # Ajusta esto según el código correcto del campo de teléfono
            phone_field_id = field.get('id')
        elif field.get('code') == 'EMAIL':  # Ajusta esto según el código correcto del campo de email
            email_field_id = field.get('id')

    return phone_field_id, email_field_id

def create_lead_with_contact(data):
    """Crea un lead en Kommo con los datos del formulario"""
    # Obtener IDs de campos de contacto
    phone_field_id, email_field_id = get_contact_field_ids()
    if not phone_field_id or not email_field_id:
        return {"success": False, "message": "No se pudieron obtener los IDs de campos de contacto"}

    # Obtener los valores válidos para location_id y person_type_id
    #valid_location_ids = get_valid_location_ids()
    #valid_shift_ids = get_valid_shift_ids()  # Obtenemos los valores de los turnos
    #valid_person_type_ids = get_valid_person_type_ids()

    #print("Valores válidos para location_id:", valid_location_ids)  # Agregamos esta línea para depuración
    #print("Valores válidos para shift_id:", valid_shift_ids)  # Agregamos esta línea para depuración

    # Preparar los datos del contacto
    contact_data = {
        "name": data['contact_name'],
        "custom_fields_values": []
    }

    # Agregar teléfono
    if data['contact_phone'] and phone_field_id:
        contact_data["custom_fields_values"].append({
            "field_id": phone_field_id,
            "values": [{"value": data['contact_phone'], "enum_code": "MOB"}]
        })

    # Agregar email
    if data['contact_email'] and email_field_id:
        contact_data["custom_fields_values"].append({
            "field_id": email_field_id,
            "values": [{"value": data['contact_email']}]
        })


    # Agregar fecha de creación
    if data['creation_date']:
        contact_data["custom_fields_values"].append({
            "field_id": 460128,  # ID del campo de la fecha de creación
            "values": [{"value": data['creation_date']}]
        })

    # Agregar tipo de persona
    if data['person_type_id']:
        contact_data["custom_fields_values"].append({
            "field_id": 459358,  # ID del campo tipo de persona
            "values": [{"enum_id": int(data['person_type_id'])}]
        })


    # Preparar datos del lead
    lead_data = {
        "name": f"Lead de {data['contact_name']}",
        "custom_fields_values": [
            {"field_id": 459024, "values": [{"value": data['registrar_name']}]},
            {"field_id": 459956, "values": [{"enum_id": int(data['location_id'])}]},  # Localización en el lead
            {"field_id": 460300, "values": [{"enum_id": int(data['shift_id'])}]},  # Turno en el lead

        ],
        "_embedded": {
            "contacts": [contact_data]
        },
        "pipeline_id": 10588331
    }

    # Crear el lead
    response = requests.post(BASE_LEAD_COMPLEX_URL, json=[lead_data], headers=headers)
    if response.status_code == 200:
        return {"success": True, "message": "Lead registrado correctamente"}
    else:
        print(f"Error al crear lead: {response.status_code} - {response.text}")
        return {"success": False, "message": f"Error al crear lead: {response.status_code} - {response.text}"}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_location_options', methods=['GET'])
def location_options():
    locations = get_valid_location_ids()
    return jsonify({'locations': locations})

@app.route('/get_shift_options', methods=['GET'])
def shift_options():
    shifts = get_valid_shift_ids()
    return jsonify({'shifts': shifts})

@app.route('/get_person_type_options', methods=['GET'])
def person_type_options():
    person_types = get_valid_person_type_ids()
    return jsonify({'person_types': person_types})

@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    data = request.get_json()

    print("Datos recibidos:", data)  # Muestra los datos recibidos en el servidor

    # Llamar a la función para crear el lead con los datos del formulario
    result = create_lead_with_contact(data)

    if result['success']:
        return jsonify({"success": True, "message": result['message']})
    else:
        print("Error al crear el lead:", result)  # Mostrar el error en el servidor
        return jsonify({"success": False, "message": result['message']}), 400


if __name__ == '__main__':
    app.run(debug=True)
