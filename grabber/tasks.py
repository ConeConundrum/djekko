from tika import parser
import re


class FinancialReportGrabber(object):

    # Regex key values profile
    # TODO Make separate profile file
    raw_data_regex_keywords = {
        'currency': {
            'keywords': {
                r'долларов': 'dollar',
                r'рублей': 'rouble',
                r'руб': 'rouble',
            },
            'reg_exp': [
                r'{}'
            ]
        },
        'measure': {
            'keywords': {
                r'в миллионах': 1000000,
                r'в миллиардах': 1000000000,
                r'в тысячах': 1000,
            },
            'reg_exp': [
                r'{}',
                r'\wденица измерения.*{}.*'
            ]

        },
        'cash': {
            'keywords': {},
            'reg_exp': []
        },
        'equity': {
            'keywords': {},
            'reg_exp': []
        },
        'liabilities': {
            'keywords': {},
            'reg_exp': []
        },
        'equity_liabilities': {
            'keywords': {},
            'reg_exp': []
        },
        'sales': {
            'keywords': {},
            'reg_exp': []

        },
        'interest_income': {
            'keywords': {},
            'reg_exp': []

        },
        'interest_expense': {
            'keywords': {},
            'reg_exp': []
        },
        'profit_before_tax': {
            'keywords': {},
            'reg_exp': []
        },
        'clean_profit': {
            'keywords': {},
            'reg_exp': []
        },
        'amortization': {
            'keywords': {},
            'reg_exp': []
        },
        'capitalization': {
            'keywords': {},
            'reg_exp': []
        },
    }

    # multipliers counted from key values
    multipliers = {
        'p/e': None,  # Капитализация к чистой прибыли
        'p/s': None,  # Капитализация к выручке
        'p/bv': None,  # Рыночная цена акции к стоимости активов на акцию
        'ebitda': None,  # Справедливая стоимость компании
        'ev/ebitda': None,  # Прибыль до налогов, процентов, амортизации
        'debt/ebitda': None,  # Рыночная оценка единицы прибыли
        'roe': None  # Рентабельность
    }

    def __init__(self, document):
        super().__init__()
        self.data = parser.from_file(document)
        self.metadata = self.data["metadata"]
        self.content = self.data["content"]
        self.data = dict()

    def _scan_one_value(self, value_dict):

        keywords = value_dict["keywords"]
        reg_exp = value_dict["reg_exp"]
        egg_set = set()
        final_set = set()

        if keywords or reg_exp:
            for keyword in keywords:
                for reg_expression in reg_exp:
                    data = re.findall(reg_expression.format(keyword), self.content)
                    if data:
                        egg_set.update(set(data))
        if egg_set:
            for egg_key in egg_set:
                final_set.add(keywords[egg_key])

        if not final_set or len(final_set) > 1:
            return None
        return final_set.pop()

    def _scanner(self, profile):

        for key in profile.keys():
            value = self._scan_one_value(profile[key])
            self.data[key] = value

    def scan(self):
        self._scanner(self.raw_data_regex_keywords)
        print(self.data)


x = FinancialReportGrabber('tes_dat/gazprom-ifrs-3q2018-ru.pdf')
x.scan()
