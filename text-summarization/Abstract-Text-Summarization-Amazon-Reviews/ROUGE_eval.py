import os
from pyrouge import Rouge155

r = Rouge155()
r._system_dir = os.getcwd() + '/rogue_data/provided_summaries'
r._model_dir = os.getcwd() + '/rogue_data/model1_50/model_summaries'

r.system_filename_pattern = 'REFERENCE_(\d+).txt'
r.model_filename_pattern = 'GENERATED_(\d+).txt'

output = r.convert_and_evaluate()
print(output)

output_dict = r.output_to_dict(output)

print("b")