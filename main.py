from discog import discog

user = 'griffinbrooks47@gmail.com'
password = 'XXX'

#artist_name = input("\nWhat artist discography do you want to use? ")
#print("\nYou entered: " + artist_name)

    #instantiates user specified discography
d1 = discog(user, password)
d1.search()