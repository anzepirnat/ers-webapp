import pandas as pd
import logging
from .models import RecsContextsExplsA3
from tqdm import tqdm

class log:
    _logger = None

    @classmethod
    def _get_logger(cls):
        if cls._logger is None:
            import logging
            cls._logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.DEBUG)
        return cls._logger

    @classmethod
    def debug(cls, message):
        cls._get_logger().debug(message)

    @classmethod
    def error(cls, message):
        cls._get_logger().error(message)

    @classmethod
    def info(cls, message):
        cls._get_logger().info(message) 
        

def remove_parantheses(text):
    return text.replace('(', '').replace(')', '')

def remove_quotes(text):
    return text.replace("'", "")

def remove_last_comma(text):
    if text[-1] == ",": 
        return text.replace(',', '')
    else:
        return text

def replace_slo_words(text):
    return text.replace('č', 'c').replace('ć', 'c').replace('š', 's').replace('đ', 'd').replace('ž', 'z')

def filter_text(text):
    return remove_last_comma(remove_parantheses(remove_quotes(replace_slo_words(text))))

def to_list(text):
    return text.split(", ")
    

def excel_to_db(file):
    # Read the Excel file with pandas (using openpyxl for .xlsx format)
    excel_data = pd.read_excel(file, sheet_name=None, engine='openpyxl')

    # Extract the specific sheets
    sheet_1 = excel_data.get('Sheet1')

    if sheet_1 is not None:
        total_rows = len(sheet_1)
        for _, row in tqdm(sheet_1.iterrows(), total=total_rows, desc="Nalaganje podatkov", unit="vrstic"):
            #log.debug(f"activity_texts: {to_list(filter_text(row['actTxt_lst']))}, type(activity_texts): {type(to_list(filter_text(row['actTxt_lst'])))}")
            RecsContextsExplsA3.objects.create(
                elder_id=row['uID'],
                activity_ids=filter_text(row['actID_lst']),
                activity_texts=filter_text(row['actTxt_lst']),
                context_time=filter_text(row['C_T']),
                context_place=filter_text(row['C_P']),
                explanation=filter_text(row['Expl'])
            )

    return "Data imported successfully!"
