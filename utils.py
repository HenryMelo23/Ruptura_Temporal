import json
import hashlib
import os

def calcular_hash(dados: dict) -> str:
    dados_sem_hash = {k: v for k, v in dados.items() if k != "hash"}
    conteudo = json.dumps(dados_sem_hash, sort_keys=True).encode()
    return hashlib.sha256(conteudo).hexdigest()

def salvar_upgrade_aureas(caminho, upgrades):
    data = {
        "upgrades": upgrades
    }
    upgrades_str = json.dumps(upgrades, sort_keys=True)
    hash_obj = hashlib.sha256(upgrades_str.encode())
    data["assinatura"] = hash_obj.hexdigest()

    with open(caminho, "w") as f:
        json.dump(data, f)


def carregar_upgrade_aureas(caminho):
    nomes_validos = ["Racional", "Impulsiva", "Devota", "Vanguarda"]
    try:
        if not os.path.exists(caminho):
            return {nome: 0 for nome in nomes_validos}

        with open(caminho, "r") as f:
            data = json.load(f)
            upgrades = data.get("upgrades", {})
            assinatura = data.get("assinatura", "")

            upgrades_str = json.dumps(upgrades, sort_keys=True)
            hash_valido = hashlib.sha256(upgrades_str.encode()).hexdigest()

            if hash_valido != assinatura:
                return {nome: 0 for nome in nomes_validos}

            # Preenche chaves ausentes
            for nome in nomes_validos:
                if nome not in upgrades:
                    upgrades[nome] = 0

            return upgrades
    except Exception as e:
        print(f"[Erro ao carregar upgrades]: {e}")
        return {nome: 0 for nome in nomes_validos}


    return upgrades
