import pandas as pd
import logging
from .models import RecsContextsExplsA3, Randomization
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

    excel_data = pd.read_excel(file, sheet_name=None, engine='openpyxl')
    sheet_1 = excel_data.get('Sheet1')

    if sheet_1 is not None:
        total_rows = len(sheet_1)
        recommendation_objects = []
        
        for _, row in tqdm(sheet_1.iterrows(), total=total_rows, desc="Nalaganje podatkov", unit="vrstic"):
            recommendation_objects.append(RecsContextsExplsA3(
                elder_id=row['uID'],
                activity_ids=filter_text(row['actID_lst']),
                activity_texts=filter_text(row['actTxt_lst']),
                context_time=filter_text(row['C_T']),
                context_place=filter_text(row['C_P']),
                explanation=filter_text(row['Expl'])
            ))
            
        if recommendation_objects:
            RecsContextsExplsA3.objects.bulk_create(recommendation_objects)

    return "Data imported successfully!"


def excel_to_db_randomization(file):

    excel_data = pd.read_excel(file, sheet_name=None, engine='openpyxl')
    sheet_1 = excel_data.get('Sheet1')

    if sheet_1 is not None:
        total_rows = len(sheet_1)
        randomization_objects = []

        for _, row in tqdm(sheet_1.iterrows(), total=total_rows, desc="Nalaganje podatkov", unit="vrstic"):
            randomization_objects.append(Randomization(
                rnd1=row['anID1_rnd_uID'],
                rnd2=row['anID2_rnd_uID'],
                rnd3=row['anID3_rnd_uID'],
                rnd4=row['anID4_rnd_uID'],
                rnd5=row['anID5_rnd_uID'],
                rnd6=row['anID6_rnd_uID'],
                rnd7=row['anID7_rnd_uID'],
                rnd8=row['anID8_rnd_uID'],
                rnd9=row['anID9_rnd_uID'],
                rnd10=row['anID10_rnd_uID'],
                rnd11=row['anID11_rnd_uID'],
                rnd12=row['anID12_rnd_uID'],
                rnd13=row['anID13_rnd_uID'],
                rnd14=row['anID14_rnd_uID'],
                rnd15=row['anID15_rnd_uID'],
                rnd16=row['anID16_rnd_uID'],
                rnd17=row['anID17_rnd_uID'],
                rnd18=row['anID18_rnd_uID'],
                rnd19=row['anID19_rnd_uID'],
                rnd20=row['anID20_rnd_uID']
            ))

        if randomization_objects:
            Randomization.objects.bulk_create(randomization_objects)

    return "Data imported successfully!"

def read_excel(excel_path: str, column_name: str):
    df = pd.read_excel(excel_path, engine='openpyxl')
    return df[column_name].tolist()
