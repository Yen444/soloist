NS=5
TEMP=1.2
TOP_P=0.5
TOP_K=3
# python soloist_decode.py \
# --model_type=gpt2 \
# --model_name_or_path='gtg_pretrained' \
# --num_samples $NS \
# --input_file=../examples/recipe/v3_recipe_test_dialogues.json \
# --top_k $TOP_K \
# --temperature $TEMP \
# --output_file=../examples/recipe/generate_test_pretrained.json \
# --max_turn 15

# all dialogues
# python soloist_decode.py \
# --model_type=gpt2 \
# --model_name_or_path='../examples/recipe/recipe_models_all_10e' \
# --num_samples $NS \
# --input_file=../examples/recipe/v3_recipe_test_dialogues.json \
# --top_k $TOP_K \
# --temperature $TEMP \
# --output_file=../examples/recipe/generate_test_all_10e.json \
# --max_turn 15

# no negative dialogues
python soloist_decode.py \
--model_type=gpt2 \
--model_name_or_path='../examples/recipe/recipe_models_all_10e_mt' \
--num_samples $NS \
--input_file=../examples/recipe/v3_recipe_test_dialogues.json \
--top_k $TOP_K \
--temperature $TEMP \
--output_file=../examples/recipe/generate_test_all_10e_mt.json \
--max_turn 15

# with machine teaching
# python soloist_decode.py \
# --model_type=gpt2 \
# --model_name_or_path='../examples/recipe/recipe_models_all_10e_mt' \
# --num_samples $NS \
# --input_file=../examples/recipe/v3_recipe_test_dialogues.json \
# --top_k $TOP_K \
# --temperature $TEMP \
# --output_file=../examples/recipe/generate_test_all_10e_mt.json \
# --max_turn 15
