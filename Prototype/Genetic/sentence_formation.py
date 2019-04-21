from . import global_variables as gv
from . import functions as f


introduction = """There is an island in which certain inhabitants called "knights" always tell the truth and others called the "knaves" always lie. In the problem you are supposed to figure out who is a knight, who's a knave. Each inhabitant will give a statment and you are supposed to decide based on this if its a "Knight" or a "Knave".
"""
 
end = """<br> Can you determine who's a Knight and who's a Knave ? """

def generate_question(g, names, count):
    """ Accepts parameters::
    g - Genome object fo rthe accepted question
    names - dictionary object mapping variable name to actual name"""
    variables = g.variables.copy()
    # Concatenate Inhabitant names
    inhabitants = ""
    for a in variables[:-1]:
        inhabitants += names[a] + ", "
    inhabitants += "and " + names[variables[-1]]

    # formulating new question introduction
    question = "You meet" + (" three " if count==3 else " two")  + " inhabitants:" + inhabitants + ".<br>"

    statements = []
    for claim, claimer in zip(g.eqn, variables):
        statements.append(equation_to_sent(claim, claimer, variables, names, False))
    question = question + " ".join(statements) + end

    return introduction, question


def equation_to_sent(original_eqn, claimer, variables, names, only_statements=True):

    # clean Equation of placeholder of '1'
    eqn = original_eqn.copy()
    eqn = f.remove_ones(eqn)

    statement = "None"
    prestatement = ""

    # Check if equation has inappropriate length
    if len(eqn)%2 == 0 :
        raise Exception("Equation inappropriate")

    # If Equation has claim about single person
    if len(eqn) == 1 and f._type(eqn[0]) in ['var', 'neg_var']:
        v = eqn[0]
        prefix = "I am " if claimer == f.root_var(v) else names[f.root_var(v)] + " is "
        suffix = "Knight" if f.is_knight(v) else "Knave"
        statement = prefix + suffix

    # If Equation calims about 2 people
    elif len(eqn) == 3 :
        v1, op, v2 = eqn
        v1, v2 = (v2, v1) if f.root_var(v2) == claimer else (v1, v2)

        # Both are same type of people
        if f._type(v1) == f._type(v2):

            if op == "&" :
                prefix = ("I" if f.root_var(v1) == claimer else names[f.root_var(v1)]) + " and " + names[f.root_var(v2)]
                suffix = "Knight" if f.is_knight(v1) else "Knave"
                statement = "Both "+prefix + " are " + suffix

            else:
                prestatement = "Atleast one of "
                prefix = "us" if gv.PEOPLE_COUNT == 2 else (
                    "me and " if f.root_var(v1) == claimer else names[f.root_var(v1)]+" and ") \
                     + names[f.root_var(v2)]
                suffix = "Knight" if f.is_knight(v1) else "Knave"
                statement = prefix + " is " + suffix

        # If one is knight and other is knave
        else:
            prestatement = "" if op == "&" else "At least one of the following is true: that, "
            part1, part2 = equation_to_sent([v1], claimer, variables, names), equation_to_sent([v2], claimer, variables, names)
            statement = part1 + (" and " if op == "&" else " or ") + part2

    # If claim is about 3 people
    elif len(eqn) == 5 :
        v1, op1, v2, op2, v3 = eqn

        # Setting the variabless in correct order according to who claims
        if f._type(v1) == f._type(v2) == f._type(v3):
            v1, v2, v3 = (v2, v1, v3) if f.root_var(v2) == claimer else ( \
                         (v3, v1, v2) if f.root_var(v3) == claimer else \
                         (v1, v2, v3))

            # All are same or atleast 1 is ...
            if op1 == op2 :
                prestatement = "All of " if op1 == "&" else "At least one of "
                prefix = ("us, " if claimer == f.root_var(v1) else "") \
                       + ("I, " + names[f.root_var(v2)] + " and " + names[f.root_var(v3)])
                suffix = "Knight" if f.is_knight(v1) else "Knave"
                statement = prefix + ( " are " if op1 == "&" else " is " ) + suffix

            # sure about atleast one
            else:
                part1, part2 = equation_to_sent(eqn[:3], claimer, variables,names), \
                               equation_to_sent([v3], claimer, variables, names)

                if op1 == "&" and op2 == "|":
                    prestatement = "At least one of the following is true: that, "
                    statement = part2 + ", OR ," + part1

                else:
                    statement = part1 + " and definitely " + part2
        else:
            if op1 == op2:
                part1, part2, part3 = equation_to_sent([v1], claimer, variables, names), \
                                      equation_to_sent([v2], claimer, variables, names), \
                                      equation_to_sent([v3], claimer, variables, names)
                prestatement = "" if op1 == "&" else "At least one of the following is true: that, "
                statement = part1 + ", " + part2 + (" and " if op1 == "&" else " or ") + part3
            else:
                prestatement = "At least one of the following is true: that, " if op1 == "&" else ""
                part1, part2 = equation_to_sent(eqn[:3], claimer, variables, names), \
                               equation_to_sent([v3], claimer, variables, names)
                statement = part2 + (" OR, "+part1 if op1 == "&" else " and, "+"".join(part1))
    
    result_statement = names[claimer] + " says that, '" + prestatement + statement + ".'"
    if only_statements:
        return statement
    return "<br>" +  result_statement + "<br>"
