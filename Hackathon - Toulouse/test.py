import spin_pulse, pkgutil

def search_class(pkg, target):
    for _, modname, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        try:
            mod = __import__(modname, fromlist=[target])
            if hasattr(mod, target):
                print(f'-> Trouvé \"{target}\" dans : {modname}')
        except Exception:
            pass

print('Recherche en cours...')
search_class(spin_pulse, 'HardwareSpecs')
search_class(spin_pulse, 'PulseSequence')
