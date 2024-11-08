from flask import Flask, make_response, jsonify, request
import json

app = Flask("Personagens")
app.json.sort_keys = False

@app.route('/espaço', methods=['GET'])
def get_personagens():
    # Abre e carrega o arquivo JSON
    with open("personagens.json") as espaco:
        dados = json.load(espaco)

        # Obtém o parâmetro 'name' da URL, se presente
        name = request.args.get('name')

        # Filtra o personagem pelo nome se o 'name' foi passado
        filtrar = [f for f in dados["results"] if f.get('name') == name]

        # Verifica se o personagem foi encontrado
        if filtrar:
            return make_response(jsonify(filtrar), 200)

        # Se o 'name' não foi fornecido, retorna todos os resultados
        elif name is None:
            return make_response(jsonify(dados["results"]), 200)

        # Caso contrário, retorna uma lista vazia se o personagem não foi encontrado
        else:
            return make_response(jsonify([]), 200)

@app.route('/espaço', methods=['POST'])
def add_personagem():
    novo_personagem = request.json

    # Abre o arquivo JSON no modo leitura e escrita (r+)
    with open("personagens.json", "r+") as planeta:
        dados1 = json.load(planeta)

        # Adiciona o novo personagem à lista
        dados1["results"].append(novo_personagem)

        # Move o cursor para o início do arquivo e sobrescreve com o novo conteúdo
        planeta.seek(0)
        json.dump(dados1, planeta, indent=4)

        # Remove qualquer conteúdo residual antigo após a nova estrutura JSON
        planeta.truncate()

    return make_response(
        jsonify(mensagem="Pessoa cadastrada com sucesso", novo_personagem=novo_personagem), 
        201
    )

@app.route('/espaço', methods=['PUT'])
def update_personagem():
    # Obtém os dados do corpo da requisição (json)
    update = request.get_json()

    # Captura o nome do personagem da URL
    name = request.args.get('name')

    # Abre o arquivo JSON no modo leitura e escrita (r+)
    with open("personagens.json", "r+") as planeta:
        dados = json.load(planeta)

        # Filtra a lista para encontrar o personagem com o nome fornecido
        personagem_encontrado = False
        for personagem in dados["results"]:
            if personagem['name'] == name:
                personagem.update(update)
                personagem_encontrado = True
                break

    if personagem_encontrado:
        # Atualiza o arquivo JSON
        with open("personagens.json", "r+") as planeta:
            planeta.seek(0)
            json.dump(dados, planeta, indent=4)
            planeta.truncate()
        return make_response(jsonify({"message": "Personagem atualizado com sucesso!", "personagem": personagem}), 200)
    else:
        return jsonify({"error": "Personagem não encontrado"})
    

@app.route('/espaço', methods=['DELETE'])
def delete_personagens():
    # Captura o nome do personagem da URL
    name = request.args.get('name')
    if not name:
        return make_response(jsonify(message="Nome do personagem é obrigatório"), 400)

    # Abre e carrega o arquivo JSON
    with open("personagens.json", "r+") as arq:
        dados = json.load(arq)

        # Filtra a lista para encontrar e remover o personagem com o nome fornecido
        personagem_deletado = False
        for personagem in dados["results"]:
            if personagem['name'] == name:
                dados['results'].remove(personagem)
                personagem_deletado = True
                break

        if personagem_deletado:
            arq.seek(0)
            json.dump(dados, arq, indent=4)
            arq.truncate()
            return make_response(jsonify({"message": "Personagem deletado com sucesso!", "personagem": personagem}), 200)
        else:
            return jsonify({"error": "Personagem não encontrado"})

if __name__ == "__main__":
    app.run(debug=True)
