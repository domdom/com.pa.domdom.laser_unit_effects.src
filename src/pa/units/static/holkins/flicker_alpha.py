flashes = 10

start_alpha = 0.6
end_alpha = 0.0


o = []
for i in range(flashes):
	t = float(i) / flashes
	if i % 3 == 0:
		a = t * end_alpha + (1 - t) * start_alpha
	else:
		a = 0.1
	o.append([t, a])

print(o)

o = []

for i in range(flashes):
	t = float(i) / flashes
	if i % 3 == 1:
		a = t * end_alpha + (1 - t) * start_alpha
	else:
		a = 0
	o.append([t, a])

print(o)

o = []

for i in range(flashes):
	t = float(i) / flashes
	if i % 3 == 2:
		a = t * end_alpha + (1 - t) * start_alpha
	else:
		a = 0
	o.append([t, a])

print(o)