from classes.schema_pb2 import Turma


def main():
    turma = Turma()

    with open("turma", "rb") as file:
        turma.ParseFromString(file.read())

    for aluno in turma.alunos:
        print("O aluno {0} possui {1} telefone(s) cadastrado(s).".format(aluno.nome, len(aluno.telefones)))


if __name__ == "__main__":
    main()