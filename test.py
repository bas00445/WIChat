file = open('brightPic.jpg', 'rb')

data  = file.read()

print(data.decode('ascii'))