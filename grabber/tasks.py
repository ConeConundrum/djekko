from tika import parser


class FinancialReportGrabber(object):

    raw_data_regex_keywords = {
        'currency': [r'долларов', r'рублей', r'руб'],  # Валюта расчета
        'measure': [r'млн.', r'тыс.', r'млрд'],  # Единицы (тыс, млн, млрд)
        'cash': [],  # Денежные средства и эквиваленты
        'equity': [],  # Капитал
        'liabilities': [],  # Обязательства
        'equity_liabilities': [],  # Активы
        'sales': [],  # Выручка
        'interest_income': [],  # Уплаченные налоговые сборы
        'interest_expense': [],  # Проценты с инвестиций компании
        'profit_before_tax': [],  # Прибыль до налогооблажения
        'clean_profit': [],  # Чистая прибыль (после налогооблажения)
        'amortization': [],  # Амортизация
        'capitalization': []  # Капитализация
    }

    raw_data_columns = {
        'currency': None,  # Валюта расчета
        'measure': None,  # Единицы (тыс, млн, млрд)
        'cash': None,  # Денежные средства и эквиваленты
        'equity': None,  # Капитал
        'liabilities':None, # Обязательства
        'equity_liabilities': None,  # Активы
        'sales': None,  # Выручка
        'interest_income': None,  # Уплаченные налоговые сборы
        'interest_expense': None,  # Проценты с инвестиций компании
        'profit_before_tax': None,  # Прибыль до налогооблажения
        'clean_profit': None,  # Чистая прибыль (после налогооблажения)
        'amortization': None,  # Амортизация
        'capitalization': None # Капитализация
    }

    multipliers = {
        'p/e': None,  # Капитализация к чистой прибыли
        'p/s': None,  # Капитализация к выручке
        'p/bv': None,  # Рыночная цена акции к стоимости активов на акцию
        'ebitda': None,  # Справедливая стоимость компании
        'ev/ebitda': None,  # Прибыль до налогов, процентов, амортизации
        'debt/ebitda': None,  # Рыночная оценка единицы прибыли
        'roe': None # Рентабельность
    }


    def __init__(self, document):
        data = parser.from_file(document)
        self.metadata = data["metadata"]
        self.content = data["content"]
