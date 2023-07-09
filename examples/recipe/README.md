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
python evaluate.py --decoded_file generate_test.json --test_file v2_recipe_test_dialogues.json