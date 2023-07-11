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



