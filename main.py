"""
Autores: Victor Vasconcelos
         Matheus Lima

Sistema para a Monitoria de campo, avaliação de cadastros.

"""
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5
import psycopg2
import datetime
import PIL.Image as Image
import io
import re



db_name = '******'
db_host = '******'
db_user = 'postgres'
db_password = '********'
connect = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
cursor = connect.cursor()
cont = 0
chave = False


def stopAnimation():
    print('saiu')
    move.stop()
    load.hide()

def startAnimation():
    print('entrou')
    move.start()
    timer.singleShot(4000, stopAnimation)
    load.show()

def Buscar_matricula():
    startAnimation()

    ctiid = main.matricula.text()
    ctiid = ''.join(c for c in ctiid if c.isdigit())

    Limpar_campos()
    valor_edit = checarMonitoria(ctiid)
    print(valor_edit)
    main.foto.clear()

    try:

        sql1 = f'''select 	u.ctiid,
                            u.ocupacao_unidade,
                            l.calcada,
                            l.limitacao, 
                            u.numero,
                            logradouro_id,
                            u.ecologradouro_id,
                            ecologdigitado,
                            u.manaus_energia,
                            u.situacao_da_unidade_construida,
                            u.situacao_relativa_ao_lote,
                            u.alinhamento,
                            u.patrimonio,
                            u.uso_do_imovel,
                            u.escoamento_sanitario,
                            u.cdcanoconstrucao,
                            u.cdcdatahabitese,
                            u.cdcnmrhabitese,
                            u.cticatid, 
                            obs_topocart,
                            u.tipo_de_construcao,
                            u.estrutura, u.parede,
                            u.cobertura, 
                            u.revestimento_da_fachada,
                            u.terraco, 
                            u.subsolo,
                            u.padrao_construtivo, 
                            u.estado_de_conservacao, 
                            e.posicao,
                            c.nome,
                            c.cpf,
                            c.rg, 
                            c.telefone,
                            c.email, 
                            c.ctgid,
                            e.pavimentos,
                            m.cpfresponsavel,
                            m.nome_fantasia,
                            m.razao_social,
                            m.tipo_atividade,
                            m.descricao_atividade,
                            m.cnpj,
                            m.nomeresponsavel,
                            p.nome,
                            l.id, 
                            u.geom,
                            u.lote_id,
                            u.obs_topocart,
                            u.complemento,
                            u.status_proprietario,
                            e.possui_construcao,
                            u.cdctpohabitese 
                    from cadastro.unidade u
                    left join cadastro.lote l on l.id = u.lote_id
                    left join cadastro.contribuinte c on u.ctictgid = c.ctgid
                    left join cadastro.edificacao e on e.unidade_id = u.ctiid
                    left join cadastro.mobiliario m on m.unidade_id = u.ctiid
                    left join public.pessoa p on p.id = u.cadastrador 
                    where ctiid = {str(ctiid)} 
                    limit 1


        '''
        cursor.execute(sql1)
        result = cursor.fetchall()
        lista = []

        # print(result)
        if result[0] != None:
            sql_edi = f"""select posicao, pavimentos, possui_construcao, principal from cadastro.edificacao where unidade_id = '{ctiid}' """
            cursor.execute(sql_edi)
            edificacao2 = cursor.fetchall()

            #print(edificacao2)
            tamanho = len(edificacao2)
            chaveF = False
            chaveV = False
            c = 0
            if tamanho >1:
                """ ***** EDIFICACAO PRINCIPAL ******* """

                for index, b in enumerate(edificacao2):
                    if tamanho == 1:
                        print('Apenas uma linha\n')
                        print('setando no primeiro 1')
                        main.posicao.setText(str(b[0]))
                        main.pavimento.setText(str(b[1]))
                        main.pav_contrucao.setText(0 ,str(b[2]))

                        main.posicao_2.setText(str(b[0]))
                        main.pavimento_2.setText(str(b[1]))
                        main.pav_contrucao_2.setItemText(0 ,str(b[2]))
                        break
                    elif b[3] == True:
                        chaveV = True
                        print('\nsetando no primeiro')
                        main.posicao.setText(str(b[0]))
                        main.pavimento.setText(str(b[1]))
                        main.pav_contrucao.setText(str(b[2]))
                        if valor_edit ==1 :
                            pass
                        else:
                            main.posicao_2.setText(str(b[0]))
                            main.pavimento_2.setText(str(b[1]))
                            main.pav_contrucao_2.setItemText(0, str(b[2]))

                    elif b[3] == False and chaveF == False:
                        chaveF = True
                        print('\nsetando no segundo aaaaaa')
                        main.posicao_edi.setText(str(b[0]))
                        main.pavimento_edi.setText(str(b[1]))
                        main.pav_em_construcao_edi.setText(str(b[2]))

                        if valor_edit ==1 :
                            pass
                        else:
                            main.posicao_edi_2.setText(str(b[0]))
                            main.pavimento_edi_2.setText(str(b[1]))
                            main.pav_em_construcao_edi_2.setItemText(0, str(b[2]))


                    elif b[
                        3] == False and index == tamanho - 1 and chaveV == False:  # O SE FOR FALSO E FOR O ULTIMO DO LOOP
                        print('\nsetando no primeiro ')
                        print('é tudo False')
                        main.posicao.setText(str(b[0]))
                        main.pavimento.setText(str(b[1]))
                        main.pav_contrucao.setText(str(b[2]))

                        main.posicao_2.setText(str(b[0]))
                        main.pavimento_2.setText(str(b[1]))
                        main.pav_contrucao_2.setItemText(0, str(b[2]))
            else:
                main.posicao.setText(str(edificacao2[0][0]))
                main.pavimento.setText(str(edificacao2[0][1]))
                main.pav_contrucao.setText(str(edificacao2[0][2]))

            for row in result:
                lista.append(row)

                # print(len(result))
                # print(lista[0][0])
                """*********** CHAMA mostrar Foto *********"""
                mostraFoto(str(lista[0][45]))

                if len(result) > 0:
                    main.ocupa.setText(str(lista[0][1]))
                    main.calcada.setText(str(lista[0][2]))
                    main.limitacao.setText(str(lista[0][3]))
                    main.logradouro.setText(str(lista[0][5]))
                    main.numero.setText(str(lista[0][4]))
                    main.complemento.setText(str(lista[0][49]))
                    main.manaus_energia.setText(str(lista[0][8]))
                    main.situacao_unidade.setText(str(lista[0][9]))
                    main.situacao_lote.setText(str(lista[0][10]))
                    main.alinhamento.setText(str(lista[0][11]))
                    main.patrimonio.setText(str(lista[0][12]))
                    main.uso_imovel.setText(str(lista[0][13]))
                    main.escoamento_sanitario.setText(str(lista[0][14]))
                    main.ano_contrucao.setText(str(lista[0][15]))
                    main.habitase.setText(str(lista[0][52]))
                    main.numero_habitante.setText(str(lista[0][17]))
                    main.data_habita.setText(str(lista[0][16]))
                    main.numero_cartorio.setText(str(lista[0][18]))
                    main.tipo_contrucao.setText(str(lista[0][20]))
                    main.estrutura.setText(str(lista[0][21]))
                    main.parede.setText(str(lista[0][22]))
                    main.cobertura.setText(str(lista[0][23]))
                    main.revestimento.setText(str(lista[0][24]))
                    main.terraco.setText(str(lista[0][25]))
                    main.subsolo.setText(str(lista[0][26]))
                    main.padrao.setText(str(lista[0][27]))
                    main.estado_conservacao.setText(str(lista[0][28]))
                    #main.posicao.setText(str(lista[0][29]))
                    #main.pavimento.setText(str(lista[0][36]))
                    #main.pav_contrucao.setText(str(lista[0][51]))

                    main.nome.setText(str(lista[0][30]))
                    main.cpf.setText(str(lista[0][31]))
                    main.rg.setText(str(lista[0][32]))
                    main.telefone.setText(str(lista[0][33]))
                    main.email.setText(str(lista[0][34]))
                    main.nome_fanttasia.setText(str(lista[0][38]))
                    main.razao.setText(str(lista[0][39]))
                    main.cnpj.setText(str(lista[0][42]))
                    main.tipo_atividade.setText(str(lista[0][40]))
                    main.descricao_atividade.setText(str(lista[0][41]))
                    main.nome_comerciante.setText(str(lista[0][43]))
                    main.cpf_comerciante.setText(str(lista[0][37]))
                    main.nome_cadastrador.setText(str(lista[0][44]))
                    main.lote_id.setText(str(lista[0][45]))
                    main.observacao.setText(str(lista[0][48]))
                    main.status_proprietario.setText(str(lista[0][50].upper()))
                    ###*****************************
                    #Check pra vê se edição existe
                    if valor_edit == 1 :
                        print(valor_edit)
                        pass
                    else:
                        #Se não mostra o mesmo valor do primeiro
                        main.ocupa_2.setItemText(0, lista[0][1])
                        main.calcada_2.setItemText(0, lista[0][2])
                        main.limitacao_2.setItemText(0, lista[0][3])
                        main.logradouro_2.setText(str(lista[0][5]))
                        main.numero_2.setText(str(lista[0][4]))
                        main.complemento_2.setText(str(lista[0][49]))
                        main.manaus_energia_2.setText(str(lista[0][8]))
                        main.situacao_unidade_2.setItemText(0, lista[0][9])
                        main.situacao_lote_2.setItemText(0, lista[0][10])
                        main.alinhamento_2.setItemText(0, lista[0][11])
                        main.patrimonio_2.setItemText(0, lista[0][12])
                        main.uso_imovel_2.setItemText(0, lista[0][13])
                        main.escoamento_sanitario_2.setItemText(0, lista[0][14])
                        main.ano_contrucao_2.setText(str(lista[0][15]))
                        main.habitase_2.setText(str(lista[0][52]))
                        main.numero_habitante_2.setText(str(lista[0][17]))
                        main.data_habita_2.setText(str(lista[0][16]))
                        main.numero_cartorio_2.setText(str(lista[0][18]))
                        main.tipo_contrucao_2.setItemText(0, lista[0][20])
                        main.estrutura_2.setItemText(0, lista[0][21])
                        main.parede_2.setItemText(0, lista[0][22])
                        main.cobertura_2.setItemText(0, lista[0][23])
                        main.revestimento_2.setItemText(0, lista[0][24])
                        main.terraco_2.setItemText(0, lista[0][25])
                        main.subsolo_2.setItemText(0, lista[0][26])
                        main.padrao_2.setItemText(0, lista[0][27])
                        main.estado_conservacao_2.setItemText(0, lista[0][28])
                        main.posicao_2.setText(str(lista[0][29]))
                        main.pavimento_2.setText(str(lista[0][36]))
                        main.pav_contrucao_2.setItemText(0, str(lista[0][51]))
                        main.nome_2.setText(str(lista[0][30]))
                        main.cpf_2.setText(str(lista[0][31]))
                        main.rg_2.setText(str(lista[0][32]))
                        main.telefone_2.setText(str(lista[0][33]))
                        main.email_2.setText(str(lista[0][34]))
                        main.nome_fanttasia_2.setText(str(lista[0][38]))
                        main.razao_2.setText(str(lista[0][39]))
                        main.cnpj_2.setText(str(lista[0][42]))
                        main.tipo_atividade_2.setText(str(lista[0][40]))
                        main.descricao_atividade_2.setText(str(lista[0][41]))
                        main.nome_comerciante_2.setText(str(lista[0][43]))
                        main.cpf_comerciante_2.setText(str(lista[0][37]))



                else:
                    print('a')
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
        connect.commit()
        QMessageBox.about(None, "MATRÍCULA INEXISTENTE!!!", "TENTE NOVAMENTE ")

def mostraFoto(lote):
    sql_imagem = f"""select imagem, count(imagem) from foto_fachada.foto_fachada_arquivo where lote_id ={str(lote)} group by imagem"""
    cursor.execute(sql_imagem)
    fotos = cursor.fetchall()

    # print(fotos)
    # print(lista[0][45])
    image = []
    if len(fotos) > 0:
        for f in fotos:
            image.append(f[0])
            row = f[1]
        # SE FOTO EXISTIR MOSTRE ELA
        # print(row)
        chave = True
        autoSize = 400
        largSize = 300
        image_pil = Image.open(io.BytesIO(image[0]))
        image_pil.save('imagem/foto.png')
        foto_red = Image.open('imagem/foto.png')
        foto_red = foto_red.resize((autoSize, largSize), Image.ANTIALIAS)
        foto_red.save('imagem/newfoto.png')
        # print(type(image_pil))
        main.foto.setPixmap(QPixmap('imagem/newfoto.png'))  # PRINTA FOTO NA TELA

def Enviar():
    try:
        unidade_id = main.matricula.text()
        monitor = main.monitor.text()
        ocup_terreno = main.comboBox.currentText()
        calcada = main.comboBox_2.currentText()
        limitacao = main.comboBox_3.currentText()
        logradouro = main.comboBox_4.currentText()
        numero = main.comboBox_5.currentText()
        complemento = main.comboBox_6.currentText()
        manaus_energia = main.comboBox_8.currentText()
        situacao_unidade = main.comboBox_9.currentText()
        situcao_lote = main.comboBox_10.currentText()
        alinhamento = main.comboBox_11.currentText()
        patrimonio = main.comboBox_12.currentText()
        uso_do_imovel = main.comboBox_13.currentText()
        escoamento_sanitario = main.comboBox_14.currentText()
        ano_contrucao = main.comboBox_15.currentText()
        habitese = main.comboBox_16.currentText()
        numero_habitese = main.comboBox_17.currentText()
        data_habitese = main.comboBox_18.currentText()
        numero_cartorio = main.comboBox_19.currentText()
        nome_cartorio = main.comboBox_20.currentText()
        ####
        tipo_contrucao = main.comboBox_21.currentText()
        parede = main.comboBox_22.currentText()
        cobertura = main.comboBox_23.currentText()
        revestimento_da_fachada = main.comboBox_24.currentText()
        terraco = main.comboBox_25.currentText()
        subsolo = main.comboBox_26.currentText()
        padrao_construtivo = main.comboBox_27.currentText()
        estado_de_conservacao = main.comboBox_28.currentText()
        posicao = main.comboBox_30.currentText()
        pavimento = main.comboBox_31.currentText()
        pav_em_construcao = main.comboBox_32.currentText()
        nome = main.comboBox_33.currentText()
        cpf = main.comboBox_34.currentText()
        rg = main.comboBox_35.currentText()
        telefone = main.comboBox_36.currentText()
        email = main.comboBox_37.currentText()
        nome_fantasia = main.comboBox_38.currentText()
        razao_social = main.comboBox_39.currentText()
        cnpj = main.comboBox_40.currentText() 
        tipo_atividade = main.comboBox_41.currentText()
        descricao_atividade = main.comboBox_42.currentText()
        nomeresponsavel = main.comboBox_43.currentText()
        cpfresponsavel = main.comboBox_44.currentText()
        obs_mon = main.observacao_avaliacao.text()
        estrutura = main.comboBox_7.currentText()
        cadastrador = main.nome_cadastrador.text()
        status_proprietario = main.status_proprietario.text()
        posicao_2 = main.comboBox_29.currentText()
        pavimento_2 = main.comboBox_45.currentText()
        pav_em_construcao_2 = main.comboBox_46.currentText()
        """*************** CHEGAR SE MONITORIA FOI REALIZADA *******************"""
        sql_check = f"""Select id, unidade_id from stage.monitoria where unidade_id = {str(unidade_id)}"""
        cursor.execute(sql_check)
        check_result = cursor.fetchall()
        if len(check_result) > 0:
            print('id =',check_result[0][0])
            print(estado_de_conservacao)
            sql_updadte = f"""UPDATE stage.monitoria
                   SET
                   nome_monitor='{monitor}',
                   ocupacao_terreno='{ocup_terreno}',
                   calcada='{calcada}',
                   limitacao='{limitacao}',
                   logradouro='{logradouro}',
                   numero='{numero}',
                   complemento='{complemento}',
                   situacao_unidade='{situacao_unidade}',
                   situacao_lote='{situacao_unidade}',
                   alinhamento='{situcao_lote}',
                   patrimonio='{patrimonio}',
                   uso_do_imovel='{uso_do_imovel}',
                   escoamento_sanitario='{escoamento_sanitario}',
                   ano_de_construcao='{ano_contrucao}',
                   habitese='{habitese}',
                   numero_habitese='{numero_habitese}',
                   numero_cartorio='{numero_cartorio}',
                   tipo_de_construcao='{tipo_contrucao}',
                   parede='{parede}',
                   cobertura='{cobertura}',
                   revestimento_fachada='{revestimento_da_fachada}',
                   terraco='{terraco}',
                   subsolo='{subsolo}',
                   padrao_construtivo='{padrao_construtivo}',
                   estado_de_conservacao='{estado_de_conservacao}',
                   posicao='{posicao}',
                   pavimento='{pavimento}',
                   pavimento_construcao='{pav_em_construcao}',
                   nome_proprietario='{nome}',
                   cpf_proprietario='{cpf}',
                   rg_proprietario='{rg}',
                   telefone_proprietario='{telefone}',
                   email_proprietario='{email}',
                   nome_fantasia='{nome_fantasia}',
                   razao_social='{razao_social}',
                   cnpj='{cnpj}',
                   tipo_atividade='{tipo_atividade}',
                   descricao_atividade='{descricao_atividade}',
                   nome_responsavel='{nomeresponsavel}',
                   cpf_responsavel='{cpfresponsavel}',
                   manaus_energia='{manaus_energia}',
                   dthabitese='{data_habitese}',
                   estrutura='{estrutura}',
                   posicao_2='{posicao_2}',
                   pavimento_2='{pavimento_2}',
                   pav_em_construcao_2='{pav_em_construcao_2}'
                   WHERE id = {str(check_result[0][0])} ;"""
            cursor.execute(sql_updadte)
            connect.commit()
            QMessageBox.about(None,'ATUALIZAÇÃO :)', 'DADOS ATUALIZADOS COM SUCESSO.')
        else:
            if status_proprietario == 'PRESENTE':
                status_proprietario = 'Presente'
            elif status_proprietario == 'AUSENTE':
                status_proprietario = 'Ausente'
            else:
                status_proprietario = 'Não Autorizado'
            if monitor != '':
                sql = f""" INSERT INTO stage.monitoria(
                    unidade_id,
                    nome_monitor,
                    ocupacao_terreno,
                    calcada,
                    limitacao,
                    logradouro,
                    numero,
                    complemento,
                    situacao_unidade,
                    situacao_lote,
                    alinhamento,
                    patrimonio,
                    uso_do_imovel,
                    escoamento_sanitario,
                    ano_de_construcao,
                    habitese,
                    numero_habitese,
                    numero_cartorio,
                    nome_cartorio,
                    tipo_de_construcao,
                    parede,
                    cobertura,
                    revestimento_fachada,
                    terraco,
                    subsolo,
                    padrao_construtivo,
                    estado_de_conservacao,
                    posicao,
                    pavimento,
                    pavimento_construcao,
                    nome_proprietario,
                    cpf_proprietario,
                    rg_proprietario,
                    telefone_proprietario,
                    email_proprietario, 
                    nome_fantasia,
                    razao_social, 
                    cnpj,
                    tipo_atividade,
                    descricao_atividade,
                    nome_responsavel, 
                    cpf_responsavel,
                    manaus_energia,
                    dthabitese,
                    observacao_monitor, estrutura,status_proprietario, posicao_2, pavimento_2, pav_em_construcao_2 )
                    VALUES ('{unidade_id}',
                            '{monitor}',
                            '{ocup_terreno}',
                            '{calcada}',
                            '{limitacao}',
                            '{logradouro}',
                            '{numero}',
                            '{complemento}',
                            '{situacao_unidade}',
                            '{situcao_lote}',
                            '{alinhamento}',
                            '{patrimonio}',
                            '{uso_do_imovel}',
                            '{escoamento_sanitario}',
                            '{ano_contrucao}',
                            '{habitese}', 
                            '{numero_habitese}',
                            '{numero_cartorio}',
                            '{nome_cartorio}',
                            '{tipo_contrucao}',
                            '{parede}',
                            '{cobertura}',
                            '{revestimento_da_fachada}',
                            '{terraco}',
                            '{subsolo}',
                            '{padrao_construtivo}',
                            '{estado_de_conservacao}',
                            '{posicao}',
                            '{pavimento}',
                            '{pav_em_construcao}',
                            '{nome}',
                            '{cpf}',
                            '{rg}',
                            '{telefone}',
                            '{email}',
                            '{nome_fantasia}',
                            '{razao_social}',
                            '{cnpj}',
                            '{tipo_atividade}',
                            '{descricao_atividade}',
                            '{nomeresponsavel}',
                            '{cpfresponsavel}',
                            '{manaus_energia}',
                            '{data_habitese}',
                            '{obs_mon}',
                            '{estrutura}', '{status_proprietario}','{posicao_2}','{pavimento_2}','{pav_em_construcao_2}')"""
                cursor.execute(sql)
                connect.commit()

                # print("foi")
                QMessageBox.about(None, "TOPOCART", "RESULTADO SALVO COM SUCESSO")
            else:
                QMessageBox.about(None, "TOPOCART", "INSIRA O NOME DO MONITOR")

    except Exception as e:
        print(e)
        #cursor.execute("ROLLBACK")
        #connect.commit()
        QMessageBox.about(None, "TOPOCART", "ERRO AO SALVAR O ARQUIVO")

def Limpar_campos():
    main.foto.clear()
    main.ocupa.clear()
    main.calcada.clear()
    main.limitacao.clear()
    main.logradouro.clear()
    main.numero.clear()
    main.complemento.clear()
    main.manaus_energia.clear()
    # main.qtd_unidade.clear()
    main.situacao_unidade.clear()
    main.situacao_lote.clear()
    main.alinhamento.clear()
    main.patrimonio.clear()
    main.uso_imovel.clear()
    main.escoamento_sanitario.clear()
    main.ano_contrucao.clear()
    main.habitase.clear()
    main.numero_habitante.clear()
    main.data_habita.clear()
    main.numero_cartorio.clear()
    main.nome_cartorio.clear()
    main.tipo_contrucao.clear()
    main.estrutura.clear()
    main.parede.clear()
    main.cobertura.clear()
    main.revestimento.clear()
    main.terraco.clear()
    main.subsolo.clear()
    main.padrao.clear()
    main.estado_conservacao.clear()
    main.posicao.clear()
    main.pavimento.clear()
    main.pav_contrucao.clear()
    main.nome.clear()
    main.cpf.clear()
    main.rg.clear()
    main.telefone.clear()
    main.email.clear()
    main.nome_fanttasia.clear()
    main.razao.clear()
    main.cnpj.clear()
    main.tipo_atividade.clear()
    main.descricao_atividade.clear()
    main.nome_comerciante.clear()
    main.cpf_comerciante.clear()
    main.nome_cadastrador.clear()
    main.lote_id.clear()
    main.observacao.clear()
    main.posicao_edi.clear()
    main.pavimento_edi.clear()
    main.pav_em_construcao_edi.clear()
    main.posicao_edi_2.clear()
    main.pavimento_edi_2.clear()

    main.matricula.setFocus()

    main.comboBox.setFocus()
    """******** Atualização da combobox *******"""
    main.comboBox.clear()
    main.comboBox_2.clear()
    main.comboBox_3.clear()
    main.comboBox_4.clear()
    main.comboBox_5.clear()
    main.comboBox_6.clear()
    main.comboBox_7.clear()
    main.comboBox_8.clear()
    main.comboBox_9.clear()
    main.comboBox_10.clear()
    main.comboBox_11.clear()
    main.comboBox_12.clear()
    main.comboBox_13.clear()
    main.comboBox_14.clear()
    main.comboBox_15.clear()
    main.comboBox_16.clear()
    main.comboBox_17.clear()
    main.comboBox_18.clear()
    main.comboBox_19.clear()
    main.comboBox_20.clear()
    ####
    main.comboBox_21.clear()
    main.comboBox_22.clear()
    main.comboBox_23.clear()
    main.comboBox_24.clear()
    main.comboBox_25.clear()
    main.comboBox_26.clear()
    main.comboBox_27.clear()
    main.comboBox_28.clear()
    main.comboBox_29.clear()
    main.comboBox_30.clear()
    main.comboBox_31.clear()
    main.comboBox_32.clear()
    main.comboBox_33.clear()
    main.comboBox_34.clear()
    main.comboBox_35.clear()
    main.comboBox_36.clear()
    main.comboBox_37.clear()
    main.comboBox_38.clear()
    main.comboBox_39.clear()
    main.comboBox_40.clear()
    main.comboBox_41.clear()
    main.comboBox_42.clear()
    main.comboBox_43.clear()
    main.comboBox_44.clear()
    main.comboBox_45.clear()
    main.comboBox_46.clear()

    opções = ["POSITIVO", "NEGATIVO", "NÃO SE APLICA"]
    positivo = QIcon('imagem/VERDE.png')
    negativo = QIcon('imagem/VERMELHO.png')
    naoseaplica = QIcon('imagem/AMARELO.png')
    main.comboBox.addItems(opções)
    main.comboBox.setItemIcon(0, positivo)
    main.comboBox.setItemIcon(1, negativo)
    main.comboBox.setItemIcon(2, naoseaplica)
    main.comboBox_2.addItems(opções)
    main.comboBox_2.setItemIcon(0, positivo)
    main.comboBox_2.setItemIcon(1, negativo)
    main.comboBox_2.setItemIcon(2, naoseaplica)
    main.comboBox_3.addItems(opções)
    main.comboBox_3.setItemIcon(0, positivo)
    main.comboBox_3.setItemIcon(1, negativo)
    main.comboBox_3.setItemIcon(2, naoseaplica)
    main.comboBox_4.addItems(opções)
    main.comboBox_4.setItemIcon(0, positivo)
    main.comboBox_4.setItemIcon(1, negativo)
    main.comboBox_4.setItemIcon(2, naoseaplica)
    main.comboBox_5.addItems(opções)
    main.comboBox_5.setItemIcon(0, positivo)
    main.comboBox_5.setItemIcon(1, negativo)
    main.comboBox_5.setItemIcon(2, naoseaplica)
    main.comboBox_6.addItems(opções)
    main.comboBox_6.setItemIcon(0, positivo)
    main.comboBox_6.setItemIcon(1, negativo)
    main.comboBox_6.setItemIcon(2, naoseaplica)
    main.comboBox_7.addItems(opções)
    main.comboBox_7.setItemIcon(0, positivo)
    main.comboBox_7.setItemIcon(1, negativo)
    main.comboBox_7.setItemIcon(2, naoseaplica)
    main.comboBox_8.addItems(opções)
    main.comboBox_8.setItemIcon(0, positivo)
    main.comboBox_8.setItemIcon(1, negativo)
    main.comboBox_8.setItemIcon(2, naoseaplica)
    main.comboBox_9.addItems(opções)
    main.comboBox_9.setItemIcon(0, positivo)
    main.comboBox_9.setItemIcon(1, negativo)
    main.comboBox_9.setItemIcon(2, naoseaplica)
    main.comboBox_10.addItems(opções)
    main.comboBox_10.setItemIcon(0, positivo)
    main.comboBox_10.setItemIcon(1, negativo)
    main.comboBox_10.setItemIcon(2, naoseaplica)
    main.comboBox_11.addItems(opções)
    main.comboBox_11.setItemIcon(0, positivo)
    main.comboBox_11.setItemIcon(1, negativo)
    main.comboBox_11.setItemIcon(2, naoseaplica)
    main.comboBox_12.addItems(opções)
    main.comboBox_12.setItemIcon(0, positivo)
    main.comboBox_12.setItemIcon(1, negativo)
    main.comboBox_12.setItemIcon(2, naoseaplica)
    main.comboBox_13.addItems(opções)
    main.comboBox_13.setItemIcon(0, positivo)
    main.comboBox_13.setItemIcon(1, negativo)
    main.comboBox_13.setItemIcon(2, naoseaplica)
    main.comboBox_14.addItems(opções)
    main.comboBox_14.setItemIcon(0, positivo)
    main.comboBox_14.setItemIcon(1, negativo)
    main.comboBox_14.setItemIcon(2, naoseaplica)
    main.comboBox_15.addItems(opções)
    main.comboBox_15.setItemIcon(0, positivo)
    main.comboBox_15.setItemIcon(1, negativo)
    main.comboBox_15.setItemIcon(2, naoseaplica)
    main.comboBox_16.addItems(opções)
    main.comboBox_16.setItemIcon(0, positivo)
    main.comboBox_16.setItemIcon(1, negativo)
    main.comboBox_16.setItemIcon(2, naoseaplica)
    main.comboBox_17.addItems(opções)
    main.comboBox_17.setItemIcon(0, positivo)
    main.comboBox_17.setItemIcon(1, negativo)
    main.comboBox_17.setItemIcon(2, naoseaplica)
    main.comboBox_18.addItems(opções)
    main.comboBox_18.setItemIcon(0, positivo)
    main.comboBox_18.setItemIcon(1, negativo)
    main.comboBox_18.setItemIcon(2, naoseaplica)
    main.comboBox_19.addItems(opções)
    main.comboBox_19.setItemIcon(0, positivo)
    main.comboBox_19.setItemIcon(1, negativo)
    main.comboBox_19.setItemIcon(2, naoseaplica)
    main.comboBox_20.addItems(opções)
    main.comboBox_20.setItemIcon(0, positivo)
    main.comboBox_20.setItemIcon(1, negativo)
    main.comboBox_20.setItemIcon(2, naoseaplica)
    main.comboBox_21.addItems(opções)
    main.comboBox_21.setItemIcon(0, positivo)
    main.comboBox_21.setItemIcon(1, negativo)
    main.comboBox_21.setItemIcon(2, naoseaplica)
    main.comboBox_22.addItems(opções)
    main.comboBox_22.setItemIcon(0, positivo)
    main.comboBox_22.setItemIcon(1, negativo)
    main.comboBox_22.setItemIcon(2, naoseaplica)
    main.comboBox_23.addItems(opções)
    main.comboBox_23.setItemIcon(0, positivo)
    main.comboBox_23.setItemIcon(1, negativo)
    main.comboBox_23.setItemIcon(2, naoseaplica)
    main.comboBox_24.addItems(opções)
    main.comboBox_24.setItemIcon(0, positivo)
    main.comboBox_24.setItemIcon(1, negativo)
    main.comboBox_24.setItemIcon(2, naoseaplica)
    main.comboBox_25.addItems(opções)
    main.comboBox_25.setItemIcon(0, positivo)
    main.comboBox_25.setItemIcon(1, negativo)
    main.comboBox_25.setItemIcon(2, naoseaplica)
    main.comboBox_26.addItems(opções)
    main.comboBox_26.setItemIcon(0, positivo)
    main.comboBox_26.setItemIcon(1, negativo)
    main.comboBox_26.setItemIcon(2, naoseaplica)
    main.comboBox_27.addItems(opções)
    main.comboBox_27.setItemIcon(0, positivo)
    main.comboBox_27.setItemIcon(1, negativo)
    main.comboBox_27.setItemIcon(2, naoseaplica)
    main.comboBox_28.addItems(opções)
    main.comboBox_28.setItemIcon(0, positivo)
    main.comboBox_28.setItemIcon(1, negativo)
    main.comboBox_28.setItemIcon(2, naoseaplica)
    main.comboBox_29.addItems(opções)
    main.comboBox_29.setItemIcon(0,positivo)
    main.comboBox_29.setItemIcon(1,negativo)
    main.comboBox_29.setItemIcon(2,naoseaplica)
    main.comboBox_30.addItems(opções)
    main.comboBox_30.setItemIcon(0, positivo)
    main.comboBox_30.setItemIcon(1, negativo)
    main.comboBox_30.setItemIcon(2, naoseaplica)
    main.comboBox_31.addItems(opções)
    main.comboBox_31.setItemIcon(0, positivo)
    main.comboBox_31.setItemIcon(1, negativo)
    main.comboBox_31.setItemIcon(2, naoseaplica)
    main.comboBox_32.addItems(opções)
    main.comboBox_32.setItemIcon(0, positivo)
    main.comboBox_32.setItemIcon(1, negativo)
    main.comboBox_32.setItemIcon(2, naoseaplica)
    main.comboBox_33.addItems(opções)
    main.comboBox_33.setItemIcon(0, positivo)
    main.comboBox_33.setItemIcon(1, negativo)
    main.comboBox_33.setItemIcon(2, naoseaplica)
    main.comboBox_34.addItems(opções)
    main.comboBox_34.setItemIcon(0, positivo)
    main.comboBox_34.setItemIcon(1, negativo)
    main.comboBox_34.setItemIcon(2, naoseaplica)
    main.comboBox_35.addItems(opções)
    main.comboBox_35.setItemIcon(0, positivo)
    main.comboBox_35.setItemIcon(1, negativo)
    main.comboBox_35.setItemIcon(2, naoseaplica)
    main.comboBox_36.addItems(opções)
    main.comboBox_36.setItemIcon(0, positivo)
    main.comboBox_36.setItemIcon(1, negativo)
    main.comboBox_36.setItemIcon(2, naoseaplica)
    main.comboBox_37.addItems(opções)
    main.comboBox_37.setItemIcon(0, positivo)
    main.comboBox_37.setItemIcon(1, negativo)
    main.comboBox_37.setItemIcon(2, naoseaplica)
    main.comboBox_38.addItems(opções)
    main.comboBox_38.setItemIcon(0, positivo)
    main.comboBox_38.setItemIcon(1, negativo)
    main.comboBox_38.setItemIcon(2, naoseaplica)
    main.comboBox_39.addItems(opções)
    main.comboBox_39.setItemIcon(0, positivo)
    main.comboBox_39.setItemIcon(1, negativo)
    main.comboBox_39.setItemIcon(2, naoseaplica)
    main.comboBox_40.addItems(opções)
    main.comboBox_40.setItemIcon(0, positivo)
    main.comboBox_40.setItemIcon(1, negativo)
    main.comboBox_40.setItemIcon(2, naoseaplica)
    main.comboBox_41.addItems(opções)
    main.comboBox_41.setItemIcon(0, positivo)
    main.comboBox_41.setItemIcon(1, negativo)
    main.comboBox_41.setItemIcon(2, naoseaplica)
    main.comboBox_42.addItems(opções)
    main.comboBox_42.setItemIcon(0, positivo)
    main.comboBox_42.setItemIcon(1, negativo)
    main.comboBox_42.setItemIcon(2, naoseaplica)
    main.comboBox_43.addItems(opções)
    main.comboBox_43.setItemIcon(0, positivo)
    main.comboBox_43.setItemIcon(1, negativo)
    main.comboBox_43.setItemIcon(2, naoseaplica)
    main.comboBox_44.addItems(opções)
    main.comboBox_44.setItemIcon(0, positivo)
    main.comboBox_44.setItemIcon(1, negativo)
    main.comboBox_44.setItemIcon(2, naoseaplica)
    main.comboBox_45.addItems(opções)
    main.comboBox_45.setItemIcon(0, positivo)
    main.comboBox_45.setItemIcon(1, negativo)
    main.comboBox_45.setItemIcon(2, naoseaplica)
    main.comboBox_46.addItems(opções)
    main.comboBox_46.setItemIcon(0, positivo)
    main.comboBox_46.setItemIcon(1, negativo)
    main.comboBox_46.setItemIcon(2, naoseaplica)

    main.ocupa_2.clear()
    main.calcada_2.clear()
    main.limitacao_2.clear()
    main.logradouro_2.clear()
    main.numero_2.clear()
    main.complemento_2.clear()
    main.manaus_energia_2.clear()
    main.situacao_unidade_2.clear()
    main.situacao_lote_2.clear()
    main.alinhamento_2.clear()
    main.patrimonio_2.clear()
    main.uso_imovel_2.clear()
    main.escoamento_sanitario_2.clear()
    main.ano_contrucao_2.clear()
    main.habitase_2.clear()
    main.numero_habitante_2.clear()
    main.data_habita_2.clear()
    main.numero_cartorio_2.clear()
    main.tipo_contrucao_2.clear()
    main.estrutura_2.clear()
    main.parede_2.clear()
    main.cobertura_2.clear()
    main.revestimento_2.clear()
    main.terraco_2.clear()
    main.subsolo_2.clear()
    main.padrao_2.clear()
    main.estado_conservacao_2.clear()
    main.posicao_2.clear()
    main.pavimento_2.clear()
    main.pav_contrucao_2.clear()
    main.nome_2.clear()
    main.cpf_2.clear()
    main.rg_2.clear()
    main.telefone_2.clear()
    main.email_2.clear()
    main.nome_fanttasia_2.clear()
    main.razao_2.clear()
    main.cnpj_2.clear()
    main.tipo_atividade_2.clear()
    main.descricao_atividade_2.clear()
    main.nome_comerciante_2.clear()
    main.cpf_comerciante_2.clear()
    main.pav_em_construcao_edi_2.clear()
    """******* RESETANDO VALORES NOS COMBOS BOX **********"""
    opcao_ocupa = ['OK', 'Sem Ocupação', 'Em Construção', 'Construção Paralizada', 'Ruínas, Demolição', 'Edificado',
                   'Estacionamento', 'Lazer', 'Agricultura', 'Depósito', 'Invadido']
    opcao_calcada = ['OK', 'Sem Calçada', 'Com Calçada']
    opcao_limitacao = ['OK', 'Murado', 'Não Murado', 'Cerca/Similar']
    opcao_situacao_unidade = ['OK', 'Frente', 'Fundos', 'Superposta Frente', 'Superposta Fundo', 'Sobreloja', 'Galeria',
                              'Vila']
    opcao_situacao_lote = ['OK', 'Isolada', 'Conjugada', 'Geminada']
    opcao_alinhamento = ['OK', 'Alinhada', 'Recuada']
    opcao_patrimonio = ['OK', 'Particular', 'Religioso', 'Público Municipal', 'Público Estadual', 'Público Federal',
                        'Ent. Sem Fins Lucrativos']
    opcao_uso_do_imovel = ['OK', 'Sem Uso', 'Residencial', 'Comercial', 'Prestação de Serviço', 'Industrial',
                           'Religioso', 'Lazer', 'Serviço Público', 'Instituição Financeira', 'Misto', 'Hotelaria',
                           'Saúde', 'Outros Serviços', 'Abastecimento D''Água', 'Telefonia', 'Subestação de Energia',
                           'Educação', 'Segurança']
    opcao_escoamento = ['OK', 'Céu Aberto', 'Fossa', 'Galeria Pluvial', 'Rede de Esgoto']
    opcao_tipo_contrucao = ['OK', 'Construção Precária', 'Casa', 'Apartamento', 'Apartamento Cobertura',
                            'Sala Comercial', 'Loja', 'Cobertura Simples (Telheiro)', 'Casas Em Cond/Lot. Fechado',
                            'Vulnerabilidade Social', 'Galpão Fechado', 'Galpão Aberto', 'Posto de Combustível',
                            'Arquitetura Especial', 'Edificação Para Uso Industrial', 'Antena', 'Container',
                            'Tanque de Armazenamento', 'Outros']
    opcao_estrutura = ['OK', 'Concreto', 'Alvenaria', 'Madeira', 'Metálica', 'Mista', 'Taipa']
    opcao_parede = ['OK', 'Sem', 'Taipa', 'Mad. Simples', 'Mad. Dupla', 'Alvenaria', 'Concreto', 'Especial', 'Outros']
    opcao_cobertura = ['OK', 'Palha / Zinco', 'Cimento Amianto', 'Telha de Barro', 'Metálica', 'Laje', 'Outros', 'Sem']
    opcao_revestimento = ['OK', 'Sem', 'Emboço', 'Reboco', 'Material Cerâmico', 'Madeira Especial', 'Especial']
    opcao_terraco = ['OK', 'Sim', 'Não']
    opcao_subsolo = ['OK', 'Sim', 'Não']
    opcao_padrao = ['OK', 'Luxo', 'Alto', 'Médio', 'Médio Popular', 'Popular', 'Baixo (Mocambo)']
    opcao_estado_concervacao = ['OK', 'Bom', 'Regular', 'Ruim']
    opcao_pav_contrucao = ['OK', 'True', 'False']
    opcao_pav_edi_2 = ['OK', 'True', 'False']
    main.ocupa_2.addItems(opcao_ocupa)
    main.calcada_2.addItems(opcao_calcada)
    main.limitacao_2.addItems(opcao_limitacao)

    main.situacao_unidade_2.addItems(opcao_situacao_unidade)
    main.situacao_lote_2.addItems(opcao_situacao_lote)
    main.alinhamento_2.addItems(opcao_alinhamento)
    main.patrimonio_2.addItems(opcao_patrimonio)
    main.uso_imovel_2.addItems(opcao_uso_do_imovel)
    main.escoamento_sanitario_2.addItems(opcao_escoamento)
    main.tipo_contrucao_2.addItems(opcao_tipo_contrucao)

    main.estrutura_2.addItems(opcao_estrutura)
    main.parede_2.addItems(opcao_parede)
    main.cobertura_2.addItems(opcao_cobertura)
    main.revestimento_2.addItems(opcao_revestimento)
    main.terraco_2.addItems(opcao_terraco)
    main.subsolo_2.addItems(opcao_subsolo)
    main.padrao_2.addItems(opcao_padrao)
    main.estado_conservacao_2.addItems(opcao_estado_concervacao)
    main.pav_contrucao_2.addItems(opcao_pav_contrucao)
    main.pav_em_construcao_edi_2.addItems(opcao_pav_edi_2)

def chama_tela():
    pesquisar.show()

def resultado():
    nome = pesquisar.txt_cadastrador.text()
    nome_cadastrador = str(nome).upper()
    # print(nome_cadastrador)

    # print(nome)
    if nome != "":
        sql_cadastrador = f""" select id, nome_cadastrador,
                                            id_cadastrador,
                                             unidade_id, 
                                             nome_monitor,
                                             dthr_atualizacao
                                              from stage.monitoria where upper(nome_cadastrador) like '%{str(nome_cadastrador)}%' """
        cursor.execute(sql_cadastrador)
        result = cursor.fetchall()

        pesquisar.tabela_cadastrador.setRowCount(len(result))
        pesquisar.tabela_cadastrador.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
                pesquisar.tabela_cadastrador.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))
        r = len(result)
        pesquisar.qtd.setText(f'{r}')
    else:
        QMessageBox.about(None, "SEM NOME CADASTRADOR", "ADCIONE UM NOME DA CADASTRADOR.")

def chamaTelaM():
    linha = pesquisar.tabela_cadastrador.currentRow()
    nome_cadastrador = pesquisar.txt_cadastrador.text()
    nome = str(nome_cadastrador).upper()
    if linha >= 0:
        result.show()
        retornaMonitoria(linha, nome)
    else:
        QMessageBox.about(None, "SEM ID SELECIONADO", "POR FAVOR SELECIONE UM ID.")

def retornaMonitoria(linha, nome):
    # **********  RETORNAR MONITORIA ************
    nome_cadastrador = nome.upper()
    # print(linha)
    # print(nome_cadastrador.upper())
    a = 'NEGATIVO'


    try:
        if linha >= 0:
            cursor.execute(
                f"select id from stage.monitoria where nome_cadastrador like  '%{nome_cadastrador.upper()}%'")
            dados_lidos = cursor.fetchall()

            valor_id = dados_lidos[linha][0]
            #print(valor_id)

            sql_monitoria = f'''select 	u.ctiid, 
                                        l.ocupacao_do_terreno,
                                        l.calcada,
                                        l.limitacao, 
                                        u.numero,
                                        logradouro_id,
                                        u.ecologradouro_id,
                                        ecologdigitado,
                                        u.manaus_energia,
                                        u.situacao_da_unidade_construida,
                                        u.situacao_relativa_ao_lote,
                                        u.alinhamento,
                                        u.patrimonio,
                                        u.uso_do_imovel,
                                        u.escoamento_sanitario,
                                        u.cdcanoconstrucao,
                                        u.cdcdatahabitese,
                                        u.cdcnmrhabitese,
                                        u.cticatid, 
                                        obs_topocart,
                                        u.tipo_de_construcao,
                                        u.estrutura, u.parede,
                                        u.cobertura, 
                                        u.revestimento_da_fachada,
                                        u.terraco, 
                                        u.subsolo,
                                        u.padrao_construtivo, 
                                        u.estado_de_conservacao, 
                                        u.posicao,
                                        c.nome,
                                        c.cpf,
                                        c.rg, 
                                        c.telefone,
                                        c.email, 
                                        c.ctgid,
                                        e.pavimentos,
                                        cm.cpfresponsavel,
                                        cm.nome_fantasia,
                                        cm.razao_social,
                                        cm.tipo_atividade,
                                        cm.descricao_atividade,
                                        cm.cnpj,
                                        cm.nomeresponsavel,
                                        p.nome,
                                        l.id, 
                                        u.geom,
                                        u.lote_id,
                                        u.obs_topocart,
                                        u.complemento,
                                        u.status_proprietario,
                                            m.nome_monitor, 
                                            m.ocupacao_terreno, m.calcada,
                                            m.limitacao, m.logradouro,
                                            m.numero, m.complemento,
                                            m.quantidade_unidade, m.situacao_unidade,
                                            m.situacao_lote, m.alinhamento,
                                            m.patrimonio, m.uso_do_imovel, 
                                            m.escoamento_sanitario, 
                                            m.ano_de_construcao, 
                                            m.habitese, m.numero_habitese,
                                            m.numero_cartorio, m.nome_cartorio,
                                            m.tipo_de_construcao, m.parede,
                                            m.cobertura, m.revestimento_fachada,
                                            m.terraco, m.subsolo, m.padrao_construtivo,
                                            m.estado_de_conservacao, m.lancou, 
                                            m.posicao, m.pavimento, 
                                            m.pavimento_construcao, 
                                            m.nome_proprietario, m.cpf_proprietario,
                                            m.rg_proprietario, m.telefone_proprietario,
                                            m.email_proprietario, m.nome_fantasia,
                                            m.razao_social, m.cnpj, m.tipo_atividade,
                                            m.descricao_atividade, m.nome_responsavel,
                                            m.cpf_responsavel, m.edif_secundaria_lancou,
                                            m.edif_secundaria_posicao, m.edif_secundaria_pavimento,
                                            m.observacao_topocart, m.observacao_monitor,
                                            m.edif_secundaria_pav_em_construcao,
                                            m.manaus_energia, m.dthabitese, m.dthr_atualizacao, posicao_2, pavimento_2, pav_em_construcao_2
                                from cadastro.unidade u
                                left join cadastro.lote l on l.id = u.lote_id
                                left join cadastro.contribuinte c on u.ctictgid = c.ctgid
                                left join cadastro.edificacao e on e.unidade_id = u.ctiid
                                left join cadastro.mobiliario cm on cm.ctgidresponsavel_id = c.ctgid
                                left join public.pessoa p on p.id = u.cadastrador 
                                join stage.monitoria as m on m.unidade_id = u.ctiid
                                where m.id =  {str(valor_id)}
                                limit 1

                    '''
            lista = []
            cursor.execute(sql_monitoria)
            monitoria = cursor.fetchall()
            if monitoria[0] != None:

                for row in monitoria:
                    lista.append(row)

                    # print(len(monitoria))
                    #print(monitoria)

                    # ******* MOSTRAR FOTO ********

                sql_imagem = f"select imagem, count(imagem) from foto_fachada.foto_fachada_arquivo where lote_id ={lista[0][45]} group by imagem"
                cursor.execute(sql_imagem)
                fotos = cursor.fetchall()
                image = []
                autoSize = 371
                largSize =500
                if len(fotos) > 0:
                    for f in fotos:
                        image.append(f[0])
                        row = f[1]
                        # SE FOTO EXISTIR MOSTRE ELA
                    chave = True

                    image_pil = Image.open(io.BytesIO(image[0]))
                    image_pil.save('foto.png')
                    foto_red = Image.open('foto.png')
                    foto_red = foto_red.resize((autoSize, largSize), Image.ANTIALIAS)
                    foto_red.save('newfoto.png')
                    # print(type(image_pil))
                    result.foto.setPixmap(QPixmap('newfoto.png'))  # PRINTA FOTO NA TELA
                    result.foto_2.setText('Sem foto disponível no momento')
                else:
                    result.foto.setText('Sem foto disponível no momento')
                    #result.foto_2.setText('Sem foto disponível no momento')

                if len(monitoria) > 0:
                    # print(lista[0][1])
                    result.matricula.setText(str(lista[0][0]))
                    result.ocupa.setText(str(lista[0][1]))
                    result.calcada.setText(str(lista[0][2]))
                    result.limitacao.setText(str(lista[0][3]))
                    result.logradouro.setText(str(lista[0][5]))
                    result.numero.setText(str(lista[0][4]))
                    result.complemento.setText(str(lista[0][49]))
                    result.manaus_energia.setText(str(lista[0][8]))
                    result.situacao_unidade.setText(str(lista[0][9]))
                    result.situacao_lote.setText(str(lista[0][10]))
                    result.alinhamento.setText(str(lista[0][11]))
                    result.patrimonio.setText(str(lista[0][12]))
                    result.uso_imovel.setText(str(lista[0][13]))
                    result.escoamento_sanitario.setText(str(lista[0][14]))
                    result.ano_contrucao.setText(str(lista[0][15]))
                    result.numero_habitante.setText(str(lista[0][17]))
                    result.data_habita.setText(str(lista[0][16]))
                    result.nome_cartorio.setText(str(lista[0][18]))
                    result.tipo_contrucao.setText(str(lista[0][20]))
                    result.parede.setText(str(lista[0][22]))
                    result.cobertura.setText(str(lista[0][23]))
                    result.revestimento.setText(str(lista[0][24]))
                    result.terraco.setText(str(lista[0][25]))
                    result.subsolo.setText(str(lista[0][26]))
                    result.padrao.setText(str(lista[0][27]))
                    result.estado_conservacao.setText(str(lista[0][28]))
                    result.pavimento.setText(str(lista[0][36]))
                    result.nome.setText(str(lista[0][30]))
                    result.cpf.setText(str(lista[0][31]))
                    result.rg.setText(str(lista[0][32]))
                    result.telefone.setText(str(lista[0][33]))
                    result.email.setText(str(lista[0][34]))
                    result.nome_fanttasia.setText(str(lista[0][38]))
                    result.razao.setText(str(lista[0][39]))
                    result.cnpj.setText(str(lista[0][42]))
                    result.tipo_atividade.setText(str(lista[0][40]))
                    result.descricao_atividade.setText(str(lista[0][41]))
                    result.nome_comerciante.setText(str(lista[0][43]))
                    result.cpf_comerciante.setText(str(lista[0][37]))
                    result.nome_cadastrador.setText(str(lista[0][44]))
                    result.lote_id.setText(str(lista[0][45]))
                    result.observacao.setText(str(lista[0][48]))
                    result.status_proprietario.setText(str(lista[0][50].upper()))
                    # *********** MONITORIA ***********
                    result.ocupa_2.setText(str(lista[0][52]))
                    result.calcada_2.setText(str(lista[0][53]))
                    result.limitacao_2.setText(str(lista[0][54]))
                    result.logradouro_2.setText(str(lista[0][55]))
                    result.numero_2.setText(str(lista[0][56]))
                    result.complemento_2.setText(str(lista[0][57]))
                    result.qtd_unidade_2.setText(str(lista[0][58]))
                    result.manaus_energia_2.setText(str(lista[0][99]))
                    result.situacao_unidade_2.setText(str(lista[0][59]))
                    result.situacao_lote_2.setText(str(lista[0][60]))
                    result.alinhamento_2.setText(str(lista[0][61]))
                    result.patrimonio_2.setText(str(lista[0][62]))
                    result.uso_imovel_2.setText(str(lista[0][63]))
                    result.escoamento_sanitario_2.setText(str(lista[0][64]))
                    result.ano_contrucao_2.setText(str(lista[0][65]))
                    result.habite_2.setText(str(lista[0][66]))
                    result.numero_habitante_2.setText(str(lista[0][67]))
                    result.data_habita_2.setText(str(lista[0][100]))
                    result.numero_cartorio_2.setText(str(lista[0][68]))
                    result.nome_cartorio_2.setText(str(lista[0][69]))
                    result.tipo_contrucao_2.setText(str(lista[0][70]))
                    result.parede_2.setText(str(lista[0][71]))
                    result.cobertura_2.setText(str(lista[0][72]))
                    result.revestimento_2.setText(str(lista[0][73]))
                    result.terraco_2.setText(str(lista[0][74]))
                    result.subsolo_2.setText(str(lista[0][75]))
                    result.padrao_2.setText(str(lista[0][76]))
                    result.estado_conservacao_2.setText(str(lista[0][77]))
                    result.lancou_2.setText(str(lista[0][78]))
                    result.posicao_2.setText(str(lista[0][79]))
                    result.pavimento_2.setText(str(lista[0][80]))
                    result.pav_contrucao_2.setText(str(lista[0][81]))
                    result.nome_2.setText(str(lista[0][82]))
                    result.cpf_2.setText(str(lista[0][83]))
                    result.rg_2.setText(str(lista[0][84]))
                    result.telefone_2.setText(str(lista[0][85]))
                    result.email_2.setText(str(lista[0][86]))
                    result.nome_fanttasia_2.setText(str(lista[0][87]))
                    result.razao_2.setText(str(lista[0][88]))
                    result.cnpj_2.setText(str(lista[0][89]))
                    result.tipo_atividade_2.setText(str(lista[0][90]))
                    result.descricao_atividade_2.setText(str(lista[0][91]))
                    result.nome_comerciante_2.setText(str(lista[0][92]))
                    result.cpf_comerciante_2.setText(str(lista[0][93]))
                    result.monitor.setText(str(lista[0][51]))
                    result.observacao_avaliacao.setText(str(lista[0][98]))

                else:
                    print('a')
    except Exception as e:
        print(e)
        QMessageBox.about(None, "SEM ID SELECIONADO!!!", "SELECIONE UM ID :) ")

def voltarMain():
    pesquisar.close()

def pegarDadosEditados():
    try:
        unidade_id = main.matricula.text()
        nome_monitor = main.monitor.text()
        listaatualiza = []
        primeiroscampos=[]
        listaatualiza.append(main.ocupa_2.currentText()) # 0
        listaatualiza.append(main.calcada_2.currentText()) # 1
        listaatualiza.append(main.limitacao_2.currentText()) # 2
        listaatualiza.append(main.logradouro_2.text()) # 3
        listaatualiza.append(main.numero_2.text()) # 4
        listaatualiza.append(main.complemento_2.text()) # 5
        listaatualiza.append(main.situacao_unidade_2.currentText()) # 6
        listaatualiza.append(main.situacao_lote_2.currentText()) # 7
        listaatualiza.append(main.alinhamento_2.currentText()) # 8
        listaatualiza.append(main.patrimonio_2.currentText()) # 9
        listaatualiza.append(main.uso_imovel_2.currentText()) # 10
        listaatualiza.append(main.escoamento_sanitario_2.currentText()) # 11
        listaatualiza.append(main.ano_contrucao_2.text()) # 12
        listaatualiza.append(main.habitase_2.text()) # 13
        listaatualiza.append(main.numero_habitante_2.text()) # 14
        listaatualiza.append(main.numero_cartorio_2.text()) # 15
        listaatualiza.append(main.nome_cartorio_2.text()) # 16
        listaatualiza.append(main.tipo_contrucao_2.currentText()) # 17
        listaatualiza.append(main.parede_2.currentText()) # 18
        listaatualiza.append(main.cobertura_2.currentText()) #19
        listaatualiza.append(main.revestimento_2.currentText()) #20
        listaatualiza.append(main.terraco_2.currentText()) # 21
        listaatualiza.append(main.subsolo_2.currentText()) # 22
        listaatualiza.append(main.padrao_2.currentText()) # 23
        listaatualiza.append(main.estado_conservacao_2.currentText()) # 24
        listaatualiza.append(main.posicao_2.text()) # 25
        listaatualiza.append(main.pavimento_2.text()) # 26
        listaatualiza.append(main.pav_contrucao_2.currentText()) # 27
        listaatualiza.append(main.nome_2.text()) # 28
        listaatualiza.append(main.cpf_2.text()) # 29
        listaatualiza.append(main.rg_2.text()) # 30
        listaatualiza.append(main.telefone_2.text()) # 31
        listaatualiza.append(main.email_2.text()) # 32
        listaatualiza.append(main.nome_fanttasia_2.text()) # 33
        listaatualiza.append(main.razao_2.text()) # 34
        listaatualiza.append(main.cnpj_2.text()) # 35
        listaatualiza.append(main.tipo_atividade_2.text()) # 36
        listaatualiza.append(main.descricao_atividade_2.text()) # 37
        listaatualiza.append(main.nome_comerciante_2.text()) # 38
        listaatualiza.append(main.cpf_comerciante_2.text()) # 39
        listaatualiza.append(main.manaus_energia_2.text()) #40
        listaatualiza.append(main.data_habita_2.text()) # 41
        listaatualiza.append(main.estrutura_2.currentText()) # 42
        listaatualiza.append(main.nome_cadastrador.text()) # 43
        listaatualiza.append(main.lote_id.text()) # 44
        listaatualiza.append(main.posicao_edi_2.text()) # 45
        listaatualiza.append(main.pavimento_edi_2.text()) # 46
        listaatualiza.append(main.pav_em_construcao_edi_2.currentText()) #47
        #print(nome_monitor,unidade_id, listaatualiza)

        primeiroscampos.append(main.ocupa.text())
        primeiroscampos.append(main.calcada.text())
        primeiroscampos.append(main.limitacao.text())
        primeiroscampos.append(main.logradouro.text())
        primeiroscampos.append(main.numero.text())
        primeiroscampos.append(main.complemento.text())
        primeiroscampos.append(main.situacao_unidade.text())
        primeiroscampos.append(main.situacao_lote.text())
        primeiroscampos.append(main.alinhamento.text())
        primeiroscampos.append(main.patrimonio.text())
        primeiroscampos.append(main.uso_imovel.text())
        primeiroscampos.append(main.escoamento_sanitario.text())
        primeiroscampos.append(main.ano_contrucao.text())
        primeiroscampos.append(main.habitase.text())
        primeiroscampos.append(main.numero_habitante.text())
        primeiroscampos.append(main.numero_cartorio.text())
        primeiroscampos.append(main.nome_cartorio.text())
        primeiroscampos.append(main.tipo_contrucao.text())
        primeiroscampos.append(main.parede.text())
        primeiroscampos.append(main.cobertura.text())
        primeiroscampos.append(main.revestimento.text())
        primeiroscampos.append(main.terraco.text())
        primeiroscampos.append(main.subsolo.text())
        primeiroscampos.append(main.padrao.text())
        primeiroscampos.append(main.estado_conservacao.text())
        primeiroscampos.append(main.posicao.text())
        primeiroscampos.append(main.pavimento.text())
        primeiroscampos.append(main.pav_contrucao.text())
        primeiroscampos.append(main.nome.text())
        primeiroscampos.append(main.cpf.text())
        primeiroscampos.append(main.rg.text())
        primeiroscampos.append(main.telefone.text())
        primeiroscampos.append(main.email.text())
        primeiroscampos.append(main.nome_fanttasia.text())
        primeiroscampos.append(main.razao.text())
        primeiroscampos.append(main.cnpj.text())
        primeiroscampos.append(main.tipo_atividade.text())
        primeiroscampos.append(main.descricao_atividade.text())
        primeiroscampos.append(main.nome_comerciante.text())
        primeiroscampos.append(main.cpf_comerciante.text())
        primeiroscampos.append(main.manaus_energia.text())
        primeiroscampos.append(main.data_habita.text())
        primeiroscampos.append(main.estrutura.text())
        primeiroscampos.append(main.nome_cadastrador.text())
        primeiroscampos.append(main.lote_id.text())
        primeiroscampos.append(main.posicao_edi.text())
        primeiroscampos.append(main.pavimento_edi.text())
        primeiroscampos.append(main.pav_em_construcao_edi.text())
        """ ****** CHEGANDO SE ALGUM DADO FOI ALTERADO ******"""
        sql_check = f"""Select id, ocupacao_terreno ,
                                                        calcada ,
                                                        limitacao ,
                                                        logradouro,
                                                        numero ,
                                                        complemento ,
                                                        situacao_unidade ,
                                                        situacao_lote ,
                                                        alinhamento ,
                                                        patrimonio ,
                                                        uso_do_imovel,
                                                        escoamento_sanitario ,
                                                        habitese ,
                                                        tipo_de_construcao,
                                                        parede ,
                                                        cobertura ,
                                                        revestimento_fachada,
                                                        terraco,
                                                        subsolo ,
                                                        padrao_construtivo ,
                                                        estado_de_conservacao ,
                                                        posicao ,
                                                        pavimento,
                                                        pavimento_construcao ,
                                                        nome_proprietario,
                                                        cpf_proprietario ,
                                                        rg_proprietario,
                                                        telefone_proprietario,
                                                        email_proprietario,
                                                        nome_fantasia ,
                                                        razao_social,
                                                        cnpj,
                                                        tipo_atividade ,
                                                        descricao_atividade,
                                                        nome_responsavel,
                                                        cpf_responsavel,
                                                        manaus_energia,
                                                        estrutura,
                                                        posicao_edificacao,
                                                        pavimento_edificacao,
                                                        pavimento_construcao
                                                        nome_monitor from stage.edicao_monitoria where unidade_id = {str(unidade_id)}"""
        cursor.execute(sql_check)
        check_result = cursor.fetchall()

        l = 0
        cont=0
        for b in listaatualiza:
            p = 0
            for j in primeiroscampos:
                if b == j and l == p:
                    cont += 1
                    break
                elif b == 'OK':
                    cont +=1
                    break

                p += 1
            l += 1
        l = 0

       # for b in listaatualiza:
        #    c =0
         #   for j in check_result:
          #      if



        if cont == len(listaatualiza):
            QMessageBox.about(None, 'OPA.',' ***** NENHUM DADO FOI MODIFICADO *****' )
        else:

            i = 0
            x = 0
            """ ***************** FORMATAÇÃO E CORREÇÃO DA ENTRADA DE DADOS ********************* """
            i=0
            indiceOk = []
            #print(listaatualiza[15])
            #print(primeiroscampos[15], 'COMPARACAO')
            """
            *********
            Verifica se os dados antigos e editos são igual 
            se sim editado rebece "null"
            """
            for b in listaatualiza:
                x=0
                for j in primeiroscampos:
                    if b == j and i ==x :
                        if i == 43 or i == 44 :
                            break
                        elif i == 15 or i ==14 or i == 25 or i == 26 or i == 27 or i == 31 or i == 35 or i ==41 or i == 45 or i ==46 or i ==47:
                            print(i)
                            listaatualiza[i] = "NULL"
                            #print(i, 'agora é nulo', j ,' ',b, ' ',x)
                            break
                        #print('iguais: ' +b+ ' - '+ j)
                        listaatualiza[i] = 'OK'
                        #print(i)

                        break
                    x += 1
                i += 1

            #print(listaatualiza)
            #print(listaatualiza[15])
            print(listaatualiza[26])
            i=0
            """
            Verifica se alguma numerico campo 
            da edição veio "None" ou "Null"
            se for String recebe Ok
            se for numerico ou boolean recebe null
            """
            for a in listaatualiza:
                print(i, ' ', a)

                if a == 'None' and i !=15 and i != 25 and i!=26 and i!=27 and i!=31 and i!=35 and i!=45 and i!= 46 and i!=47:
                    listaatualiza[i] = 'OK'
                elif i == 15  and a == None:
                    if a == 'None' :
                        listaatualiza[i]= 'NULL'
                        continue
                    #print(a)
                    #a = ''.join(c for c in a if c.isdigit())
                    #a = int(a)
                    #listaatualiza[i] = a
                elif i == 25 and (a == None or a == '' or a == 'None' or a == 'OK' ):
                    if a == 'None' or a == '' or a == 'OK':
                       # print(i)
                        listaatualiza[i]= 'NULL'
                        #print((listaatualiza[i]))
                        continue
                    #print(a)
                    # a = ''.join(c for c in a if c.isdigit())
                    # a = int(a)
                    # listaatualiza[i] = a
                elif i == 26 and (a == None or a =='' or a == 'None' or a == 'OK' ):
                    if a == 'None' or a =='' or a == 'OK':
                        print('26')
                        listaatualiza[i] = 'NULL'
                        print((listaatualiza[i]))
                        continue
                    #print(a)
                    # a = ''.join(c for c in a if c.isdigit())
                    # a = int(a)
                    # listaatualiza[i] = a
                elif i == 27 and (a == None or a =='' or a == 'None' or a == 'OK' ):
                    if a == 'None' or a =='' or a == 'OK':
                        a = 'NULL'
                        listaatualiza[i] = a
                        print((listaatualiza[i]))
                        continue
                    elif a == 'False':
                        a = False
                        listaatualiza[i] = a
                    else:
                        a = True
                        listaatualiza[i] = a
                elif i == 31 and (a == None or a =='' or a == 'None' or a == 'OK' ):
                    if a == 'None' or a =='' or a == 'OK':
                        print('telefone')
                        listaatualiza[i]= 'NULL'
                        continue
                    #print(a)
                    # a = ''.join(c for c in a if c.isdigit())
                    # a = int(a)
                    # listaatualiza[i] = a
                elif i == 35 and (a == '' or a == None or a == 'None' or a == 'OK') :
                    if a == 'None' or a =='':
                        listaatualiza[i]= 'NULL'
                        continue
                    #print(a)
                    # a = ''.join(c for c in a if c.isdigit())
                    # a = int(a)
                    # listaatualiza[i] = a
                """    
                elif i == 45 and (a == None or a == '' or a == 'None' or a == 'OK' ):
                    print(i)
                    listaatualiza[i]= 'NULL'
                    continue
                    #print(a)
                    a = ''.join(c for c in a if c.isdigit())
                    a = int(a)
                    listaatualiza[i] = a
                elif i == 46 and (a == None or a =='' or a == 'None' or a == 'OK' ):
                    if a == 'None' or a =='' or a == 'OK':
                        print('asdasdasd')
                        listaatualiza[i]= 'NULL'
                        continue
                    #print(a)
                    #a = ''.join(c for c in a if c.isdigit())
                    #a = int(a)
                    #listaatualiza[i] = a
                elif i == 47 and (a == None or a =='' or a == 'None' or a == 'OK'):
                    if a == 'None' or a =='' or a == 'OK':
                        print('asdasdasd')
                        listaatualiza[i]= 'NULL'
                        continue
                    elif a == 'False':
                        a = False
                        listaatualiza[i] = a
                    else:
                        a = True
                        listaatualiza[i] = a
                """
                i += 1
            #print(primeiroscampos)
            #print(listaatualiza)
            #print(listaatualiza[15])
            if listaatualiza[31] == None or listaatualiza[31] == 'None' or listaatualiza[31] == 'OK':
                listaatualiza[31] = 'NULL'
            if listaatualiza[31] == None or listaatualiza[31] == 'None' or listaatualiza[31] == 'OK':
                listaatualiza[31] = 'NULL'
            if listaatualiza[45] == None or listaatualiza[45] == 'None' or listaatualiza[45] == 'OK' :
                listaatualiza[45] = 'NULL'
            if listaatualiza[46] == None or listaatualiza[46] == 'None' or listaatualiza[46] == 'OK':
                listaatualiza[46] = 'NULL'
            if listaatualiza[47] == None or listaatualiza[47] == 'None' or listaatualiza[47] == 'OK':
                listaatualiza[47] = 'NULL'
            print(listaatualiza[27] ,listaatualiza[45], listaatualiza[46], listaatualiza[47])
            if len(check_result) > 0 :

                print(listaatualiza)
                print('id=', check_result[0][0])
                sql_updadate = f""" update stage.edicao_monitoria set ocupacao_terreno = '{listaatualiza[0]}',
                                                calcada = '{listaatualiza[1]}',
                                                limitacao = '{listaatualiza[2]}',
                                                logradouro = '{listaatualiza[3]}',
                                                numero = '{listaatualiza[4]}',
                                                complemento = '{listaatualiza[5]}',
                                                situacao_unidade = '{listaatualiza[6]}',
                                                situacao_lote = '{listaatualiza[7]}' ,
                                                alinhamento = '{listaatualiza[8]}',
                                                patrimonio = '{listaatualiza[9]}',
                                                uso_do_imovel= '{listaatualiza[10]}',
                                                escoamento_sanitario = '{listaatualiza[11]}',
                                                habitese = '{listaatualiza[13]}',
                                                tipo_de_construcao = '{listaatualiza[17]}',
                                                parede = '{listaatualiza[18]}',
                                                cobertura = '{listaatualiza[19]}',
                                                revestimento_fachada = '{listaatualiza[20]}',
                                                terraco = '{listaatualiza[21]}',
                                                subsolo = '{listaatualiza[22]}',
                                                padrao_construtivo = '{listaatualiza[23]}',
                                                estado_de_conservacao = '{listaatualiza[24]}',
                                                posicao = {listaatualiza[25]},
                                                pavimento = {listaatualiza[26]},
                                                pavimento_construcao = {listaatualiza[27]},
                                                nome_proprietario = '{listaatualiza[28]}',
                                                cpf_proprietario = '{listaatualiza[29]}',
                                                rg_proprietario = '{listaatualiza[30]}',
                                                telefone_proprietario = {listaatualiza[31]},
                                                email_proprietario = '{listaatualiza[32]}',
                                                nome_fantasia = '{listaatualiza[33]}',
                                                razao_social = '{listaatualiza[34]}',
                                                cnpj = {listaatualiza[35]},
                                                tipo_atividade = '{listaatualiza[36]}',
                                                descricao_atividade = '{listaatualiza[37]}',
                                                nome_responsavel = '{listaatualiza[38]}',
                                                cpf_responsavel = '{listaatualiza[39]}',
                                                manaus_energia = '{listaatualiza[40]}',
                                                estrutura = '{listaatualiza[42]}',
                                                nome_monitor = '{nome_monitor}',
                                                posicao_edificacao = {listaatualiza[45]},
                                                pavimento_edificacao = {listaatualiza[46]},
                                                pavimento_construcao_edificacao ={listaatualiza[47]}
                                                where id = {str(check_result[0][0])}; """
                cursor.execute(sql_updadate)
                connect.commit()
                QMessageBox.about(None, 'ATUALIZAÇÃO', '**** DADOS ATUALIZADOS COM SUCESSO. **** ')
            else:
                if nome_monitor != '':
                    """ ***************** INSERÇÃO DE DADOS EDITADOS ************************* """
                    sql_insert_edicao = """ INSERT INTO stage.edicao_monitoria(unidade_id,
                                                ocupacao_terreno,
                                                calcada,
                                                limitacao,
                                                logradouro,
                                                numero,
                                                complemento,
                                                situacao_unidade,
                                                situacao_lote,
                                                alinhamento,
                                                patrimonio,
                                                uso_do_imovel,
                                                escoamento_sanitario,
                                                habitese,
                                                numero_habitese,
                                                numero_cartorio,
                                                tipo_de_construcao,
                                                parede,
                                                cobertura,
                                                revestimento_fachada,
                                                terraco,
                                                subsolo,
                                                padrao_construtivo,
                                                estado_de_conservacao,
                                                posicao,
                                                pavimento,
                                                pavimento_construcao,
                                                nome_proprietario,
                                                cpf_proprietario,
                                                rg_proprietario,
                                                telefone_proprietario,
                                                email_proprietario,
                                                nome_fantasia,
                                                razao_social,
                                                cnpj,
                                                tipo_atividade,
                                                descricao_atividade,
                                                nome_responsavel,
                                                cpf_responsavel,
                                                manaus_energia,
                                                estrutura,
                                                nome_monitor,
                                                nome_cadastrador,
                                                lote_id,
                                                posicao_edificacao,
                                                pavimento_edificacao,
                                                pavimento_construcao_edificacao
                                                ) VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', {},{},'{}','{}','{}','{}','{}','{}','{}', '{}',{},{},{}, '{}','{}','{}', {},'{}','{}','{}', {}, '{}', '{}','{}','{}','{}','{}', '{}', '{}', {},{},{},{}) """.format(
                        unidade_id, listaatualiza[0], listaatualiza[1], listaatualiza[2], listaatualiza[3],
                        listaatualiza[4], listaatualiza[5],
                        listaatualiza[6], listaatualiza[7], listaatualiza[8], listaatualiza[9], listaatualiza[10],
                        listaatualiza[11], listaatualiza[13], listaatualiza[14], listaatualiza[15], listaatualiza[17],
                        listaatualiza[18], listaatualiza[19]
                        , listaatualiza[20], listaatualiza[21], listaatualiza[22], listaatualiza[23], listaatualiza[24],
                        listaatualiza[25], listaatualiza[26], listaatualiza[27], listaatualiza[28], listaatualiza[29],
                        listaatualiza[30],
                        listaatualiza[31], listaatualiza[32], listaatualiza[33], listaatualiza[34], listaatualiza[35],
                        listaatualiza[36], listaatualiza[37], listaatualiza[38], listaatualiza[39], listaatualiza[40],
                        listaatualiza[42], nome_monitor, listaatualiza[43], listaatualiza[44], listaatualiza[45], listaatualiza[46], listaatualiza[47])
                    cursor.execute(sql_insert_edicao)
                    connect.commit()
                    QMessageBox.about(None,'Parabens! :)','Edição salva com sucesso')
                else:
                    QMessageBox.about(None,"ATENÇÃO!!", "**** NOME DO MONITOR ESTÁ VAZIO ****")
    except Exception as e :
        print(e)
        cursor.execute("ROLLBACK")
        connect.commit()
        QMessageBox.about(None, 'OPA.', f'**** ALGUM CAMPO ERRADO OU FALHA AO ENVIAR. ****')

def checarMonitoria(ctiid):
    print(ctiid)
    valor_edit=0
    lista_monitoria = []
    try:
        sql_check = f"""SELECT  unidade_id,
            ocupacao_terreno,
            calcada,
            limitacao,
            logradouro,
            numero,
            complemento,
            situacao_unidade,
            situacao_lote,
            alinhamento,
            patrimonio,
            uso_do_imovel,
            escoamento_sanitario,
            ano_de_construcao,
            habitese,
            numero_habitese,
            numero_cartorio,
            nome_cartorio,
            tipo_de_construcao,
            parede,
            cobertura,
            revestimento_fachada,
            terraco,
            subsolo,
            padrao_construtivo,
            estado_de_conservacao,
            lancou,
            posicao,
            pavimento,
            pavimento_construcao,
            nome_proprietario, 
            cpf_proprietario,
            rg_proprietario,
            telefone_proprietario,
            email_proprietario,
            nome_fantasia,
            razao_social,
            cnpj,
            tipo_atividade,
            descricao_atividade,
            nome_responsavel,
            cpf_responsavel,
            manaus_energia,
            dthabitese,
            estrutura,
            posicao_2,
            pavimento_2,
            pav_em_construcao_2
            FROM stage.monitoria where unidade_id = {str(ctiid)} """
        cursor.execute(sql_check)
        resultado_sql = cursor.fetchall()

        #print(resultado_sql)
        if len(resultado_sql) > 0:
            QMessageBox.about(None,'Opa.', 'Você já fez a monitoria dessa matrícula')

            main.comboBox.setCurrentText(resultado_sql[0][1])
            main.comboBox_2.setCurrentText(resultado_sql[0][2])
            main.comboBox_3.setCurrentText(resultado_sql[0][3])
            main.comboBox_4.setCurrentText(resultado_sql[0][4])
            main.comboBox_5.setCurrentText(resultado_sql[0][5])
            main.comboBox_6.setCurrentText(resultado_sql[0][6])
            main.comboBox_8.setCurrentText(resultado_sql[0][42])
            main.comboBox_9.setCurrentText(resultado_sql[0][7])
            main.comboBox_10.setCurrentText(resultado_sql[0][8])
            main.comboBox_11.setCurrentText(resultado_sql[0][9])
            main.comboBox_12.setCurrentText(resultado_sql[0][10])
            main.comboBox_13.setCurrentText(resultado_sql[0][11])
            main.comboBox_14.setCurrentText(resultado_sql[0][12])
            main.comboBox_15.setCurrentText(resultado_sql[0][13])
            main.comboBox_16.setCurrentText(resultado_sql[0][14])
            main.comboBox_17.setCurrentText(resultado_sql[0][15])
            main.comboBox_18.setCurrentText(resultado_sql[0][43])
            main.comboBox_19.setCurrentText(resultado_sql[0][16])
            main.comboBox_20.setCurrentText(resultado_sql[0][17])
            main.comboBox_21.setCurrentText(resultado_sql[0][18])
            main.comboBox_7.setCurrentText(resultado_sql[0][44])
            main.comboBox_22.setCurrentText(resultado_sql[0][19])
            main.comboBox_23.setCurrentText(resultado_sql[0][20])
            main.comboBox_24.setCurrentText(resultado_sql[0][21])
            main.comboBox_25.setCurrentText(resultado_sql[0][22])
            main.comboBox_26.setCurrentText(resultado_sql[0][23])
            main.comboBox_27.setCurrentText(resultado_sql[0][24])
            main.comboBox_28.setCurrentText(resultado_sql[0][25])
            main.comboBox_30.setCurrentText(resultado_sql[0][27])
            main.comboBox_31.setCurrentText(resultado_sql[0][28])
            main.comboBox_32.setCurrentText(resultado_sql[0][29])
            main.comboBox_33.setCurrentText(resultado_sql[0][30])
            main.comboBox_34.setCurrentText(resultado_sql[0][31])
            main.comboBox_35.setCurrentText(resultado_sql[0][32])
            main.comboBox_36.setCurrentText(resultado_sql[0][33])
            main.comboBox_37.setCurrentText(resultado_sql[0][34])
            main.comboBox_38.setCurrentText(resultado_sql[0][35])
            main.comboBox_39.setCurrentText(resultado_sql[0][36])
            main.comboBox_40.setCurrentText(resultado_sql[0][37])
            main.comboBox_41.setCurrentText(resultado_sql[0][38])
            main.comboBox_42.setCurrentText(resultado_sql[0][39])
            main.comboBox_43.setCurrentText(resultado_sql[0][40])
            main.comboBox_44.setCurrentText(resultado_sql[0][41])
            main.comboBox_29.setCurrentText(resultado_sql[0][45])
            main.comboBox_45.setCurrentText(resultado_sql[0][46])
            main.comboBox_46.setCurrentText(resultado_sql[0][47])

            sql_check_edicao = f""" SELECT id,
            unidade_id, 
            ocupacao_terreno,
            calcada,
            limitacao,
            logradouro,
            numero, 
            complemento,
            situacao_unidade,
            situacao_lote,
            alinhamento, 
            patrimonio, 
            uso_do_imovel,
            escoamento_sanitario,
            ano_de_construcao,
            habitese,
            numero_habitese,
            numero_cartorio, 
            nome_cartorio,
            tipo_de_construcao,
            parede,
            cobertura,
            revestimento_fachada,
            terraco,
            subsolo,
            padrao_construtivo,
            estado_de_conservacao,
            posicao,
            pavimento,
            pavimento_construcao,
            nome_proprietario,
            cpf_proprietario,
            rg_proprietario,
            telefone_proprietario,
            email_proprietario,
            nome_fantasia,
            razao_social,
            cnpj,
            tipo_atividade,
            descricao_atividade,
            nome_responsavel,
            cpf_responsavel, 
            manaus_energia, 
            dthabitese, 
            estrutura, 
            nome_monitor,
            lote_id,
            posicao_edificacao,
            pavimento_edificacao,
            pavimento_construcao_edificacao
                FROM stage.edicao_monitoria where unidade_id = {str(ctiid)}; """

            cursor.execute(sql_check_edicao)
            edit_resultado = cursor.fetchall()
            """******** VERIFICA SE EXISTE EDIÇÃO ************"""
            if len(edit_resultado) > 0:
               print('tem edicao')
               valor_edit = 1
               main.ocupa_2.setItemText(0, edit_resultado[0][2])
               main.calcada_2.setItemText(0, edit_resultado[0][3])
               main.limitacao_2.setItemText(0, edit_resultado[0][4])
               main.logradouro_2.setText(str(edit_resultado[0][5]))
               main.numero_2.setText(str(edit_resultado[0][6]))
               main.complemento_2.setText(str(edit_resultado[0][7]))
               main.manaus_energia_2.setText(str(edit_resultado[0][42]))
               main.situacao_unidade_2.setItemText(0, edit_resultado[0][8])
               main.situacao_lote_2.setItemText(0, edit_resultado[0][9])
               main.alinhamento_2.setItemText(0, edit_resultado[0][10])
               main.patrimonio_2.setItemText(0, edit_resultado[0][11])
               main.uso_imovel_2.setItemText(0, edit_resultado[0][12])
               main.escoamento_sanitario_2.setItemText(0, edit_resultado[0][13])
               main.ano_contrucao_2.setText(str(edit_resultado[0][14]))
               main.habitase_2.setText(str(edit_resultado[0][15]))
               main.numero_habitante_2.setText(str(edit_resultado[0][16]))
               main.data_habita_2.setText(str(edit_resultado[0][43]))
               main.numero_cartorio_2.setText(str(edit_resultado[0][17]))
               main.tipo_contrucao_2.setItemText(0, edit_resultado[0][19])
               main.estrutura_2.setItemText(0, edit_resultado[0][44])
               main.parede_2.setItemText(0, edit_resultado[0][20])
               main.cobertura_2.setItemText(0, edit_resultado[0][21])
               main.revestimento_2.setItemText(0, edit_resultado[0][22])
               main.terraco_2.setItemText(0, edit_resultado[0][23])
               main.subsolo_2.setItemText(0, edit_resultado[0][24])
               main.padrao_2.setItemText(0, edit_resultado[0][25])
               main.estado_conservacao_2.setItemText(0, edit_resultado[0][26])
               main.posicao_2.setText(str(edit_resultado[0][27]))
               main.pavimento_2.setText(str(edit_resultado[0][28]))
               main.pav_contrucao_2.setItemText(0, str(edit_resultado[0][29]))
               main.nome_2.setText(str(edit_resultado[0][30]))
               main.cpf_2.setText(edit_resultado[0][31])
               main.rg_2.setText(str(edit_resultado[0][32]))
               main.telefone_2.setText(str(edit_resultado[0][33]))
               main.email_2.setText(str(edit_resultado[0][34]))
               main.nome_fanttasia_2.setText(str(edit_resultado[0][35]))
               main.razao_2.setText(str(edit_resultado[0][36]))
               main.cnpj_2.setText(str(edit_resultado[0][37]))
               main.tipo_atividade_2.setText(str(edit_resultado[0][38]))
               main.descricao_atividade_2.setText(str(edit_resultado[0][39]))
               main.nome_comerciante_2.setText(str(edit_resultado[0][40]))
               main.cpf_comerciante_2.setText(str(edit_resultado[0][41]))
               main.posicao_edi_2.setText(str(edit_resultado[0][47]))
               main.pavimento_edi_2.setText(str(edit_resultado[0][48]))
               main.pav_em_construcao_edi_2.setItemText(0, str(edit_resultado[0][49]))
               print(edit_resultado[0][47], edit_resultado[0][48], edit_resultado[0][49])

        else:
            pass
    except Exception as e:
        cursor.execute("ROLLBACK")
        connect.commit()
        print('ChecarMonitoria ',e)

    #main.comboBox.setCurrentText()
    return valor_edit

if __name__ == "__main__":

    app = QtWidgets.QApplication([])


    main = uic.loadUi("vw/home.ui")
    pesquisar = uic.loadUi("vw/vw_pesquisar.ui")
    result = uic.loadUi("vw/vw_resultado.ui")
    editar = uic.loadUi("vw/editar.ui")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("imagem/map_icon.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
    main.setWindowIcon(icon)
    main.setWindowTitle('Monitoria')
    main.bt_pesquisar.clicked.connect(Buscar_matricula)
    load = QtWidgets.QLabel(main)
    load.move(650, 50)
    load.resize(32, 32)
    load.setObjectName('loading')
    move = QMovie('imagem/Loading_Key.gif')
    timer = QTimer(None)
    load.setMovie(move)

    main.btn_enviar.clicked.connect(Enviar)
    main.btn_limpar.clicked.connect(Limpar_campos)
    main.bt_pesquisar_resultado.clicked.connect(chama_tela)
    pesquisar.btn_pesquisar_cadastrador.clicked.connect(resultado)
    #pesqu1isar.btn_monitoria.clicked.connect(chamaTelaM)
    pesquisar.btn_voltar.clicked.connect(voltarMain)
    main.btn_editar.clicked.connect(pegarDadosEditados)


    main.showMaximized()
    app.exec()
