import pygsheets


class GoogleSheet:
    def __init__(self, key_json, sheet_url):
        client = pygsheets.authorize(service_file=key_json)
        self.sheets = client.open_by_url(sheet_url)
        self.worksheet = None

    def set_worksheet(self, sheet_name):
        self.worksheet = self.sheets.worksheet_by_title(sheet_name)

    def get_values(self, start, end):
        return self.worksheet.get_values(start, end)