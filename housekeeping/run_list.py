import os
import re
import json
import pandas as pd
from collections import defaultdict
from itertools import product


def create_offline_rl_run_list(
        env_ids,
        algos,
        problem_setting="offline_rl",
        save_as_txt=False,
    ):
    """
    env_ids: list of environment IDs
    algos:   list of algorithm names ('td3', 'bc', 'combined')
    problem_setting: subfolder under args/
    save_as_txt: optionally save --key=value files
    """

    # current working directory
    wd = os.getcwd() + '/'
    if 'housekeeping' in wd:
        wd = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/'

    runs = list(product(env_ids, algos))

    def short_env_id(eid: str) -> str:
        parts = eid.split('-')
        if len(parts) >= 3:
            return f"{parts[0]}_{parts[1][0]}_{parts[-1]}"
        return re.sub(r'[^A-Za-z0-9]+', '_', eid)

    def format_run_id(env_id, algo):
        return f"{short_env_id(env_id)}_{algo}"

    def save_args_to_txt(arguments_dict, output_file):
        with open(output_file, 'w') as file:
            for key, value in arguments_dict.items():
                file.write(f"--{key}={value}\n")

    # build dataframe (env_id, algo, run_id)
    run_csv = {
        'env_id': [],
        'algo': [],
        'run_id': [],
    }

    for env_id, algo in runs:
        run_id = format_run_id(env_id, algo)
        run_csv['env_id'].append(env_id)
        run_csv['algo'].append(algo)
        run_csv['run_id'].append(run_id)

    run_csv = pd.DataFrame(run_csv)

    # directory
    extra = f'args/{problem_setting}/' if problem_setting else 'args/'
    rfolder = wd + extra
    os.makedirs(rfolder, exist_ok=True)
    print('Run list folder:', rfolder)

    # full descriptor
    run_csv.to_csv(rfolder + 'run_list_description.csv', index=False)

    # write individual json and run_list.csv
    run_csv_new = defaultdict(list)

    for _, row in run_csv.iterrows():

        par_args = {
            "env_id": row["env_id"],
            "algo": row["algo"],
            "run_id": row["run_id"],
        }

        json_path = os.path.join(rfolder, f"{row['run_id']}.json")
        with open(json_path, 'w') as f:
            json.dump(par_args, f, indent=2)

        if save_as_txt:
            txt_path = os.path.join(rfolder, f"{row['run_id']}.txt")
            save_args_to_txt(par_args, txt_path)

        run_csv_new['run_id'].append(row['run_id'])
        run_csv_new['file'].append(extra + f"{row['run_id']}.json")

    run_csv2 = pd.DataFrame(run_csv_new)
    run_csv2.to_csv(rfolder + 'run_list.csv', index=False, header=False)

    print('Run list saved as:', rfolder + 'run_list.csv')

create_offline_rl_run_list(
    env_ids=[
        'halfcheetah-medium-v2',
        'antmaze-umaze-diverse-v2'
    ],
    algos=['td3', 'bc', 'combined'],
    problem_setting=""
)

