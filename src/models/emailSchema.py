from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    remetente: EmailStr
    destinatario: EmailStr
    assunto: str
    corpoEmail: str

class SMPTConfigSchema(BaseModel):
    emailHost: str
    emailPort: int
    emailHostUser: EmailStr
    emailHostPassword: str
    serverEmail: EmailStr
    emailUseTls: bool
    emailUseSsl: bool
