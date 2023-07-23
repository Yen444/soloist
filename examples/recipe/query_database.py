import json
import os 
import sys
from pysondb import db
import numpy as np
import sqlite3
import random

def lower_case(json_list):
   new_list = []
   for dict_item in json_list:
      new_dict = dict((str(k).lower(), str(v).lower()) for k,v in dict_item.items())
      new_list.append(new_dict)
   return new_list

def create_database():

   with open("recipe_db.json", "r") as json_file:
      data_json = json.load(json_file)

   os.remove('recipes.db')
   conn = sqlite3.connect('recipes.db')
   cursor = conn.cursor()
   cursor.execute('''CREATE TABLE Recipes 
               (id INT PRIMARY KEY NOT NULL, 
               name TEXT,
               type TEXT,
               ingredients TEXT,
               instructions TEXT,
               substitution TEXT,
               equipment TEXT,
               time TEXT, 
               is_quick TEXT,
               difficulty TEXT,
               is_vegan TEXT);''')

   conn.commit()



   for data_idx in range(len(data_json)):
      entry = data_json[data_idx]

      #time_entry = entry['time'].split(" ")
      #time_entry = time_entry[0].split("-")
      #time_entry = int(np.round(float(time_entry[0]))) # just ignore stuff like 1.5 to 2.0 hours
      cursor.execute(f'''INSERT INTO Recipes (id, name, type, ingredients, instructions, 
               substitution, equipment, time, is_quick, difficulty, is_vegan) \n
               VALUES ({data_idx}, \"{entry['name']}\", \"{entry['type']}\", \"{entry['ingredients']}\",
               \"{entry['instructions']}\", \"{entry['substitution']}\", \"{entry['equipment']}\",
               \"{entry['time']}\",\"{entry['is_quick']}\", \"{entry['difficulty']}\", \"{entry['is_vegan']}\");''')

   conn.commit()
   conn.close()

def query_database(del_response : str, db_state=None):
   """
   argurment: 
      del_response: dexicalized output from the model including both belief state and delexicalized response. Each belief state is seperate by semicolon ';' and the response starts with string 'system'
      db_state: keep track of recommended recipes
   return:
      lexicalized response to be shown in the bot
      db_state
   """
   # initialize db_state
   if db_state is None:
      db_state = {}
   # parse belief state
   bs_idx = del_response.find('belief')
   res_idx = del_response.find('system')

   bs_str = del_response[bs_idx + len(str('belief')) +3: res_idx]
   bs_list = bs_str.split(';')

   res = del_response[res_idx+len(str('system')) +3:]
   print(f'belief states {bs_list}')
   #print(f'respond {res}')

   # encode query from belief state
   query = "SELECT name FROM Recipes WHERE"
   for bs in bs_list:
      bs = bs.split('=')
      slot = bs[0].strip()
      val = bs[1].strip()
      print(f'slot: {slot}')
      print(f'val: {val}')
      if val == 'recommended_recipe_name_1':
         name = db_state['recommended_recipe_name_1']
         query = f'SELECT name FROM Recipes WHERE name = {name}'
         break
      elif val == 'recommended_recipe_name_2':
         name = db_state['recommended_recipe_name_2']
         query = f'SELECT name FROM Recipes WHERE name = {name}'
         break
      else: 
         if val == 'dont care' or val == 'not mentioned' or val == "don't care":
            query = query
         elif 'negative' in val:
            val_neg = val.split(' ')
            val_neg = "'" + f'%{val_neg[-1]}%' + "'"
            if query.endswith('WHERE'):
               query += f' {slot} NOT LIKE {val_neg}'
            else:
               query += f' AND {slot} NOT LIKE {val_neg}'
         else:
            val_pos = "'" f'%{val}%' + "'"
            if query.endswith('WHERE'):
               query += f' {slot} LIKE {val_pos}'
            else:
               query += f' AND {slot} LIKE {val_pos}'
   
   # get matches from db
   if query.endswith('WHERE'):
      query = query.replace('WHERE', '')
   print(query)
   conn = sqlite3.connect('recipes.db')
   cursor = conn.cursor()
   cursor.execute(query)
   matches = cursor.fetchall() 
   print(matches)
   # lexicalize response
   """if len(matches) == 0:
      res = 'Sorry. I do not have any recipe that meet your requests at the moment. What else can I help you?'
   else:
      match_idx = random.randint(0, len(matches)-1)
      match = matches[match_idx]
      if '[recipe_name_1]' in res:
         name = match[1]
         res = res.replace('[recipe_name_1]', name)
         db_state['recommended_recipe_name_1'] = name 
      if '[recipe_name_2]' in res:
         name = matches[1][1]
         res = res.replace('[recipe_name_2]', name)
         db_state['recommended_recipe_name_2'] = name
      if '[recipe_name_3]' in res:
         name = matches[2][1]
         res = res.replace('[recipe_name_3]', name)
         db_state['recommended_recipe_name_3'] = name
      if '[recipe_type]' in res:
         type = match[2]
         res = res.replace('[recipe_type]', type)
      if '[recipe_ingredients]' in res:
         ingredients = match[3]
         res = res.replace('[recipe_ingredients]', ingredients)
      if '[recipe_instructions]' in res:
         instructions = match[4]
         res = res.replace('[recipe_instructions]', instructions)
      if '[recipe_substituion]' in res:
         substitution = match[5]
         res = res.replace('[recipe_substituion]', substitution)
      if '[recipe_equipment]' in res:
         equipment = match[6]
         res = res.replace('[recipe_equipment]', equipment)
      if '[recipe_time]' in res:
         time = match[7]
         res = res.replace('[recipe_time]', time)
      if '[recipe_is_quick]' in res:
         is_quick = match[8]
         res = res.replace('[recipe_is_quick]', is_quick)
      if '[recipe_difficulty]' in res:
         difficulty = match[9]
         res.replace('[recipe_difficulty]', difficulty)
      if '[recipe_is_vegan]' in res:
         is_vegan = match[10]
         res = res.replace('[recipe_is_vegan]', is_vegan)
      #confirm ingredient
      if '[recipe_ingredient_value]' in res:
         ingredient_bs = [bs for bs in bs_list if 'ingredient' in bs]
         ingredient_bs = ingredient_bs[0].split('=')
         ingredient_value = ingredient_bs[1].split(' ')
         ingredient_value = f'out {ingredient_value[-1]}' if 'negative' in ingredient_value else f'{ingredient_value[-1]}' # when confirm the ingredients that user wants or doesn't want
         res = res.replace('[recipe_ingredient_value]', ingredient_value)

   return res, db_state"""

if __name__ == "__main__":
   query_database("belief : type = main dish ; ingredients = chicken ; is_quick = yes  system: Certainly! Here are the ingredients and instructions for preparing the [recipe_name_1]: [recipe_ingredients], [recipe_instructions].")