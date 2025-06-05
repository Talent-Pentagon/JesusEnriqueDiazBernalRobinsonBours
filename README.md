# JesusEnriqueDiazBernalRobinsonBours - C3

## Video [[Link al Video](https://www.youtube.com/watch?v=SnsAAUf-JXo)]

## Agent

SWE Agent es un sistema que cuenta con múltiples herramientas esenciales para la resolución automática de problemas en repositorios. Entre sus funcionalidades se incluyen:

- Edición de código
- Envío y compilación de soluciones (soporte para C, C++, Java y Python)
- Gestión de configuraciones iniciales mediante archivos `.yaml`
- Documentación adicional para el desarrollador
- Conexión con el modelo de lenguaje
- Script de benchmark que limpia y estructura las salidas

## Model

Utilizamos la plataforma **Modal** para manejar múltiples operaciones clave:

- Hosteo de servidores para el proveedor **Ollama**
- Push y Pull de modelos desde y hacia **Hugging Face**

## Finetuning

- Encendimos un servidor de **Unsloth** dentro de Modal para realizar el fine-tuning de nuestro modelo.
- Al finalizar el proceso, el modelo ajustado se guarda automáticamente en **Hugging Face**.

## Webpage [[Link a la página](https://c3-swe-agent.vercel.app/)]

Desarrollamos una aplicación web con **Next.js** que está actualmente **hosteada en Vercel**. Esta aplicación:

- Realiza una solicitud POST al endpoint del servidor, enviando cuatro parámetros: archivo YAML, enlace al repositorio, enlace al issue, y clave de autorización.
- El servidor está expuesto mediante una **IP pública de una máquina virtual en Azure**, la cual corre un servidor **Flask**.
- Este servidor genera el endpoint y espera los parámetros enviados desde el frontend, para luego ejecutar el comando que corre el SWE Agent.
- El agente busca la solución, genera el patch y retorna su contenido al cliente.
- En el frontend se muestra un **preview del patch**, además de una opción para **descargarlo** si el usuario así lo desea.]

Desarrollamos una aplicación web con **Next.js** que está actualmente **hosteada en Vercel**. Esta aplicación:

- Realiza una solicitud POST al endpoint del servidor, enviando cuatro parámetros: archivo YAML, enlace al repositorio, enlace al issue, y clave de autorización.
- El servidor está expuesto mediante una **IP pública de una máquina virtual en Azure**, la cual corre un servidor **Flask**.
- Este servidor genera el endpoint y espera los parámetros enviados desde el frontend, para luego ejecutar el comando que corre el SWE Agent.
- El agente busca la solución, genera el patch y retorna su contenido al cliente.
- En el frontend se muestra un **preview del patch**, además de una opción para **descargarlo** si el usuario así lo desea.

## Clasificador

Se utilizaron 70,000 muestras del dataset original de Obscurax. Estas muestras se procesaron mediante el clasificador, y se generó un nuevo dataset con columnas adicionales de clasificación y confiabilidad. Para el fine-tuning, se filtraron todas las entradas que contenían la palabra "procedural", quedando un total aproximado de 30,000 muestras.

### Analizador Léxico [[Link al Documento](https://drive.google.com/file/d/1jpbVdxEE62At6rxIpu3xk58cQp_EtmQG/view?usp=sharing)]

El sistema recibe como entrada un código que puede pertenecer a una de las siguientes categorías: **OOP, Procedural, Híbrido o Texto**.

#### Ejemplo de entrada:

```c
int main() {
    int a = 10;
    int b = a * 15;
    if (b > 10) {
        printf("b es mayor que 10\n");
    } else {
        printf("b no es mayor\n");
    }
    function_call();
}
```

El **analizador léxico** procesa cada token con base en una tabla de tokens predefinida, y genera una salida de tokens, además de una tabla de símbolos que contiene todos los identificadores.

#### Tabla de Tokens

| Token            | ID    |
| ---------------- | ----- |
| (                | 1     |
| )                | 2     |
| {                | 3     |
| }                | 4     |
| class            | 5     |
| struct           | 6     |
| Identificadores+ | 7, 1+ |

La salida de los tokens es utilizada como entrada para el analizador sintáctico.

### Analizador Sintáctico [[Link al Documento](https://drive.google.com/file/d/1mu3DX20ey_zug8y3x-iHzZHzqAV-M2s-/view?usp=sharing)]

El **analizador sintáctico** se basa en una gramática libre de contexto definida como sigue:

```
CLASSIFICATION → IDS CODE $
CODE → CLASSES IDS CODE
     | SEPS IDS CODE
     | ε
CLASSES → class IDS SEPS
        | struct IDS SEPS
IDS → identifier IDS
     | ε
SEPS → ( IDS ) SEPS’
     | { STATEMENTS }
SEPS’ → { STATEMENTS }
      | ε
STATEMENTS → IDS STATEMENTS'
           | ε
STATEMENTS' → CLASSES STATEMENTS
            | SEPS STATEMENTS
            | ε
```

El analizador retorna como salida:

- Output del lexer
- Output del parser
- Valores estimados de OOP y Procedural
- Conclusión (OOP, Procedural, Híbrido o Texto) con su confiabilidad (0-100%)
- Un archivo externo con el tipo de código detectado y su porcentaje de confiabilidad.

## Evaluación

- Creamos 60 tests en total (C++, Java y Python), cada uno con su respectivo conjunto de pruebas unitarias (unit tests).
- La evaluación de las soluciones generadas se realizó utilizando la métrica **Functional Correctness** con el método **Pass@k**.
- Se probaron distintos valores de k: `[1, 2, 3, 5]`, verificando si al menos una de las soluciones generadas por el modelo resolvía correctamente el problema planteado.

### Functional Correctness

#### Pass@k

_El modelo de lenguaje genera k soluciones candidatas para un problema dado (por ejemplo, un fragmento con errores y su descripción). Si al menos una de estas k soluciones pasa un conjunto predefinido de pruebas unitarias, el problema se considera resuelto por el modelo._

Pasos:

- Para cada problema o bug de programación, el modelo genera k soluciones diferentes (por ejemplo, utilizando un valor alto de "temperature" o muestreo top-p).
- Cada una de las k soluciones generadas se ejecuta frente a un conjunto de pruebas unitarias específicas del problema.
- Si alguna de las k muestras pasa todas las pruebas, el problema se considera como "aprobado".
- Pass@k se calcula como el número total de problemas "aprobados" dividido entre el número total de problemas.

## Contribuidores

- **Juan José Salazar Cortés** – [jjsc2003@live.com](mailto:jjsc2003@live.com)
- **Jesus Enrique Diaz Bernal Robinson Bours** – [jusus.diazb2003@gmail.com](mailto:jusus.diazb2003@gmail.com)
- **Moisés Hiram Pineda Campos** – [moypineda10@gmail.com](mailto:moypineda10@gmail.com)
- **Mariana Esquivel Hernández** – [esquivelmariana0702@gmail.com](mailto:esquivelmariana0702@gmail.com)
- **Diego Sanchez Luna** – [geekdeer@gmail.com](mailto:geekdeer@gmail.com)
