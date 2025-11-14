# ================= Format algo id ================= #
def format_algorithm_id(alg, arm_puller, args=None, dataset=None):

    alg = "_".join(map(str,alg)).replace('.','') + '_' + \
            arm_puller if isinstance(alg, tuple) \
            else alg + '_' + arm_puller

    # abbreviate algorithm names
    if "Axeltron" in alg:
        alg_short = alg.replace("Axeltron", "Ax")
    elif "Axeltron_vanilla" in alg:
        alg_short = alg.replace("Axeltron_vanilla", "Ax_V")
    else:
        alg_short = str(alg)

    # default if no args
    if args is None:
        parts = [alg_short]

    elif alg_short.startswith("Ax"):
        # hyperparam parts
        parts = [
            alg_short,
            f"k{args['k']}",
            f"tk{args['top_k']}",
            f"ep{args['epochs']}",
            f"lr{str(args['lr']).replace('.','p')}",
            f"np{args['num_per']}",
            ]
        
        if 'eps' in args:
            parts.append(f"eps{str(args['eps']).replace('.','p')}")

        # target
        trg = args.get("target", "")
        if trg:
            parts.append("trg" + trg.replace("_", ""))
        
    elif alg_short.startswith("SHARP"):

        parts = [
            alg_short,
            f"a{str(args['ADAPT_ALPHA']).replace('.','p')}",
            f"decay{1 if args['DECAY_RATIONING'] else 0}",
            f"adapt{1 if args['ADAPT_RATIONING'] else 0}",
            f"prune{1 if args['PRUNE'] else 0}",
            f"d{str(args['delta']).replace('.','p')}",
            f"wrr{1 if args['WEIGHTED_ROUND_ROBIN'] else 0}",
        ]
    return parts

# ================= Format run_id ================= #
def format_run_id(problem, alg, arm_puller, args=None, dataset=None, extra_name = ''):

    parts = format_algorithm_id(alg, arm_puller, args=args, dataset=None)

    ret = f"{problem}_alg" 
    if parts:
        ret += "_" + "_".join(parts)
    if extra_name:
        ret += "_" + extra_name
    return ret


AXELTRON_PRESETS = {
    # ============================  Axeltron  ============================
    "Ax":           {'k':10,'top_k':None,'epochs':5,'lr':0.01,'num_per':30,'target':'permute_max'},
    "Ax tk10":      {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':30,'target':'permute_max'},
    "Ax gradient_tk10": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_theta'},
    "Ax gradient_tk5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_theta'},
    "Ax gradient_tk15":  {'k':10,'top_k':15, 'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_theta'},
    "Ax gradient_tk6":  {'k':10,'top_k':6,   'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_theta'},

    "Ax gradient_tk10_np5": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},
    "Ax gradient_tk5_np5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},
    "Ax gradient_tk15_np5":  {'k':10,'top_k':15, 'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},

    "Ax gradient_tk10_np5": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},
    "Ax gradient_tk5_np5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},
    "Ax gradient_tk15_np5":  {'k':10,'top_k':15, 'epochs':5,'lr':0.01,'num_per':5,'target':'gradient_theta'},

    "Ax tk10_np50": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':50,'target':'permute_max'},
    "Ax tk10_np100":{'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':100,'target':'permute_max'},
    "Ax tk5_np100": {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':100,'target':'permute_max'},
    "Ax tk5_np5":   {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':50,'target':'permute_max'},

    "Ax tk10_np150":{'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':150,'target':'permute_max'},
    "Ax tk5_np150": {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':150,'target':'permute_max'},

    "Ax gradient_one_tk10": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':None,'target':'gradient_one'},
    "Ax gradient_one_tk5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':None,'target':'gradient_one'},

    "Ax gradient_action_tk10": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':None,'target':'gradient_action'},
    "Ax gradient_action_tk5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':None,'target':'gradient_action'},

    "Ax gradient_step_tk10": {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_step'},
    "Ax gradient_step_tk5":  {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_step'},
    "Ax gradient_step_tk15": {'k':10,'top_k':15,  'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_step'},
    "Ax gradient_step_tk5_k5":  {'k':5,'top_k':5,   'epochs':5,'lr':0.01,'num_per':30,'target':'gradient_step'},
    "Ax gradient_step_tk10_k5": {'k':5,'top_k':10,  'epochs':10,'lr':0.01,'num_per':30,'target':'gradient_step'},

}

AXELTRON_VANILLA_PRESETS = {
    # ========================  Axeltron Vanilla  ========================
    "Ax V":                 {'k':10,'top_k':None,'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla'},
    "Ax V tk10":            {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla'},

    "Ax V soft-argmax_tk_10_trgmaxall":{'k':10,'top_k':10, 'epochs':5,'lr':0.01,'num_per':30,'target':'max_all'},
    "Ax V soft-argmax_tk_15_trgmaxall":{'k':10,'top_k':15, 'epochs':5,'lr':0.01,'num_per':30,'target':'max_all'},
    "Ax V soft-argmax_tk_5_trgmaxall":{'k':10,'top_k':5, 'epochs':5,'lr':0.01,'num_per':30,'target':'max_all'},

    "Ax V soft-argmax_tk10":         {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max'},
    "Ax V soft-argmax_tk2":          {'k':10,'top_k':2,   'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max'},
    "Ax V soft-argmax_tk5_np10":     {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':10,'target':'vanilla_max'},
    "Ax V soft-argmax_tk5_np50":     {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':50,'target':'vanilla_max'},
    "Ax V soft-argmax_tk5_np100":    {'k':10,'top_k':5,   'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max'},
    "Ax V soft-argmax_tk10_np50":    {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':50,'target':'vanilla_max'},

    "Ax V soft-argmax_tk10_np100":   {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max'},
    
    "Ax V soft-argmax_tk15_np100":   {'k':10,'top_k':15,  'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max'},
    "Ax V soft-argmax_tk20_np100":   {'k':10,'top_k':20,  'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max'},
    "Ax V soft-argmax_tk10_np150":   {'k':10,'top_k':10,  'epochs':5,'lr':0.01,'num_per':150,'target':'vanilla_max'},
    "Ax V soft-argmax_tk15_np150":   {'k':10,'top_k':15,  'epochs':5,'lr':0.01,'num_per':150,'target':'vanilla_max'},

    "Ax V soft-argmax_tk5_np100_eps1":   {'k':10,'top_k':5, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_np100_eps1":   {'k':10,'top_k':10, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},

    "Ax V soft-argmax_tk5_np30_eps1":   {'k':10,'top_k':5, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_np30_eps1":   {'k':10,'top_k':10, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},

    "Ax V soft-argmax_tk5_np100_eps1_k5":   {'k':5,'top_k':5, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_np100_eps1_k5":   {'k':5,'top_k':10, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk5_np100_eps1_k15":   {'k':15,'top_k':5, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_np100_eps1_k15":   {'k':15,'top_k':10, 'epochs':5,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},

    "Ax V soft-argmax_tk5_eps1_k5":   {'k':5,'top_k':5, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_eps1_k5":   {'k':5,'top_k':10, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk5_eps1_k15":   {'k':15,'top_k':5, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_eps1_k15":   {'k':15,'top_k':10, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},

    "Ax V soft-argmax_tk5_np100_eps1_ep15":   {'k':10,'top_k':5, 'epochs':15,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_np100_eps1_ep15":   {'k':10,'top_k':10, 'epochs':15,'lr':0.01,'num_per':100,'target':'vanilla_max', 'eps':1},
    
    "Ax V soft-argmax_tk5_eps1":   {'k':10,'top_k':5, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},
    "Ax V soft-argmax_tk10_eps1":   {'k':10,'top_k':10, 'epochs':5,'lr':0.01,'num_per':30,'target':'vanilla_max', 'eps':1},

}

SHARP_PRESETS = {

    "SHARP (α=1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP (α=0.3)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP (α=0.5)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP (α=0.1)": {'ADAPT_ALPHA': 0.1, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},

    "SHARP no adapt": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP no prune": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    
    "SHARP no adapt (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    "SHARP no prune (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    
    "SHARP no adapt/decay (only prune)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':False, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP no adapt/prune (only decay)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'max'},
    
    "SHARP no adapt/prune/decay (α=1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP no adapt/prune/decay (α=0.5)" : {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05, 'overlap_denominator' : 'max'},
    "SHARP no adapt/prune/decay (α=0.3)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05, 'overlap_denominator' : 'max'},

    # "SHARP (α=1,δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP (α=0.3,δ=0.1)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP (α=0.5,δ=0.1)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},

    # "SHARP no adapt (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP no prune (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    
    # "SHARP no adapt/decay (only prune) (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':False, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune (only decay) (δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.1, 'overlap_denominator' : 'max'},
    
    # "SHARP no adapt/prune/decay (α=1, δ=0.1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune/decay (α=0.5, δ=0.1)" : {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.1, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune/decay (α=0.3, δ=0.1)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.1, 'overlap_denominator' : 'max'},

    # "SHARP (α=1,δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.2, 'overlap_denominator' : 'max'},
    # "SHARP (α=0.3,δ=0.2)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.2, 'overlap_denominator' : 'max'},
    
    # "SHARP no adapt (δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.2, 'overlap_denominator' : 'max'},
    # "SHARP no prune (δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.2, 'overlap_denominator' : 'max'},
    
    # "SHARP no adapt/decay (only prune) (δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':False, 'delta':0.2, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune (only decay) (δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.2, 'overlap_denominator' : 'max'},
    
    # "SHARP no adapt/prune/decay (α=1, δ=0.2)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.2, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune/decay (α=0.5, δ=0.2)" : {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.2, 'overlap_denominator' : 'max'},
    # "SHARP no adapt/prune/decay (α=0.3, δ=0.2)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.2, 'overlap_denominator' : 'max'},

    # "SHARP (α=1, min)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'min'},
    # "SHARP (α=0.3, min)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'min'},
    
    # "SHARP no adapt (min)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'min'},
    # "SHARP no prune (min)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05, 'overlap_denominator' : 'min'},
    
}

SHARP__PRESETS = {

    "SHARP_ (α=1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True },
    "SHARP_ (α=0.3)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True},
    "SHARP_ (α=0.5)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True},
    "SHARP_ (α=0.1)": {'ADAPT_ALPHA': 0.1, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True},

    "SHARP_ no prune": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':True, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True},
    "SHARP_ no wrr": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':True, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':True, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':True},

    "SHARP_ no adapt/decay/wrr (only prune)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':False, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/prune/wrr (only decay)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/decay/prune (only wrr)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':True},

    "SHARP_ no adapt/prune (only decay & wrr)": {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':True},

    "SHARP_ no adapt/decay/wrr (only prune, α=0)": {'ADAPT_ALPHA': 0, 'ADAPT_RATIONING':False, 'PRUNE':True, 'DECAY_RATIONING':False, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/prune/wrr (only decay, α=0)": {'ADAPT_ALPHA': 0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':True, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/decay/prune (only wrr, α=0)": {'ADAPT_ALPHA': 0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':True},

    "SHARP_ no adapt/prune/decay/wrr (α=1)": {'ADAPT_ALPHA': 1.0, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/prune/decay/wrr (α=0.5)" : {'ADAPT_ALPHA': 0.5, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05, 'WEIGHTED_ROUND_ROBIN':False},
    "SHARP_ no adapt/prune/decay/wrr (α=0.3)": {'ADAPT_ALPHA': 0.3, 'ADAPT_RATIONING':False, 'PRUNE':False, 'DECAY_RATIONING':False, 'delta':0.05,'WEIGHTED_ROUND_ROBIN':False},

    }

PRESET_REGISTRY = {
    "Axeltron": AXELTRON_PRESETS,
    "Axeltron_vanilla": AXELTRON_VANILLA_PRESETS,
    "SHARP": SHARP_PRESETS,
    "SHARP_": SHARP__PRESETS,       
    }


SELECTED_PLOT = {
    
    "Axeltron": [
    ],

    "Axeltron_vanilla": [
    ],

    "SHARP": [

    # "SHARP (α=1)",
    # "SHARP (α=0.5)",
    # "SHARP (α=0.3)",

    # "SHARP no adapt",
    # "SHARP no prune",

    # "SHARP no adapt/decay (only prune)",
    # "SHARP no adapt/prune (only decay)",

    ],

"SHARP_": [

    "SHARP_ (α=0.5)",
    "SHARP_ (α=1)", # out

    "SHARP_ no prune",
    "SHARP_ no wrr",
    "SHARP_ no adapt", # out

    "SHARP_ no adapt/prune/wrr (only decay)",
    "SHARP_ no adapt/decay/wrr (only prune)", # out
    "SHARP_ no adapt/decay/prune (only wrr)", # out

    "SHARP_ no adapt/prune (only decay & wrr)", # out

    "SHARP_ no adapt/decay/wrr (only prune, α=0)", # out
    "SHARP_ no adapt/prune/wrr (only decay, α=0)", # out
    "SHARP_ no adapt/decay/prune (only wrr, α=0)", # out

    "SHARP_ no adapt/prune/decay/wrr (α=1)", # out
    "SHARP_ no adapt/prune/decay/wrr (α=0.5)", # out
    "SHARP_ no adapt/prune/decay/wrr (α=0.3)", # out

    ]
}

# ==========================  Plot labels  ===========================

labels_paper_bernoulli = {
    
    'SHRR_consumption': "SHRR",
    'AT_LUCB_C_consumption': "AT-LUCB-C",
    # 'SHARP__consumption_a0p5_decay1_adapt1_prune1_d0p05_wrr1': "SHARP",
    'SHARP__consumption_a0p5_decay1_adapt1_prune0_d0p05_wrr1': "SHARP", # NO PRUNE VERSION
    }

labels_paper_bernoulli_SHARP_= {"_".join(format_algorithm_id('SHARP_', "consumption", args = SHARP__PRESETS[k])):k for k in SELECTED_PLOT['SHARP_']}
print(labels_paper_bernoulli_SHARP_)

labels_extra_rations_bernoulli = {
    
    'SHRR_consumption': "SHRR",
    'SHARP__consumption_a0p5_decay1_adapt0_prune0_d0p05_wrr0': "SHARP no adapt/prune/wrr (only decay)",
    # 'SHARP__consumption_a0p5_decay1_adapt1_prune1_d0p05_wrr1': "SHARP",
    'SHARP__consumption_a0p5_decay1_adapt1_prune0_d0p05_wrr1': "SHARP", # NO PRUNE VERSION
    'SHARP__consumption_a0p5_decay0_adapt0_prune1_d0p05_wrr0': "SHARP no adapt/decay/wrr (only prune)",

    }


# labels_paper_bernoulli_SHARP_ = {

#     # 'SHARP__consumption_a0p3_decay1_adapt1_prune1_d0p05_wrr1': "SHARP (α=0.3)",
#     'SHARP__consumption_a1p0_decay1_adapt1_prune1_d0p05_wrr1': "SHARP (α=1)",
#     'SHARP__consumption_a0p5_decay1_adapt1_prune1_d0p05_wrr1': "SHARP (α=0.5)",
#     # 'SHARP__consumption_a0p5_decay1_adapt1_prune1_d0p01_wrr1': "SHARP (α=0.1)",

#     'SHARP__consumption_a0p5_decay1_adapt1_prune0_d0p05_wrr1': "SHARP no prune",
#     'SHARP__consumption_a0p5_decay1_adapt1_prune1_d0p05_wrr0': "SHARP no wrr",

#     'SHARP__consumption_a0p5_decay0_adapt0_prune1_d0p05_wrr0': "SHARP no adapt/decay/wrr (only prune)",
#     'SHARP__consumption_a0p5_decay1_adapt0_prune0_d0p05_wrr0': "SHARP no adapt/prune/wrr (only decay)",
#     'SHARP__consumption_a0p5_decay0_adapt0_prune0_d0p05_wrr1': "SHARP no adapt/decay/prune (only wrr)",

#     'SHARP__consumption_a0_decay0_adapt0_prune1_d0p05_wrr0': "SHARP no adapt/decay/wrr (only prune, α=0)",
#     'SHARP__consumption_a0_decay1_adapt0_prune0_d0p05_wrr0': "SHARP no adapt/prune/wrr (only decay, α=0)",
#     'SHARP__consumption_a0_decay0_adapt0_prune0_d0p05_wrr1': "SHARP no adapt/decay/prune (only wrr, α=0)",

#     'SHARP__consumption_a1p0_decay0_adapt0_prune0_d0p05_wrr1': "SHARP no adapt/prune/decay (α=1)",
#     'SHARP__consumption_a0p5_decay0_adapt0_prune0_d0p05_wrr1': "SHARP no adapt/prune/decay (α=0.5)",
#     'SHARP__consumption_a0p3_decay0_adapt0_prune0_d0p05_wrr1': "SHARP no adapt/prune/decay (α=0.3)",

#     }

labels_paper_bernoulli_SHARP = {

    'SHARP_consumption_a0p3_decay1_adapt1_prune1_d0p05_max': "SHARP (α=0.3)",
    'SHARP_consumption_a1p0_decay1_adapt1_prune1_d0p05_max': "SHARP (α=1)",
    'SHARP_consumption_a0p5_decay1_adapt1_prune1_d0p05_max': "SHARP (α=0.5)",

    'SHARP_consumption_a1p0_decay1_adapt0_prune1_d0p05_max': "SHARP no adapt",
    'SHARP_consumption_a1p0_decay1_adapt1_prune0_d0p05_max': "SHARP no prune",

    'SHARP_consumption_a1p0_decay0_adapt0_prune1_d0p05_max': "SHARP no adapt/decay (only prune)",
    'SHARP_consumption_a1p0_decay1_adapt0_prune0_d0p05_max': "SHARP no adapt/prune (only decay)",

    }

labels_paper_bernoulli_Ax = {
    # "Ax_consumption_k10_tkNone_ep5_lr0p01_np30_trgpermutemax": "Ax baseline", # not done
    
    # 'Ax_consumption_k10_tk10_ep5_lr0p01_np30_trgpermutemax': "Ax baseline top_k=10", # unsilence

    # 'Ax_consumption_k10_tk6_ep5_lr0p01_np30_trggradienttheta': "Ax gradient top_k=6", 
    # 'Ax_consumption_k10_tk5_ep5_lr0p01_np30_trggradienttheta': "Ax gradient top_k=5", 
    # 'Ax_consumption_k10_tk15_ep5_lr0p01_np30_trggradienttheta': "Ax gradient top_k=15", 
    'Ax_consumption_k10_tk10_ep5_lr0p01_np30_trggradienttheta': "Ax gradient top_k=10", 

    'Ax_consumption_k10_tk5_ep5_lr0p01_np5_trggradienttheta': "Ax gradient top_k=5 np5 (new)", 
    'Ax_consumption_k10_tk15_ep5_lr0p01_np5_trggradienttheta': "Ax gradient top_k=15 np5 (new)", 
    'Ax_consumption_k10_tk10_ep5_lr0p01_np5_trggradienttheta': "Ax gradient top_k=10 np5 (new)", 

    # "Ax_consumption_k10_tk10_ep5_lr0p01_np50_trgpermutemax": "Ax baseline top_k=10 np50", # unsilence
    # "Ax_consumption_k10_tk5_ep5_lr0p01_np50_trgpermutemax": "Ax baseline top_k=5 np50", # unsilence
    "Ax_consumption_k10_tk10_ep5_lr0p01_np100_trgpermutemax": "Ax baseline top_k=10 np100", 
    "Ax_consumption_k10_tk5_ep5_lr0p01_np100_trgpermutemax": "Ax baseline top_k=5 np100", 

    "Ax_vanilla_consumption_k10_tk10_ep5_lr0p01_np30_eps1_trgvanillamax" :" Ax_V vanilla_max top_k=10 eps1",
    "Ax_vanilla_consumption_k10_tk5_ep5_lr0p01_np30_eps1_trgvanillamax" :" Ax_V vanilla_max top_k=5 eps1",

    # "Ax_V_consumption_k10_tkNone_ep5_lr0p01_np30_trgvanilla": "Ax_V baseline", # not done

    # 'Ax_V_consumption_k10_tk10_ep5_lr0p01_np30_trgvanilla': "Ax_V baseline top_k=10", # unsilence
    # 'Ax_V_consumption_k10_tk10_ep5_lr0p01_np30_trgvanillamax': "Ax_V vanilla_max top_k=10", # unsilence
    
    # 'Ax_V_consumption_k10_tk10_ep5_lr0p01_np30_trgmaxall': "Ax_V max_all top_k=10", 
    # 'Ax_V_consumption_k10_tk15_ep5_lr0p01_np30_trgmaxall': "Ax_V max_all top_k=15", 
    # 'Ax_V_consumption_k10_tk5_ep5_lr0p01_np30_trgmaxall': "Ax_V max_all top_k=5", 
    
    # 'Ax_vanilla_consumption_k10_tk2_ep5_lr0p01_np30_trgvanillamax': "Ax_V vanilla_max top_k=2", # unsilence
    # 'Ax_vanilla_consumption_k10_tk5_ep5_lr0p01_np10_trgvanillamax' : "Ax_V vanilla_max top_k=5 np10", # unsilence
    # 'Ax_vanilla_consumption_k10_tk5_ep5_lr0p01_np50_trgvanillamax' : "Ax_V vanilla_max top_k=5 np50", # unsilence
    # 'Ax_vanilla_consumption_k10_tk10_ep5_lr0p01_np50_trgvanillamax' : "Ax_V vanilla_max top_k=10 np50", # unsilence

    'Ax_vanilla_consumption_k10_tk5_ep5_lr0p01_np100_trgvanillamax' : "Ax_V vanilla_max top_k=5 np100", 
    'Ax_vanilla_consumption_k10_tk10_ep5_lr0p01_np100_trgvanillamax' : "Ax_V vanilla_max top_k=10 np100", 

    'Ax_vanilla_consumption_k10_tk5_ep5_lr0p01_np100_eps_1_trgvanillamax' : "Ax_V vanilla_max top_k=5 np100 eps1", 
    'Ax_vanilla_consumption_k10_tk10_ep5_lr0p01_np100_eps_1_trgvanillamax' : "Ax_V vanilla_max top_k=10 np100 eps1", 

    # 'Ax_vanilla_consumption_k10_tk5_ep15_lr0p01_np100_eps_1_trgvanillamax' : "Ax_V vanilla_max top_k=5 np100 eps1 ep15", 
    # 'Ax_vanilla_consumption_k10_tk10_ep15_lr0p01_np100_eps_1_trgvanillamax' : "Ax_V vanilla_max top_k=10 np100 eps1 ep15", 

    # 'Ax_vanilla_consumption_k15_tk5_ep5_lr0p01_np100_eps1_trgvanillamax': "Ax_V vanilla_max top_k=5 np100 eps1 k15",
    'Ax_vanilla_consumption_k5_tk5_ep5_lr0p01_np100_eps1_trgvanillamax': "Ax_V vanilla_max top_k=5 np100 eps1 k5",
    # 'Ax_vanilla_consumption_k5_tk10_ep5_lr0p01_np100_eps1_trgvanillamax': "Ax_V vanilla_max top_k=10 np100 eps1 k5",
    # 'Ax_vanilla_consumption_k15_tk10_ep5_lr0p01_np100_eps1_trgvanillamax': "Ax_V vanilla_max top_k=10 np100 eps1 k15",

    # 'Ax_vanilla_consumption_k10_tk15_ep5_lr0p01_np100_trgvanillamax' : "Ax_V vanilla_max top_k=15 np100", # unsilence
    # 'Ax_vanilla_consumption_k10_tk20_ep5_lr0p01_np100_trgvanillamax' : "Ax_V vanilla_max top_k=20 np100", # unsilence
    # 'Ax_vanilla_consumption_k10_tk10_ep5_lr0p01_np150_trgvanillamax' : "Ax_V vanilla_max top_k=10 np150", # unsilence
    # 'Ax_vanilla_consumption_k10_tk15_ep5_lr0p01_np150_trgvanillamax' : "Ax_V vanilla_max top_k=15 np150", # unsilence
}

# =====================================  Archived  ======================================

# One gradient only:

    # "Ax_consumption_k10_tk10_ep5_lr0p01_npNone_trggradientone": "Ax gradient_one top_k=10",
    # "Ax_consumption_k10_tk5_ep5_lr0p01_npNone_trggradientone": "Ax gradient_one top_k=5",

    # "Ax_consumption_k10_tk10_ep5_lr0p01_np30_trggradientstep": "Ax gradient_step top_k=10",
    # "Ax_consumption_k10_tk5_ep5_lr0p01_np30_trggradientstep": "Ax gradient_step top_k=5",
    # "Ax_consumption_k10_tk15_ep5_lr0p01_np30_trggradientstep": "Ax gradient_step top_k=15",
    # "Ax_consumption_k10_tk5_ep5_lr0p01_np30_trggradientstep": "Ax gradient_step top_k=5 k5",    
    # "Ax_consumption_k10_tk5_ep5_lr0p01_np30_trggradientstep": "Ax gradient_step top_k=10 k5",    


labels_paper_classifier = {
    
    'SHRR_classifier': "SHRR",
    'AT_LUCB_C_classifier': "AT-LUCB-C",
    # 'SHARP_classifier_a1p0_decay1_adapt1_prune1_d0p05_max': "SHARP (α=1)",
    'SHARP__classifier_a0p5_decay1_adapt1_prune1_d0p05_max': "SHARP_ (α=0.5)",

    }


labels_paper_classifier_SHARP = {

    'SHARP_classifier_a0p3_decay1_adapt1_prune1_d0p05_max': "SHARP (α=0.3)",
    'SHARP_classifier_a1p0_decay1_adapt1_prune1_d0p05_max': "SHARP (α=1)",
    'SHARP_classifier_a0p5_decay1_adapt1_prune1_d0p05_max': "SHARP (α=0.5)",

    'SHARP_classifier_a1p0_decay1_adapt0_prune1_d0p05_max': "SHARP no adapt",
    'SHARP_classifier_a1p0_decay1_adapt1_prune0_d0p05_max': "SHARP no prune",

    'SHARP_classifier_a1p0_decay1_adapt0_prune1_d0p1_max': "SHARP no adapt (δ=0.1)",
    'SHARP_classifier_a1p0_decay1_adapt1_prune0_d0p1_max': "SHARP no prune (δ=0.1)",

    'SHARP_classifier_a1p0_decay0_adapt0_prune1_d0p05_max': "SHARP no adapt/decay (only prune)",
    'SHARP_classifier_a1p0_decay1_adapt0_prune0_d0p05_max': "SHARP no adapt/prune (only decay)",

    'SHARP_classifier_a1p0_decay0_adapt0_prune0_d0p05_max': "SHARP no adapt/prune/decay (α=1)",
    'SHARP_classifier_a0p5_decay0_adapt0_prune0_d0p05_max': "SHARP no adapt/prune/decay (α=0.5)",
    'SHARP_classifier_a0p3_decay0_adapt0_prune0_d0p05_max': "SHARP no adapt/prune/decay (α=0.3)",

    # 'SHARP_classifier_a0p3_decay1_adapt1_prune1_d0p1_max': "SHARP (α=0.3,δ=0.1)",
    # 'SHARP_classifier_a1p0_decay1_adapt1_prune1_d0p1_max': "SHARP (α=1,δ=0.1)",
    # 'SHARP_classifier_a0p5_decay1_adapt1_prune1_d0p1_max': "SHARP (α=0.5,δ=0.1)",

    }

labels_paper_classifier_SHARP_ = {

    'SHARP__classifier_a0p3_decay1_adapt1_prune1_d0p05_max': "SHARP_ (α=0.3)",
    'SHARP__classifier_a1p0_decay1_adapt1_prune1_d0p05_max': "SHARP_ (α=1)",
    'SHARP__classifier_a0p5_decay1_adapt1_prune1_d0p05_max': "SHARP_ (α=0.5)",

    'SHARP__classifier_a0p5_decay1_adapt1_prune0_d0p05_max': "SHARP_ no prune",

    'SHARP__classifier_a0p5_decay0_adapt0_prune1_d0p05_max': "SHARP_ no adapt/decay (only prune)",
    'SHARP__classifier_a0p5_decay1_adapt0_prune0_d0p05_max': "SHARP_ no adapt/prune (only decay)",

    'SHARP__classifier_a1p0_decay0_adapt0_prune0_d0p05_max': "SHARP_ no adapt/prune/decay (α=1)",
    'SHARP__classifier_a0p5_decay0_adapt0_prune0_d0p05_max': "SHARP_ no adapt/prune/decay (α=0.5)",
    'SHARP__classifier_a0p3_decay0_adapt0_prune0_d0p05_max': "SHARP_ no adapt/prune/decay (α=0.3)",

}

labels_paper_classifier_Ax = {

}