import random
import matplotlib.pyplot as plt
import numpy as np

class PlantaExperimental:
    def __init__(self, tipo):
        self.altura = 0.0  # cm
        self.saude = 100  # %
        self.frutos = 0
        self.tipo = tipo
        self.idade = 0
        self.fase = "germinacao"
        self.max_altura = 150.0
 
        # Nutrientes NPK (valores base em %)
        self.N = 70  # Nitrogênio (crescimento vegetativo)
        self.P = 70  # Fósforo (floração/frutificação)
        self.K = 70  # Potássio (saúde/resistência)

        # Ajustes iniciais conforme o tipo de tratamento
        if tipo == "NPK":
            self.N += 30  # Fertilizante NPK comercial (alto N)
            self.P += 20
            self.K += 10
        elif tipo == "choque":
            self.fator_choque = 1.15  # Efeito do choque elétrico
        elif tipo == "organico":
            self.N += 15  # Fertilizante orgânico (equilíbrio NPK)
            self.P += 10
            self.K += 15

        # Fatores ambientais iniciais
        self.temperatura = 25  # °C
        self.luz = 70  # %
        self.umidade = 60  # %

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

        # Fatores de influência do NPK (normalizados)
        fator_N = 1 + (self.N - 70) / 100  # Nitrogênio: impacto no crescimento
        fator_P = 1 + (self.P - 70) / 150  # Fósforo: impacto em flores/frutos
        fator_K = 1 + (self.K - 70) / 200  # Potássio: impacto na saúde

        # Taxa de crescimento base por fase (ajustada por NPK e ambiente)
        if self.fase == "germinacao":
            base = 0.3 * fator_N * (self.temperatura / 25) * (self.luz / 70) * (self.umidade / 60)
        elif self.fase == "vegetativa":
            base = 1.2 * fator_N * (self.temperatura / 25) * (self.luz / 70) * (self.umidade / 60)
        elif self.fase == "floracao":
            base = 0.7 * fator_P * (self.temperatura / 25) * (self.luz / 70) * (self.umidade / 60)
        else:  # frutificacao
            base = 0.2 * fator_P * (self.temperatura / 25) * (self.luz / 70) * (self.umidade / 60)

        # Efeito do choque elétrico (se aplicável)
        if self.tipo == "choque" and energia_choque > 0:
            base *= self.fator_choque
            self.saude = max(50, self.saude - random.uniform(1.0, 2.0))

        # Limitação de crescimento (função sigmoidal)
        ponto_transicao = self.max_altura * 0.7
        fator_saturacao = 1 / (1 + np.exp(0.08 * (self.altura - ponto_transicao)))
        self.altura = min(self.altura + base * fator_saturacao * random.uniform(0.95, 1.05), self.max_altura)

        # Consumo de nutrientes (variação aleatória e fase dependente)
        if self.fase == "vegetativa":
            self.N = max(0, self.N - random.uniform(0.8, 2.0))
            self.P = max(0, self.P - random.uniform(0.2, 0.8))
            self.K = max(0, self.K - random.uniform(0.1, 0.5))
        elif self.fase == "floracao" or self.fase == "frutificacao":
            self.N = max(0, self.N - random.uniform(0.3, 1.0))
            self.P = max(0, self.P - random.uniform(0.3, 1.0))  # Reduzir consumo de fósforo
            self.K = max(0, self.K - random.uniform(0.2, 0.8))
        else:
            self.N = max(0, self.N - random.uniform(0.5, 1.5))
            self.P = max(0, self.P - random.uniform(0.3, 1.0))
            self.K = max(0, self.K - random.uniform(0.2, 0.8))

        # Saúde influenciada pelo Potássio (K) e estresse
        self.saude = min(100, self.saude + 0.2 * fator_K + random.uniform(-0.5, 0.5))

        # Produção de frutos (depende de Fósforo, saúde e estresse)
        if self.fase == "frutificacao" and self.saude > 65:
            if random.random() < 0.2 * (self.P / 100) * (self.luz / 70):  # Aumentar probabilidade e adicionar fator de luz
                self.frutos += 1

        # Variação ambiental diária
        self.temperatura += random.uniform(-1, 1)
        self.luz += random.uniform(-5, 5)
        self.umidade += random.uniform(-3, 3)


class SistemaEnergiaLab:
    def __init__(self):
        self.energia_armazenada = 1.0
        self.tensao = 15
        self.corrente = 4e-6

    def gerar_energia(self):
        self.energia_armazenada = min(1.5, self.energia_armazenada + 0.6)

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
    "Controle": PlantaExperimental("controle"),
    "NPK": PlantaExperimental("NPK"),
    "Choque": PlantaExperimental("choque")
}

sistema_energia = SistemaEnergiaLab()
dados = {tipo: {"altura": [], "saude": [], "frutos": [], "N": [], "P": [], "K": []} for tipo in plantas}
dados["energia"] = []

# Simulação principal
tempo_choque_diario = 10  # minutos
for dia in range(dias_experimento):
    sistema_energia.gerar_energia()
    energia_choque = sistema_energia.aplicar_choque(tempo_choque_diario) if dia > 0 else 0.0

    for tipo, planta in plantas.items():
        if tipo == "Choque" and energia_choque > 0:
            planta.crescer(energia_choque)
        else:
            planta.crescer()

        # Registrar dados
        dados[tipo]["altura"].append(planta.altura)
        dados[tipo]["saude"].append(planta.saude)
        dados[tipo]["frutos"].append(planta.frutos)
        dados[tipo]["N"].append(planta.N)
        dados[tipo]["P"].append(planta.P)
        dados[tipo]["K"].append(planta.K)

    dados["energia"].append(sistema_energia.energia_armazenada)


# Visualização
plt.figure(figsize=(16, 12))
cores = {"Controle": "blue", "NPK": "green", "Choque": "red"}

# Gráfico de Altura
plt.subplot(3, 2, 1)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["altura"], color=cor, label=tipo)
plt.title("Crescimento das Plantas")
plt.ylabel("Altura (cm)")
plt.legend()
plt.grid(True)

# Gráfico de Frutos
plt.subplot(3, 2, 2)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["frutos"], color=cor, label=tipo)
plt.title("Produção de Frutos")
plt.ylabel("Número de Frutos")
plt.legend()
plt.grid(True)

# Gráfico de Saúde
plt.subplot(3, 2, 3)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["saude"], color=cor, label=tipo)
plt.title("Saúde das Plantas")
plt.ylabel("Saúde (%)")
plt.ylim(50, 105)
plt.legend()
plt.grid(True)

# Gráfico de Nitrogênio (N)
plt.subplot(3, 2, 4)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["N"], color=cor, label=tipo)
plt.title("Níveis de Nitrogênio (N)")
plt.ylabel("Concentração (%)")
plt.legend()
plt.grid(True)

# Gráfico de Fósforo (P)
plt.subplot(3, 2, 5)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["P"], color=cor, label=tipo)
plt.title("Níveis de Fósforo (P)")
plt.ylabel("Concentração (%)")
plt.legend()
plt.grid(True)

# Gráfico de Potássio (K)
plt.subplot(3, 2, 6)
for tipo, cor in cores.items():
    plt.plot(dados[tipo]["K"], color=cor, label=tipo)
plt.title("Níveis de Potássio (K)")
plt.ylabel("Concentração (%)")
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
    print(f"  N final: {dados[tipo]['N'][-1]:.1f}%")
    print(f"  P final: {dados[tipo]['P'][-1]:.1f}%")
    print(f"  K final: {dados[tipo]['K'][-1]:.1f}%")
