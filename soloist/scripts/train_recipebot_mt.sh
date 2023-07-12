#!/bin/bash
# QUY
# lr 1e-5 to 5e-5
# mc_loss_efficient 0.1 to 1
# etc.
# 
CUDA_VISIBLE_DEVICES=7,8 python -m torch.distributed.launch \
--nproc_per_node=2 \
--nnodes=1 \
--node_rank=0 \
--master_addr="localhost" \
--master_port=8898 soloist_train.py \
--output_dir=../examples/recipe/recipe_models_all_10e_mt \
--model_type=gpt2 \
--model_name_or_path=../examples/recipe/recipe_models_all_10e \
--do_train \
--train_data_file=../examples/recipe/mt_recipe_train_dialogues.json  \
--eval_data_file=../examples/recipe/v3_recipe_valid_dialogues.json  \
--add_special_action_tokens=../examples/recipe/special_tokens.txt \
--per_gpu_train_batch_size 1 \
--num_train_epochs 4 \
--learning_rate 5e-5 \
--overwrite_cache \
--save_steps 5000 \
--max_seq 100 \
--overwrite_output_dir \
--max_turn 15 \
--num_candidates 1 \
--mc_loss_efficient 0.33 \
--add_response_prediction \
--add_same_belief_response_prediction \
--add_belief_prediction \
# --add_dp_prediction