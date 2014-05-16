sb_groups:
    -
        name: devops
        gid: 2000
    -
        name: admin
        gid: 999

sb_users:
    -
        sso: vagrant
        fullname: Vagrant User
        mail: vagrant@world.com
        groups: ['devops']
