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

## 02 · Entrenar y evaluar pCTR (UBA)

[`notebooks/02_train_pctr_taobao.ipynb`](notebooks/02_train_pctr_taobao.ipynb)
continúa la exploración con una clasificación binaria de clics. Reutiliza los
CSV y la limpieza de nombres/joins; no necesita ejecutar el notebook 01.

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 python scripts/run_notebook.py 02_train_pctr_taobao.ipynb
```

El ejecutor mantiene como opción por defecto el notebook 01. Para ejecutar
interactivamente el segundo, usar el kernel del entorno `.venv` y trabajar
desde `notebooks/`.

- Muestra Bernoulli reproducible del **5% de impresiones**, semilla 42, leída
  por bloques. No balancea clases ni altera deliberadamente el CTR de evaluación.
  `SAMPLE_FRACTION=0.01` reduce el uso de memoria; `1.0` usa el dataset completo
  y requiere bastante más memoria y tiempo. La muestra no conserva historiales
  completos ni bloques de anuncios por usuario.
- Train: **6–10 de mayo**; validación: **11–12**; test: **13**, hora de China.
- Baseline constante, regresión logística y LightGBM (CPU, cuatro threads).
  `RUN_LIGHTGBM=False` permite omitir el tercer modelo.
- Selección por logloss y umbrales por F1 de validación; test reservado para
  accuracy, precision, recall, F1, ROC-AUC, PR-AUC (average precision) y logloss.
- Curvas ROC/PR, efecto del umbral, calibración y diagnóstico por segmentos.

La preparación se ajusta solo con train. Los IDs y agregados de clics no son
features. Los metadatos de usuario/anuncio carecen de fecha de vigencia:
se explicita el supuesto de disponibilidad previa, sin afirmar que el dataset
permita demostrarlo. Los resultados son predictivos y no causales.

### Resultado guardado del notebook 02

Ejecución con la muestra del 5%: 1.327.227 impresiones; 831.179 para train,
330.705 para validación y 165.343 para test. La tabla unida ocupa unos 81 MB y
la matriz dispersa de entrenamiento unos 96 MB (252 features transformadas);
el proceso también necesita memoria para lectura, copias y modelos.

| Modelo | ROC-AUC test | AP test | Logloss test |
|---|---:|---:|---:|
| Constante | 0,50000 | 0,04998 | 0,19850 |
| Logística | 0,54823 | 0,05848 | 0,19785 |
| LightGBM | 0,54721 | 0,05860 | 0,19787 |

LightGBM fue seleccionado por validación, aunque la logística obtiene una
logloss de test apenas menor. No cambiamos la selección mirando test.
A umbral 0,5 los tres modelos tienen aproximadamente 95% de accuracy y recall
cero. El notebook muestra el cambio al elegir umbrales con validación y analiza
la sobreestimación del CTR para anuncios nuevos en la muestra.
