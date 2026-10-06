from PIL import Image
pts = {
 "header_bg":("01",460,150),"hero_pill":("01",330,915),"hero_pill_text":None,
 "page_bg_services":("01",460,1160),"card_white":("01",200,1300),
 "bottom_nav_bg":("01",720,1640),"bottom_nav_icon":("01",355,1595),
 "card_white2":("02",200,700),"service_yellow":("03",180,1000),
 "learn_more_btn":("03",345,1282),"services_bg":("03",60,800),
 "stat_yellow":("06",100,760),"brands_bg":("06",460,600),
 "testimonial_card":("08",90,420),"avatar":("08",122,720),
 "page_link_blue":None,"read_reviews_pill":("08",290,1115),
 "about_underline":("09",110,553),"about_bg":("09",30,1450),
 "footer_card":("11",100,620),"footer_bg":("11",460,1000),
 "footer_band_yellow":("11",460,190),"steps_bg_top":("10",30,300),"steps_bg_bottom":("10",30,1600),
 "nav_label_white":None,
}
for k,v in pts.items():
    if not v: continue
    f,x,y=v; x=int(x*1320/921); y=int(y*2868/2000); im=Image.open(f"screens/{f}.png").convert("RGB")
    # median of 5x5
    px=sorted(im.getpixel((x+dx,y+dy)) for dx in range(-2,3) for dy in range(-2,3))
    r,g,b=px[12]; print(f"{k:22s} #{r:02x}{g:02x}{b:02x}")
