## Fine-Tune Soloist with Recipe

*Training*
```bash
# under the inner soloist folder
cd soloist
sh scripts/train_recipebot.sh
```
*Decoding*
```bash
# under the inner soloist folder
cd soloist
sh scripts/decode_recipe.sh
```
*Evaluating*
```bash
# under example/recipe folder
python evaluate.py --decoded_file [generated_test.json] --test_file [test_dialogues.json]


# without fine-tuning
`python evaluate.py --decoded_file generate_test_pretrained.json --test_file v3_recipe_test_dialogues.json`
* no belief state prediction
* bleu: 3.8270043718399063e-05

`python evaluate.py --decoded_file generate_test_all_10e.json --test_file v3_recipe_test_dialogues.json`
belief : type = soup ; ingredients = pasta ; is_quick = yes ; is_alcohol = yes ; is_vegan = [recommended_recipe_name_2].
belief : type = soup ; is_quick = yes ; is_vegan = yes ; ingredients = negative chicken ; type = not mentioned
belief : type = breakfast ; is_vegan = [recommended_recipe_name_2]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
belief acc: 0.7199074074074076
bleu: 0.08390782474220881

`python evaluate.py --decoded_file generate_test_noneg_10e.json --test_file v3_recipe_test_dialogues.json`
belief : ingredients = cheeses  difficulty = easy ; type = main dish ; ingredients = pasta 
belief acc: 0.7569444444444444
bleu: 0.002268855876410508

`python evaluate.py --decoded_file generate_test_all_10e_mt.json --test_file v3_recipe_test_dialogues.json`
belief : type = soup  ; type = not mentioned  ; ingredients = not mentioned  ; is_vegan  ; is_quick = yes ; type = not mentioned  ; is_vegan = no  ; type = not mentioned  ; is_quick = yes  ; is_quick = yes  ; is_quick = yes  ; type = not mentioned  ; is_quick = yes  ; is_vegan = no  ; is_quick = yes  ; is_quick = yes  ; is
belief : type = soup  ; ingredients = not mentioned  ; type = salad  ; is_vegan = [recommended_recipe_name_2]  ; is_quick = yes  ; type = not mentioned  ; is_quick = yes  ; is_vegan = no ; type = not mentioned  ; is_quick = yes  ; is_quick = yes  ; is_quick = yes  ; type = not mentioned  ; is_quick = yes  ; type = not mentioned  ; ingredients = not mentioned  ; is_quick 
belief : type = dessert  ; ingredients = not mentioned  ; is_quick = yes  ; type = main dish ; type = dont care  ; is_vegan = yes  ; is_quick = yes  ; type = main dish ; is_vegan = no  ; type = not mentioned  ; ingredients = not mentioned  ; is_quick = yes  ; type = not mentioned  ; type = not mentioned  ; ingredients = not mentioned  ; ingredients = not mentioned  ; is_quick = yes  
belief acc: 0.7500000000000002
bleu: 0.10520654336549765