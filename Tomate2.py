import random
import matplotlib.pyplot as plt
import numpy as np

class PlantaExperimental:
    def __init__(self, tipo):
        self.altura = 0.0  # cm
        self.saude = 100    # %
        self.nutrientes = 100  # %
        self.frutos = 0
        self.tipo = tipo
        self.idade = 0
        self.fase = "germinacao"
        self.max_altura = 150.0

        # Parâmetros realistas ajustados
        if tipo == "fertilizante":
            self.fator_crescimento = 1.25  # +25% mais realista
            self.consumo_nutrientes = 0.8
        elif tipo == "choque":
            self.fator_crescimento = 1.0
            self.consumo_nutrientes = 1.3  # Maior consumo de nutrientes
        else:
            self.fator_crescimento = 1.0
            self.consumo_nutrientes = 1.0

    def atualizar_fase(self):
        if self.idade < 10:
            nova_fase = "germinacao"
        elif 10 <= self.idade < 30:
            nova_fase = "vegetativa"
        elif 30 <= self.idade < 50:
            nova_fase = "floracao"
        else:
            nova_fase = "frutificacao"
            
        if nova_fase != self.fase:
            self.fase = nova_fase

    def crescer(self, energia_choque=0):
        self.idade += 1
        self.atualizar_fase()

        # Taxas de crescimento realistas por fase
        if self.fase == "germinacao":
            base = 0.3  # Crescimento lento inicial
        elif self.fase == "vegetativa":
            base = 1.2  # Reduzido para evitar crescimento explosivo
        elif self.fase == "floracao":
            base = 0.7
        else:
            base = 0.2  # Foco na frutificação

        crescimento_diario = base * self.fator_crescimento

        # Efeito do choque ajustado
        if self.tipo == "choque" and energia_choque > 0:
            crescimento_diario *= 1.15  # Bônus mais conservador
            self.saude = max(50, self.saude - random.uniform(1.0, 2.0))

        # Fator de saturação sigmoidal melhorado
        ponto_transicao = self.max_altura * 0.7
        fator_saturacao = 1 / (1 + np.exp(0.08 * (self.altura - ponto_transicao)))
        crescimento_diario *= fator_saturacao * random.uniform(0.95, 1.05)

        # Atualização única da altura
        self.altura = min(self.altura + crescimento_diario, self.max_altura)

        # Sistema de nutrientes e saúde
        self.nutrientes -= self.consumo_nutrientes * random.uniform(0.8, 1.2)
        self.nutrientes = max(0, self.nutrientes)
        self.saude = min(100, self.saude + random.uniform(0.1, 0.4))

        # Produção de frutos mais realista
        if self.fase == "frutificacao" and self.nutrientes > 40 and self.saude > 70:
            if random.random() < 0.12 * (self.saude/100):  # Chance reduzida
                self.frutos += 1

class SistemaEnergiaLab:
    def __init__(self):
        self.energia_armazenada = 1.0
        self.tensao = 15
        self.corrente = 4e-6

    def gerar_energia(self):
        self.energia_armazenada = min(1.5, self.energia_armazenada + 0.6)  # Recarga mais lenta

    def aplicar_choque(self, tempo_minutos):
        tempo_segundos = tempo_minutos * 60
        energia_necessaria = self.tensao * self.corrente * tempo_segundos
        if self.energia_armazenada >= energia_necessaria:
            self.energia_armazenada -= energia_necessaria
            return energia_necessaria
        return 0.0

# Configuração do experimento
dias_experimento = 90
plantas = {
    "Fertilizante": PlantaExperimental("fertilizante"),
    "Controle": PlantaExperimental("controle"),
    "Choque": PlantaExperimental("choque")
}

sistema_energia = SistemaEnergiaLab()
dados = {tipo: {"altura": [], "saude": [], "nutrientes": [], "frutos": [], "fase": []} for tipo in plantas}
dados["energia"] = []

# Simulação principal
tempo_choque_diario = 20  # minutos
for dia in range(dias_experimento):
    sistema_energia.gerar_energia()
    energia_choque = sistema_energia.aplicar_choque(tempo_choque_diario) if dia > 0 else 0.0
    
    for tipo, planta in plantas.items():
        if tipo == "Choque" and energia_choque > 0:
            planta.crescer(energia_choque)
        else:
            planta.crescer()
        
        # Registrar dados
        for key in dados[tipo]:
            dados[tipo][key].append(getattr(planta, key.lower()) if key != "fase" else planta.fase)
    
    dados["energia"].append(sistema_energia.energia_armazenada)
    
    # Log parcial
    if dia % 15 == 0:
        print(f"Dia {dia}: {plantas['Choque'].fase} | Energia {sistema_energia.energia_armazenada:.2f}J | " +
              f"Choque: {plantas['Choque'].altura:.1f}cm, {plantas['Choque'].frutos} frutos")

# Visualização
plt.figure(figsize=(14, 10))
cores = {"Fertilizante": "green", "Controle": "blue", "Choque": "red"}

# Gráfico de Crescimento
plt.subplot(2, 2, 1)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["altura"], color=cor, label=tipo)
    
# Marcadores de fase
for fase_dia, fase_nome in [(10, "Vegetativa"), (30, "Floração"), (50, "Frutificação")]:
    plt.axvline(x=fase_dia, color='gray', linestyle=':', alpha=0.5)
    plt.text(fase_dia+5, 10, fase_nome, rotation=90, va='bottom')

plt.title("Crescimento de Tomateiros por Fase")
plt.ylabel("Altura (cm)")
plt.legend()
plt.grid(True)

# Gráfico de Frutos
plt.subplot(2, 2, 2)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["frutos"], color=cor, label=tipo)
plt.title("Produção de Frutos")
plt.ylabel("Número de Frutos")
plt.legend()
plt.grid(True)

# Gráfico de Saúde
plt.subplot(2, 2, 3)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["saude"], color=cor, label=tipo)
plt.title("Saúde das Plantas")
plt.ylabel("Saúde (%)")
plt.ylim(50, 105)
plt.legend()
plt.grid(True)

# Gráfico de Energia
plt.subplot(2, 2, 4)
plt.plot(dados["energia"], 'orange', label='Energia Disponível')
plt.title("Energia no Sistema (15V, 4μA)")
plt.ylabel("Joules (J)")
plt.axhline(y=0.072, color='red', linestyle='--', label='Energia por choque')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Resultados finais
print("\n=== RESULTADOS FINAIS ===")
for tipo in plantas:
    print(f"\n{tipo}:")
    print(f"  Altura final: {dados[tipo]['altura'][-1]:.1f} cm")
    print(f"  Frutos produzidos: {dados[tipo]['frutos'][-1]}")
    print(f"  Saúde final: {dados[tipo]['saude'][-1]:.1f}%")
    print(f"  Nutrientes finais: {dados[tipo]['nutrientes'][-1]:.1f}%")
    print(f"  Dias em frutificação: {sum(1 for fase in dados[tipo]['fase'] if fase == 'frutificacao')}")

print(f"\nEnergia média disponível: {np.mean(dados['energia']):.3f} J")
print(f"Total de choques aplicados: {sum(1 for e in dados['energia'] if e < 1.0)}")