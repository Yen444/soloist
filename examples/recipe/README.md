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

# Result for model trained with negative values 
* belief acc: 0.5833333333333334
* bleu: 0.04839118727874588

# Result for model trained without negative values
* belief acc: 0.625
* bleu: 0.06708893123943638

# best result
## Training hyperparameters
--num_train_epochs 10 \
--learning_rate 5e-5 \
--max_seq 100 \
--overwrite_output_dir \
--max_turn 15 \
--num_candidates 1 \
--mc_loss_efficient 0.33 \
--add_response_prediction \
--add_same_belief_response_prediction \
--add_belief_prediction

## Decoding hyperparameters (recipe_models_noneg_10e)
--top_k 3
--top_p 0.9 (default)
--temperature 1.2
--max_turn 15
* belief acc: 0.8083333333333335
* bleu: 0.06054026895113356

## Same hyperparameters (recipe_models_all_10e)
* belief acc: 0.7944444444444446
* bleu: 0.10981937228466401

`python evaluate.py --decoded_file generate_test_all_10e.json --test_file v3_recipe_test_dialogues.json``

* belief : type = main dish ; ingredients = negative eggs ; ingredients = negative cream ; is_vegan = yes ; name = [recommended_recipe_name_1]system [recommended_recipe_name_2]system [recommended_recipe_name_2]system [recipe_ingredients]
* belief : type = soup ; ingredients = negative eggs ; is_vegan = no ; type = not mentioned ; ingredients = not mentionedsystem [recommended_recipe_name_2]. You can try this delicious recipe for [recipe_name_1]
* belief : type = dessert ; ingredients = negative eggs ; ingredients = negative cornstarch ;arch ; type = not mentioned ;archstone ;archsystem ; is_vegan = no ; is_vegan = no ; is_quick = yes ; show
* belief : type = dessert ; ingredients = negative eggs ; ingredients = negative cornstarch ; type = not mentioned ; ingredients = not mentionedsystem [recipe_ingredients]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
* belief : type = dessert ; ingredients = negative eggs ; ingredients = negative corn ; show_tickets = dont care ; type = not mentioned. Don't you take this type of a recipe! Don't you!!! Don!!! will give you the recipe. Don!!! will be preparing this dish. Don! Wanna try the [recipe_name_1]?

`python evaluate.py --decoded_file generate_test_all_10e_mt.json --test_file v3_recipe_test_dialogues.json`
* belief : type = soup  ; ingredients = dont care  ; is_quick = yes  ; ingredients = dont caresystem [recommended_recipe_name_2]. I have a delicious recipe for [recipe_name_1]. It is also delicious.
* belief : type = main dish ; is_quick = yes  ; ingredients = not mentionedsystem [recommended_recipe_name_2]are all ready for you! How about trying [recipe_name_1]?
* belief : type = not mentioned  ; ingredients = not mentioned  ; is_quick = yes  ; ingredients = not mentionedsystem [recipe_instructions]with [recipe_ingredient_value]?
* belief : type = salad ; ingredients = not mentioned  ; is_quick = yessystem [recommended_recipe_name_2]. I have a delicious recipe for you: [recipe_name_1].
belief acc: 0.6583333333333334
bleu: 0.1342515337376161
