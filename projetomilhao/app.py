from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calcular_aportes():
    if request.method == 'POST':
        # Recebe os dados do formulário
        aporte_inicial = float(request.form['aporte_inicial'])
        aporte_mensal = float(request.form['aporte_mensal'])
        inflacao_ano_percentual = float(request.form['inflacao_ano'])
        rendimento_nominal_percentual = float(request.form['rendimento_nominal'])
        total_anos = int(request.form['total_anos'])

        # Cálculos (pegue do script atual)
        inflacao_ano = inflacao_ano_percentual / 100
        rendimento_nominal = rendimento_nominal_percentual / 100
        inflacao_mensal = (1 + inflacao_ano) ** (1 / 12) - 1
        rendimento_mensal = (1 + rendimento_nominal) ** (1 / 12) - 1

        saldo_final = aporte_inicial
        total_aportes = aporte_inicial

        for ano in range(1, total_anos + 1):
            for _ in range(12):
                aporte_mensal *= (1 + inflacao_mensal)
                saldo_final = saldo_final * (1 + rendimento_mensal) + aporte_mensal
                total_aportes += aporte_mensal

        ganhos_nominais = saldo_final - total_aportes
        rendimento_real = saldo_final - (total_aportes * (1 + inflacao_ano) ** total_anos)
        imposto_renda = ganhos_nominais * 0.15
        saldo_final_com_ir = saldo_final - imposto_renda

        valor_atual_sem_ir = saldo_final / ((1 + inflacao_ano) ** total_anos)
        valor_atual_com_ir = saldo_final_com_ir / ((1 + inflacao_ano) ** total_anos)

        # Envia os resultados para o HTML
        return render_template('index.html', resultados={
            'saldo_sem_ir': saldo_final,
            'saldo_com_ir': saldo_final_com_ir,
            'total_aportes': total_aportes,
            'ganhos_nominais': ganhos_nominais,
            'rendimento_real': rendimento_real,
            'imposto_renda': imposto_renda,
            'valor_atual_sem_ir': valor_atual_sem_ir,
            'valor_atual_com_ir': valor_atual_com_ir
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)