import stateless.generate as G

G.init_set_of_bytes([i for i in range(256)])

def create_valid_inputs(validator, n=1):
    i = 0
    parray = []
    while True:
        created_bits = G.generate(validator.validate, parray)
        if created_bits is not None:
            print(repr(created_bits), file=sys.stderr)
            with open('file.x', 'wb+') as f:
                f.write(created_bits.b)
            i += 1
            if (i >= n):
                break

if __name__ == "__main__":
    import importlib.util
    import sys
    my_module = sys.argv[1]
    spec = importlib.util.spec_from_file_location("decoder", my_module)
    my_decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_decoder)
    create_valid_inputs(my_decoder)
