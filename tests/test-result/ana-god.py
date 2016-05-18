
# jd
fid = open('God-class-JD.txt')
names = fid.read().splitlines()
god_class_jd = []
for i in range(0, np.shape(names)[0]):
	l = names[i].split('\t')
	if(np.shape(god_class_jd)[0]==0 or l[0]!=god_class_jd[-1]):
		god_class_jd.append(l[0])
		print l[0]

np.save( 'god_class_jd.npy', god_class_jd)

#PMD
fid = open('god_class_pmd.txt')
names = fid.read().splitlines()
god_class_pmd = []
for i in range(0, np.shape(names)[0]):
	l = names[i].split('.')
	tmp = l[0][4:]
	t = '.'.join(tmp.split('/'))
	god_class_pmd.append(t)
	print t

np.save( 'god_class_pmd.npy', god_class_pmd)

common = []

for i in range(0, np.shape(god_class_jd)[0]):
	for j in range(0, np.shape(god_class_pmd)[0]):
		if (god_class_jd[i]==god_class_pmd[j]):
			common.append(god_class_jd[i])
			break;

print np.shape(common)
np.save('common_god.npy', common)
