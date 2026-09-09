import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Função para digitar letra por letra lentamente
def digitar_lentamente(elemento, texto, atraso=0.1):
    elemento.clear()
    for caractere in texto:
        elemento.send_keys(caractere)
        time.sleep(atraso)  # Pausa em segundos entre cada letra


# 1. Lista com os dados dos 5 alunos
alunos = [
    {
        "nome": "Ana Beatriz Silva",
        "email": "ana.silva@email.com",
        "turma": "Turma A",
        "turno": "Manhã",
    },
    {
        "nome": "Carlos Eduardo Santos",
        "email": "carlos.santos@email.com",
        "turma": "Turma B",
        "turno": "Noite",
    },
    {
        "nome": "Fernanda Oliveira",
        "email": "fernanda.oliveira@email.com",
        "turma": "Turma C",
        "turno": "Tarde",
    },
    {
        "nome": "Lucas Gabriel Costa",
        "email": "lucas.costa@email.com",
        "turma": "Turma A",
        "turno": "Noite",
    },
    {
        "nome": "Mariana Ramos",
        "email": "mariana.ramos@email.com",
        "turma": "Turma B",
        "turno": "Manhã",
    },
]

# URL do seu Google Forms
URL_FORM = "https://forms.gle/mBRBrgXxZmbyCrUn7"

# Configuração do Navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    for index, aluno in enumerate(alunos, start=1):
        print(
            f"[{index}/5] Cadastrando: {aluno['nome']} ({aluno['turma']} - Turno: {aluno['turno']})..."
        )

        # Abre o formulário
        driver.get(URL_FORM)
        time.sleep(1)  # Pausa inicial para visualização da página

        # Preenche Nome e E-mail letra por letra
        inputs_texto = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//input[@type='text' or @type='email']")
            )
        )

        # Digita o Nome (0.08 segundos por letra)
        digitar_lentamente(inputs_texto[0], aluno["nome"], atraso=0.08)
        time.sleep(0.5)

        # Digita o E-mail
        digitar_lentamente(inputs_texto[1], aluno["email"], atraso=0.08)
        time.sleep(0.5)

        # Seleciona a Turma
        radio_turma = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@role='radio' and @data-value='{aluno['turma']}']")
            )
        )
        radio_turma.click()
        time.sleep(0.5)

        # Seleciona o Turno
        btn_turno = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[(@role='radio' or @role='checkbox') and @data-value='{aluno['turno']}']",
                )
            )
        )
        btn_turno.click()

        # Pausa de 1.5 segundo para todos verem o formulário todo preenchido
        time.sleep(1.5)

        # Clica em Enviar
        btn_enviar = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[text()='Enviar' or text()='Submit']/ancestor::div[@role='button']",
                )
            )
        )
        btn_enviar.click()

        # Aguarda confirmação de envio
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(text(), 'registrada') or contains(text(), 'recorded')]",
                )
            )
        )
        print(f"   ✓ {aluno['nome']} cadastrado com sucesso!")

        # Pausa entre um aluno e outro
        time.sleep(2)

    print("\n🎉 Todos os 5 alunos foram cadastrados visualmente com sucesso!")

finally:
    driver.quit()
