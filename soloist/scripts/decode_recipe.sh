# 3k checkpoint
MODEL_NAME='../examples/recipe/recipe_models_all_10e/checkpoint-3000'
OUTPUT=../examples/recipe/generate_test/generate_test_all_10e_cp3k.json
NS=5
TEMP=1.2
TOP_P=0.5
TOP_K=3

python soloist_decode_experiment.py \
--model_type=gpt2 \
--model_name_or_path $MODEL_NAME \
--num_samples $NS \
--input_file=../examples/recipe/all_dialogues/v3_recipe_test_dialogues.json \
--top_k $TOP_K \
--temperature $TEMP \
--output_file $OUTPUT \
--max_turn 15

python ../examples/recipe/evaluate.py \
--decoded_file $OUTPUT \
--test_file=../examples/recipe/all_dialogues/v3_recipe_test_dialogues.json 
