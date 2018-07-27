## Data 

Data is obtained from *Voxforge* and *Youtube*.

### Distribution of downloaded data

|              | English | German | French |
| ------------ | ------- | ------ | ------ |
| **Voxforge** | 119.5h  | 31.7h  | 37.2h  |
| **Youtube**  | 32.6h   | 25.5h  | 37.5h  |

### Youtube Channels

| English                                                      | German                                                       | French                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [**CNN Happening Now**](https://www.youtube.com/playlist?list=PL6XRrncXkMaUoSMd-1D5uIt7uZ0nWxkMy), [**BBC Newsnight**](https://www.youtube.com/playlist?list=PLJxnQXiytA_Qc0B57aViue2G3DPet1Z0L) | [**DW UnterVierAugen**](https://www.youtube.com/playlist?list=PL9ECA8F31017E3F46), [hr info](https://www.youtube.com/playlist?list=PLxU1pHkNqAIDn6WNyIuuqCXCi2TtRqH2H), [euronews](https://www.youtube.com/playlist?list=PLD9tv0TxyeYImYwTKofUasNWsiYfkDk-k), [Welt Podcasts](https://www.youtube.com/playlist?list=PLslDofkqdKI-QNI9YqkQeWk8ZzM2B9WTF), [**NDR talkshow**](https://www.youtube.com/playlist?list=PLQrsocOZ_VClb9iaNbySjTOiFNdFnju5t), [**ZDF politik**](https://www.youtube.com/playlist?list=PLD6fiKkLW6F_Owv1TeZj95fitfXHoKheX), | [**BFMTV Politique**](https://www.youtube.com/playlist?list=PL-qBKb-rfbhjb5QBUIYISMHZ6PvYqcC95),  [RFI direct](https://www.youtube.com/watch?v=tBzGPx4x5H0&index=2&list=PLi_zbgj_QX4pPjiZArbYMhAsFmAYSvOSn&t=0s), [RTL Midi](https://www.youtube.com/playlist?list=PLRwgXecE0bRMLhW1lVAETAqG7SiLsbmEx), [**france info**](https://www.youtube.com/playlist?list=PLg6GanYvTasViFfi77n3JHrN-hKkhb4pe), [**france24 débat**](https://www.youtube.com/playlist?list=PLCnUnV3yCIYu6A1hEDKOOj2q9zasW1LH-) |



### To download files 

- From Voxforge: ```python data/download_voxforge.py <language>```
- From Youtube: ```youtube-dl --config-location "download_scripts/youtube-dl.conf"  --output "raw/youtube/some/path/%(playlist_title)s-%(title)s.%(ext)s" <playlist_url>```