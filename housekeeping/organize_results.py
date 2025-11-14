import os
import shutil
import gzip

def organize_experiment_results(directory_path, save_at=None, move_or_copy='move', overwrite=False):

    """
    Organizes folders like g27b_algorithm_SHARP_1 into grouped folders by experiment code.
    Inside each, results.pkl.gz is renamed to {algorithm}_results.pkl.gz and 
    run_list_description.csv is copied only once.
    """

    assert move_or_copy in ['move', 'copy'], 'move_or_copy must be either "move" or "copy"'
    print(f'Overwrite: {overwrite}')

    if save_at is None:
        save_at = directory_path

    print(f'Organizing files in directory: {directory_path}')
    print(f'Saving organized files at: {save_at}')

    for foldername in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, foldername)

        if not os.path.isdir(folder_path):
            continue

        if '_algorithm_' not in foldername and '_alg_' not in foldername:
            print(f"Skipping non-matching folder: {foldername}")
            continue
        

        if '_algorithm_'  in foldername:
            alg = '_algorithm_'
        elif '_alg_' in foldername:
            alg = '_alg_'


        try:
            experiment_code, algorithm_name = foldername.split(alg, 1)
            # experiment_code = decode_experiment_code(experiment_code)
        except ValueError:
            print(f"Invalid folder name format: {foldername}")
            continue

        # Target directory: /save_at/experiment_code/
        target_dir = os.path.join(save_at, experiment_code)
        os.makedirs(target_dir, exist_ok=True)

        # 1. Copy or move results.pkl.gz as {algorithm}_results.pkl.gz
        src_result = os.path.join(folder_path, 'results.pkl.gz')
        dst_result = os.path.join(target_dir, f'{algorithm_name}_results.pkl.gz')

        if not os.path.exists(src_result):
            print(f"Missing results file in: {foldername}")
        elif not os.path.exists(dst_result) or overwrite:
            if move_or_copy == 'move':
                shutil.move(src_result, dst_result)
            else:
                shutil.copy2(src_result, dst_result)
        else:
            print(f"Results already exist at: {dst_result}. Skipping...")

        # 2. Copy run_list_description.csv once per experiment
        src_csv = os.path.join(folder_path, 'run_list_description.csv')
        dst_csv = os.path.join(target_dir, 'run_list_description.csv')

        if os.path.exists(src_csv) and (not os.path.exists(dst_csv) or overwrite):
            shutil.copy2(src_csv, dst_csv)
        elif not os.path.exists(dst_csv):
            print(f"Missing CSV in: {foldername}")

        # Optionally move or delete the original folder
        if move_or_copy == 'move':
            try:
                os.rmdir(folder_path)
            except Exception as e:
                print(f"Could not remove original folder {folder_path}: {e}")

def decode_experiment_code(code):
    """
    Decodes experiment code like 'g27b' into a dictionary:
        {
            'distribution': 'Gaussian',
            'number': '27',
            'type': 'baseline_known'
        }
    """
    if len(code) < 3:
        raise ValueError(f"Invalid experiment code format: {code}")

    dist_map = {'b': 'Bernoulli', 'g': 'Gaussian'}
    type_map = {'b': 'baseline_known', 'g': 'generic'}

    dist = dist_map.get(code[0])
    number = ''.join(filter(str.isdigit, code[1:]))
    type_char = code[-1]
    type_ = type_map.get(type_char)

    if not dist or not number or not type_:
        raise ValueError(f"Could not decode experiment code: {code}")

    return f"{dist}_{number}_{type_}"

# === Run the function ===

directory_path = os.getcwd()+'/results/'
save_at = os.getcwd() + '/results_organized/'

organize_experiment_results(directory_path, save_at, move_or_copy='copy', overwrite=True)
