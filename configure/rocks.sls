pull-source:
  pkg:
    - installed
    - name: git
  git:
    - latest
    - name: https://github.com/saltstackme/salt-rocks.git
    - rev: master
    - target: /srv/salt-rocks