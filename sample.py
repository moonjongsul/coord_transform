import coord_transform as ct

cTm = ct.Matrix()
cTm.set_rvec([10, 20, 30], 'deg')
cTm.set_tvec([0.1, 0.2, 0.3])

print(cTm.get_tvec('m'))
print(cTm.get_tvec('mm'))
print(cTm.get_rvec('rad'))
print(cTm.get_rvec('deg'))
print(cTm.get_T())
print(cTm.get_invT())