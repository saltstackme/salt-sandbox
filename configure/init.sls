{%- if salt['grains.get']('kernel') == 'Linux' -%}
include:
  - configure.packages
  - configure.users
  - configure.rocks
{%- endif -%}
