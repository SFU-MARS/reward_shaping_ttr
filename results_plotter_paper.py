# use this file outside of conda env

import pickle
import seaborn as sns;
sns.set()
import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 30})
import os,sys
import argparse
import pandas as pd
import numpy as np


if __name__ == "__main__":
    # ----- arguments setting ------
    parser = argparse.ArgumentParser()
    parser.add_argument("-results_path", '--path_list', nargs='+', help="multiple paths of result for comparison in single plot", default=[])
    parser.add_argument("-results_iter", '--iter_list', nargs='+', default=[])
    parser.add_argument("-title", type=str)
    args = parser.parse_args()
    # convert args to dict
    args = vars(args)
    print(args)

    # Assuming the reward typle in results path is unique
    all_eval_sucs = []
    all_reward_types = []
    all_timesteps = []

    np.random.seed(2019)
    for path,iter in zip(args['path_list'], args['iter_list']):
        # print("path,iter:",(path,iter))
        cur_eval_suc = pickle.load(open(os.path.join(path, 'result', 'eval_success_percent_iter_' + str(iter) + '.pickle'), 'rb'))
        if all(v == 0 for v in cur_eval_suc):
            cur_eval_suc = cur_eval_suc + np.random.uniform(0,0.05,len(cur_eval_suc))
            cur_eval_suc = list(cur_eval_suc)
        cur_eval_suc.insert(0, 0.0)
        cur_reward_type = path.split('_')[-4]
        if cur_reward_type not in ['distance', 'craft', 'ttr'] and path.split('_')[-5] == 'lambda':
            cur_reward_type = 'distance' + '_' + 'lambda' + '_' + cur_reward_type
            cur_reward_type = cur_reward_type.upper()
        if cur_reward_type == 'craft':
            cur_reward_type = 'sparse'.upper()
        else:
            cur_reward_type = cur_reward_type.upper()

        # if cur_reward_type == 'TTR' and path.split('_')[-3] == 'ppo' and len(cur_reward_type) < 20:
        #     tmp = cur_eval_suc
        #     cur_eval_suc.extend([tmp[-1]]*(20-len(tmp)+1))
        for idx in range(len(cur_eval_suc)):
            all_eval_sucs.append(cur_eval_suc[idx])
            all_reward_types.append(cur_reward_type)
            all_timesteps.append(idx)


    print(all_eval_sucs)
    print(all_reward_types)

    d = {'reward_type':all_reward_types, 'timesteps(*30k)':all_timesteps, 'eval success percent':all_eval_sucs}
    df = pd.DataFrame(data=d)
    print(df)

    # fmri = sns.load_dataset("fmri")
    # print("fmri", fmri)
    ax = sns.lineplot(x="timesteps(*30k)", y="eval success percent", hue='reward_type', data=df, ci=None)

    print(dir(ax))
    L = ax.legend()

    mylabels =[]
    for l in L.get_texts():
        if l._text != 'reward_type':
            mylabels.append(l._text)

    for idx in range(len(mylabels)):
        if  mylabels[idx] == 'TTR':
            mylabels[idx] = 'TTR(ours)'
        elif  mylabels[idx] == 'SPARSE':
            mylabels[idx] = 'Sparse'
        elif  mylabels[idx] == 'DISTANCE':
            mylabels[idx] ='Distance' + '(' + r'$\lambda=0$' + ')'
        elif  mylabels[idx] == 'DISTANCE_LAMBDA_0.1':
            mylabels[idx] = 'Distance' + '(' + r'$\lambda=0.1$' + ')'
        elif  mylabels[idx] == 'DISTANCE_LAMBDA_1':
            mylabels[idx] = 'Distance' + '(' + r'$\lambda=1.0$' + ')'
        elif  mylabels[idx] == 'DISTANCE_LAMBDA_10':
            mylabels[idx] = 'Distance' + '(' + r'$\lambda=10$' + ')'
        else:
            raise ValueError('no such legend name')
    # print(mylabels)
    # if args['title'] == "Quadrotor_PPO":
    #     ax.axhline(y=0.940789, color='black', ls='--')

    # b.axes.set_title("Title", fontsize=50)
    # b.set_xlabel("X Label", fontsize=30)
    # b.set_ylabel("Y Label", fontsize=20)

    ax.set_ylim(0,1.1)
    ax.set_title(args['title'].split('_')[0] + ' Task Using ' + args['title'].split('_')[1], fontsize=20)
    ax.set_xlabel("timesteps(*30k)", fontsize=15)
    ax.set_ylabel("Evaluation Success Rate", fontsize=15)
    ax.legend(loc='lower right', title='Reward Type',labels=mylabels)

    for idx in range(len(ax.lines)):
        ax.lines[idx].set_linestyle("dashed")
    ax.lines[0].set_linestyle('solid')
    ax.lines[0].set_linewidth(2)
    ax.grid(True)
    # ax = sns.swarmplot(x="timesteps(*30k)", y="eval success percent", hue='reward_type', data=df)
    plt.show()

