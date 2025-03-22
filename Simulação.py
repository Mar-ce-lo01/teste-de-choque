import random
import matplotlib.pyplot as plt

# Parâmetros inicias
energia_bateria = 0.0 # Energia da bateria
capacidade_bateria = 10.0 # Capacidade da bateria  
energia_por_impacto = 0.05 # Energia garada por impacto piezoelétrico
choque_energia = 0.01 # Energia por choque

# Taxas de crescimento hipotese (cm/dia)
crecimento_fertilizante = 0.15 # Crescimento com fertilizante (cm/dia)
crecimneto_controle = 0.10 # Crescimento sem fertilizante (cm/dia)
crecimento_choque = 0.12 # Crescimento com choque eletrico (cm/dia)

# Tamanho inicial das alfaces (cm)
alface_fertilizante = 0.0 
alface_controle = 0.0
alface_choque = 0.0


# Função para gerar energia piezoelétrica
tempo = []
tam_fertilizante = []
tam_contole = []
tam_choque = []
enetgia = []

def gerara_energia():
    global energia_bateria
    impacto = random.uniform(0.03, 0.07)
    if energia_bateria + impacto <= capacidade_bateria:
        energia_bateria += impacto
    else:
        energia_bateria = capacidade_bateria  
        return impacto

# Função para aplicar choque no vaso 3   
def gerar_choque():
    global energia_bateria, alface_choque
    if energia_bateria >= choque_energia:
        energia_bateria -= choque_energia
        alface_choque += crecimento_choque * random.uniform(0.8, 1.2)
        return True
    return False

# Simulçao principal (30 "dias")
print("Simulação do experimento com 3 vasos de alface...")
for t in range(30):
    gerara_energia()

    alface_fertilizante += crecimento_fertilizante * random.uniform(0.8, 1.2)
    alface_controle += crecimneto_controle * random.uniform(0.8, 1.2)
    if t % 5 == 0 and t > 0:
        if gerar_choque():
            print(f"Dia {t+1}: Choque aplicado! Energia restante: {energia_bateria:.2f} J")
    

    tempo.append(t + 1)
    tam_fertilizante.append(alface_fertilizante)
    tam_contole.append(alface_controle)
    tam_choque.append(alface_choque)
    enetgia.append(energia_bateria)

# Resultados finais
print(f"\nResultados após 30 dias:")
print(f"Alface com fertilizante: {alface_fertilizante:.2f} cm")
print(f"Alface sem fertilizante: {alface_controle:.2f} cm")
print(f"Alface com choque elétrico: {alface_choque:.2f} cm")

# Gráfico
plt.figure(figsize=(12, 8))

# Grafico de crescimento
plt.subplot(2, 1, 1)
plt.plot(tempo, tam_fertilizante, label="Com Fertilizante", color="green")
plt.plot(tempo, tam_contole, label="Sem Fertilizante (controle)", color="blue")
plt.plot(tempo, tam_choque, label="Com Choque elétrico", color="red")
plt.xlabel("Tempo (dias)")
plt.ylabel("Crecimento (cm)")
plt.title("Crescimento das alfaces em 3 condições") 
plt.legend()

plt.tight_layout()
plt.show()