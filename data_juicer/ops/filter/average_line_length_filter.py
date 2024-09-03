import sys

from jsonargparse.typing import PositiveInt

from data_juicer.utils.constant import Fields, InterVars, StatsKeys

from ..base_op import OPERATORS, Filter
from ..op_fusion import INTER_LINES

OP_NAME = 'average_line_length_filter'


@OPERATORS.register_module(OP_NAME)
@INTER_LINES.register_module(OP_NAME)
class AverageLineLengthFilter(Filter):
    """Filter to keep samples with average line length within a specific
    range."""

    _batched_op = True

    def __init__(self,
                 min_len: PositiveInt = 10,
                 max_len: PositiveInt = sys.maxsize,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param min_len: The min filter length in this op, samples will
            be filtered if their average line length is below this
            parameter.
        :param max_len: The max filter length in this op, samples will
            be filtered if their average line length exceeds this
            parameter.
        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.min_len = min_len
        self.max_len = max_len

    def compute_stats(self, samples, context=False):
        samples_list = samples[self.text_key]
        samples_stats = samples[Fields.stats]
        context_key = f'{InterVars.lines}'

        for i, stat in enumerate(samples_stats):
            # check if it's computed already
            if StatsKeys.avg_line_length in stat:
                continue

            if context and context_key in samples[Fields.context][i]:
                lines = samples[Fields.context][i][context_key]
            else:
                lines = samples_list[i].splitlines()
                if context:
                    samples[Fields.context][i][context_key] = lines
            samples_stats[i][StatsKeys.avg_line_length] = \
                len(samples_list[i]) / len(lines) if len(lines) != 0 else 0.0
        return samples

    def process(self, samples):
        if isinstance(samples[Fields.stats], list):
            bool_results = []
            for stat in samples[Fields.stats]:
                if self.min_len <= stat[
                        StatsKeys.avg_line_length] <= self.max_len:
                    bool_results.append(True)
                else:
                    bool_results.append(False)
            return bool_results
        else:
            # single sample for ray filter
            if self.min_len <= samples[Fields.stats][
                    StatsKeys.avg_line_length] <= self.max_len:
                return True
            else:
                return False
