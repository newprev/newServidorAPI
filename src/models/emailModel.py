import json
from pathlib import Path
import smtplib
import email.message

from dotenv import load_dotenv
from os import getenv

from src.models.advogadosSchema import AdvogadoResponse
from src.models.emailSchema import EmailSchema, SMPTConfigSchema
from src.models.escritoriosSchema import EscritorioResponse


class EmailModel:

    def __init__(self, adv: AdvogadoResponse = None, escritorio: EscritorioResponse = None):
        self._carregaVariaveisDeAmbiente()
        self._advogadoAtual = adv
        self._escritorio = escritorio
        self._smtpServer: SMPTConfigSchema = self._getSMTPServerConfig()
        self._header: tuple = ('Content-Type', 'text/html')

    def _sendEmailProccess(self, emailModel: EmailSchema) -> bool:
        src = smtplib.SMTP_SSL(self._smtpServer.emailHost, self._smtpServer.emailPort)

        try:
            msgEmail = email.message.Message()
            msgEmail['Subject'] = emailModel.assunto
            msgEmail['From'] = emailModel.remetente
            msgEmail['To'] = emailModel.destinatario
            msgEmail.add_header(*self._header)
            msgEmail.set_payload(emailModel.corpoEmail)

            # src.starttls()
            src.login(self._smtpServer.emailHostUser, self._smtpServer.emailHostPassword)
            src.sendmail(emailModel.remetente, emailModel.destinatario, msgEmail.as_string().encode('utf-8'))
            return True

        except Exception as err:
            print(f"_sendEmailProccess - err: {err=}")

        finally:
            src.quit()

    def sendPrimeiroAcesso(self, codAcesso: int) -> None:
        if self._advogadoAtual is None:
            raise Exception('Modelo dadvogado não enviado')

        email: EmailSchema = EmailSchema(
            remetente='thomas.anderson@newprev.dev.br',
            destinatario=self._advogadoAtual.email,
            assunto=f'Seja bem vindo(a), {self._advogadoAtual.nomeAdvogado}',
            corpoEmail=f'Olá!\nÉ um prazer ter você conosco. Abaixo estão alguns dos seus dados. Pedimos que confirme-os e, se tudo estiver correto, insira o código de acesso e defina a sua senha.\n\nCódigo de acesso: {codAcesso}',
        )

        self._sendEmailProccess(email)

    def sendBoasVindasEscritorio(self) -> None:
        if self._escritorio is None:
            raise Exception('Modelo do escritorio não enviado')

        email: EmailSchema = EmailSchema(
            remetente='thomas.anderson@newprev.dev.br',
            destinatario=self._escritorio.email,
            assunto=f'Seja bem vindo(a), {self._escritorio.nomeFantasia}',
            corpoEmail=f'Olá!\nÉ um prazer ter você conosco. Abaixo estão alguns dos seus dados. Pedimos que confirme-os e, se tudo estiver correto, é só acessar nossa plataforma e '
        f'cadastrar os advogados que trabalharão na {self._escritorio.nomeFantasia}!',
        )

        self._sendEmailProccess(email)

    def sendBoasVindasAdvogado(self) -> None:
        if self._advogadoAtual is None or self._escritorio is None:
            raise Exception('Modelo do advogado não enviado')

        email: EmailSchema = EmailSchema(
            remetente='thomas.anderson@newprev.dev.br',
            destinatario=self._advogadoAtual.email,
            assunto=f'Seja bem vindo(a), {self._advogadoAtual.primeiroNome}',
            corpoEmail=f'Olá!\nÉ um prazer ter você conosco. \n\nAo fazer o seu cadastro, o escritório {self._escritorio.nomeFantasia} criou uma senha '
                       f'provisória. Ao acessar a nossa aplicação instalada na sua máquina (Desktop/Notebook), você precisará dessa senha.'
                       f'Agradecemos seu acesso!',
        )

        self._sendEmailProccess(email)

    def _carregaVariaveisDeAmbiente(self):
        """
            Carregando variáveis de ambiente
        """
        pathEnvVars = Path('') / '.env'
        if not pathEnvVars.is_file():
            raise Exception('Não foi possível encontrar o arquivo com as variáveis de ambiente.')
        else:
            load_dotenv(pathEnvVars.absolute())

    def _getSMTPServerConfig(self) -> SMPTConfigSchema:
        pathDatasource: Path = Path(getenv('DATASOURCE_PATH'))
        if not pathDatasource.exists():
            raise Exception("Variavel de ambiente DATASOURCE_PATH nao configurada")

        pathConfigSMTP: Path = pathDatasource / 'marioCart.json'

        with open(pathConfigSMTP, encoding='utf-8', mode='r') as cacheLogin:
            banco = json.load(cacheLogin)

        return SMPTConfigSchema(
            emailHost=banco["emailHost"],
            emailPort=banco["port"],
            emailHostUser=banco["emailHostUser"],
            emailHostPassword=banco["emailHostPassword"],
            serverEmail=banco["serverEmail"],
            emailUseTls=banco["emailUseTls"],
            emailUseSsl=banco["emailUseSsl"]
        )
