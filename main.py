import os

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from pandash import query_to_df
from pandaspread import write_to_spreadsheet
from redash_dynamic_query import RedashDynamicQuery

if __name__ == '__main__':
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=os.environ.get('CLIENT_SECRET_FILE'),
                                                                   scopes='https://www.googleapis.com/auth/spreadsheets')
    service = discovery.build(serviceName='sheets',
                              version='v4',
                              http=credentials.authorize(httplib2.Http()),
                              discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    redash = RedashDynamicQuery(endpoint='http://demo.redash.io',
                                apikey=os.environ.get('REDASH_API_KEY'),
                                data_source_id=1,
                                max_wait=60)

    df = query_to_df(redash, 1)
    write_to_spreadsheet(service=service,
                         spreadsheet_id="スプレッドシートID",
                         spreadsheet_range="シート1!A1",
                         df=df)
