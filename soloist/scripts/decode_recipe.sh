NS=3
TEMP=1
TOP_P=0.5
python soloist_decode.py \
--model_type=gpt2 \
--model_name_or_path='recipe_models' \
--num_samples $NS \
--input_file=../examples/recipe/v2_recipe_test_dialogues.json \
--top_p $TOP_P \
--temperature $TEMP \
--output_file=generate_test.json \
--max_turn 14
