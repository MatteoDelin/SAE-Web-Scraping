import GetPage as gp

def export_txt(texte,nom):
    with open("donneMAL/"+nom+".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texte))

# lien_mal=gp.get_url_mal(1)
# for lien in lien_mal:
#     data=gp.get_data_page(lien)
#     export_txt(data,lien.strip('/').split('/')[-1])

lien_ani=gp.get_url_anilist(1)
for e in lien_ani:
    print(e)

print(len(lien_ani))