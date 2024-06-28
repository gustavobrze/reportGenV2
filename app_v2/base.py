import pandas as pd
from datetime import datetime
from calendar import monthrange
from workalendar.america.brazil import BrazilBankCalendar

def format_base(sheet):
    
    base = pd.read_excel(sheet, sheet_name='Clientes', skiprows=6, index_col=1)
    base_2 = base.drop(columns=[col for col in base.columns if col.startswith('Unnamed')])

    return base_2

def client_list(sheet):

    base = format_base(sheet)

    base_2 = base[base['RECEBIMENTO']=='No fim do contrato']

    clients = base_2['NOME CLIENTE'].unique()

    return clients

def generateReport(sheet, client):

    base = format_base(sheet)
    eachClient = base[(base['NOME CLIENTE']==client) & ((base['STATUS']=='ATIVO ') | (base['STATUS']=='ATIVO')) & ((base['RECEBIMENTO']=='No fim do contrato') | (base['RECEBIMENTO']=='No fim do contrato '))]

    current_month = datetime.today().month
    current_year = datetime.today().year

    rent_cliente = pd.DataFrame(columns=['Data aporte', 'Vencimento', 'Valor aportado', 'Valor atual'])

    calendar = BrazilBankCalendar()

    rows = list()

    for key, value in eachClient.iterrows():

        name = value['NOME CLIENTE']
        cpf = value['CPF ']
        init_value = value['VALOR DEPOSITADO ']
        init_date = value['DI APLICAÇÃO']
        final_date = value['DF APLICAÇÃO']
        i = value['RENTABILIDADE CONTRATADA']
        i_str = i

        if "," in i:
            i = i.replace(',','.')
        
        rate = float(i.split('%')[0])/100 #decimal
        acc_value = init_value

        #checar se está em datetime
        if type(init_date) == datetime:
            pass

        else:
            init_date = datetime.strptime(init_date,'%d/%m/%Y')

        if type(final_date) == datetime:
            pass

        else:
            final_date = datetime.strptime(final_date,'%d/%m/%Y')
        
        d1 = calendar.add_working_days(init_date, 1)

        if final_date > init_date:

            init_day = d1.day
            init_month = d1.month
            init_year = d1.year

            num_days = monthrange(init_year, init_month)

            #Cálculo da rentabilidade do primeiro mês
            num_days_first_month = num_days[1] - init_day
            interest_first_month = (init_value * rate)/30 * num_days_first_month
            acc_value += interest_first_month

            #Cálculo da rentabilidade dos demais meses
            year_diff = current_year - init_year
            num_months = current_month - init_month + (12 * year_diff) - 1 #Meses fechados
        
            for n in range(0,num_months):

                interest_other_months = acc_value * rate
                acc_value += interest_other_months
            
            new_row = [datetime.strftime(init_date, '%d/%m/%Y'), datetime.strftime(final_date, '%d/%m/%Y'), init_value, acc_value, i_str]
            #rent_cliente = rent_cliente.append(new_row, ignore_index=True)
            rows.append(new_row)

        else:
            pass
    
    rent_cliente = pd.DataFrame(columns=['Data aporte', 'Vencimento', 'Valor aportado', 'Valor atual', 'Rentabilidade'], data=rows)

    total_init = 0
    total_acc = 0

    for v1, v2 in zip(rent_cliente['Valor atual'], rent_cliente['Valor aportado']):
        total_acc += v1
        total_init += v2
    '''
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    rent_cliente['Valor aportado'] = [locale.currency(x, grouping=True) for x in rent_cliente['Valor aportado']]
    rent_cliente['Valor atual'] = [locale.currency(x, grouping=True) for x in rent_cliente['Valor atual']]

    total_init = locale.currency(total_init, grouping=True)
    total_acc = locale.currency(total_acc, grouping=True)'''

    return [name, cpf, i, rent_cliente, total_init, total_acc]
