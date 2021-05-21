import os
import pandas as pd
import numpy as np
import enchant
import cProfile


default_path = './emails/'


def retrieve_content_for(tag):
  for dirpath,dirnames,filenames in os.walk(default_path + tag) :
      print()
  content = {'id':[], 'content':[]}
  for filename in filenames:
      lines = []
      path = os.path.join(default_path, tag, filename)
      f = open(path, "r", encoding='latin1')
      data_start = False
      for x in f:
          if data_start :
              lines.append(x)
          elif x == '\n':
              data_start = True
      content['content'].append("\n".join(lines))
      content['id'].append(filename)
  return content


def concatanate_data():
  spam_data = retrieve_content_for('spam')
  ham_data = retrieve_content_for('ham')
  spam_data['type'] = []
  for values in spam_data['id'] :
    spam_data['type'].append('spam')
  for key in ham_data:
    spam_data[key] = list([*spam_data[key],*ham_data[key]])
  for values in ham_data['id']:
    spam_data['type'].append('ham')
  return spam_data


def convert_to_data_frame():
  return pd.DataFrame(concatanate_data())

data = convert_to_data_frame()
data.head()


def check_alphabet(z):
  asc = ord(z)
  if ((asc >= 65 and asc <=90) or (asc >=97 and asc <= 122)) :
    return True
  else:
    return False


def clean_content(content):
    content = content.lower()
    for x in content:
        if (not check_alphabet(x)) :
            content = content.replace(x, " ")
    content = content.strip()
    return content


def convert_to_set_of_tokens(content):
    content = clean_content(content)
    return set(content.split(" "))


def convert_to_list_of_tokens(content):
    content = clean_content(content)
    return list(content.split(" "))


def create_a_bag_of_words():
  bag = set({})
  spell = enchant.Dict('en_US')
  for content in data['content']:
    bag = bag.union(convert_to_set_of_tokens(content))
  new_bag = []
  ignore_words = [' ','is','are','am','i','or','and','the','a','an','has','have','do','does']
  for x in bag:
      if x not in ignore_words and len(x) > 0:
          if spell.check(x):
              new_bag.append(x)
  return new_bag

bag = create_a_bag_of_words()


def create_default_vector():
  zero_vector = []
  for x in range(0,len(bag)):
    zero_vector.append(0)
  return np.array(zero_vector)

def count_frequency(content, keyword):
    c = 0
    for x in content:
        if x == keyword:
            c = c + 1 
    return c


def convert_to_count_vector(content):
  zero_vector = create_default_vector()
  i = 0
  for word in bag:
    if(word in convert_to_list_of_tokens(content)):
      zero_vector[i] = count_frequency(convert_to_list_of_tokens(content), word)
    i = i + 1
  return zero_vector

def convert_all_data():
  i = 0
  temp_content = []
  for content in data['content']:
      temp_content.append(convert_to_count_vector(content))
      i = i + 1
  data['content'] = temp_content
  
convert_all_data()

data.head()