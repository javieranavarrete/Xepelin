# Xepelin

La url de deploy de la api es 'https://extreme-pixel-398708.rj.r.appspot.com/'

el comando curl es 'curl -X POST https://extreme-pixel-398708.rj.r.appspot.com/scrap -d '{"category": <categoria>, "webhook": <webhookUrl>}' -H 'Content-Type: application/json'

el link a Google sheets es 'https://docs.google.com/spreadsheets/d/1JLNLF8dxi-DGPMtj8KwPRAY52uKirijKPTiZGtizj_Q'

El código de la api, así como también el del scraper se encuentran juntos en el archivo main.py

Consideraciones: la categoría provista debe existir, si bien puede tener variaciones entre mayúsculas y minúsculas, en escencia sólo se debe dar alguno de los siguientes strings: 'emprendedores', 'pymes', 'corporativos', 'empresarios-exitosos', 'educacion-financiera', 'noticias'.

Los datos se guardan y entre cada scrapeo se borra la hoja y se vuelve a poblar.

Respecto al bonus, no alcancé a implementarlo, pero es posible de hacer si internamente se maneja una estructura con todas las secciones (pueden ser 'harcodeadas' o, mejor aún, scrapearlas también de la navbar) y se omite la parte de borrar la hoja entre llamados al scrapper, puesto que bastaría con ejecutar buena parte del código  para todas las categorías almacenadas y el resultado sería los datos de todo el blog.

Es muy importante aclarar que el deploy de la appi puede mostrar el root('/') mostrando que está activa, sin embargo no puede recibir los POST, root('/scrap'). Sospecho que eso se debe a que para el deploy usé google cloud platform, herramienta que nunca había utilizado antes y creo que fallé en la configuración de los permisos. Sin embargo, si el código se ejecuta localmente, funciona bien y guarda lo solicitado en el Gsheet. 

Si se desea probar localmente, se debe hacer con el comando 'gunicorn -w 1 -b 0.0.0.0:8000 "main:create_app()" --timeout 0' para inicializar el servicio, y luego se puede hacer el curl: 'curl -X POST 0.0.0.0:8000/scrap -d '{"category": "<categoria>", "webhook": "<webhook>"}' -H 'Content-Type: application/json''
