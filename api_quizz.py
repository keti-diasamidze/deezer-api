import json
import requests

#1
#ეს არის API პოპულარული მუსიკის მოსასმენი პლატფორმის, deezer-ის არტისტების შესახებ.
artist_id = input("Artist id:")
resp = requests.get(f"https://api.deezer.com/artist/{artist_id}")
# print(resp.status_code)
# print(resp.content)
# print(resp.headers)
# print(resp.text)
# print(resp.json())

#2
#შევინახოთ მონაცემები  json ფაილში
with open("artists.json", "w") as file:
    json.dump(resp.json(), file, indent=4)


#3
#load და dumps ფუნქციების გამოყენებით სტრუქტურიზებული მონაცემების დაბეჭდვა
res = json.loads(resp.text)
res_structured = json.dumps(res, indent=4)
print(res_structured)

#როგორ მუშაობს ეს პროგრამა: ამ პრორამის დახმარებით მომხმარებელს საშუალება აქვს შეიყვანოს ნებისმიერი რიცხვი და პროგრამა ამ რიცხვის შესაბამისი
# რენდომ მუსიკოსის შესახებ ინფორმაციას მიაწვდის მომხმარებელს. ეს ინფორმაცია მოიცავს:მუსიკოსის სახელს,ალბომების რაოდენობას,მსმენელთა რაოდენობას
#მათი ტოპ 5 ალბომის ჩამონათვალსა და ამ ალბომების ხანგრძლივობას. დამატებით, პროგრამა API-დან იღებს მუსიკოსის სურათს და ინახავს ცალკე ფაილში.
#(მუსიკოსის სახელის ჩაწერის მიხედვით ინფორმაციის ჩვენებაზეც ვიფიქრე, თუმცა ყველა არტისტის API არ არსებობს, ეს API ინფორმაცია მხოლოდ კონკრეტულ
#არტისტზე გვიჩვენებს, რომელსაც აიდის მიხედვით არჩევს)
json1 = (resp.json())
picture_url = requests.get(json1['picture'])
file1 = open('pictuer.jpg', 'wb')
file1.write(picture_url.content)
album_url = requests.get(json1['tracklist']).json()

#არჩეული არტისტის ალბომების შესახებ ინფორმაცია ცალკე json ფაილად შევინახოთ
# with open("albums.json", "w") as file:
#     json.dump(album_url1, file, indent=4)


artist_name = json.dumps(json1['name'])
most_famous_album = json.dumps(album_url['data'][0]["title_short"])
albom_duration = json.dumps(album_url['data'][0]["duration"])
album_rank = json.dumps(album_url['data'][0]["rank"])
number_of_fans = (json.dumps(json1['nb_fan']))

print(f"თქვენს მიერ არჩეული არტისტის სახელია {artist_name}, მისი ყველაზე ცნობილი სიმღერაა {most_famous_album},რომლის ხანგრძლივობაცაა "
      f"{albom_duration} წამი, სიმღერა რეიტინგში არის {album_rank}-ე, მუსიკოსს კი მთლიანობაში ჰყავს {number_of_fans} მსმენელი,"
      f"დამატებით, იხილეთ არჩეული არტისტის ტოპ 5 სიმღერის ჩამონათვალი:"  )

try:
    for each in range(0,5):
        print(album_url["data"][each]["title_short"])
except IndexError as msg:
    print("თქვენს მიერ არჩეული არტისტის სიმღერების შესახებ სხვა ინფორმაცია არ მოიძებნება ")


#4
#საბოლოოდ, მომხმარებლის მიერ არჩეული აიდის მიხედვით შერჩეუილი არტისტის შესახებ ინფორმაცია ავტომატურად ემატება ბაზას. ბაზა მოიცავს
#მუსიკოსის დასახელებას,ყველაზე ცნობილ სიმღერას, ამ სიმღერის ხანგრძლივობას,რეიტინგში ადგილს და მსმენელთა რაოდენობას.
import sqlite3

conn = sqlite3.connect('artist_info.sqlite')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE if not exists artists
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist       VARCHAR (50),
            famous_album VARCHAR (50),
            alb_duration INTEGER,
            alb_ranking INTEGER ,
            nb_fans INTEGER );''')


cursor.execute("INSERT INTO artists ( artist,famous_album, alb_duration, alb_ranking, nb_fans) VALUES(?,?, ?, ?, ?)",
               (artist_name, most_famous_album, albom_duration, album_rank,number_of_fans))
conn.commit()

conn.close()