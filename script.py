import requests
import json
import hashlib

urlget = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=TOKEN'
request = requests.get(urlget)

filename = "answer.json"

with open(filename, "w") as file:
    file.write(request.text)

with open(filename) as file:
    data = json.load(file)
    encoding = file.encoding

numero_casas = data["numero_casas"]
frase = data["cifrado"]
alfabeto = "abcdefghijklmnopqrstuvwxyz"
res = ""
for letra in frase:
    if letra in alfabeto:
        pos = alfabeto.find(letra)
        pos = (pos - numero_casas)
        
        if pos >= len(alfabeto):
            pos = pos - len(alfabeto)
            res = res + alfabeto[pos]
        elif pos < 0:
            pos = len(alfabeto) + pos
            res = res + alfabeto[pos]      
        else:
            res = res + alfabeto[pos]
    else:
        res = res + letra

#print(res)

data["decifrado"] = res
resumo = hashlib.sha1(data["decifrado"].encode(encoding)).hexdigest()
data["resumo_criptografico"] = resumo

with open(filename, "w") as file:
        json.dump(data, file)

#print(data)

file = {'answer': open(filename, 'rb'), 'content-type': 'multipart/form-data'}

urlpost = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=TOKEN'
response = requests.post(urlpost, files=file)

print(response.status_code)
print(response.raise_for_status())