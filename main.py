import error_correction as ec

napis = "kot"

print("Napis: ", napis)
napis_bin = ec.string_to_binary(napis)
napis_bin_d = ec.binary_to_string(napis_bin)
napis_bin_kod = ec.encode_string(napis)
napis_pin_dekod = ec.decode_string(napis_bin_kod)
print("W postaci binarnej: ", ec.print_binary_string(napis_bin))
print("Po odkodowaniu z postaci binarnej: ", napis_bin_d)
print("W postaci zakodowanej: ", ec.print_binary_string(napis_bin_kod))
print("W postaci odkodowanej: ", napis_pin_dekod)

