import smtplib
import email.message

from src.models.advogadosSchema import AdvogadoRequest
from src.models.emailSchema import SMPTConfigSchema, EmailSchema


class EmailModel:

    def __init__(self, adv: AdvogadoRequest, smtpServer: SMPTConfigSchema):
        self.advogadoAtual = adv
        self.smtpServer = smtpServer
        self.header: tuple = ('Content-Type', 'text/html')

    def sendEmailProccess(self, emailModel: EmailSchema) -> bool:
        src = smtplib.SMTP(f'{self.smtpServer.serverEmail}:{self.smtpServer.emailPort}')

        try:
            msgEmail = email.message.Message()
            msgEmail['Subject'] = emailModel.assunto
            msgEmail['From'] = emailModel.remetente
            msgEmail['To'] = emailModel.destinatario
            msgEmail.add_header(*self.header)
            msgEmail.set_payload(emailModel.corpoEmail)

            src.starttls()
            src.login(self.smtpServer.emailHost, self.smtpServer.emailHostPassword)
            src.sendmail(emailModel.remetente, emailModel.destinatario, msgEmail.as_string().encode('utf-8'))

            print(f"Email enviado com sucesso.")
            return True

        except Exception as err:
            print(f"sendEmailProccess - err: {err=}")

        finally:
            src.quit()

    def sendPrimeiroAcesso(self, codAcesso: int):

        email: EmailSchema = EmailSchema(
            remetente='thomas.anderson@newprev.dev.br',
            destinatario=self.advogadoAtual.email,
            assunto=f'Seja bem vindo(a), {self.advogadoAtual.nomeAdvogado}',
            corpoEmail=f'Olá!\nÉ um prazer ter você conosco. Abaixo estão alguns dos seus dados. Pedimos que confirme-os e, se tudo estiver correto, insira o código de acesso e defina a sua senha.\n\nCódigo de acesso: {codAcesso}',
        )

        self.sendEmailProccess(email)
        