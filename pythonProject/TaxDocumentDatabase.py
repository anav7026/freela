from TaxDocument import TaxDocument
import json
class TaxDocumentDatabase:
    def __init__(self, json_file='TaxDocumentInfo.json', global_doc_dictionary=None):
        self.tax_doc_lst=[]
        self.json_file=json_file
        self.global_doc_dictionary=global_doc_dictionary if global_doc_dictionary else {}
        self.load_doc_from_json()
    
    def load_doc_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                doc_data = json.load(file)
                
                for doc in doc_data:
                    doc_name = doc["Tax Document Name"]
                    if doc_name not in self.global_doc_dictionary:
                        new_doc = TaxDocument(doc["Tax Document Name"], doc["Due Date"], doc["Description"], doc["PDF Link"])
                        self.global_doc_dictionary[doc_name] = new_doc
                        self.tax_doc_lst.append(new_doc)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")

    def find_doc(self, doc_name):
        for doc in self.tax_doc_lst:
            if doc.form_name==doc_name:
                return doc
        return None
    





