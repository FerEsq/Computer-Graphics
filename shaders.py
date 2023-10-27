'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 27.10.2023
 '''

# Graphics Library Shader Language: GLSL

vertex_shader = """
    #version 400 core

    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 inColor;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;

    out vec4 outColor;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        outColor = vec4(inColor, 1.0);
    }
"""

fragment_shader = """
    #version 400 core
    in vec4 outColor;
    out vec4 fragColor;
    
    void main() {
        fragColor = outColor;
    }

"""