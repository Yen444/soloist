NS=5
TEMP=1
TOP_P=0.5
python soloist_decode.py \
--model_type=gpt2 \
--model_name_or_path='../examples/recipe/recipe_models_all' \
--num_samples $NS \
--input_file=../examples/recipe/v3_recipe_test_dialogues.json \
--top_p $TOP_P \
--temperature $TEMP \
--output_file=../examples/recipe/generate_test_all.json \
--max_turn 14
