from random import randrange
from datetime import datetime, date,timedelta

def gerarIdMaster():

    """
    Gerar id master aleatorio

        3 - aleatorios 
        2 - mes
        3 - aleatorios
        2 - dia
        3 - aleatorios
        2 - ano

    """

    idmaster = str(randrange(100, 999))
    idmaster += str(date.today().month).zfill(2)
    idmaster += str(randrange(100, 999))
    idmaster += str(date.today().day).zfill(2)
    idmaster += str(randrange(100, 999))
    idmaster += str(date.today().year)[2:4]

    return idmaster


def gerarIdParcelamento():

    """
    Gerar id parcelamento aleatorio

        3 - aleatorios 
        2 - mes
        3 - aleatorios
        2 - dia
        3 - aleatorios
        2 - ano

    """

    id_parcelamento = str(randrange(100, 999))
    id_parcelamento += str(date.today().month).zfill(2)
    id_parcelamento += str(randrange(100, 999))
    id_parcelamento += str(date.today().day).zfill(2)
    id_parcelamento += str(randrange(100, 999))
    id_parcelamento += str(date.today().year)[2:4]

    return id_parcelamento


def gerarIdRecorrencia():

    """
    Gerar id recorrencia aleatorio

        3 - aleatorios 
        2 - mes
        3 - aleatorios
        2 - dia
        3 - aleatorios
        2 - ano

    """

    id_recorrencia = str(randrange(100, 999))
    id_recorrencia += str(date.today().month).zfill(2)
    id_recorrencia += str(randrange(100, 999))
    id_recorrencia += str(date.today().day).zfill(2)
    id_recorrencia += str(randrange(100, 999))
    id_recorrencia += str(date.today().year)[2:4]

    return id_recorrencia


def dataAtual():
    return datetime.today().strftime("%Y-%m-%d")


def dataHoraAtual():
    return datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def dataAtualFormatada():
    return datetime.today().strftime("%d/%m/%Y")


def dataHoraAtualFormatada():
    return datetime.today().strftime("%d/%m/%Y %H:%M:%S") 


def data_range_dia():
    """
        Funcao para retornar range de datas do dia atual para querys
    """
    data_atual = datetime.now().date()

    data_inicio = data_atual
    data_fim = data_atual
    
    return [data_inicio, data_fim]


def data_range_dia_parametro(data_atual):

    """
        Funcao para retornar range de datas (dt_ini - dt_fim) do dia para querys partindo de uma data 

            Args:
                data_atual (YYYY-mm-dd): Data padrao sistema

            Exemplo de uso:
                 dataRange = data_range_dia_parametro(data_atual)
                
            Returns:
                Range de data_atual - dt_atual : [2024-01-01, 2024-01-01] 
        """
        
    data_atual_obj = datetime.strptime(data_atual, '%Y-%m-%d')

    return [ data_atual_obj.strftime("%Y-%m-%d"), data_atual_obj.strftime("%Y-%m-%d") ]

def data_range_semana():
    """
        Funcao para retornar range de datas da semana atual para querys
    """
    data_atual = datetime.now().date()

    # Dia da semana (segunda-feira = 0, domingo = 6)
    dia_semana = data_atual.weekday()

    # Calcular o início e o fim da semana
    inicio_semana = data_atual - timedelta(days=dia_semana)
    fim_semana = inicio_semana + timedelta(days=6)

    return [inicio_semana, fim_semana]


def data_range_mes():
    """
        Funcao para retornar range de datas do mes atual para querys
    """
    data_atual = datetime.now().date()

    # Calcular o início e o fim do mês
    inicio_mes = data_atual.replace(day=1)
    ultimo_dia_mes = inicio_mes.replace(month=inicio_mes.month % 12 + 1, day=1) - timedelta(days=1)

    return [inicio_mes, ultimo_dia_mes]


def data_range_mes_parametro(data_atual):

    """
        Funcao para retornar range de datas (primeiro e ultimo diado mes atual) para querys partindo de uma data 

            Args:
                data_atual (YYYY-mm-dd): Data padrao sistema

            Exemplo de uso:
                 dataRange = data_range_mes_parametro(dt_mes_corrente)
                
            Returns:
                Range de datas do mes de data_atual ex: [2024-01-01, 2024-01-31] 
        """
        
    data_atual_obj = datetime.strptime(data_atual, '%Y-%m-%d')

    # Calcular o início e o fim do mês
    inicio_mes = data_atual_obj.replace(day=1)
    ultimo_dia_mes = inicio_mes.replace(month=(inicio_mes.month % 12) + 1, day=1) - timedelta(days=1)

    inicio_mes_formatado = inicio_mes.strftime("%Y-%m-%d")
    ultimo_dia_mes_formatado = ultimo_dia_mes.strftime("%Y-%m-%d")

    # ***   Corrigindo um bug na virada do ano que sempre trazia um range a menos 
    # ***   Ex:  01-12-2023 - 01-12-2022
    ultimo_dia_mes_bug_biblioteca_corrigido = inicio_mes_formatado[0:4] + "-" + ultimo_dia_mes_formatado[5:7] + "-" + ultimo_dia_mes_formatado[8:10]
    
    return [ inicio_mes.strftime("%Y-%m-%d"), ultimo_dia_mes_bug_biblioteca_corrigido]


def data_range_semana_parametro(data_atual):

    """
        Funcao para retornar range de datas (data_atual -7 ) para querys partindo de uma data 

            Args:
                data_atual (YYYY-mm-dd): Data padrao sistema

            Exemplo de uso:
                 dataRange = data_range_semana_parametro(data_atual)
                
            Returns:
                Range de data_atual - 7 : [2024-01-01, 2024-01-07] 
        """
        
    data_atual_obj = datetime.strptime(data_atual, '%Y-%m-%d')
    data_7_dias_atras = data_atual_obj - timedelta(days=7)

    return [ data_7_dias_atras.strftime("%Y-%m-%d"), data_atual_obj.strftime("%Y-%m-%d") ]


def data_range_ano():

    """
        Funcao para retornar range de datas (01/01/ano - 31/12/ano) para querys

            Args:
                ano (YYYY): Data padrao sistema

            Exemplo de uso:
                 dataRange = data_range_ano_parametro(ano)
                
            Returns:
                Range de ano : [ano-01-01, ano-12-31] 
        """
    data_atual = dataHoraAtual()
    ano = data_atual[0:4]
    dt_ini = datetime.strptime(ano + "/01/01", "%Y/%m/%d")
    dt_fim = datetime.strptime(ano + "/12/31", "%Y/%m/%d")

    return [ dt_ini.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d") ]


def data_range_ano_parametro(ano):

    """
        Funcao para retornar range de datas (01/01/ano - 31/12/ano) para querys partindo de uma data 

            Args:
                ano (YYYY): Data padrao sistema

            Exemplo de uso:
                 dataRange = data_range_ano_parametro(ano)
                
            Returns:
                Range de ano : [ano-01-01, ano-12-31] 
        """
        
    dt_ini = datetime.strptime(ano + "/01/01", "%Y/%m/%d")
    dt_fim = datetime.strptime(ano + "/12/31", "%Y/%m/%d")

    return [ dt_ini.strftime("%Y-%m-%d"), dt_fim.strftime("%Y-%m-%d") ]


def querydict_to_dict(querydict):
    return {chave: querydict.getlist(chave)[0] if querydict.getlist(chave) else '' for chave in querydict.keys()}