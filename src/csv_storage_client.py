from csv_store_model import CSVStoreModel

class CSVStorageClient(object):
    def add_csv(self, business_name, file_path, file_summary):
        try:
            new_csv_file = CSVStoreModel(business_name=business_name, file_path=file_path, file_summary=file_summary)
            new_csv_file.save()
        except Exception as e:
            return("Error \n %s" % (e))

        return {'Success': 'CSV File was successfully uploaded with name ' + file_path}
        
