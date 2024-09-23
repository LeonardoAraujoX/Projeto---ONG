import sqlite3
from datetime import datetime

conn = sqlite3.connect('adocao.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS Animais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    especie TEXT NOT NULL,
                    porte TEXT NOT NULL,
                    pelagem TEXT NOT NULL,
                    sexo TEXT NOT NULL,
                    observacoes TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Adotantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    contato TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Adocoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    adotante_id INTEGER NOT NULL,
                    animal_id INTEGER NOT NULL,
                    FOREIGN KEY (adotante_id) REFERENCES Adotantes(id),
                    FOREIGN KEY (animal_id) REFERENCES Animais(id)
                )''')

conn.commit()

def calcular_idade(data_nascimento):
    data_nasc = datetime.strptime(data_nascimento, "%d/%m/%Y")
    idade = (datetime.now() - data_nasc).days // 365
    return idade

def cadastrar_animal(nome, data_nascimento, especie, porte, pelagem, sexo):
    cursor.execute('''INSERT INTO Animais (nome, data_nascimento, especie, porte, pelagem, sexo)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (nome, data_nascimento, especie, porte, pelagem, sexo))
    conn.commit()

def listar_animais():
    cursor.execute('SELECT * FROM Animais')
    return cursor.fetchall()

def remover_animal(animal_id):
    cursor.execute('DELETE FROM Animais WHERE id = ?', (animal_id,))
    conn.commit()

def cadastrar_adotante(nome, cpf, endereco, contato):
    cursor.execute('''INSERT INTO Adotantes (nome, cpf, endereco, contato)
                      VALUES (?, ?, ?, ?)''',
                   (nome, cpf, endereco, contato))
    conn.commit()

def listar_adotantes():
    cursor.execute('SELECT * FROM Adotantes')
    return cursor.fetchall()

def registrar_adocao(adotante_id, animal_id):
    cursor.execute('''INSERT INTO Adocoes (adotante_id, animal_id)
                      VALUES (?, ?)''', (adotante_id, animal_id))
    conn.commit()

def listar_adocoes():
    cursor.execute('SELECT * FROM Adocoes')
    return cursor.fetchall()
def menu():
    print("Seja bem-vindo!")
    print("Opção 1 - Cadastrar Animal")
    print("Opção 2 - Listar Animais Disponíveis para Adoção")
    print("Opção 3 - Adotar Animal")
    print("Opção 4 - Listar Adotantes")
    print("Opção 5 - Histórico de Adoções")
    print("Opção 6 - Sair")

while True:
    menu()
    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Tente novamente...")
        continue

    if opcao == 1:
        try:
            nome = input("Informe o nome do animal: ").strip()
            if not nome or any(char.isdigit() for char in nome):
                raise ValueError("Nome inválido")

            data_nascimento = input("Informe a data de nascimento aproximada do animal (dd/mm/yyyy): ")
            try:
                datetime.strptime(data_nascimento, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Data de nascimento inválida")

            especie = input("Informe a espécie do animal (cachorro ou gato): ").lower().strip()
            if especie not in ["cachorro", "gato"]:
                raise ValueError("Espécie inválida")

            porte = input("Informe o porte do animal (pequeno, médio, grande): ").lower().strip()
            if porte not in ["pequeno", "médio", "grande"]:
                raise ValueError("Porte inválido")

            pelagem = input("Informe a pelagem do animal: ").strip()
            if not pelagem or any(char.isdigit() for char in pelagem):
                raise ValueError("Pelagem inválida")

            sexo = input("Informe o sexo do animal (macho ou fêmea): ").lower().strip()
            if sexo not in ["macho", "fêmea"]:
                raise ValueError("Sexo inválido")

            cadastrar_animal(nome, data_nascimento, especie, porte, pelagem, sexo)
            print(f"{nome} cadastrado com sucesso!")
        except ValueError as err:
            print(err)

    elif opcao == 2:
        animais = listar_animais()
        if animais:
            print("Os animais disponíveis são:")
            print()
            for a in animais:
                print(f"ID: {a[0]}, Nome: {a[1]}, Data de nascimento: {a[2]}, Espécie: {a[3]}, Porte: {a[4]}, Pelagem: {a[5]}, Sexo: {a[6]}")
                print(f"Observações: {a[7] if a[7] else 'Nenhuma'}")
                print("---------------------------------------")
        else:
            print("Não há animais disponíveis!")

    elif opcao == 3:
        try:
            especie = input("Informe a espécie (cachorro ou gato) ou pressione Enter para pular: ").lower().strip()
            porte = input("Informe o porte (pequeno, médio, grande) ou pressione Enter para pular: ").lower().strip()
            sexo = input("Informe o sexo (macho ou fêmea) ou pressione Enter para pular: ").lower().strip()

            print("Animais disponíveis que se encaixam nos critérios:")
            print()
            animais = listar_animais()
            animais_filtrados = [a for a in animais if (not especie or a[3] == especie) and
                                                        (not porte or a[4] == porte) and
                                                        (not sexo or a[6] == sexo)]

            if not animais_filtrados:
                print("Não há animais disponíveis que correspondam aos critérios.")
                continue

            for a in animais_filtrados:
                print(f"ID: {a[0]}, Nome: {a[1]}, Data de nascimento: {a[2]}, Espécie: {a[3]}, Porte: {a[4]}, Pelagem: {a[5]}, Sexo: {a[6]}")
                print(f"Observações: {a[7] if a[7] else 'Nenhuma'}")
                print("---------------------------------------")

            max_idade = input("Deseja filtrar por idade máxima? (em anos, ou pressione Enter para pular): ").strip()
            if max_idade:
                try:
                    max_idade = int(max_idade)
                    animais_filtrados = [a for a in animais_filtrados if calcular_idade(a[2]) <= max_idade]
                except ValueError:
                    print("Idade máxima inválida, continuando sem filtro de idade.")
            
            if not animais_filtrados:
                print("Não há animais disponíveis que correspondam aos critérios de idade.")
                continue

            print("Animais disponíveis após filtro de idade:")
            for a in animais_filtrados:
                print(f"ID: {a[0]}, Nome: {a[1]}, Data de nascimento: {a[2]}, Espécie: {a[3]}, Porte: {a[4]}, Pelagem: {a[5]}, Sexo: {a[6]}")
                print(f"Observações: {a[7] if a[7] else 'Nenhuma'}")
                print("---------------------------------------")

            identificador_animal = int(input("Digite o identificador do animal que deseja adotar: "))
            animal_para_adocao = next((a for a in animais_filtrados if a[0] == identificador_animal), None)

            if animal_para_adocao:
                nome_adotante = input("Informe seu nome: ")
                cpf_adotante = input("Informe seu CPF: ")
                endereco_adotante = input("Informe seu endereço: ")
                contato_adotante = input("Informe seu contato: ")

                cadastrar_adotante(nome_adotante, cpf_adotante, endereco_adotante, contato_adotante)
                adotante_id = cursor.lastrowid
                registrar_adocao(adotante_id, identificador_animal)
                remover_animal(identificador_animal)
                print(f"Você adotou {animal_para_adocao[1]}!")
            else:
                print("Identificador não encontrado!")
        except ValueError:
            print("Identificador inválido!")


    elif opcao == 4:
        adotantes = listar_adotantes()
        if adotantes:
            for adotante in adotantes:
                print(f"ID: {adotante[0]}")
                print(f"Nome: {adotante[1]}")
                print(f"CPF: {adotante[2]}")
                print(f"Endereço: {adotante[3]}")
                print(f"Contato: {adotante[4]}")
                print("---------------------------------------")
        else:
            print("Não há adotantes cadastrados!")

    elif opcao == 5:
        adocoes = listar_adocoes()
        if adocoes:
            for adocao in adocoes:
                adotante_id = adocao[1]
                animal_id = adocao[2]

                cursor.execute('SELECT nome FROM Adotantes WHERE id = ?', (adotante_id,))
                adotante = cursor.fetchone()
                if adotante:
                    adotante_nome = adotante[0]
                
                else:
                    adotante_nome = "nao tem"

                cursor.execute('SELECT nome FROM Animais WHERE id = ?', (animal_id,))
                animal = cursor.fetchone()

                print(f"Adotante: {adotante_nome} (ID: {adotante_id}) adotou o animal de (ID: {animal_id})")
                print("---------------------------------------")
        else:
            print("Não há adoções registradas!")

    elif opcao == 6:
        print("Saindo...")
        break
    else:
        print("opcao invalida, escolha uma opcao valida!")
    
conn.close()