import model
import Data_operations
import csv
class system :
    def __init__(self):
        m = model.model()
        data = Data_operations.Data_operations()
    def predict_doc(self,text,modelname='',mode=0):#add default model name
        embedded_vector ,_,_ = self.m.embedd_doc(text,mode)
        softmax_prediction = self.m.predict(embedded_vector,modelname)
        return softmax_prediction
    def add_sample(self,text,lable,filename="new_EmotionalTone_dataset.csv"):#make sure to add an empty one
        row = [text,lable]
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)