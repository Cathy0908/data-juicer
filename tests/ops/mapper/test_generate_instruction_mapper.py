import unittest
import json
from data_juicer.ops.mapper.generate_instruction_mapper import GenerateInstructionMapper
from data_juicer.utils.unittest_utils import (SKIPPED_TESTS,
                                              DataJuicerTestCaseBase)

# Skip tests for this OP in the GitHub actions due to disk space limitation.
# These tests have been tested locally.
@SKIPPED_TESTS.register_module()
class GenerateInstructionMapperTest(DataJuicerTestCaseBase):

    text_key = 'text'

    def test_generate_instruction(self):
        op = GenerateInstructionMapper(
            hf_model='Qwen/Qwen-7B-Chat', 
            seed_file='demos/data/demo-dataset-chatml.jsonl',
            instruct_num=2
        )

        from data_juicer.format.empty_formatter import EmptyFormatter
        dataset = EmptyFormatter(3, [self.text_key]).load_dataset()

        dataset = dataset.map(op.process)

        for item in dataset:            
            out_sample = json.loads(item[self.text_key])
            # test one output qa sample
            self.assertIn('role', out_sample['messages'][0])
            self.assertIn('content', out_sample['messages'][0])


if __name__ == '__main__':
    unittest.main()