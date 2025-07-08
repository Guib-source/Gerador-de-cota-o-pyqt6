import json, os
from PyQt6.QtWidgets import QMessageBox

def caminho_json():
    return os.path.join(os.path.dirname(__file__), "..", "data", "aeroportos.json")

def carregar_aeroportos():
    with open(caminho_json(), encoding="utf-8") as f:
        dados = json.load(f)
    return [f"{item['Cidade']} ({item['IATA']})" for item in dados]

def salvar_aeroporto(cidade: str, iata: str):
    caminho = caminho_json()
    with open(caminho, encoding='utf-8') as f:
        dados = json.load(f)
    
    if any(item['IATA'].upper() == iata.upper() for item in dados):
        QMessageBox.warning(None, 'Duplicado', f'O aeroporto com IATA {iata.upper()} já existe.')
        return False
    
    novo = {'Cidade': cidade.title(), 'IATA': iata.upper()}
    dados.append(novo)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f , indent=2, ensure_ascii=False)
    return True