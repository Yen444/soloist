#!/bin/bash
# lr 1e-5 to 5e-5
# mc_loss_efficient 0.1 to 1
# etc.

# for train ALWAYS CHANGE THIS
# OUTPUT=finetuned_models/all_9e_baseline
# OUTPUT=gtg_pretrained
# MODEL_NAME=gtg_pretrained

# EPOCHS=9
# # for decode ALWAYS CHANGE THIS
GENERATE=../examples/recipe/generate_test/no_fine_tuning.json
# # # CHANGE THIS IF MT / NO-NEG / extra
# # TRAIN_FILE=../examples/recipe/all_dialogues/v3_recipe_train_dialogues.json

# # # training valid dataset, should not change
# # EVAL_FILE=../examples/recipe/all_dialogues/v3_recipe_valid_dialogues.json  
# # decode hyperparameters, should not change for all experiments
# NS=5
# TEMP=1.2
# TOP_P=0.5
# TOP_K=3

# # # TRAIN: SET ADD_KB OR ADD_DP IF DESIRED; change CUDA if necessary
# # CUDA_VISIBLE_DEVICES=2 python soloist_train_experiment.py \
# # --output_dir $OUTPUT \
# # --model_type=gpt2 \
# # --model_name_or_path $MODEL_NAME \
# # --do_train \
# # --train_data_file $TRAIN_FILE \
# # --eval_data_file $EVAL_FILE \
# # --add_special_action_tokens=../examples/recipe/special_tokens.txt \
# # --per_gpu_train_batch_size 1 \
# # --num_train_epochs $EPOCHS \
# # --learning_rate 5e-5 \
# # --overwrite_cache \
# # --max_seq 100 \
# # --overwrite_output_dir \
# # --max_turn 15 \
# # --num_candidates 1 \
# # --mc_loss_efficient 0.33 \
# # --add_response_prediction \
# # --add_same_belief_response_prediction \
# # --add_belief_prediction \
# # --save_steps 6000
# # # --add_kb_to_context
# # # --evaluate_during_training
# # # --add_dp_to_response

# # DECODE SET ADD_KB IF DESIRE;
# CUDA_VISIBLE_DEVICES=2 python soloist_decode_experiment.py \
# --model_type=gpt2 \
# --model_name_or_path $OUTPUT \
# --num_samples $NS \
# --input_file=../examples/recipe/all_dialogues/v3_recipe_test_dialogues.json \
# --top_k $TOP_K \
# --temperature $TEMP \
# --output_file $GENERATE \
# --max_turn 15
# # --add_kb_to_context

# # also change this back to test set for other experiment
python ../examples/recipe/evaluate.py \
--decoded_file $GENERATE \
--test_file=../examples/recipe/all_dialogues/v3_recipe_test_dialogues.json \
--bleu_only