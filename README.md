# ads-data-course

Exploración de impresiones y clics de anuncios de Taobao (mayo de 2017).

## Preparación

Python 3.12. Ejecutar desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python download_data.py
python scripts/run_notebook.py
```

La descarga requiere acceso HTTPS a `huggingface.co` y a sus destinos de
archivos bajo `*.hf.co`. No requiere una cuenta de Hugging Face.
El script comprueba los SHA-256 de los tres CSV y reutiliza archivos válidos.
Los datos ocupan aproximadamente 1,1 GB y están excluidos de Git.
El notebook completo requiere alrededor de 6 GB de memoria libre.

El notebook está en `notebooks/01_explore_taobao_ads.ipynb`; su directorio de
trabajo debe ser `notebooks/`. El ejecutor configura esa ruta, ejecuta todas
las celdas y solo reemplaza las salidas guardadas si la ejecución termina bien.
Validado en el entorno en la nube el 25 de octubre de 2026: los tres CSV
pasaron la comprobación SHA-256 y las 30 celdas se ejecutaron con el conjunto
completo. El notebook contiene las salidas de esa ejecución (26.557.961
impresiones, 1.366.056 clics; CTR del 5,14%).

## Datos

“Ad Display/Click Data on Taobao.com”, Alibaba / Tianchi:
https://tianchi.aliyun.com/dataset/56

Licencia de los datos: CC BY-NC-SA 4.0. La descarga usa una revisión fija de
una copia pública en Hugging Face; véase `download_data.py`.
