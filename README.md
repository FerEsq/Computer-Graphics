# Lab-1
Branch para el laboratorio 1 del curso.

## Explicación de la IA
Le pregunté a chatGPT que creara una función utilizando el método de llenado de polígonos
discutido en clase y extraído de la página web adjunta, luego implementé la función obtenida dentro
de mi código bajo el nombre “glFill()”

https://www.cs.uic.edu/~jbell/CourseNotes/ComputerGraphics/PolygonFilling.html

Este método consiste en crear una “caja imaginaria” dentro del polígono para verificar si un punto
está dentro o fuera del mismo, sí el punto está dentro se colorea del color asignado, de lo contrario,
no se colorea. De esta manera, se colorean todos los puntos dentro del polígono, llenándolo por
completo.