from classes.schema_pb2 import Aluno, Telefone, Turma


def main():
    aluno = Aluno(nome="José Carlos da Silva", matricula="2018370254", telefones=[])
    aluno.telefones.append(Telefone(telefone="(83) 3215-5123", tipo=Telefone.RESIDENCIAL))

    turma = Turma(alunos=[])
    turma.alunos.append(aluno)

    with open("turma", "wb") as file:
        print(turma.SerializeToString())
        file.write(turma.SerializeToString())

if __name__ == "__main__":
    main()