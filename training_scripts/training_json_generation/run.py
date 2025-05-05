import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-type", type=str, default="llava")
    args = parser.parse_args()

    if args.model_type == "llava":
        import MLLM_io_generation.create_json_for_MLLM_training.step_1_llava as step_1_postprocess_qa_wh_mc
        import MLLM_io_generation.create_json_for_MLLM_training.step_2_llava as step_2_postprocess_reasoning
        step_1_postprocess_qa_wh_mc.generate_qa_wh_mc_step1('s1_test.json', qa=True, mc=True, wh=True, after=True)
        step_2_postprocess_reasoning.generate_reasoning_step2('s1_test.json', 's2_test.json')

    if args.model_type == "internlmxcomposer":
        import MLLM_io_generation.create_json_for_MLLM_training.step_1_internlmxcomposer as step_1_postprocess_qa_wh_mc
        import MLLM_io_generation.create_json_for_MLLM_training.step_2_internlmxcomposer as step_2_postprocess_reasoning
        step_1_postprocess_qa_wh_mc.generate_qa_wh_mc_step1('s1_test.json', qa=True, mc=True, wh=True, after=True)
        step_2_postprocess_reasoning.generate_reasoning_step2('s1_test.json', 's2_test.json')

    if args.model_type == "mplugowl2":
        import MLLM_io_generation.create_json_for_MLLM_training.step_1_mplugowl2 as step_1_postprocess_qa_wh_mc
        import MLLM_io_generation.create_json_for_MLLM_training.step_2_mplugowl2 as step_2_postprocess_reasoning
        step_1_postprocess_qa_wh_mc.generate_qa_wh_mc_step1('s1_test.json', qa=True, mc=True, wh=True, after=True)
        step_2_postprocess_reasoning.generate_reasoning_step2('s1_test.json', 's2_test.json')

    if args.model_type == "qwenvl":
        import MLLM_io_generation.create_json_for_MLLM_training.step_1_qwenvl as step_1_postprocess_qa_wh_mc
        import MLLM_io_generation.create_json_for_MLLM_training.step_2_qwenvl as step_2_postprocess_reasoning
        step_1_postprocess_qa_wh_mc.generate_qa_wh_mc_step1('s1_test.json', qa=True, mc=True, wh=True, after=True)
        step_2_postprocess_reasoning.generate_reasoning_step2('s1_test.json', 's2_test.json')

    # check step 1 data distributions
    # step_1_postprocess_qa_wh_mc.json_stat('s1_test.json')
