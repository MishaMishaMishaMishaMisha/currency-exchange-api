import requests

url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

def get_current_currency() -> list[dict]:
    
    response = requests.get(url)
    return response.json()


print(get_current_currency())

# table currency
# id currency_name currency_code rate_to_uah exchangedate
