# Lab-2
Branch para el laboratorio 2 del curso.

## Shaders

  ### shader1.bmp
  Consiste en el difuminado entre tres colores (rosa, morado y celeste).
  
  Para implementarlo utilizar los siguientes fragmentShader y directionalLight:
  ```bash
    rend.fragmentShader = shaders.difusedShader
    directionalLight = (0,0,-1)
  ```  

  ### shader2.bmp
  Consiste en un shader de color verde que imita una cámara de visión nocturna.
  
  Para implementarlo utilizar los siguientes fragmentShader y directionalLight:
  ```bash
    rend.fragmentShader = shaders.saturatedShader
    directionalLight = (0,0,1)
  ```

  ### shader3.bmp
  Consiste en un outline shader de color celeste.
  
  Para implementarlo utilizar los siguientes fragmentShader y directionalLight:
  ```bash
    rend.fragmentShader = shaders.outlineShader
    directionalLight = (0,0,-1)
  ```

## Documentación
  Puede encontrar las conversaciones con ChatGPT que se llevaron a cabo para realizar este laboratorio en este [archivo.](IA.pdf)
