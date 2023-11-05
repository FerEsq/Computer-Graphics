'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 04.11.2023
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

gourad_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;

    uniform float lightIntensity;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        fragColor = texture(tex, UVs) * intensity;
    }
"""

cell_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    float rand(vec2 co) {
        return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
    }

    void main() {
        float edgeSens = 0.4 + 0.1 * sin(time + rand(UVs));
        float intensity = 0.85 + 0.15 * sin(time + rand(UVs));

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;
        vec4 color = texture(tex, UVs) * gouraudIntensity;
        
        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (gintensity > edgeSens) {
            fragColor = color;
        } else if (gintensity > intensity) {
            fragColor = vec4(0, 0, 0, 1);
        } else {
            fragColor = vec4(0, 0, 0, 1);
        }
    }

"""

multicolor_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        vec3 gradientColor = vec3(UVs.y + sin(time * normal.x), UVs.x + cos(time * normal.y), 1.0 - UVs.x + tan(time * normal.z));
        fragColor = vec4(gradientColor, 1.0) * intensity;
    }
"""

noise_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;
    layout (binding = 1) uniform sampler2D noiseTex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float edgeSens = 0.4;
        float intensity = 0.85;

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;

        vec2 noiseCoords = UVs + vec2(time * -0.1);
        float noise = texture(noiseTex, noiseCoords).r;
        vec2 distortedCoords = UVs + vec2(noise * 0.1 + sin(time) * 0.05);
        vec4 color = texture(tex, UVs) * gouraudIntensity;

        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (noise > 0.8) {
            if (gintensity > edgeSens) {
                fragColor = color;
            } else if (gintensity > intensity) {
                fragColor = vec4(0, 0, 0, 1);
            } else {
                fragColor = vec4(0, 0, 0, 1);
            }
        } else {
            fragColor = texture(noiseTex, distortedCoords);
        }
    }

"""