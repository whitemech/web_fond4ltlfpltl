"""
 Author: Ramon Fraga Pereira
 Adapted from prp planner (https://github.com/QuMuLab/planner-for-relevant-policies).
"""

import re, pprint

def read_file(file_name):
    """ Return a list of the lines of a file. """
    f = open(file_name, 'r')
    file_lines = [line.rstrip("\n") for line in f.readlines()]
    f.close()
    return file_lines

def get_lines(file_name, lower_bound = None, upper_bound = None):
    """ Gets all of the lines between the regex lower bound and upper bound. """

    toReturn = []

    f = open(file_name, 'r')
    file_lines = [line.rstrip("\n") for line in f.readlines()]
    f.close()

    if not lower_bound:
        accepting = True
    else:
        accepting = False
        pattern_low = re.compile(lower_bound, re.MULTILINE)

    if not upper_bound:
        upper_bound = 'THIS IS SOME CRAZY STRING THAT NOONE SHOULD EVER HAVE -- NARF!'

    pattern_high = re.compile(upper_bound, re.MULTILINE)

    for line in file_lines:
        if accepting:
            if pattern_high.search(line):
                return toReturn

            toReturn.append(line)
        else:
            if pattern_low.search(line):
                accepting = True

    return toReturn


def parse_var(lines, index):
    """ Parse SAS+ to instantiaded facts. """

    assert 'begin_variable' == lines[index]
    index += 1

    name = lines[index]
    index += 1

    assert '-1' == lines[index]
    index += 1

    num_vals = int(lines[index])
    index += 1

    vals = []
    for i in range(num_vals):
        if 'NegatedAtom' == lines[index][:11]:
            vals.append("not(%s)" % lines[index].split('Atom ')[-1])
        else:
            vals.append(lines[index].split('Atom ')[-1])
        index += 1

    assert 'end_variable' == lines[index]
    index += 1

    if 2 == len(vals):
        if '<none of those>' == vals[0]:
            vals[0] = "!%s" % vals[1]
        elif '<none of those>' == vals[1]:
            vals[1] = "!%s" % vals[0]

    return (name, vals, index)

def translate_lines(lines):
    translated_policy = 'Policy:'
    for line in lines:
        if 'If' == line[:2]:
            translated_policy += "If holds: %s" % '/'.join([mapping[item] for item in line.split(' ')[2:]]) + '\n'
        else:
            translated_policy += line + '\n'

    return translated_policy

""" Global variables. """
index = 0
var_lines = ''
num_vars = 0
mapping = {}

def translate(output_sas, policy, output_policy):
    """ Translate a policy with SAS+ vars to a policy with standard instantiated facts. """

    index = 0
    """ output is the SAS+ file generated by prp planner """
    var_lines = get_lines(output_sas, lower_bound = 'end_metric', upper_bound = 'begin_state')
    num_vars = int(var_lines[index])
    index += 1

    set_fluents = set()
    no_turnDomain_idx = None
    for i in range(num_vars):
        (name, vals, index) = parse_var(var_lines, index)
        # print(f"{name}, {vals}, {index}")
        for j in range(len(vals)):
            mapping[f"{name}:{j}"] = vals[j]
            set_fluents.add(vals[j])
            if vals[j] == "not(turndomain())":
                no_turnDomain_idx = f"{name}:{j}"
    # print(no_turnDomain_idx)

    # print "Mapping:\n"
    # print '\n'.join(["  %s\t<-> \t %s" % (k,mapping[k]) for k in sorted(mapping.keys())])
    # print

    policy_lines = read_file(policy)
    new_policy_lines = []
    for line in policy_lines:
        if no_turnDomain_idx in line or "trans-" in line:
            continue
        new_policy_lines.append(line)

    translated_policy = translate_lines(policy_lines)
    # print(
    #     translated_policy
    # )
    translated_policy_2 = translate_lines(new_policy_lines)
    with open(output_policy, "w") as f:
        f.write(translated_policy_2)

    # translated_policy_file = open(output_policy, "w")
    # translated_policy_file.write(translated_policy)
    # translated_policy_file.close()

    return mapping, set_fluents, translated_policy
