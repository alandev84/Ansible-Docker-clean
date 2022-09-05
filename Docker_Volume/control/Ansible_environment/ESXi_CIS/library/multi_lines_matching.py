#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
import re
__metaclass__ = type

DOCUMENTATION = r'''
---
module: multi_lines_matching

short_description: check if the file have consequent lines match given pattern. The paterns are give as list.

version_added: "1.0.0"

description: This is my longer description explaining my test info module.

options:
    file_path:
        description: the spefific file path
        required: true
        type: str
    lines:
        description: pattern list, which compoment is one pattern which the line has to match.
        required: true
        type: list


author:
    - Zhang Jin (jinzha@redhat.com)
'''

EXAMPLES = r'''

    multi_lines_matching:
      file_path: /tmp/log
      lines:
        - '^\[\s*org/gnome/login-screen\s*\]\s*$'
        - '^\s*banner-message-enable\s*=\s*true\s*$'
        - "^\\s*banner-message-text\\s*=\\s*{{ gdm_banner_message }}\\s*$"

Note: ' and "  are different
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
found:
    description: the result of the search
    type: bool
    returned: always
    sample:  true / false
matched_lines:
    description: Gives all matched lines with line number in the file
    type: line
    returned: always
    sample: 
        "changed": false,
        "failed": false,
        "found": true,
        "matched_lines": [
            "Line Num : 17 -- [ org/gnome/login-screen]\n",
            "Line Num : 18 -- banner-message-enable=true   \t\n",
            "Line Num : 19 -- banner-message-text=gdm_banner_ message\n"
        ],
        "message": ""

'''

from ansible.module_utils.basic import AnsibleModule


#global pattern_index 
# define available arguments/parameters a user can pass to the module
module_args = dict(
    file_path=dict(type='str', required=True),
    lines=dict(type='list', required=True),
)


# the AnsibleModule object will be our abstraction working with Ansible
# this includes instantiation, a couple of common attr would be the
# args/params passed to the execution, as well as if the module
# supports check mode
module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
)

pattern_index = 0
line_index = 0
found = False

def match_line(line, patterns, l_index, i, result):
    global pattern_index, line_index, found
    p_index = pattern_index

    #result['matched_lines'].append("Found :" + str(p_index))
    
    #if p_index == len(patterns):
    #    result['found'] = True
    #    module.exit_json(**result)
    #    found = True
    #    p_index = 0
    #    l_index = 0

    pattern = patterns[p_index]

    if p_index == l_index:

        if re.match(pattern, line):
            p_index += 1
            result['matched_lines'].append("Line Num : " + str(i) + " -- " + line)
            if p_index == len(patterns):
                result['found'] = True
                module.exit_json(**result)
        else:
            p_index = 0
            l_index = 0
            result['matched_lines'] = []
        
    pattern_index = p_index
    line_index = l_index


def file_line(file_path, patterns, result):
    global pattern_index, line_index, found

    try:
        f = open(file_path, "r")
    except OSError:
        result['found'] = False
        result['matched_lines'].append("Cannot read fiel: " + file_path)
        module.exit_json(**result)

    i = 0
    for x in f:
        i += 1
        p_index = pattern_index
        l_index = line_index
        if p_index == l_index + 1:
            l_index += 1
        line_index = l_index
        match_line(x, patterns, l_index, i, result)
    f.close()

def run_module():

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        found= False,
        message='',
        matched_lines=[],
    )


    file_line(module.params['file_path'], module.params['lines'], result)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
