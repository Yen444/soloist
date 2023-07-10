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

