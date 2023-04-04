for i in range(0,1000):
    print(f"  php{i}:")
    print(f'    cmd: "/usr/bin/php -S 0:'+ str(4242 + i) + '"')
    print('    numprocs: 1')
    print('    umask: 022')
    print('    workingdir: /tmp')
