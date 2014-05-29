emacs:
  pkg:
    {% if grains['os'] == 'Ubuntu' and grains['oscodename'] == 'precise' %}
    - name: emacs23-nox
    {% elif grains['os'] == 'Ubuntu' and grains['oscodename'] == 'trusty' %}
    - name: emacs24-nox
    {% elif grains['os'] == 'Redhat' or grains['os'] == 'CentOS' %}
    - name: emacs-nox
    {% endif %}
    - installed
  file:
    - managed
    - name: /root/.emacs
    - source: salt://configure/files/emacs.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - pkg: emacs

screen:
  pkg:
    - installed

git:
  pkg:
    - installed

salt:
  pkg:
    - installed
    - pkgs:
      - salt-common
      - salt-master
      - salt-minion
      - salt-cloud
  file:
    - managed
    - name: /etc/salt/master
    - source: salt://configure/files/master.jinja
    - template: jinja
    - require:
      - pkg: salt