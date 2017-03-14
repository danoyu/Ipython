'''
Created on Feb 8, 2017

@author: Dan 
'''
# -*- coding: utf-8 -*-

#===============================================================================
# SCRIPTS FOR CREATE NEW CLASSIFIERS FROM THE WATSON NLC SERVICE AND MANIPULATE IT
# THE INPUT FOR CREATE A CLASSIFIER MUST BE A .CSV FILE 
#===============================================================================



import json
import time
from watson_developer_cloud import NaturalLanguageClassifierV1
import os
from datashape.coretypes import null
import codecs


#classifier_id='cedf17x168-nlc-3397' 
#classifier_smallexp_id = 'cedec3x167-nlc-4394'

nlc_usr="e457cd66-3148-4a8b-877a-3dfaba378639" #user of NLC
nlc_psw="iQ73gqox40ee"  #password of NLC


#nlc_usr = '96e6ee96-1661-4aae-9956-c07db9eef464'
#nlc_psw = 'v2nb6hPx87JH'

#file = "training_set.csv"
#nameDir = '../training_csv_files/'

natural_language_classifier = NaturalLanguageClassifierV1(
  username=nlc_usr,
  password=nlc_psw)



# Create a new classifier train with the training_file
# The training data must have at least five records (rows) and no more than 15,000 records
def create_classifier(training_file, name, nb = None):
    print ('Name of the new classifier : ' , name)
    print('Training with',nb , 'percent with the file', training_file)
    print(list_classifiers_name_id())
    print(len(list_classifiers_name_id()))
    #with open(training_file, 'rb') as f:
    with codecs.open(training_file, 'rb',encoding='utf-8', errors='ignore') as training_data:
            t = time.clock()
            classifier = natural_language_classifier.create(
                    training_data=training_data,
                    name=name,
                    language='en')
            t = time.clock() - t
    print('creating time : ' + str(t))
    status = get_status(name)
    t = time.clock()
    while status != 'Available':
        status = get_status(name)
    t = time.clock() - t
    print('traning time : ' + str(t))
    return classifier

# create_classifier('../training_csv_files/training_50.csv','class1')


# return a list of ids of the classifiers available
def list_classifiers_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = list()
    x = json.dumps(classifiers, indent=2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers.append(classi[i]['classifier_id'])
    return list_classifiers

# print(list_classifiers_id())

# return a of dictionary with ids and names of the classifiers available
def list_classifiers_name_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = dict()
    x = json.dumps(classifiers, indent=2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers[classi[i]['name']] = classi[i]['classifier_id']
    return list_classifiers

# print(list_classifiers_name_id())


# delete all the classifiers available by the name
def delete_all_classifiers():
    ids = list_classifiers_name_id()
    for id in ids:
        natural_language_classifier.remove(ids[id])
    
# delete_by_name_classifiers()

# print(list_classifiers_name_id())

# delete a classifiers by his name
def delete_classifier_by_name(name):
    names = list_classifiers_name_id()
    natural_language_classifier.remove(names[name])

# delete a classifiers by his id
def delete_classifier_by_id(id):
    natural_language_classifier.remove(id)
    
# delete_by_id_classifiers('')

#get the id of a classifier by his name
def get_id_classifier(name):
    ids = list_classifiers_name_id()
    return ids[name]

#get the status of a classifier by his name
def get_status(name):
    id = get_id_classifier(name)
    return natural_language_classifier.status(id)['status']
        
# class a sentence with the classifier who named classifier_name
def classify(classifier_name, sentence):
    classifiers = list_classifiers_name_id()
    
    # API CALL 
    natural_language_classifier = NaturalLanguageClassifierV1(
    username=nlc_usr, password=nlc_psw)
    t = time.clock()
    classes = natural_language_classifier.classify(classifiers[classifier_name], sentence)
    t = time.clock() - t
    print('API call time : ' , str(t))
    myjson = json.dumps(classes)
                 
    # Parsing 
    jsonparser = json.loads(myjson);  # parse the ans of the api
    answer_class = jsonparser["classes"][0]["class_name"]  # classified class with more confidence 
                
    return answer_class



