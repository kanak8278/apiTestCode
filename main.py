import json
import argparse
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def decrypt_data(encrypted_data, key, iv):
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(encrypted_data_bytes), AES.block_size)
    return pt.decode('utf-8')

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def make_api_call(config, api_key, key, iv, response_file):
    api_details = config['apis'][api_key]
    if api_key == 'case_otp_send' or api_key == 'case_otp_validate':
        url = f"{config['base_url']}{api_details['endpoint']}"
    else:
        url = f"{config['applicant_base_url']}{api_details['endpoint']}"
    headers = api_details['headers']
    print("Headers:", headers)
    body = json.dumps(api_details['body'])
    print("Body:", body)
    encrypted_body = encrypt_data(body, key, iv)
    print("Encrypt Body:", encrypted_body)
    response = requests.post(url, headers=headers, json={"data": encrypted_body})
    if response.status_code == 200:
        code = response.json()['code']
        if code.startswith('ERR'):
            response_data = code + ': ' + error_codes[code] 
        else:
            response_data = decrypt_data(response.json()['data'], key, iv)
    else:
        response_data = f"Error: {response.status_code}"

    with open(response_file, 'a') as file:
        file.write(f"\nAPI: {api_key}\nResponse: {response_data}\n")

    return response_data

# Load configuration and keys
config_file = 'config.json'
error_codes_file = 'error_codes.json'
key = b'7413690528pprrbb7413690528telela'
iv = b'telela7539508521'
config = load_json(config_file)
error_codes = load_json(error_codes_file)

# Extract API names from the config for the help message
api_names = list(config['apis'].keys())
api_list_string = '\n'.join(api_names)

# Custom help message
help_message = f'API Call Script\n\nAvailable APIs:\n{api_list_string}\n\nUsage: script.py [API_NAME] [--headers HEADERS_JSON] [--body BODY_JSON]'

# Setup command line argument parsing
parser = argparse.ArgumentParser(description=help_message, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('api_name', type=str, help='Name of the API to call')
parser.add_argument('--headers', type=str, help='JSON string for headers', default='{}')
parser.add_argument('--body', type=str, help='JSON string for body', default='{}')
args = parser.parse_args()

# Parse headers and body from JSON strings
try:
    custom_headers = json.loads(args.headers)
    custom_body = json.loads(args.body)
except json.JSONDecodeError:
    print("Invalid JSON format in headers or body arguments.")
    exit(1)

# Response file to save outputs
response_file = 'api_responses.txt'

# Call the specified API
api_key = args.api_name
if api_key in config['apis']:
    # Override config values with command line arguments
    config['apis'][api_key]['headers'].update(custom_headers)
    config['apis'][api_key]['body'].update(custom_body)

    print(f"\nCalling API: {api_key}")
    response = make_api_call(config, api_key, key, iv, response_file)
    
    print(f"Response:")
    print(response)
  
else:
    print(f"API {api_key} not found in configuration.")
