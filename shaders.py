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
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""