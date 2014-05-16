#
# disable password authentication
# add devops sudo access and adds users to specific groups
# uses users.sls pillar
#
{#
/etc/ssh/sshd_config:
  file:
    - replace
    - pattern: #PasswordAuthentication yes
    - repl: PasswordAuthentication no
    - backup: True
    - dry_run: True
    - show_changes: True
#}

PubkeyAuthentication:
  file:
    - sed
    - name: /etc/ssh/sshd_config
    - before: '#PubkeyAuthentication yes'
    - after: 'PubkeyAuthentication yes'
    - backup: .bck

PasswordAuthentication:
  file:
    - sed
    - name: /etc/ssh/sshd_config
    - before: 'PasswordAuthentication yes'
    - after: 'PasswordAuthentication no'
    - backup: .bck

PermitRootLogin:
  file:
    - sed
    - name: /etc/ssh/sshd_config
    - before: 'PermitRootLogin no'
    - after: 'PermitRootLogin yes'
    - backup: .bck

UncommentPermitRootLogin:
  file:
    - sed
    - name: /etc/ssh/sshd_config
    - before: '#PermitRootLogin'
    - after: 'PermitRootLogin'
    - backup: .bck

UncommentPasswordAuthentication:
  file:
    - sed
    - name: /etc/ssh/sshd_config
    - before: '#PasswordAuthentication'
    - after: 'PasswordAuthentication'
    - backup: .bck

ssh:
  service:
    - running
    - reload: True
    - watch:
      - file: UncommentPermitRootLogin
      - file: PermitRootLogin
      - file: PasswordAuthentication
      - file: PubkeyAuthentication
      - file: UncommentPasswordAuthentication

/etc/sudoers:
  file:
    - append
    - text: |
        %devops ALL=(ALL) NOPASSWD: ALL

{%- for group in pillar['sb_groups'] %}
{{ group.name }}:
  group:
    - present
    - require:
        - file: /etc/sudoers
{%- endfor %}

{%- for user in pillar['sb_users'] %}
{{ user.sso }}:
  user:
    - present
    - fullname: {{ user.fullname }}
    - shell: /bin/bash
    - groups:
{%-     for group in user.groups %}
        - {{ group }}
    - require:
      - group: {{ group }}
{%-     endfor %}    
  ssh_auth:
    - present
    - user: {{ user.sso }}
    - source: salt://common/files/{{ user.sso }}.id_rsa.pub
    - require:
      - user: {{ user.sso }}
{%- endfor %}