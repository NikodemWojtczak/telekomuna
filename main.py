import error_correction as ec
import file_handler as fh

napis = "kot"

print("Napis: ", napis)
napis_zakodowany = ec.encode_string(napis)
print(fh.print_binary_string(napis_zakodowany))
napis_zakodowany = list(napis_zakodowany)
napis_zakodowany[0] = '1'
napis_zakodowany[19] = '1'
napis_zakodowany[37] = '0'
napis_zakodowany = ''.join(napis_zakodowany)
print(fh.print_binary_string(napis_zakodowany))
napis_zakodowany = ec.correct_string(napis_zakodowany, ec.verify_string(napis_zakodowany))
print(fh.print_binary_string(napis_zakodowany))