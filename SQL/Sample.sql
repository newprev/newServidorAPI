SELECT * FROM Endereco;

SELECT * FROM Escritorio esc
	JOIN Endereco ende
		ON esc.escritorioId = ende.escritorioId;

SELECT * FROM Advogado;


SELECT * FROM Endereco;
SELECT * FROM Escritorio;

/*
DELETE FROM Endereco WHERE escritorioId = 50;
DELETE FROM Escritorio WHERE escritorioId = 50;
*/

/*DROP TABLE Endereco;
DROP TABLE Contato;
DROP TABLE PrevAuth;
DROP TABLE TrocaSenha;
DROP TABLE Advogado;
DROP TABLE Escritorio;
*/

INSERT INTO Escritorio (nomeFantasia,cnpj,telefone,email,inscEstadual,ativo,dataUltAlt,dataCadastro) VALUES
	 ('Damarest','321654987','11972457874','damarest@gmail.com','3216548',1,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 ('Nóbrega','365215872','11654877788','nobrega@gmail.com','987456',0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 ('Pinheiro Neto','65154878','11654874456','pinheiro.neto@gmial.com','985487',1,'2024-04-30 00:00:00','2024-04-30 00:00:00');

INSERT INTO Advogado (escritorioId,primeiroNome,sobrenome,email,senha,numeroOAB,cpf,nacionalidade,estadoCivil,admin,ativo,confirmado,dataUltAlt,dataCadastro) VALUES
	 (1,'Ali','Attie','ali.attie@gmail.com','3215','1325','48368108098','brasileiro','solteiro',0,1,0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (2,'Mc','Donalds','mc.donalds@gmail.com','5154','6586','02925597041','brasileiro','solteiro',0,1,0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (3,'Tim','Burton','tim.burton@gmail.com','6598','8552','56291826097','brasileiro','solteiro',0,1,0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (1,'Nicola','Tesla','nicola.tesla@gmail.com','6325','4985','68272655012','brasileiro','solteiro',0,1,0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (1,'Albert','Einstein','albert.einstein@gmail.com','6582','2585','46786901077','brasileiro','solteiro',0,1,0,'2024-04-30 00:00:00','2024-04-30 00:00:00');

INSERT INTO Endereco (escritorioId,advogadoId,endereco,numero,cep,complemento,cidade,estado,bairro,ativo,dataUltAlt,dataCadastro) VALUES
	 (1,NULL,'Avenida Recife',56,'56285970',NULL,'Araripina','PE','Distrito de Nascente',1,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (NULL,1,'Distrito Batingas',96,'57317973',NULL,'Batingas','AL','Distrito Batingas',1,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (2,NULL,'Avenida Presidente Vargas',327,'64145970',NULL,'Avenida Presidente Vargas 327','PI','Centro',1,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (NULL,3,'Praça da Matriz',65,'15442970',NULL,'Mangaratú','SP','Centro',0,'2024-04-30 00:00:00','2024-04-30 00:00:00'),
	 (NULL,4,'Avenida Rinópolis',365,'17740970',NULL,'Rinópolis','SP','Centro',1,'2024-04-30 00:00:00','2024-04-30 00:00:00');

INSERT INTO Contato (escritorioId, advogadoId, numero, ehWatsapp, ehTelegram, principal, dataUltAlt, dataCadastro) VALUES
	(1, NULL, 11654874452, 0, 0, 1, '2024-05-04 00:00:00', '2024-05-04 00:00:00'),
	(NULL, 1, 11845744568, 0, 1, 0, '2024-05-04 00:00:00', '2024-05-04 00:00:00'),
	(2, NULL, 11915478854, 0, 1, 1, '2024-05-04 00:00:00', '2024-05-04 00:00:00'),
	(NULL, 2, 11963258789, 1, 0, 0, '2024-05-04 00:00:00', '2024-05-04 00:00:00'),
	(1, NULL, 11947852200, 1, 0, 1, '2024-05-04 00:00:00', '2024-05-04 00:00:00'),
	(1, NULL, 11958778787, 1, 1, 1, '2024-05-04 00:00:00', '2024-05-04 00:00:00');
	
INSERT INTO TrocaSenha (escritorioId,advogadoId,codAcesso,primAcesso,tipoTroca,dataUltAlt,dataCadastro) VALUES
	 (NULL,1,67773,0,'ES','2024-06-23 14:30:59','2024-06-23 14:30:59'),
	 (NULL,5,28317,0,'ES','2024-06-23 14:30:59','2024-06-23 14:30:59');


SELECT * FROM Contato;
SELECT * FROM TrocaSenha;
SELECT * FROM PrevAuth;
SELECT confirmado, Advogado.* FROM Advogado 
WHERE cpf = '48368108098';

START TRANSACTION
#COMMIT
UPDATE Advogado
	SET confirmado = 0
	WHERE advogadoId = 2;

