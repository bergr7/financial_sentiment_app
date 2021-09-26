# Análisis de sentimiento con FinBERT y despliegue de una web app con Streamlit

Este repositorio contine la implementación que acompaña a el articulo "Utilizando modelos de lenguaje de estado del arte para el análisis de sentimiento de noticas".

### Autores:

- [Miguel Camacho](https://es.linkedin.com/in/miguel-camacho-7b873652) - CTO en Smartvel y Director del Big Data Internation Campus
- [Bernardo García del Río](https://www.linkedin.com/in/bernardo-garc%C3%ADa-del-r%C3%ADo-b4a98873/) - AI Engineer en Flowrite y Tutor en Big Data Internation Campus

## Uso rápido de la web app
____
Uso en un entorno local. Es necesario tener instalada una versión reciente de la [distribución anaconda](https://www.anaconda.com/products/individual).

Desde la terminal:

1. Descargar el respositorio en local:
````
$ git clone https://github.com/bergr7/financial_sentiment_app
````
2. Crear un nuevo entorno virtual y activarlo:
`````
$ conda env create -f environment.yml
$ conda activate sentiment_app
`````
3. Dirigirse al directorio /src dentro del repositorio.
4. Iniciar la web app:
`````
$ streamlit run app.py
`````
5. Introducir el ticker y hacer click en "Extraer noticias" para visualizar las noticias y los gráficas.

![App](/img/app.png)

> Para realizar el análisis de sentimiento, la applicación utiliza el modelo FinBERT que requiere unos recursos computacionales altos. El análisis puede tardar unos minutos en máquinas que no cuenten con GPU o que tengan procesadores antiguos.

## Instalación
_____
- Instalar una versión de la [distribución anaconda](https://www.anaconda.com/products/individual) reciente, si es que no se cuenta con ella.
- Crear un entonrno virtual a partir del archivo envinronment.yml:
`````
$ conda env create -f environment.yml
$ conda activate sentiment_app
`````

## Contenido
_______

- **`sentiment_analysis.ipynb`**: En este notebook se explican todos los pasos necesarios para realizar el análisis de sentimiento utilizando el modelo FinBERT.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1-OJkcwMAcLm2S5A1glyLhyQH6bbaq5F2)
    - Extracción de noticias utilizando una fuente RSS
    - Preparación de los datos
    - Modelado e Inferencia
- **`config.py`, `dataset.py`, `parser.py` e `inference.py`**: Las funciones utilizadas en `sentiment_analysis.ipynb` se aislan en varios módulos para ser utilizadas en `app.py`.
- **`utils.py`**: Contiene varias funciones de ayuda a la hora de extrer datos y graficar.
- **`app.py`**: Contiene el código para crear y ejecutar la web app utilizando el framework [Streamlit](https://docs.streamlit.io/en/stable/).

## Agradecimientos
____
- [Seeking Alpha](https://seekingalpha.com) por sus fuentes RSS gratuitas.
- ProsusAI por su paper [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063) y hacer de dominio público el modelo FinBERT.
- [Streamlit](https://docs.streamlit.io/en/stable/) por haber desarrollado un framework para el desarrollo de aplicaciones web sencillo y muy rápido de utilzar.