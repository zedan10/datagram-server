from csv_store_model import CSVStoreModel
from datagram_user_mongodb_client import Datagram_User_Client

datagramUserClient = Datagram_User_Client()

class CSVStorageClient(object):
    def add_csv(self, api_token, business_name, file_path, file_summary):
        business_id = self.check_valid_api_token(api_token)
        if 'error' in business_id:
            return business_id
        else:
            try:
                new_csv_file = CSVStoreModel(business_id=business_id, business_name=business_name, file_path=file_path, file_summary=file_summary)
                new_csv_file.save()
            except Exception as e:
                return("Error \n %s" % (e))

            return {'Success': 'CSV File was successfully uploaded with name ' + file_path}

    def check_valid_api_token(self, api_token):
        if datagramUserClient.check_valid_api_token(api_token) == True:
            return datagramUserClient.get_business_id_by_api_token(api_token)
        else:
            return {'error': "Could not authenticate"}  
        
