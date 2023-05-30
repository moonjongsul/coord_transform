import coord_transform as ct

cTm = ct.Matrix()
cTm.set_rvec([10, 20, 30], 'deg')
cTm.set_tvec([0.1, 0.2, 0.3])

print('1: ', cTm.get_tvec('m'))
print('2: ', cTm.get_tvec('mm'))
print('3: ', cTm.get_rvec('rad'))
print('4: ', cTm.get_rvec('deg'))
print('5: ', cTm.get_T())
print('6: ', cTm.get_invT())