from flask import Flask, render_template, request
import csv

app = Flask(__name__)


def carregar_notas_fiscais():
    try:
        with open('notas_fiscais.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def salvar_notas_fiscais(notas):
    with open('notas_fiscais.csv', 'w', newline='') as file:
        fieldnames = ['empresa', 'hospede', 'numero', 'data', 'valor_total',
                      'inicio_hospedagem', 'fim_hospedagem', 'tipo_tarifa']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(notas)


notas_fiscais = carregar_notas_fiscais()


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    if request.method == 'POST':
        empresa = request.form.get('empresa')
        hospede = request.form.get('hospede')
        numero = request.form.get('numero')
        data = request.form.get('data')
        valor_total = request.form.get('valor_total')
        inicio_hospedagem = request.form.get('inicio_hospedagem')
        fim_hospedagem = request.form.get('fim_hospedagem')
        tipo_tarifa = request.form.get('tipo_tarifa')
        nova_nota = {'empresa': empresa, 'hospede': hospede, 'numero': numero, 'data': data, 'valor_total': valor_total,
                     'inicio_hospedagem': inicio_hospedagem, 'fim_hospedagem': fim_hospedagem,
                     'tipo_tarifa': tipo_tarifa}
        notas_fiscais.append(nova_nota)
        salvar_notas_fiscais(notas_fiscais)
        return '', 201
    elif request.method == 'GET':
        return render_template('index.html', notas=notas_fiscais)
    elif request.method == 'DELETE':
        numero = request.args.get('numero')
        for nota in notas_fiscais:
            if nota['numero'] == numero:
                notas_fiscais.remove(nota)
                salvar_notas_fiscais(notas_fiscais)
                return '', 204
        return 'Nota não encontrada', 404


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=1985)
