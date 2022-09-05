
This is CIS hardening playbooks.

We frequently count the customer's question if they can reuse the playbooks developed for other customers. The purpose of developing these playbooks is to answer such questions

These playbooks base on past projects and were rewritten and can be used as starting point for other hardening projects. 

Note it is not a product. The efforts are needed to make it fit the specific client's requirement and environment.


roles/cis-rhel/vars/cis_rhel7_globe_vars.yaml :  Main index for all CIS item including the item
                                                   1. Item name
                                                   2. Serverity level
                                                   3. Verification method (playbook or shell scirpt)

Playbook location:
roles/cis-rhel/files/rhel7/verification:     verification playbook for each CIS item
roles/cis-rhel/files/rhel7/remediation:      remediation  playbook for each CIS item

Script location:
roles/cis-rhel/templates/rhel7/verification: verification shell script for each CIS item
roles/cis-rhel/templates/rhel7/remediation:  remediation  shell script for each CIS item


For the use case which use playbook for remediation and verification, there are some 
common format:

Note: it is not always suitiable for all cases. 





Sceinario 1:  loop

roles/cis-rhel/vars/cis_rhel7_globe_vars.yaml:

...
cis_rules:
  .
  .
  .
  5.3.3:
      name: 5.3.3 Ensure permissions on SSH public host key files are configured (Automated)
      remediation_method: playbook
      server_lv: Level 1
      verification_method: playbook
...

Remediation:

roles/cis-rhel/files/rhel7/remediation/5-3-3.yaml:
---

- name: "{{ cis_rules[cis_item]['name'] }}"
  block:
    - name: "{{ cis_rules[cis_item]['name'] }} - search file"
      command: find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub'
      register: host_pub_files
      changed_when: false
      failed_when: false

    - name: "{{ cis_rules[cis_item]['name'] }} - fix permission"
      file:
        dest: "{{ item }}"
        owner: root
        group: root
        mode: 0600
      with_items: "{{ host_pub_files.stdout_lines }}"

Verification:

roles/cis-rhel/files/rhel7/verification/5-3-3.yaml:
---

- name: init cis_result value as FAIL
  set_fact:
    cis_result: true

- name: "{{ cis_rules[cis_item]['name'] }}"
  block:
    - name: "{{ cis_rules[cis_item]['name'] }} - search file"
      command: find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub'
      register: host_pub_files
      changed_when: false
      failed_when: false

    - name: "{{ cis_rules[cis_item]['name'] }} - fix permission"
      file:
        dest: "{{ item }}"
        owner: root
        group: root
        mode: 0600
      with_items: "{{ host_pub_files.stdout_lines }}"
      check_mode: true
      ignore_errors: true
      register: result

    - name: Reset cis_result value
      set_fact:
        cis_result: false
      when:
        - not item[1]
        - item[0]
        - (result.skipped is not defined)  or
          not result.skipped
      loop: "{{ result.results | json_query('[].[changed,failed]') }}"


Sceinario 2:  Single tasks

roles/cis-rhel/vars/cis_rhel7_globe_vars.yaml:
...
cis_rules:
  .
  .
  .
  6.2.1:
      name: 6.2.1 Ensure accounts in /etc/passwd use shadowed passwords (Automated)
      remediation_method: playbook
      server_lv: Level 1
      verification_method: playbook
...

Remediation:

roles/cis-rhel/files/rhel7/remediation/6-1-2.yaml:
---

- name: "{{ cis_rules[cis_item]['name'] }}"
  file:
    dest: /etc/passwd
    owner: root
    group: root
    mode: 0644


Verification:

roles/cis-rhel/files/rhel7/verification/6-1-2.yaml:
---
  
- name: init cis_result value as FAIL
  set_fact:
    cis_result: true

- name: "{{ cis_rules[cis_item]['name'] }}"
  file:
    dest: /etc/passwd
    owner: root
    group: root
    mode: 0644
  check_mode: true
  ignore_errors: true
  register: result

- name: Reset cis_result value
  set_fact:
    cis_result: false
  when:
    - not result['failed']
    - result['changed']

