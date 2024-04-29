# Social_Media
Herramientas para trabajar con las redes sociales de forma inteligente: 

## Deleting-X.py 

Herramienta para eliminar huella digital de la red social X/Twitter. 

1. Solicita un archivo de tus datos en X/Twitter. Este archivo estará disponible para su descarga después de unos días. Si tus datos están listos para la descarga, recibirás una notificación en tu aplicación de Twitter o por correo electrónico.

2. Una vez que hayas descargado tu archivo, necesitas extraer el archivo ZIP en tu disco. Necesitarás el archivo llamado tweets.js que está incluido en el archivo. Incluye cada tweet/respuesta/retweet, junto con el correspondiente ID de tweet. Para permitir que este script de Python elimine publicaciones con los ID de tweet de tu archivo, también debes proporcionar información de sesión, de lo contrario, el script de Python no tendrá autorización. La forma más sencilla de obtenerlos es desde tu navegador.

Es importante copiar los siguientes headers: Cookie, X-Csrf-Token y Authorization. Pero si tienes dudas, simplemente copia y pega todos los encabezados de solicitud en un archivo en tu disco duro, por ejemplo, request-headers.txt.

3. El request-headers.txt debe quedar así:

```
Authorization: Bearer AAAAAAAAAAAAAAAAAAAAANR[...]
X-Csrf-Token: b0a38[...]
Cookie: [...] _twitter_sess=BAhD[...]; auth_token=24fa[...]
```

4. Para más info sobre como ejecutar el borrado de forma personalizada:

```
./Deleting-X.py -h
```

![Screenshot_1](https://github.com/kta41/Social_Media/assets/19204433/74a346b7-cf73-41b1-a46e-4110dee81456)

