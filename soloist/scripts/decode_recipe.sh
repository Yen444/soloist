NS=5
TEMP=1.2
TOP_P=0.5
TOP_K=3
python soloist_decode.py \
--model_type=gpt2 \
--model_name_or_path='../examples/recipe/recipe_models_all_10e' \
--num_samples $NS \
--input_file=../examples/recipe/v3_recipe_test_dialogues.json \
--top_k $TOP_K \
--temperature $TEMP \
--output_file=../examples/recipe/generate_test_all_10e.json \
--max_turn 15

# --model_name_or_path='../examples/recipe/recipe_models_noneg_10e' \
# --num_samples $NS \
# --input_file=../examples/recipe/v3_recipe_test_dialogues.json \

# python soloist_decode.py \
# --model_type=gpt2 \
# --model_name_or_path='../examples/recipe/recipe_models_all' \
# --num_samples $NS \
# --input_file=../examples/recipe/v3_recipe_test_dialogues.json \
# --top_p $TOP_P \
# --top_k $TOP_K \
# --temperature $TEMP \
# --output_file=../examples/recipe/generate_test_all.json \
# --max_turn 14
