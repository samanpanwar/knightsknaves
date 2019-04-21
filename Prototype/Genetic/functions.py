import random
import itertools
from . import global_variables as gv


def make_random_block(block_size):
    """Make boolean equation with block_size number of variables with random operators in between"""    
    # create non-negated blocks
    nn_var = random.sample(gv.VARIABLES, block_size)
    while  nn_var == ['1']*block_size:
        nn_var = random.sample(gv.VARIABLES, block_size)

    # randomly add negation
    for i, var in enumerate(nn_var):
        if random.choice([True, False]):
            nn_var[i] = negate(var)
    operants = random.choices(gv.OPERAND, k=block_size-1)

    # Aleternate variables and equations into a single equation
    equation = [None]*(len(nn_var) + len(operants))
    equation[::2], equation[1::2] = nn_var, operants

    return equation


def random_equation(blk_size=gv.BLOCK_SIZE, ppl_cnt=gv.PEOPLE_COUNT):
    """Create random boolean equation"""
    eqn = []
    for _ in range(ppl_cnt):
        eqn.append(make_random_block(blk_size))
    return eqn


def truth_table(n):
    """Get Truth Table for `n` columns"""
    return itertools.product([True, False], repeat=n)


def similarity_score(row1, row2):
    """Hamming Bipolar Score between 2 lists of Truth Values"""
    score = 0
    for a, b in zip(row1, row2):
        if a == b:
            score+=1
        else:
            score+=-1
    return score


def apply_operator(a,op,b):
    if op == "&" :
        return a and b
    elif op == "|" :
        return a or b


def evaluate(original_equation, truth_values={"a":True,"b":True,"c":True}):
    def val(a):
        return not truth_values[a[1:]] if a[0] == "-" else truth_values[a]

    eqn = [ _ for _ in original_equation if _ is not '1']
    prev = eqn[0]
    for ele in eqn[1:]:
        if prev in gv.OPERAND and ele in gv.OPERAND:
            eqn.remove(prev)
        prev = ele
    if len(eqn) > 1:
        eqn = eqn[1:] if eqn[0] in gv.OPERAND else eqn
        eqn = eqn[:-1] if eqn[-1] in gv.OPERAND else eqn
    if len(eqn) > 2:
        ans = val(eqn[0])
        for op, var in zip(eqn[1::2], eqn[2::2]):
            ans = apply_operator(ans, op, val(var))
        return ans 
    elif len(eqn) == 1:  
        try:
            return val(eqn[0])
        except Exception:
            print(original_equation)
            raise
    print(eqn, original_equation)


def _type(ch):
    if ch in gv.OPERAND:
        return "op"
    elif ch[0] is '-' and ch[1:].isalpha():
        return "neg_var"
    elif ch.isalpha() :
        return "var"
    elif ch is '1':
        return "wildcard"
    else:
        raise Exception("Parameter is not appropriate...")


def root_var(var):
    """Get root variable i.e. 'A' for '-A' if possible"""
    if _type(var) in ["var", "neg_var"]:
        return var[-1:]  # hack for single Named variable
    else :
        print(var, '*'*20)
        raise Exception("Parameter passed is not a variable...")


def is_illegal(equation, truth_values):
    """Check for paradox : Knave says 'He is a Knave'"""
    for claim in equation: 
        for person, truth in truth_values.items():
            if not truth and root_var(person) in claim:
                return True
    return False


def is_knight(var):
    if var[0] == '-':
        return False
    return True


def negate(ch):
    if ch in gv.OPERAND:
        return negate_operator(ch)
    return negate_variable(ch)


def negate_variable(ch):
    if ch[0]=='-':
        return ch[1:]
    else:
        return '-'+ch if ch is not '1' else ch


def negate_operator(op):
    return '|' if op == '&' else '&'


def negate_equation(eqn):
    neg_eqn = []
    for ele in eqn:
        neg_eqn.append(negate(ele))
    return neg_eqn


def remove_ones(eq):
    """Remove placeholders '1' in boolean equations and return equation"""
    eqn = [ _ for _ in eq if _ is not '1']
    prev = eqn[0]
    for ele in eqn[1:]:
        if prev in gv.OPERAND and ele in gv.OPERAND:
            eqn.remove(prev)
        prev = ele
    if len(eqn) > 1:
        eqn = eqn[1:] if eqn[0] in gv.OPERAND else eqn
        eqn = eqn[:-1] if eqn[-1] in gv.OPERAND else eqn
    return eqn
