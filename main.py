import generate
import jpegdecoder as decoder
from struct import error as struct_error

def validate_jpeg(input_bytes):
    """ return:
        rv: "complete", "incomplete" or "wrong", 
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        if len(input_bytes) > 1000000: return Status.Complete, -1, ''
        decoder.JPEG().decode(input_bytes)
        return generate.Status.Complete, -1, ""
    except struct_error as e:
        msg = str(e)
        if msg.startswith("unpack requires a buffer of "):
            return generate.Status.Incomplete, 0, ''
        else:
            raise e
    except generate.NeedMoreException as e:
        return generate.Status.Incomplete, 0, ''

def create_valid_inputs(n=1):
    i = 0
    parray = []
    while True:
        created_bits = generate.generate(validate_jpeg, parray)
        if created_bits is not None:
            #if random.randint(1,10) > 1:
            #    parray = created_bits.ba
            #    continue
            print(repr(created_bits.ba), file=sys.stderr)
            with open('file.x', 'wb+') as f:
                f.write(created_bits.ba)
            i += 1
            if (i >= n):
                break

if __name__ == "__main__":
    import sys
    create_valid_inputs()
