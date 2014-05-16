pull-source:
  pkg:
    - installed
    - name: git
  git:
    - latest
    - name: https://github.com/rackerlabs/salt-rocks.git
    - rev: master
    - target: /srv/salt-rocks